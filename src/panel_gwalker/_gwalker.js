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
  const [currentChart, setCurrentChart] = model.useState("current_chart")
  const [exportCurrentChart,setExportCurrentChart] = model.useState("export_current_chart")
  const [currentChartList, setCurrentChartList] = model.useState("current_chart_list")
  const [exportCurrentChartList,setExportCurrentChartList] = model.useState("export_current_chart_list")
  const [transformedData, setTransformedData] = useState([]);

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
    const result = transform(data);
    setTransformedData(result);
  }, [data]);

  return <GraphicWalker
    ref={graphicWalkerRef}
    data={transformedData}
    fields={fields}
    appearance={appearance}
    {...config}
   />
}
