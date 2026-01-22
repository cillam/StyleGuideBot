import { useState } from 'react';

export default function CitationCard({ sources }) {
  const [expandedIndex, setExpandedIndex] = useState(null);

  if (!sources || sources.length === 0) {
    return null;
  }

  const toggleExpand = (index) => {
    setExpandedIndex(expandedIndex === index ? null : index);
  };

  return (
    <div className="mt-3 space-y-2">
      <p className="text-xs text-gray-600 font-semibold uppercase tracking-wide">Sources</p>
      <div className="space-y-2">
        {sources.map((source, index) => (
          <div key={index} className="border border-purple-200 rounded-lg overflow-hidden bg-gradient-to-r from-purple-50 to-purple-100">
            <button
              onClick={() => toggleExpand(index)}
              className="w-full flex items-center justify-between px-3 py-2 text-left hover:bg-purple-100 transition-colors"
            >
              <span className="flex items-center gap-2 text-xs font-medium text-purple-700">
                <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10A7.968 7.968 0 0014.5 4c-1.255 0-2.443.29-3.5.804V12a1 1 0 11-2 0V4.804z" />
                </svg>
                {source.title}
              </span>
              <svg
                className={`w-4 h-4 text-purple-600 transition-transform ${
                  expandedIndex === index ? 'rotate-180' : ''
                }`}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            
            {expandedIndex === index && (
              <div className="px-3 py-3 bg-white border-t border-purple-200">
                <p className="text-xs text-gray-700 leading-relaxed whitespace-pre-wrap">
                  {source.content}
                </p>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}