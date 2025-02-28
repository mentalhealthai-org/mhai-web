// src/pages/chat/MyDiary.js

import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

import getCSRFToken from '../../libs/csrf';

function MyDiary() {
  const csrftoken = getCSRFToken();
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const [isSending, setIsSending] = useState(false);
  const [pendingMessageId, setPendingMessageId] = useState(null);
  const lastMessageIdRef = useRef(null);
  const pollingInterval = 1000; // 1 second in milliseconds

  const apiUrl = '/api/my-diary/';

  // Function to fetch messages
  const fetchMessages = () => {
    axios
      .get(apiUrl, {
        withCredentials: true,
      })
      .then((response) => {
        setMessages(response.data);
        if (response.data.length > 0) {
          lastMessageIdRef.current = response.data[response.data.length - 1].id;

          const latestMessage = response.data[response.data.length - 1];
          if (!latestMessage.response) {
            setIsSending(true);
            setPendingMessageId(latestMessage.id);
          } else {
            setIsSending(false);
            setPendingMessageId(null);
          }
        } else {
          setIsSending(false);
          setPendingMessageId(null);
        }
        setLoading(false);
      })
      .catch((error) => {
        setError('Failed to fetch messages.');
        setLoading(false);
      });
  };

  // Fetch messages on component mount
  useEffect(() => {
    fetchMessages();

    // Set up polling
    const interval = setInterval(() => {
      checkForNewMessages();
    }, pollingInterval);

    // Clean up interval on component unmount
    return () => clearInterval(interval);
  }, []);

  // Function to check for new messages
  const checkForNewMessages = () => {
    axios
      .get(apiUrl, {
        withCredentials: true,
      })
      .then((response) => {
        setMessages(response.data);
        if (response.data.length > 0) {
          lastMessageIdRef.current = response.data[response.data.length - 1].id;
        }
      })
      .catch((error) => {
        console.error('Error checking for new messages:', error);
      });
  };

  // useEffect to monitor messages and pendingMessageId
  useEffect(() => {
    if (pendingMessageId !== null) {
      const pendingMessage = messages.find(
        (msg) => String(msg.id) === String(pendingMessageId)
      );
      if (pendingMessage && pendingMessage.response) {
        // AI response received
        setIsSending(false);
        setPendingMessageId(null);
      }
    }
  }, [messages, pendingMessageId]);

  // Function to handle sending a new message
  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!userInput.trim()) return;
    setIsSending(true);
    setError('');

    axios
      .post(
        apiUrl,
        { prompt: userInput },
        {
          withCredentials: true,
          headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
          },
        }
      )
      .then((response) => {
        setMessages((prevMessages) => [...prevMessages, response.data]);
        lastMessageIdRef.current = response.data.id;
        setUserInput('');
        setPendingMessageId(response.data.id);
        // isSending remains true until AI response is received
      })
      .catch((error) => {
        setError('Failed to send message.');
        setIsSending(false);
      });
  };

  // Scroll to the bottom of the chat when messages update
  const messagesEndRef = useRef(null);
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  if (loading) return <p>Loading chat...</p>;
  if (error) return <div className="alert alert-danger">{error}</div>;

  return (
    <div className="container mt-4">
      <div className="row">
        {/* Main Content */}
        <div className="col-md-12">
          <h2>Chat with AI</h2>

          <div className="chat-container" style={{ maxHeight: '60vh', overflowY: 'auto', paddingTop: '1rem' }}>
            {messages.map((msg) => (
              <div key={msg.id}>
                {/* User Message */}
                <div
                  className="p-3 rounded-3 mt-2 ms-5 position-relative"
                  style={{ backgroundColor: '#D5E8D4' }}
                >
                  <strong>You: </strong>
                  {msg.prompt}
                  <div className="small position-absolute" style={{ bottom: '5px', right: '10px' }}>
                    {msg.prompt_timestamp}
                  </div>
                </div>
                {/* AI Response */}
                {msg.response ? (
                  <div
                    className="p-3 rounded-3 mt-2 me-5 position-relative"
                    style={{ backgroundColor: '#D4E4F7' }}
                  >
                    <strong>Mhai:</strong> {msg.response}
                    <div className="small position-absolute" style={{ bottom: '5px', right: '10px' }}>
                      {msg.response_timestamp}
                    </div>
                  </div>
                ) : (
                  <div
                    className="p-3 rounded-3 mt-2 me-5 position-relative"
                    style={{ backgroundColor: '#D4E4F7' }}
                  >
                    <strong>Mhai:</strong> <em>Typing...</em>
                  </div>
                )}
              </div>
            ))}
            <div ref={messagesEndRef}></div>
          </div>

          <form onSubmit={handleSendMessage} className="mt-3">
            <div className="input-group">
              <input
                type="text"
                className="form-control"
                placeholder="Type your message..."
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                disabled={isSending}
              />
              <button className="btn btn-primary" type="submit" disabled={isSending}>
                {isSending ? 'Sending...' : 'Send'}
              </button>
            </div>
          </form>
          {error && <div className="alert alert-danger mt-2">{error}</div>}
        </div>
      </div>
    </div>
  );
}

export default MyDiary;
