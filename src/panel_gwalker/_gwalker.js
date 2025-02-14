import {GraphicWalker, TableWalker, GraphicRenderer, PureRenderer, ISegmentKey} from "graphic-walker"
import {useCallback, useEffect, useState, useRef} from "react"

function transform(data) {
  if (data == null) {
    return {}
  }
  const keys = Object.keys(data);
  const length = data[keys[0]].length;

  return Array.from({ length }, (_, i) =>
    keys.reduce((obj, key) => {
      obj[key] = data[key][i];
      return obj;
    }, {})
  );
}

function cleanToDict(value){
    value = JSON.stringify(value)
    value = JSON.parse(value)
    return value
}

function transformSpec(spec) {
  /* The spec must be an null or array of objects */
  if (spec === null) {
    return null;
  }
  if (typeof spec === 'string') {
    spec = JSON.parse(spec);
  }

  if (!Array.isArray(spec)) {
    return [spec];
  }
  return spec;
}

export function render({ model, el, view }) {
  // Model state
  const [appearance] = model.useState('appearance')
  const [themeKey] = model.useState('theme_key')
  const [config] = model.useState('config')
  const [data] = model.useState('object')
  const [fields] = model.useState('field_specs')
  const [spec] = model.useState('spec')
  const [kernelComputation] = model.useState('kernel_computation')
  const [renderer] = model.useState('renderer')
  const [index] = model.useState('index')
  const [pageSize] = model.useState('page_size')
  const [hideProfiling] = model.useState('hide_profiling')
  const [tab] = model.useState('tab')
  const [containerHeight] = model.useState('container_height')

  // Data State
  const [computation, setComputation] = useState(null);
  const [transformedData, setTransformedData] = useState([]);
  const [transformedSpec, setTransformedSpec] = useState([]);
  const events = useRef(new Map());
  const [transformedIndexSpec, setTransformedIndexSpec] = useState(null)
  const [containerStyle, setContainerStyle] = useState({})

  // Refs
  const graphicWalkerRef = useRef(null);
  const storeRef = useRef(null);
  const [refUpdated, setRefUpdated] = useState(false);

  // Python -> JS Message handler
  useEffect(() => {
    model.on('msg:custom', async (e) => {
      let exporter
      if (e.action === 'compute') {
	events.current.set(e.id, e.result)
	return
      } else if (e.action === 'add_chart') {
	storeRef.current.appendFromCode(e.spec)
	return
      }
      if (e.mode === 'spec') {
	exporter = storeRef.current
      } else {
	exporter = graphicWalkerRef.current
      }
      if (exporter === null) {
	return
      }
      let value, exported
      if (e.scope === 'current') {
	if (e.mode === 'vega-lite') {
          exported = exporter.lastSpec
	} else if (e.mode === 'spec') {
          exported = exporter.currentVis
	} else {
          exported = await graphicWalkerRef.current.exportChart()
	}
	value = cleanToDict(exported)
      } else if (e.scope === 'all') {
	value = []
	exported = await (e.mode === 'spec' ? exporter.exportCode() : exporter.exportChartList())
	for await (const chart of exported) {
          value.push(cleanToDict(chart))
	}
      }
      model.send_msg({action: 'export', data: value, id: e.id})
    })
  }, [])

  if (renderer === 'profiler') {
    const resize = () => {
      const table = view.container.children[0].shadowRoot.querySelector('div.overflow-y-auto.h-full')
      if (table != null) {
	table.style.maxHeight = '100%'
      }
    }
    model.on('after_render', resize)
    model.on('after_layout', resize)
  }

  // Data Transforms
  useEffect(() => {
    let result = null
    if (!kernelComputation){
      result = transform(data);
    }
    setTransformedData(result);
  }, [data, kernelComputation]);

  useEffect(() => {
    setTransformedSpec(transformSpec(spec))
  }, [spec]);

  useEffect(() => {
    if (transformedSpec != null) {
      let filteredSpecs;
      if (Array.isArray(index)) {
        filteredSpecs = index.map(i => transformedSpec[i]).filter(item => item != null);
      } else if (index != null && transformedSpec.length > index) {
        filteredSpecs = [transformedSpec[index]];
      } else {
        filteredSpecs = transformedSpec;
      }
      if (filteredSpecs && filteredSpecs.length > 0) {
        setTransformedIndexSpec(filteredSpecs);
      } else {
        setTransformedIndexSpec(null);
      }
    } else {
      setTransformedIndexSpec(null);
    }
  }, [transformedSpec, index]);

  const wait_for = async (event_id) => {
    while (!events.current.has(event_id)) {
      await new Promise(resolve => setTimeout(resolve, 10));
    }
  }

  const computationFunc = async (value) => {
    const event_id = crypto.randomUUID()
    model.send_msg({
      action: 'compute',
      payload: cleanToDict(value),
      id: event_id
    })
    await wait_for(event_id)
    const result = events.current.get(event_id)
    events.current.delete(event_id)
    if (Object.keys(result).length === 0) {
      return []
    }
    const data = transform(result);
    return data
  }

  useEffect(() => {
    if (kernelComputation) {
      setComputation(() => computationFunc)
    }
    else {
      setComputation(null)
    }
  }, [kernelComputation]);

  useEffect(() => {
    if (renderer === "explorer") {
      const key = tab === "data" ? ISegmentKey.data : ISegmentKey.vis;
      storeRef.current?.setSegmentKey(key);
    }
  }, [tab, refUpdated, renderer]);

  useEffect(() => {
    setContainerStyle({
        height: containerHeight,
        width: "100%"
    })
  }, [containerHeight])

  useEffect(() => {
    if (storeRef.current === null) {
      return
    }
    storeRef.current.resetVisualization()
  }, [fields])

  useEffect(() => {
    const interval = setInterval(() => {
      if (storeRef.current !== null) {
        setRefUpdated(true);
	clearInterval(interval);
      }
    }, 10);
    return () => clearInterval(interval);
  }, []);

  if (renderer === "profiler") {
    return <TableWalker
      storeRef={storeRef}
      ref={graphicWalkerRef}
      data={transformedData}
      fields={fields}
      computation={computation}
      appearance={appearance}
      vizThemeConfig={themeKey}
      pageSize={pageSize}
      hideProfiling={hideProfiling}
      {...config}
    />
  } else if (renderer === "viewer") {
    // See https://github.com/Kanaries/pygwalker/blob/main/app/src/index.tsx#L466
    return (
      <>
        {transformedIndexSpec?.map((chart, index) => (
          <div className="pn-gw-container" key={transformedIndexSpec ? `withSpec-${index}` : `nullSpec-${index}`}>
            <h3 style={{ marginLeft: "15px" }}>{chart.name || `Chart ${index}`}</h3>
            <GraphicRenderer
              id={index}
              storeRef={storeRef}
              ref={graphicWalkerRef}
              data={transformedData}
              fields={fields}
              chart={[chart]} // only 'chart' differs for each iteration
              computation={computation}
              appearance={appearance}
              vizThemeConfig={themeKey}
              containerStyle={containerStyle}
              {...config}
              /* hack to force re-render if the transformedSpec is reset to null */
              key={transformedSpec ? "withSpec" : "nullSpec"}
              />
          </div>
        ))}
      </>
    );
  } else if (renderer === "chart") {
    if (!data | !transformedData) {
      return <div>No data to render. Set 'kernel_computation=False' when creating GraphicWalker.</div>;
    }
    return (
      <>
        {transformedIndexSpec?.map((chart, index) => (
          <div className="pn-gw-container" key={transformedIndexSpec ? `withSpec-${index}` : `nullSpec-${index}`}>
            <h3 style={{ marginLeft: "15px" }}>{chart.name || `Chart ${index}`}</h3>
            <div style={{"height": containerHeight}}>
              <PureRenderer
                id={index}
                storeRef={storeRef}
                ref={graphicWalkerRef}
                rawData={transformedData}
                visualState={chart.encodings || null}
                visualConfig={chart.config || null}
                visualLayout={chart.layout || null}
                appearance={appearance}
                vizThemeConfig={themeKey}
                {...config}
                /* hack to force re-render if the transformedSpec is reset to null */
                key={transformedSpec ? "withSpec" : "nullSpec"}
                />
            </div>
          </div>
        ))}
      </>
    );
  }

  return <GraphicWalker
    storeRef={storeRef}
    ref={graphicWalkerRef}
    data={transformedData}
    fields={fields}
    chart={transformedSpec}
    hideProfiling={hideProfiling}
    computation={computation}
    appearance={appearance}
    vizThemeConfig={themeKey}
    /* hack to force re-render if the transformedSpec is reset to null */
    key={transformedSpec ? "withSpec" : "nullSpec"}
    {...config}
  />
}
