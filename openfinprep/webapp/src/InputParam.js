import './InputParam.css';
import { keyToColumnLabel } from './Utils';
import { useState } from 'react';

function InputParam({p}){
    const [ value, setValue ] = useState(p['default'] !== undefined ? p['default'] : "");

    let type = p.type || "text";
    let placeholder = "Type " + type;
    if (type === "number") placeholder = "0";

    return <div className="input-param">
        <label key="label" for={p.name} className="form-label ">{keyToColumnLabel(p.name)}</label>
        <input key="input" value={value} type={type} className="form-control input-sm" id={p.name} placeholder={placeholder}></input>
    </div>
}

export default InputParam;