import logo from './logo.svg';
import './App.css';
import MenuItem from './MenuItem';
import Alert from './Alert';
import { useEffect, useState } from 'react';

function App() {
  const [endpoints, setEndpoints] = useState([]);
  const [error, setError] = useState(null);

  const fetchEndpoints = async () => {
      try {
        const response = await fetch('/endpoints');
        if (!response.ok) {
          throw new Error(`Cannot load endpoints, status: ${response.status}`);
        }
        setEndpoints(await response.json());
      } catch (err) {
        setError(err.message);
      }
  };

  useEffect(() => {
    fetchEndpoints(); // Call the fetch function when the component mounts
  }, []); // Empty dependency array means this runs once after initial render

  return (
    <div className="app">
      <header className="header">
        <a href="/"><img src={logo} className="logo" alt="logo" title="OpenFinPrep" /></a>
      </header>

      <div className="main-container">
        <div className="ep-menu">
          {endpoints.map(ep => 
            <MenuItem key={ep.group} title={ep.group}>
              {ep.endpoints.map(e => 
                <MenuItem key={e.name} title={e.name} tags={e.tags} />)
              }
            </MenuItem>)};
        </div>
        <div className="main-content">
          {error ? <Alert setError={setError}>{error}</Alert> : ""}
        </div>
      </div>
    </div>
  );
}

export default App;
