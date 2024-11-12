// src/pages/chat/MhaiChat.js

import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

import getCSRFToken from '../../libs/csrf';
// import ProfileSideBar from '../../components/mhai_chat/side_bar_menu'; // Optional if you want to include the sidebar

function MhaiChat() {
  const csrftoken = getCSRFToken();
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const [isSending, setIsSending] = useState(false);
  const lastMessageIdRef = useRef(null);
  const pollingInterval = 5000; // X seconds in milliseconds

  const apiUrl = '/api/chat/';

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
        params: {
          since_id: lastMessageIdRef.current,
        },
      })
      .then((response) => {
        if (response.data.length > 0) {
          setMessages((prevMessages) => [...prevMessages, ...response.data]);
          lastMessageIdRef.current = response.data[response.data.length - 1].id;
        }
      })
      .catch((error) => {
        console.error('Error checking for new messages:', error);
      });
  };

  // Function to handle sending a new message
  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!userInput.trim()) return;
    setIsSending(true);
    setError('');

    axios
      .post(
        apiUrl,
        { user_input: userInput },
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
        setIsSending(false);
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
        {/* Sidebar (Optional) */}
        {/* <div className="col-md-3">
          <ProfileSideBar active="chat" />
        </div> */}
        {/* Main Content */}
        <div className="col-md-12">
          <h2>Chat with AI</h2>
          <div className="chat-container" style={{ maxHeight: '60vh', overflowY: 'auto', border: '1px solid #ccc', padding: '1rem' }}>
            {messages.map((msg) => (
              <div key={msg.id}>
                <div><strong>You:</strong> {msg.user_input}</div>
                <div><strong>AI:</strong> {msg.ai_response}</div>
                <hr />
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

export default MhaiChat;
