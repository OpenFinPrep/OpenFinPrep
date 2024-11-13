import './InputParam.css';
import { keyToColumnLabel } from './Utils';
import { useState } from 'react';

function InputParam({ p, updateParam, onEnter }){
    const [ value, setValue ] = useState(p['default'] !== undefined ? p['default'] : "");

    const onChange = e => {
        setValue(e.target.value);
        updateParam(p.name, e.target.value);
    };
    const onKeyDown = e => {
        if (e.which === 13){
            onEnter();
        }
    }

    let type = p.type || "text";
    let placeholder = "Type " + type;
    if (type === "number") placeholder = "0";

    return <div className="input-param">
        <label key="label" htmlFor={p.name} className="form-label ">{keyToColumnLabel(p.name)}</label>
        <input key="input" onKeyDown={onKeyDown} onChange={onChange} value={value} type={type} className="form-control input-sm" id={p.name} placeholder={placeholder}></input>
    </div>
}

export default InputParam;