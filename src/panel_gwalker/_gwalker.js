import {GraphicWalker} from "graphic-walker"
import {useEffect, useState, useRef} from "react"

function transform(data) {
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

export function render({ model }) {
  const [data] = model.useState('object')
  const [fields] = model.useState('fields')
  const [appearance] = model.useState('appearance')
  const [config] = model.useState('config')
  const [transformedData, setTransformedData] = useState([]);
  const graphicWalkerRef = useRef(null);
  const storeRef = useRef(null);

  model.on('msg:custom', async (e) => {
    let exporter
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
	exported = exporter.exportChart()
      }
      value = cleanToDict(exported)
    } else if (e.scope === 'all') {
      value = []
      exported = await (e.mode === 'spec' ? exporter.exportCode() : exporter.exportChartList())
      for await (const chart of exported) {
        chartList.push(cleanToDict(chart))
      }
    }
    model.send_msg({id: e.id, data: value})
  })

  useEffect(() => {
    const result = transform(data);
    setTransformedData(result);
  }, [data]);

  return <GraphicWalker
    storeRef={storeRef}
    ref={graphicWalkerRef}
    data={transformedData}
    fields={fields}
    appearance={appearance}
    {...config}
   />
}
