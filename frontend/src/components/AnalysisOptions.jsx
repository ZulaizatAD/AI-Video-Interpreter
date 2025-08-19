import React from 'react';

const AnalysisOptions = ({ options, selectedType, onTypeChange }) => {
  const optionLabels = {
    detailed_summary: 'Detailed Summary',
    bullet_summary: 'Bullet Point Summary',
    timestamped_summary: 'Timestamped Summary',
    quiz_generation: 'Generate Quiz',
    technical_analysis: 'Technical Analysis',
    object_identification: 'Object Identification'
  };

  return (
    <div className="space-y-3">
      {Object.entries(options).map(([key, option]) => (
        <label
          key={key}
          className={`block p-4 border rounded-lg cursor-pointer transition-colors duration-200 ${
            selectedType === key
              ? 'border-secondary-500 bg-secondary-50'
              : 'border-primary-200 hover:border-secondary-300 hover:bg-primary-50'
          }`}
        >
          <div className="flex items-start space-x-3">
            <input
              type="radio"
              name="analysisType"
              value={key}
              checked={selectedType === key}
              onChange={(e) => onTypeChange(e.target.value)}
              className="mt-1 text-secondary-500 focus:ring-secondary-500"
            />
            <div className="flex-1">
              <h3 className="font-medium text-gray-800 mb-1">
                {optionLabels[key] || key}
              </h3>
              <p className="text-sm text-gray-600">{option.description}</p>
            </div>
          </div>
        </label>
      ))}
    </div>
  );
};

export default AnalysisOptions;