import './EpView.css';
import 'react-data-grid/lib/styles.css';
import { useEffect, useState } from 'react';
import DataGrid from 'react-data-grid';

function EpView({ endpoint, setError }){
    const [rows, setRows] = useState([]);
    const [columns, setColumns] = useState([]);
    
    const keyToColumnLabel = key => {
        return key.replace(/_([a-z])/g, (_, letter) => ` ${letter.toUpperCase()}`)
                     .replace(/^\w/, c => c.toUpperCase());
    };

    useEffect(() => {
        const controller = new AbortController();
        let request = null;
        
        const fetchData = async () => {
            setColumns([]);
            setRows([]);
            
            if (request != null){
                controller.abort();
                request = null;
                }
                
            try {
                request = fetch(endpoint.url, { signal: controller.signal });
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
    }, [endpoint, setError]);
    
    return (<div className="ep-view">
        <div className="ep-header">
            <h3>{endpoint.name}</h3>
        </div>
        <DataGrid columns={columns} rows={rows} />
    </div>)
}

export default EpView;