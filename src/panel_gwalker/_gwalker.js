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
  const [serverComputation] = model.useState('server_computation')
  const [appearance] = model.useState('appearance')
  const [config] = model.useState('config')
  const [payloadRequest, setPayloadRequest] = model.useState("_payload_request");
  const [transformedData, setTransformedData] = useState([]);
  const [computation, setComputation] = useState(null);

  const graphicWalkerRef = useRef(null);

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
    let result = null
    if (!serverComputation){
      result = transform(data);
    }
    setTransformedData(result);
  }, [data, serverComputation]);

  // input value: https://github.com/Kanaries/graphic-walker/blob/main/computation.md#payload
  // Return value: https://github.com/Kanaries/graphic-walker/blob/main/computation.md#return-value
  const _computationFunc = async (value) => {
    value = cleanToDict(value);
    const originalResponse = model._payload_response;
    setPayloadRequest(value);

    let result = null;

    // Polling loop
    while (originalResponse === model._payload_response) {
        await new Promise(resolve => setTimeout(resolve, 75));
    }

    // Once model._payload_response changes, set result
    result = model._payload_response;

    // Hack: reset request to be able to send the same request again. Same for response.
    model._payload_request = {}
    model._payload_response = [];
    return result;
  }

  useEffect(() => {
    if (serverComputation){
      setComputation(()=>_computationFunc)
    }
    else {
      setComputation(null)
    }
  }, [serverComputation]);

  return <GraphicWalker
    storeRef={storeRef}
    ref={graphicWalkerRef}
    data={transformedData}
    fields={fields}
    computation={computation}
    appearance={appearance}
    {...config}
   />
}
