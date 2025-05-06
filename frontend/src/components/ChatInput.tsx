'use client';

import { useState } from 'react';

export default function ChatInput({ onSendQuery, isLoading }) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim() && !isLoading) {
      onSendQuery(query);
      setQuery('');
    }
  };

  const handleKeyDown = (e) => {
    // Submit on Enter (without Shift key)
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="relative">
      <textarea
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={handleKeyDown}
        className="input min-h-[60px] max-h-[200px] resize-y pr-[100px]"
        placeholder="Ask a question..."
        disabled={isLoading}
      />
      <button
        type="submit"
        disabled={!query.trim() || isLoading}
        className={`absolute right-2 bottom-2 btn ${
          !query.trim() || isLoading ? 'bg-gray-300 text-gray-500 cursor-not-allowed' : 'btn-primary'
        }`}
      >
        {isLoading ? 'Sending...' : 'Send'}
      </button>
      <div className="absolute left-2 bottom-2 text-xs text-gray-500">
        {query.length > 0 ? `${query.length} characters` : 'Type your question'}
      </div>
    </form>
  );
}