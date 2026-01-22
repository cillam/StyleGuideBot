import { useState, useEffect } from 'react';
import { styleGuideAPI } from '../services/api';
import { sessionManager } from '../utils/sessionManager';
import MessageList from './MessageList';
import MessageInput from './MessageInput';

export default function ChatContainer() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [queryCount, setQueryCount] = useState(0);

  // Initialize session on mount
  useEffect(() => {
    const id = sessionManager.getSessionId();
    setSessionId(id);
  }, []);

// Handle sending a message
const handleSendMessage = async (userMessage) => {
  if (!userMessage.trim()) return;

  // Add user message to chat
  const userMsg = {
    id: Date.now(),
    type: 'user',
    content: userMessage,
    timestamp: new Date()
  };
  setMessages(prev => [...prev, userMsg]);
  
  // Increment query count
  setQueryCount(prev => prev + 1);

  // Set loading state
  setLoading(true);
  setError(null);

  try {
    // Get reCAPTCHA token
    const recaptchaToken = await window.grecaptcha.execute(
      import.meta.env.VITE_RECAPTCHA_SITE_KEY,
      { action: 'submit' }
    );
    console.log('Sending:', { userMessage, sessionId, recaptchaToken });
    // Call API with token
    const response = await styleGuideAPI.query(userMessage, sessionId, recaptchaToken);

    // Add bot response to chat
    const botMsg = {
      id: Date.now() + 1,
      type: 'bot',
      content: response.answer,
      sources: response.sources,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, botMsg]);

  } catch (err) {
    setError('Failed to get response. Please try again.');
    console.error('Error:', err);
  } finally {
    setLoading(false);
  }
};

  // Handle starting new session
  const handleNewChat = async () => {
    // Delete the old session from database
    if (sessionId) {
      try {
        await styleGuideAPI.deleteSession(sessionId);
        console.log('Session deleted from database');
      } catch (error) {
        console.error('Failed to delete session:', error);
        // Continue anyway - clear the UI even if delete fails
      }
    }
    
    // Clear session storage and create new session
    sessionManager.clearSession();
    const newId = sessionManager.getSessionId();
    setSessionId(newId);
    setMessages([]);
    setError(null);
    setQueryCount(0);
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 to-purple-500 shadow-lg">
        <div className="max-w-4xl mx-auto flex justify-between items-center p-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center text-white font-bold shadow-md">
              SG
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">StyleGuideBot</h1>
              <div className="flex items-center gap-2">
                <p className="text-xs text-purple-100">Wikipedia Manual of Style Assistant</p>
                <span className="text-xs text-purple-200">•</span>
                <p className="text-xs text-purple-200">{queryCount}/20 queries</p>
              </div>
            </div>
          </div>
          <button 
            onClick={handleNewChat}
            className="px-4 py-2 bg-white/20 backdrop-blur-sm text-white rounded-lg hover:bg-white/30 transition-all font-medium shadow-md hover:shadow-lg"
          >
            <svg className="w-5 h-5 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            New Chat
          </button>
        </div>
      </div>
      
      {/* Messages */}
      <MessageList messages={messages} loading={loading} />
      
      {/* Error Display */}
      {(error || queryCount >= 20) && (
        <div className="bg-red-50 border-t-2 border-red-200 p-4">
          <div className="max-w-4xl mx-auto flex items-center gap-2 text-red-700">
            <svg className="w-5 h-5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            <span>{queryCount >= 20 ? "You've reached the maximum of 20 queries. Click 'New Chat' to continue." : error}</span>
          </div>
        </div>
      )}
      
      {/* Input */}
      <MessageInput 
        onSend={handleSendMessage} 
        disabled={loading || queryCount >= 20} 
      />
    </div>
  );
}