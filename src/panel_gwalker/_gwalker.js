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
  const [computation] = model.useState('computation')
  const [appearance] = model.useState('appearance')
  const [config] = model.useState('config')
  const [currentChart, setCurrentChart] = model.useState("current_chart")
  const [exportCurrentChart,setExportCurrentChart] = model.useState("export_current_chart")
  const [currentChartList, setCurrentChartList] = model.useState("current_chart_list")
  const [exportCurrentChartList,setExportCurrentChartList] = model.useState("export_current_chart_list")
  const [payloadRequest, setPayloadRequest] = model.useState("_payload_request");
  const [transformedData, setTransformedData] = useState([]);
  const [computationFunc, setComputationFunc] = useState(null);

  const graphicWalkerRef = useRef(null);

  if (exportCurrentChart && graphicWalkerRef && graphicWalkerRef.current){
    (async () => {
      let value = await graphicWalkerRef.current.exportChart()
      value=cleanToDict(value)
      setCurrentChart(value)
      setExportCurrentChart(false)
    })()
  }

  if (exportCurrentChartList && graphicWalkerRef && graphicWalkerRef.current){
    const chartList = [];
    (async () => {
        for await (const chart of graphicWalkerRef.current.exportChartList()) {
            chartList.push(cleanToDict(chart))
        }
        setCurrentChartList(chartList)
        setExportCurrentChartList(false)
    })()
  }

  useEffect(() => {
    let result = null
    if (computation=="client"){
      result = transform(data);
    }
    setTransformedData(result);
  }, [data, computation]);

  const _computationFunc = (value) => {
    console.log("payload_request dirty", value, model)

    value = cleanToDict(value)
    const originalResponse=model._payload_response
    console.log("payload_request clean", value, model)
    console.log("setPayloadRequest", setPayloadRequest)
    setPayloadRequest(value)

    (async() => {
        while (originalResponse==model._payload_response) {
          await new Promise(resolve => setTimeout(resolve, 100));
        }
        console.log("response", model._payload_response)
        return model._payload_response
    }
    )()

    console.log("payload_response", model._payload_response)
  }

  useEffect(() => {
    if (computation=="server"){
      setComputationFunc(()=>_computationFunc)
    }
    else {
      setComputationFunc(null)
    }
  }, [computation]);



  return <GraphicWalker
    ref={graphicWalkerRef}
    data={transformedData}
    fields={fields}
    computation={computationFunc}
    appearance={appearance}
    {...config}
   />
}
