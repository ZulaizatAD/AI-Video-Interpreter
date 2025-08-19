import React from 'react';
import { Video, Brain } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-white shadow-sm border-b border-primary-200">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-secondary-500 p-2 rounded-lg">
              <Video className="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-800">AI Video Interpreter</h1>
              <p className="text-gray-600">Analyze videos with advanced AI technology</p>
            </div>
          </div>
          <div className="flex items-center space-x-2 text-secondary-600">
            <Brain className="w-5 h-5" />
            <span className="text-sm font-medium">Powered by Gemini AI</span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;