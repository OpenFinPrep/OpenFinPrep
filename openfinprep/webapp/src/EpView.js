import './EpView.css';
import InputParam from './InputParam';
import { keyToColumnLabel, buildUrlWithQuery } from './Utils';
import 'react-data-grid/lib/styles.css';
import { useEffect, useState } from 'react';
import DataGrid from 'react-data-grid';

function EpView({ endpoint, setError }){
    const [rows, setRows] = useState([]);
    const [columns, setColumns] = useState([]);
    const [showApply, setShowApply] = useState(false);

    const [ params, setParams ] = useState({});

    const updateParam = (key, value) => {
        // This doesn't actually trigger any changes
        // because the params object does not change
        params[key] = value;
        setShowApply(true);
    };

    const applyParams = () => {
        const newParams = {...params};
        setParams(newParams);
    };

    const openUrl = () => {
        window.open(buildUrlWithQuery(endpoint.url, params), "_blank");
    }

    useEffect(() => {
        const controller = new AbortController();
        let request = null;
        
        const fetchData = async () => {
            setColumns([]);
            setRows([]);
            setShowApply(false);
            
            if (request != null){
                controller.abort();
                request = null;
                }
                
            try {
                request = fetch(buildUrlWithQuery(endpoint.url, params), { signal: controller.signal });
                const response = await request;
                if (!response.ok) {
                    throw new Error(`Cannot load ${endpoint.url}, status: ${response.status}`);
                }
                const rows = await response.json()
                let columns = [];
                if (rows.length > 0){
                    columns = Object.keys(rows[0]).map(k => { 
                        return {
                            key: k, 
                            name: keyToColumnLabel(k)
                        }
                    });
                }
                setRows(rows);
                setColumns(columns);
            } catch (err) {
                setError(err.message);
            } finally {
                request = null;
            }
        };

        fetchData();
    }, [setError, params, setShowApply, endpoint.url]);

    useEffect(() => {
        setParams(Object.assign({}, ...endpoint.params.map(p => ({
            [p.name]: p['default'] !== undefined ? p['default'] : ''})
        )));
    }, [endpoint]);

    return (<div className="ep-view">
        <div className="ep-header">
            <h3>{endpoint.name}</h3>
            <div className="ep-buttons">
                {showApply ? <button onClick={applyParams} className="btn btn-primary"><i className="fa fa-check"></i> Apply</button> : ""}
                <button onClick={openUrl} className="btn btn-light"><i className="fa fa-link"></i> URL</button>
                <button className="btn btn-dark"><i className="fa fa-download"></i> Export as CSV</button>
            </div>
        </div>
        {endpoint.params ? <div className="params">
            {endpoint.params.map(p => <InputParam key={p.name} p={p} updateParam={updateParam} onEnter={applyParams} />)}
        </div> : ""}
        <DataGrid className="rdg-light" columns={columns} rows={rows} />
    </div>)
}

export default EpView;