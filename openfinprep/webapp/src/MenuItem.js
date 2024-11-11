import { useState } from 'react';
import './MenuItem.css';


function MenuItem({title, tags, children}){
    const [expanded, setExpanded] = useState(false);

    return ([<div key="p" className={"menu-item " + (!children ? "menu-sub-item" : "")} onClick={() => setExpanded(!expanded)}>
        <div className="title">{title}{tags ? tags.map(t => <span className={"badge text-bg-" + t.type}>{t.label}</span>): ""}</div>
        {children ? <i className={"fa fa-chevron-" + (expanded ? "up" : "down")}></i> : ""}
    </div>,
    expanded ? <div key="c">{children}</div>: ""]);
}

export default MenuItem;