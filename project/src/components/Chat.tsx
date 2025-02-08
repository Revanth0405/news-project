import React, { useState } from 'react';
import { Send, Newspaper, Brain, Shield } from 'lucide-react';

interface Message {
  type: 'user' | 'ai';
  content: string;
}

interface Analysis {
  summary: string;
  ethical: string;
  insights: string[];
}

function Chat() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    setMessages(prev => [...prev, { type: 'user', content: input }]);
    
    setIsLoading(true);
    setTimeout(() => {
      setAnalysis({
        summary: "This is a simulated AI summary of the news topic you've requested. In a real application, this would contain an actual analysis of news articles related to your query.",
        ethical: "Here we would provide ethical considerations and potential biases in the news coverage.",
        insights: [
          "Key insight 1: Important statistical data",
          "Key insight 2: Relevant market trends",
          "Key insight 3: Social impact analysis"
        ]
      });
      setIsLoading(false);
    }, 1500);

    setInput('');
  };

  return (
    <div className="pt-16">
      <header className="bg-black/30 p-6 shadow-lg">
        <h1 className="text-3xl font-bold text-center text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400">
          AI POWERED NEWS SUMMARIZER WITH ETHICAL ANALYSIS AND KEY INSIGHTS
        </h1>
      </header>

      <div className="container mx-auto p-4 flex flex-col md:flex-row gap-6 max-w-7xl">
        <div className="flex-1 bg-gray-800/50 rounded-lg shadow-xl p-4">
          <div className="h-[60vh] overflow-y-auto mb-4 space-y-4">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`flex ${
                  message.type === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                <div
                  className={`max-w-[80%] rounded-lg p-3 ${
                    message.type === 'user'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-700 text-gray-100'
                  }`}
                >
                  {message.content}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-center">
                <div className="animate-pulse text-blue-400">Analyzing...</div>
              </div>
            )}
          </div>

          <form onSubmit={handleSubmit} className="flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Enter a news topic or query..."
              className="flex-1 bg-gray-700 text-white rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              type="submit"
              className="bg-blue-600 hover:bg-blue-700 rounded-lg px-4 py-2 transition-colors"
            >
              <Send className="w-5 h-5" />
            </button>
          </form>
        </div>

        {analysis && (
          <div className="md:w-96 bg-gray-800/50 rounded-lg shadow-xl p-4 space-y-6">
            <div>
              <div className="flex items-center gap-2 mb-2">
                <Newspaper className="w-5 h-5 text-blue-400" />
                <h2 className="text-xl font-semibold">Summary</h2>
              </div>
              <p className="text-gray-300">{analysis.summary}</p>
            </div>

            <div>
              <div className="flex items-center gap-2 mb-2">
                <Shield className="w-5 h-5 text-emerald-400" />
                <h2 className="text-xl font-semibold">Ethical Analysis</h2>
              </div>
              <p className="text-gray-300">{analysis.ethical}</p>
            </div>

            <div>
              <div className="flex items-center gap-2 mb-2">
                <Brain className="w-5 h-5 text-purple-400" />
                <h2 className="text-xl font-semibold">Key Insights</h2>
              </div>
              <ul className="list-disc list-inside text-gray-300 space-y-2">
                {analysis.insights.map((insight, index) => (
                  <li key={index}>{insight}</li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Chat;