import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState('');
  const [error, setError] = useState('');
  const [dragActive, setDragActive] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragActive(true);
  };

  const handleDragLeave = () => {
    setDragActive(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const handleUpload = async (event) => {
    event.preventDefault();
    if (!file) {
      alert('Please select a file.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://127.0.0.1:8000/classify', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResult(response.data);
      setError(null);
    } catch (err) {
      setError('Error uploading or processing the file.');
      setResult(null);
    }
  };

  const handleClear = () => {
    setFile(null);
    setResult('');
    setError('');
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Email Classification</h1>
        <div
          className={`form-container ${dragActive ? 'drag-active' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <form onSubmit={handleUpload} className='upload-form'>
            <div className='file-input-container'>
              <label
                htmlFor="file-upload"
                className={`file-drop-zone ${dragActive ? 'drag-active' : ''}`}
              >
                {file ? file.name : 'Drag and drop a file here or click to upload'}
                <input
                  id="file-upload"
                  type="file"
                  onChange={handleFileChange}
                  className="pdf-input"
                  accept="application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/pdf,.eml,.doc,.docx"
                />
              </label>
            </div>
            <div>
              <button type="submit" className="submit-button">
                Upload and Classify
              </button>
              <button
                type="button"
                className="clear-button"
                onClick={handleClear}
                style={{ marginLeft: '10px' }}
              >
                Clear
              </button>
            </div>
          </form>
          <div className="response-text">
            {result && (
              <div className="mt-4">
                <h2 className="font-bold">Classification:</h2>
                <p>{result.classification}</p>
                <h2 className="font-bold">Confidence Score:</h2>
                <p>{result.confidence_score.toFixed(2)}</p>
                <h2 className="font-bold">Main Requests:</h2>
                <ul>
                  {result.main_requests.map((request, index) => (
                    <li key={index}>{request}</li>
                  ))}
                </ul>
                <h2 className="font-bold">Sub Requests:</h2>
                <ul>
                  {result.sub_requests.map((subRequest, index) => (
                    <li key={index}>{subRequest}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      </header>
    </div>
  );
}

export default App;