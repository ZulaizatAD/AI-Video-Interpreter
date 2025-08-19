import React from "react";
import { Copy, CheckCircle } from "lucide-react";

const ResultsDisplay = ({ results }) => {
  const [copied, setCopied] = React.useState(false);

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(results.result);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error("Failed to copy text: ", err);
    }
  };

  const formatResult = (text) => {
    // Split by double newlines to create paragraphs
    const paragraphs = text.split("\n\n");
    return paragraphs.map((paragraph, index) => (
      <p key={index} className="mb-4 last:mb-0">
        {paragraph.split("\n").map((line, lineIndex) => (
          <React.Fragment key={lineIndex}>
            {line}
            {lineIndex < paragraph.split("\n").length - 1 && <br />}
          </React.Fragment>
        ))}
      </p>
    ));
  };

  return (
    <div className="space-y-4">
      {/* Analysis Info */}
      <div className="bg-primary-50 border border-primary-200 rounded-lg p-4">
        <h3 className="font-medium text-gray-800 mb-2">Analysis Type</h3>
        <p className="text-sm text-gray-600">{results.analysis_description}</p>
      </div>

      {/* Results */}
      <div className="relative">
        <div className="flex items-center justify-between mb-3">
          <h3 className="font-medium text-gray-800">Results</h3>
          <button
            onClick={copyToClipboard}
            className="flex items-center space-x-2 text-sm text-secondary-600 hover:text-secondary-700 transition-colors duration-200"
          >
            {copied ? (
              <>
                <CheckCircle className="w-4 h-4" />
                <span>Copied!</span>
              </>
            ) : (
              <>
                <Copy className="w-4 h-4" />
                <span>Copy</span>
              </>
            )}
          </button>
        </div>

        <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 max-h-96 overflow-y-auto">
          <div className="text-gray-800 leading-relaxed whitespace-pre-wrap">
            {formatResult(results.result)}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultsDisplay;
