import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [files, setFiles] = useState([]); // Updated to handle multiple files
  const [result, setResult] = useState('');
  const [error, setError] = useState('');
  const [dragActive, setDragActive] = useState(false);

  const handleFileChange = (e) => {
    setFiles(Array.from(e.target.files)); // Convert FileList to an array
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
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      setFiles(Array.from(e.dataTransfer.files)); // Convert FileList to an array
    }
  };

  const handleUpload = async (event) => {
    event.preventDefault();
    if (files.length === 0) {
      alert('Please select at least one file.');
      return;
    }

    const formData = new FormData();
    files.forEach((file) => formData.append('files', file)); // Append all files
  
    try {
      const response = await axios.post('http://127.0.0.1:8000/classify', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResult(response.data);
      setError(null);
      console.log("response.dat", response.data);
      console.log("response.data.results", response.data.results);
      console.log(result);
    } catch (err) {
      setError('Error uploading or processing the files.');
   //   setResult(null);
    }
  };

  const handleClear = () => {
    setFiles([]);
    setResult('');
    setError('');
  };

  return (
    <div className="App">
      <div className="App-container">
        <h1>Email Classification Orchestrator</h1>
        <div
          className={`form-container ${dragActive ? 'drag-active' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <form onSubmit={handleUpload} className="upload-form">
            <div className="file-input-container">
              <label
                htmlFor="file-upload"
                className={`file-drop-zone ${dragActive ? 'drag-active' : ''}`}
              >
                {files.length > 0
                  ? files.map((file) => file.name).join(', ')
                  : 'Drag and drop files here or click to upload'}
                <input
                  id="file-upload"
                  type="file"
                  onChange={handleFileChange}
                  className="pdf-input"
                  accept="application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/pdf,.eml,.doc,.docx"
                  multiple // Allow multiple file uploads
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
            {result && Array.isArray(result) && (
              <div className="mt-4">
                <h2 className="font-bold">Classification Results:</h2>
                <ul className='classification-list'>
                  {result.map((fileResult, index) => (
                     <li key={index} className="file-result">
                     <h3>Filename: {fileResult.filename}</h3>
                     <p><strong>Classification:</strong> {fileResult.classification}</p>
                     <p><strong>Confidence Score:</strong> {(fileResult.confidence_score * 100).toFixed(2)}%</p>
                     <p><strong>Main Request:</strong> {fileResult.main_request || "Unknown"}</p>
                     <p><strong>Sub Requests:</strong></p>
                     {fileResult.sub_requests.length > 0 ? (
                       <ul>
                         {fileResult.sub_requests.map((subRequest, subIndex) => (
                           <li key={subIndex}>{subRequest}</li>
                         ))}
                       </ul>
                     ) : (
                       <p>No sub-requests found.</p>
                     )}
                   </li>
                  ))} 
                </ul>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;