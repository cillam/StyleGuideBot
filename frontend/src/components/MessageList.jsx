import { useEffect, useRef } from 'react';
import Message from './Message';

export default function MessageList({ messages, loading }) {
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto bg-gradient-to-b from-gray-50 to-gray-100 p-6">
      {messages.length === 0 && (
        <div className="flex flex-col items-center justify-center h-full text-center">
          <div className="w-16 h-16 mb-4 rounded-full bg-gradient-to-br from-purple-600 to-purple-500 flex items-center justify-center text-white shadow-lg">
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
          </div>
          <p className="text-2xl font-bold text-gray-800 mb-2">Welcome to StyleGuideBot!</p>
          <p className="text-gray-600 max-w-md">Ask me anything about the Wikipedia Manual of Style. I'm here to help with formatting, punctuation, and writing guidelines.</p>
        </div>
      )}
      
      {messages.map((message) => (
        <Message
          key={message.id}
          type={message.type}
          content={message.content}
          sources={message.sources}
        />
      ))}
      
      {loading && (
        <div className="flex gap-3 justify-start mb-6">
          <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-purple-600 to-purple-500 flex items-center justify-center text-white font-bold text-sm shadow-md">
            SG
          </div>
          <div className="bg-white px-4 py-3 rounded-2xl rounded-bl-md shadow-sm border border-gray-200">
            <div className="flex gap-1">
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
              <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
            </div>
          </div>
        </div>
      )}
      
      <div ref={messagesEndRef} />
    </div>
  );
}