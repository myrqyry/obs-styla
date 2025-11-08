
import React, { useState } from 'react';
import axios from 'axios';

const Converter: React.FC = () => {
  const [jsonInput, setJsonInput] = useState('');
  const [ovtOutput, setOvtOutput] = useState('');

  const handleConvert = async () => {
    try {
      const r = await axios.post('/api/convert', { json: jsonInput });
      setOvtOutput(r.data.ovt);
    } catch (e: any) {
      setOvtOutput(`Conversion failed: ${String(e)}`);
    }
  };

  return (
    <div className="converter">
      <h3>JSON to OVT Converter</h3>
      <textarea
        className="converter-input"
        value={jsonInput}
        onChange={(e) => setJsonInput(e.target.value)}
        placeholder="Paste your JSON here"
      />
      <button onClick={handleConvert}>Convert</button>
      <textarea
        className="converter-output"
        value={ovtOutput}
        readOnly
        placeholder="OVT output will appear here"
      />
    </div>
  );
};

export default Converter;
