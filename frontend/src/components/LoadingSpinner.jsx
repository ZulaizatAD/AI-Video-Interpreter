import React from 'react';
import { Loader2 } from 'lucide-react';

const LoadingSpinner = () => {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <Loader2 className="w-8 h-8 text-secondary-500 animate-spin mb-4" />
      <p className="text-gray-600 mb-2">Analyzing your video...</p>
      <p className="text-sm text-gray-500">This may take a few moments</p>
    </div>
  );
};

export default LoadingSpinner;