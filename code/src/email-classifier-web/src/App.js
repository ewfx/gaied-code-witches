import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [subject, setSubject] = useState('');
  const [content, setContent] = useState('');
  const [file, setFile] = useState(null);
  const [result, setResult] = useState('');
  const [error, setError] = useState(''); 

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
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
                  'Content-Type': 'multipart/form-data'
              }
          });

          setResult(response.data);
          setError(null);
      } catch (err) {
          setError('Error uploading or processing the file.');
          setResult(null);
      }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Email Classification</h1>
        <div className="form-container">
          <form>
            <div>
              <input
                type="text"
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                placeholder="Enter subject"
                className="subject-input"
              />
              <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Enter email content"
                className="content-textarea"
              />
              <input type="file" onChange={handleFileChange} className="pdf-input" accept="application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/pdf,.eml,.doc,.docx" />
            </div>
            <div>
              <button type="submit" className="submit-button" onClick={handleUpload}>Upload and Classify</button>
            </div>
          </form>
          <div
            className="response-text"
          >
            {result && (
                        <div className="mt-4">
                            <h2 className="font-bold">Classification:</h2>
                            <p>{result.classification}</p>
                            <h2 className="font-bold">Confidence Score:</h2>
                            <p>{result.confidence_score}</p>
                            <h2 className="font-bold">Requests:</h2>
                            <p> {result.main_requests} </p>
                            <h2 className="font-bold">Sub Requests: </h2>
                            <p> {result.sub_requests} </p>
                        </div>
                    )
            }
          </div>
        </div>
      </header>
    </div>
  );
}

export default App;