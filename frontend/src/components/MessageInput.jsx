import { useState, useRef, useEffect } from 'react';

export default function MessageInput({ onSend, disabled }) {
  const [input, setInput] = useState('');
  const [error, setError] = useState('');
  const inputRef = useRef(null);

  // Auto-focus when disabled changes (bot finishes responding)
  useEffect(() => {
    if (!disabled && inputRef.current) {
      inputRef.current.focus();
    }
  }, [disabled]);

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const trimmedInput = input.trim();
    
    // Check minimum length
    if (trimmedInput.length < 3) {
      setError('Please enter at least 3 characters');
      setTimeout(() => setError(''), 2000);
      return;
    }
    
    // Check maximum length
    if (trimmedInput.length > 500) {
      setError('Message too long. Please keep it under 500 characters.');
      setTimeout(() => setError(''), 3000);
      return;
    }
    
    if (trimmedInput && !disabled) {
      setError('');
      onSend(trimmedInput);
      setInput('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="border-t bg-white p-4 shadow-lg">
      <div className="flex flex-col gap-2 max-w-4xl mx-auto">
        <div className="flex gap-3">
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={disabled}
            placeholder="Ask about Wikipedia's style guide..."
            className="flex-1 px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed transition-all"
          />
          <button
            type="submit"
            disabled={disabled || !input.trim()}
            className="px-6 py-3 bg-gradient-to-r from-purple-600 to-purple-500 text-white font-medium rounded-xl hover:from-purple-700 hover:to-purple-600 disabled:from-gray-300 disabled:to-gray-300 disabled:cursor-not-allowed shadow-md hover:shadow-lg transition-all transform hover:scale-105 active:scale-95"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </button>
        </div>
        {error && (
          <p className="text-xs text-red-600 ml-1">{error}</p>
        )}
      </div>
    </form>
  );
}