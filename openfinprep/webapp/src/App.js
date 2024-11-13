import logo from './logo.svg';
import './App.css';
import MenuItem from './MenuItem';
import Alert from './Alert';
import EpView from './EpView';
import { useEffect, useState } from 'react';

function App() {
  const [endpoints, setEndpoints] = useState([]);
  const [error, setError] = useState(null);
  const [selectedEp, setSelectedEp] = useState(null);

  const onMount = async () => {
      try {
        const response = await fetch('/api/endpoints');
        if (!response.ok) {
          throw new Error(`Cannot load /api/endpoints, status: ${response.status}`);
        }
        const eps = await response.json();
        setEndpoints(eps);

        // Select first by default
        if (eps[0] && eps[0].endpoints) setSelectedEp(eps[0].endpoints[0]);
      } catch (err) {
        setError(err.message);
      }
  };

  useEffect(() => {
    onMount();
  }, []);

  return (
    <div className="app">
      <header className="header">
        <a href="/"><img src={logo} className="logo" alt="logo" title="OpenFinPrep" /></a>
      </header>

      <div className="main-container">
        <div className="ep-menu col-xs-5 col-sm-5 col-md-4 col-lg-3 col-xl-2">
          {endpoints.map(ep => 
            <MenuItem key={ep.group} title={ep.group}>
              {ep.endpoints.map(e => 
                <MenuItem key={e.name} title={e.name} tags={e.tags} onClick={() => setSelectedEp(e)} />)
              }
            </MenuItem>)}
        </div>
        <div className="main-content">
          {error ? <Alert setError={setError}>{error}</Alert> : ""}
          {selectedEp ? <EpView endpoint={selectedEp} setError={setError} /> : ""}
        </div>
      </div>
    </div>
  );
}

export default App;
