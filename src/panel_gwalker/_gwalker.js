import {GraphicWalker} from "graphic-walker"
import {useEffect, useState} from "react"

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

export function render({ model }) {
  const [data] = model.useState('object')
  const [fields] = model.useState('fields')
  const [appearance] = model.useState('appearance')
  const [config] = model.useState('config')
  const [currentChart, setCurrentChart] = model.useState("current_chart")
  const [saveCurrentChart] = model.useState("save_current_chart")
  const [transformedData, setTransformedData] = useState([]);

  console.log(saveCurrentChart)

  useEffect(() => {
    const result = transform(data);
    setTransformedData(result);
  }, [data]);

  return <GraphicWalker
    data={transformedData}
    fields={fields}
    appearance={appearance}
    {...config}
   />
}
