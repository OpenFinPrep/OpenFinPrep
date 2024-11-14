import './EpView.css';
import InputParam from './InputParam';
import { keyToColumnLabel, buildUrlWithQuery, downloadFile } from './Utils';
import 'react-data-grid/lib/styles.css';
import { useEffect, useState, useRef } from 'react';
import DataGrid from 'react-data-grid';

function EpView({ endpoint, setError }){
    const [rows, setRows] = useState([]);
    const [columns, setColumns] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showApply, setShowApply] = useState(false);
    const [params, setParams] = useState(Object.assign({},...endpoint.params.map(p => ({
        [p.name]: p['default'] !== undefined ? p['default'] : ''})
    )));
    const [url, setUrl] = useState(null);
    const prevEndpoint = useRef(endpoint);
    const dataGrid = useRef(null);

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

    const exportToCSV = () => {
        function getGridContent(gridEl) {
            return {
              head: getRows('.rdg-header-row'),
              body: getRows('.rdg-row:not(.rdg-summary-row)'),
              foot: getRows('.rdg-summary-row')
            };
          
            function getRows(selector) {
              return Array.from(gridEl.querySelectorAll(selector)).map((gridRow) => {
                return Array.from(gridRow.querySelectorAll('.rdg-cell')).map(
                  (gridCell) => gridCell.innerText
                );
              });
            }
        }

        function serialize(value) {
            if (typeof value === 'string') {
              const formattedValue = value.replace(/"/g, '""');
              return formattedValue.includes(',') ? `"${formattedValue}"` : formattedValue;
            }
            return value;
        }

        const { head, body, foot } = getGridContent(dataGrid.current.element);
        const content = [...head, ...body, ...foot]
            .map((cells) => cells.map(serialize).join(','))
            .join('\n');
        downloadFile("export.csv", new Blob([content], { type: 'text/csv;charset=utf-8;' }));
    }

    useEffect(() => {
        if (prevEndpoint.current !== endpoint){
            // Switched endpoint, recreate params object

            setParams(Object.assign({},...endpoint.params.map(p => ({
                [p.name]: p['default'] !== undefined ? p['default'] : ''})
            )));
            prevEndpoint.current = endpoint;
        }else{

            // Update URL

            const urlParams = {};
            const queryParams = {};
            endpoint.params.forEach(p => {
                if (params[p.name] !== undefined && params[p.name] !== ''){
                    if (p.location === 'url'){
                        urlParams[p.name] = params[p.name];
                    }else{
                        queryParams[p.name] = params[p.name];
                    }
                }
            });
            let url = endpoint.url;
            for (let p in urlParams){
                url = url.replace(":" + p, urlParams[p]);
            }
            setUrl(buildUrlWithQuery(url, queryParams));
        }
    }, [endpoint, setParams, params]);

    useEffect(() => {
        if (!url) return;
        const controller = new AbortController();
        let request = null;
        
        const fetchData = async () => {
            setLoading(true);
            setColumns([]);
            setRows([]);
            setShowApply(false);
            setError("");
            
            if (request != null){
                controller.abort();
                request = null;
            }
                
            try {
                request = fetch(url, { signal: controller.signal });
                const response = await request;
                if (!response.ok) {
                    throw new Error(`Cannot load ${url}, status: ${response.status}`);
                }
                const rows = await response.json()
                let columns = [];
                if (rows.length > 0){
                    let row = rows[0];
                    columns = Object.keys(row).map(k => { 
                        let cell = {
                            key: k, 
                            name: keyToColumnLabel(k)
                        };
                        
                        // Format numbers
                        // if (typeof row[k] === 'number'){
                        //     cell.formatter = function({ row }){
                        //         return row[k].toLocaleString();
                        //     };
                        // }

                        return cell;
                    });
                }
                setRows(rows);
                setColumns(columns);
            } catch (err) {
                setError(err.message);
            } finally {
                request = null;
                setLoading(false);
            }
        };

        fetchData();
    }, [setError, url, setLoading]);

    return (<div className="ep-view">
        <div className="ep-header">
            <h3>{endpoint.name}</h3>
            <div className="ep-buttons">
                {showApply ? <button onClick={applyParams} className="btn btn-primary"><i className="fa fa-check"></i> Apply</button> : ""}
                <button onClick={openUrl} className="btn btn-light"><i className="fa fa-link"></i> URL</button>
                <button onClick={exportToCSV} className="btn btn-dark"><i className="fa fa-download"></i> Export as CSV</button>
            </div>
        </div>
        {endpoint.params ? <div className="params">
            {endpoint.params.map(p => <InputParam key={endpoint.url + p.name} p={p} updateParam={updateParam} onEnter={applyParams} />)}
        </div> : ""}
        {loading ? <div className="text-center"><i className="fa fa-spin fa-circle-notch"></i></div>
        : <DataGrid ref={dataGrid} className="rdg-light" columns={columns} rows={rows} />}

    </div>)
}

export default EpView;