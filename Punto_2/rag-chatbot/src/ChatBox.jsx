import React, { useState, useCallback } from 'react';
import axios from 'axios';
import './ChatBox.css';

function parseTaggedMessage(message) {
const regex = /^\[(\w+)]\s*/;
const match = message.match(regex);

if (match) {
const tag = match[1];
const content = message.replace(regex, '');
return { tag, content };
}

return { tag: null, content: message };
}


const ChatBox = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const token = process.env.REACT_APP_TOKEN;
  const headers = { headers: { Authorization: token } };



  const sendMessage = useCallback(async () => {
    if (!input.trim()) return;

    const userMsg = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
        const improveResp = await axios.post(
            process.env.REACT_APP_API_IMPROVE,
            { question: input },
            headers
            );
        const improved = improveResp.data.answer;

        const { tag, content } = parseTaggedMessage(improved);
            
        if (tag === 'real') {
        const retrieveResp = await axios.post(
            process.env.REACT_APP_API_RETRIEVE,
            { question: content },
            headers
        );
        const answer = retrieveResp.data.answer;
        const generateResp = await axios.post(
            process.env.REACT_APP_API_GENERATE,
            {
            question: content,
            answer: answer,
            },
            headers
        );
        const botMsg = { role: 'bot', content: generateResp.data.answer };
        setMessages((prev) => [...prev, botMsg]);
        } else {
        const botMsg = { role: 'bot', content: content };
        setMessages((prev) => [...prev, botMsg]);
        }
      setInput('');
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        { role: 'error', content: 'Error al obtener respuesta del RAG' },
      ]);
    } finally {
      setLoading(false);
    }
  }, [input, headers]);

  return (
    <div className="chat-container">
      <div className="chat-title">The Chosen One</div>
      <div className="chat-subtitle">Chat con RAG</div>

      <div className="chat-box">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <span className={`bubble ${msg.role}`}>
              <strong>
                {msg.role === 'user'
                  ? 'Tú'
                  : msg.role === 'bot'
                  ? 'RAGBot'
                  : 'Error'}
                :
              </strong>{' '}
              {msg.content}
            </span>
          </div>
        ))}
        {loading && (
          <div className="message bot">
            <span className="bubble bot">
              <em>RAG está pensando...</em>
            </span>
          </div>
        )}
      </div>

      <div className="input-container">
        <input
          className="chat-input"
          type="text"
          placeholder="Escribe tu pregunta..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
        />
        <button onClick={sendMessage} className="chat-button">
          Enviar
        </button>
      </div>
    </div>
  );
};

export default ChatBox;
