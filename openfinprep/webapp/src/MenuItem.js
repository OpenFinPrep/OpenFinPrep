import { useState } from 'react';
import './MenuItem.css';


function MenuItem({title, tags, onClick, children}){
    const [expanded, setExpanded] = useState(false);

    const handleClick = () => {
        let handled = false;
        if (onClick) handled = onClick();
        if (!handled) setExpanded(!expanded);
    };

    return ([<div key="p" className={"menu-item " + (!children ? "menu-sub-item" : "")} onClick={handleClick}>
        <div className="title">{title}{tags ? tags.map(t => <span key={t.label} className={"badge text-bg-" + t.type}>{t.label}</span>): ""}</div>
        {children ? <i className={"fa fa-chevron-" + (expanded ? "up" : "down")}></i> : ""}
    </div>,
    expanded ? <div key="c">{children}</div>: ""]);
}

export default MenuItem;