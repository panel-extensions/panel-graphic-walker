import {GraphicWalker, TableWalker, GraphicRenderer, PureRenderer} from "graphic-walker"
import {useEffect, useState, useRef} from "react"

function transform(data) {
  if (data==null) {
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

function fetchSpec(url) {
  return fetch(url)
    .then(response => response.json())
    .catch(err => {
      console.error('Error fetching spec from URL', err);
    });
}

function transformSpec(spec, fields) {
  /* The spec must be an null or array of objects */
  if (spec === null) {
    return null;
  }
  if (typeof spec === 'string') {
    if (spec.startsWith('http://') || spec.startsWith('https://')) {
      spec = fetchSpec(spec);
    } else {
      spec = JSON.parse(spec);
    }
  }

  if (!Array.isArray(spec)) {
    return [spec];
  }
  return spec;
}

export function render({ model }) {
  // Model state
  const [appearance] = model.useState('appearance')
  const [themeKey] = model.useState('theme_key')
  const [config] = model.useState('config')
  const [data] = model.useState('object')
  const [fields] = model.useState('fields')
  const [spec] = model.useState('spec')
  const [serverComputation] = model.useState('server_computation')
  const [renderer] = model.useState('renderer')
  const [index] = model.useState('index')
  const [pageSize] = model.useState('page_size')

  // Data State
  const [computation, setComputation] = useState(null);
  const [transformedData, setTransformedData] = useState([]);
  const [transformedSpec, setTransformedSpec] = useState([]);
  const events = useRef(new Map());
  const [visualState, setVisualState]=useState(null)
  const [visualConfig, setVisualConfig]=useState(null)
  const [visualLayout, setVisualLayout]=useState(null)

  // Refs
  const graphicWalkerRef = useRef(null);
  const storeRef = useRef(null);

  // Python -> JS Message handler
  model.on('msg:custom', async (e) => {
    let exporter
    if (e.action === 'compute') {
      events.current.set(e.id, e.result)
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
      if (e.mode === 'spec') {
        exported = exporter.currentVis
      } else {
        exported = await window.graphicWalker.current.exportChart()
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

  // Data Transforms
  useEffect(() => {
    let result = null
    if (!serverComputation){
      result = transform(data);
    }
    setTransformedData(result);
  }, [data, serverComputation]);

  useEffect(() => {
    setTransformedSpec(transformSpec(spec))
  }, [spec]);

  useEffect(() => {
    if (transformedSpec!=null && transformedSpec.length >= index + 1) {
      const indexSpec = transformedSpec[index];

      setVisualState(indexSpec.encodings || null);
      setVisualConfig(indexSpec.config || null);
      setVisualLayout(indexSpec.layout || null);
    } else {
      setVisualState(null);
      setVisualConfig(null);
      setVisualLayout(null);
    }
  }, [transformedSpec, index])

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
    return transform(result);
  }

  useEffect(() => {
    if (serverComputation){
      setComputation(() => computationFunc)
    }
    else {
      setComputation(null)
    }
  }, [serverComputation]);
  // "GraphicWalker", "TableWalker", "GraphicRenderer", "PureRenderer"
  if (renderer=='TableWalker') {
    return <TableWalker
      storeRef={storeRef}
      ref={graphicWalkerRef}
      data={transformedData}
      fields={fields}
      computation={computation}
      appearance={appearance}
      vizThemeConfig={themeKey}
      pageSize={pageSize}
      {...config}
    />
  }

  if (renderer=='GraphicRenderer') {
    return <GraphicRenderer
      storeRef={storeRef}
      ref={graphicWalkerRef}
      data={transformedData}
      fields={fields}
      chart={transformedSpec}
      computation={computation}
      appearance={appearance}
      vizThemeConfig={themeKey}
      pageSize={pageSize}
      /* hack to force re-render if the transformedSpec is reset to null */
      key={transformedSpec ? "withSpec" : "nullSpec"}
      {...config}
    />
  }

  if (renderer=="PureRenderer") {
    return <PureRenderer
      ref={graphicWalkerRef}
      rawData={transformedData}
      visualState={visualState}
      visualConfig={visualConfig}
      visualLayout={visualLayout}
      appearance={appearance}
      vizThemeConfig={themeKey}
      /* hack to force re-render if the transformedSpec is reset to null */
      key={transformedSpec ? "withSpec" : "nullSpec"}
    />
  }

  return <GraphicWalker
    storeRef={storeRef}
    ref={graphicWalkerRef}
    data={transformedData}
    fields={fields}
    chart={transformedSpec}
    computation={computation}
    appearance={appearance}
    vizThemeConfig={themeKey}
    /* hack to force re-render if the transformedSpec is reset to null */
    key={transformedSpec ? "withSpec" : "nullSpec"}
    {...config}
  />
}
