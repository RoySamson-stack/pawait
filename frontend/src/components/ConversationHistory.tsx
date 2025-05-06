'use client';

export default function ConversationHistory({ conversations }) {
  // Group conversations by date
  const groupedConversations = conversations.reduce((groups, conversation) => {
    const date = new Date(conversation.timestamp).toLocaleDateString();
    if (!groups[date]) {
      groups[date] = [];
    }
    groups[date].push(conversation);
    return groups;
  }, {});

  // Format date for display
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);
    
    if (date.toDateString() === today.toDateString()) {
      return 'Today';
    } else if (date.toDateString() === yesterday.toDateString()) {
      return 'Yesterday';
    } else {
      return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
      });
    }
  };

  // Format time for display
  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  // Truncate text for display
  const truncateText = (text, maxLength = 40) => {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  };

  return (
    <div className="space-y-4">
      {Object.keys(groupedConversations).length === 0 ? (
        <div className="text-center py-4 text-gray-500">
          No conversation history
        </div>
      ) : (
        Object.entries(groupedConversations)
          .sort(([dateA], [dateB]) => new Date(dateB) - new Date(dateA))
          .map(([date, items]) => (
            <div key={date} className="space-y-2">
              <h3 className="text-xs font-medium text-gray-500 uppercase tracking-wider">
                {formatDate(date)}
              </h3>
              <div className="space-y-1">
                {items
                  .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
                  .map((item) => (
                    <div
                      key={item.id}
                      className="p-2 rounded-md hover:bg-gray-100 cursor-pointer text-sm"
                    >
                      <div className="font-medium text-gray-800">
                        {truncateText(item.query)}
                      </div>
                      <div className="text-xs text-gray-500">
                        {formatTime(item.timestamp)}
                      </div>
                    </div>
                  ))}
              </div>
            </div>
          ))
      )}
    </div>
  );
}