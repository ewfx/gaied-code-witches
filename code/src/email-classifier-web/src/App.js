import React, { useState } from 'react';
import './App.css';

function App() {
  const [subject, setSubject] = useState('');
  const [content, setContent] = useState('');
  const [pdfLink, setPdfLink] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await fetch('https://api.example.com/send-email', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ subject, content, pdfLink }),
      });
      const data = await response.json();
      setResponse(JSON.stringify(data, null, 2));
      console.log('Success:', data);
    } catch (error) {
      setResponse('Error: ' + error.toString());
      console.error('Error:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Email Orchestrator</h1>
        <div className="form-container">
          <form onSubmit={handleSubmit}>
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
              <input
                type="text"
                value={pdfLink}
                onChange={(e) => setPdfLink(e.target.value)}
                placeholder="Enter PDF attachment link"
                className="pdf-input"
              />
            </div>
            <div>
              <button type="submit" className="submit-button">Submit</button>
            </div>
          </form>
          <textarea
            value={response}
            readOnly
            placeholder="Response will be shown here"
            className="response-textarea"
          />
        </div>
      </header>
    </div>
  );
}

export default App;