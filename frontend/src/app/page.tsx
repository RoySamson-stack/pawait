'use client';

import { useState, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import ChatInput from '../components/ChatInput';
import ChatMessage from '../components/ChatMessage';
import ConversationHistory from '../components/ConversationHistory';
import LoadingSpinner from '../components/LoadingSpinner';
import { sendQuery } from '../services/api';

export default function Home() {
  const [conversations, setConversations] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load conversations from localStorage on initial render
  useEffect(() => {
    const savedConversations = localStorage.getItem('conversations');
    if (savedConversations) {
      try {
        setConversations(JSON.parse(savedConversations));
      } catch (error) {
        console.error('Failed to parse saved conversations:', error);
      }
    }
  }, []);

  // Save conversations to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem('conversations', JSON.stringify(conversations));
  }, [conversations]);

  const handleSendQuery = async (query) => {
    if (!query.trim()) return;
    
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await sendQuery(query);
      
      const newConversation = {
        id: uuidv4(),
        query,
        response: response.response,
        timestamp: new Date().toISOString(),
      };
      
      setConversations((prev) => [...prev, newConversation]);
    } catch (err) {
      console.error('Error sending query:', err);
      setError('Failed to get response. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const clearHistory = () => {
    setConversations([]);
    localStorage.removeItem('conversations');
  };

  return (
    <main className="flex flex-col md:flex-row min-h-screen">
      {/* Sidebar with conversation history */}
      <div className="md:w-1/4 bg-white border-r border-gray-200 p-4">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold text-red-800">History</h2>
          {conversations.length > 0 && (
            <button 
              onClick={clearHistory}
              className="text-sm text-red-500 hover:text-red-700"
            >
              Clear All
            </button>
          )}
        </div>
        <ConversationHistory conversations={conversations} />
      </div>
      
      {/* Main chat area */}
      <div className="flex-1 flex flex-col h-screen">
        {/* Header */}
        <header className="bg-white shadow-sm p-4 border-b border-gray-200">
          <h1 className="text-2xl font-bold text-center text-primary-700">LLM Q&A Assistant</h1>
        </header>
        
        {/* Messages area */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {conversations.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center text-gray-500">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
              <p className="text-xl font-medium">No conversations yet</p>
              <p className="mt-2 ">Ask a question to get started!</p>
            </div>
          ) : (
            conversations.map((item) => (
              <div key={item.id} className="space-y-2 text-black">
                <ChatMessage isUser={true}  content={item.query} timestamp={item.timestamp} />
                <ChatMessage isUser={false} content={item.response} timestamp={item.timestamp} />
              </div>
            ))
          )}
          
          {isLoading && (
            <div className="flex justify-center">
              <LoadingSpinner />
            </div>
          )}
          
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md">
              {error}
            </div>
          )}
        </div>
        
        {/* Input area */}
        <div className="p-4 border-t border-gray-200 bg-white text-black">
          <ChatInput onSendQuery={handleSendQuery} isLoading={isLoading} />
        </div>
      </div>
    </main>
  );
}