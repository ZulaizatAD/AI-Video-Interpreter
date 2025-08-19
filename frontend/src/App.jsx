import React, { useState } from "react";
import Header from "./components/Header";
import VideoUploader from "./components/VideoUploader";
import AnalysisOptions from "./components/AnalysisOptions";
import ResultsDisplay from "./components/ResultsDisplay";
import LoadingSpinner from "./components/LoadingSpinner";
import { analyzeVideoFile, getAnalysisOptions } from "./services/api";
import { FileVideo, AlertCircle } from "lucide-react";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [analysisType, setAnalysisType] = useState("");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [analysisOptions, setAnalysisOptions] = useState({});

  React.useEffect(() => {
    fetchAnalysisOptions();
  }, []);

  const fetchAnalysisOptions = async () => {
    try {
      const options = await getAnalysisOptions();
      setAnalysisOptions(options.analysis_options);
    } catch (err) {
      setError("Failed to fetch analysis options");
    }
  };

  const handleFileSelect = (file) => {
    setSelectedFile(file);
    setResults(null);
    setError(null);
  };

  const handleAnalysisTypeChange = (type) => {
    setAnalysisType(type);
  };

  const handleAnalyze = async () => {
    if (!selectedFile || !analysisType) {
      setError("Please select a video file and analysis type");
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const result = await analyzeVideoFile(selectedFile, analysisType);
      setResults(result);
    } catch (err) {
      setError(err.message || "Analysis failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setAnalysisType("");
    setResults(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-background-primary">
      <Header />

      <main className="container mx-auto px-4 py-8 max-w-6xl">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column - Upload and Options */}
          <div className="space-y-6">
            {/* Video Upload Section */}
            <div className="card">
              <div className="flex items-center mb-4">
                <FileVideo className="w-6 h-6 text-secondary-500 mr-2" />
                <h2 className="text-xl font-semibold text-gray-800">
                  Upload Video
                </h2>
              </div>
              <VideoUploader
                onFileSelect={handleFileSelect}
                selectedFile={selectedFile}
              />
            </div>

            {/* Analysis Options */}
            <div className="card">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">
                Analysis Type
              </h2>
              <AnalysisOptions
                options={analysisOptions}
                selectedType={analysisType}
                onTypeChange={handleAnalysisTypeChange}
              />
            </div>

            {/* Action Buttons */}
            <div className="flex space-x-4">
              <button
                onClick={handleAnalyze}
                disabled={!selectedFile || !analysisType || loading}
                className="btn-primary flex-1"
              >
                {loading ? "Analyzing..." : "Analyze Video"}
              </button>
              <button
                onClick={handleReset}
                className="btn-secondary"
                disabled={loading}
              >
                Reset
              </button>
            </div>

            {/* Error Display */}
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start">
                <AlertCircle className="w-5 h-5 text-red-500 mr-2 mt-0.5 flex-shrink-0" />
                <p className="text-red-700">{error}</p>
              </div>
            )}
          </div>

          {/* Right Column - Results */}
          <div className="card">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">
              Analysis Results
            </h2>

            {loading && <LoadingSpinner />}

            {results && !loading && <ResultsDisplay results={results} />}

            {!results && !loading && (
              <div className="text-center py-12 text-gray-500">
                <FileVideo className="w-16 h-16 mx-auto mb-4 opacity-50" />
                <p>Upload a video and select an analysis type to get started</p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
