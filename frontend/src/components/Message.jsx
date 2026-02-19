import CitationCard from './CitationCard';
import ReactMarkdown from 'react-markdown';

export default function Message({ type, content, sources }) {
  const isUser = type === 'user';

  return (
    <div className={`flex gap-3 ${isUser ? 'justify-end' : 'justify-start'} mb-6`}>
      {/* Bot Avatar */}
      {!isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white font-bold text-sm shadow-md">
          SG
        </div>
      )}

      {/* Message Content */}
      <div className={`max-w-[75%] ${isUser ? 'order-2' : 'order-1'}`}>
        <div
          className={`px-4 py-3 rounded-2xl shadow-sm ${
            isUser
              ? 'bg-gradient-to-r from-purple-600 to-purple-500 text-white rounded-br-md'
              : 'bg-white text-gray-800 border border-gray-200 rounded-bl-md'
          }`}
        >
          {isUser ? (
            <p className="whitespace-pre-wrap leading-relaxed">{content}</p>
          ) : (
            <div className="[&>p]:mb-3 [&>h1]:mb-2 [&>h2]:mb-2 [&>h3]:mb-2 [&>ul]:mb-3 [&>ul]:list-disc [&>ul]:ml-5 [&>ol]:mb-3 [&>ol]:list-decimal [&>ol]:ml-5 [&>li]:mb-1">
              <ReactMarkdown>{content}</ReactMarkdown>
            </div>
          )}
        </div>
        {!isUser && <CitationCard sources={sources} />}
      </div>

      {/* User Avatar */}
      {isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-gray-600 to-gray-500 flex items-center justify-center text-white font-bold text-sm shadow-md">
          U
        </div>
      )}
    </div>
  );
}