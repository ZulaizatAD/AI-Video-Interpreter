import { useState, useCallback } from 'react';
import { toast } from 'react-hot-toast';

export const useVideoAnalysis = () => {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [progress, setProgress] = useState(0);

  const analyzeVideo = useCallback(async (file, analysisType, customPrompt) => {
    if (!file) {
      toast.error('Please select a video file first');
      return;
    }

    if (analysisType === 'custom' && !customPrompt?.trim()) {
      toast.error('Please enter a custom prompt for analysis');
      return;
    }

    setIsAnalyzing(true);
    setProgress(0);
    setResult(null);

    const formData = new FormData();
    formData.append('video_file', file);
    formData.append('analysis_type', analysisType);
    
    if (analysisType === 'custom') {
      formData.append('custom_prompt', customPrompt);
    }

    try {
      // Simulate progress
      const progressInterval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + Math.random() * 10;
        });
      }, 500);

      const response = await fetch('http://localhost:8000/analyze-video', {
        method: 'POST',
        body: formData,
      });

      clearInterval(progressInterval);
      setProgress(100);

      const data = await response.json();

      if (data.success) {
        setResult(data);
        toast.success('Video analysis completed!');
      } else {
        toast.error(data.error || 'Analysis failed');
        setResult(data);
      }
    } catch (error) {
      console.error('Error:', error);
      toast.error('Failed to analyze video. Please check your connection.');
      setResult({
        success: false,
        error: 'Network error occurred',
        analysis_type: analysisType
      });
    } finally {
      setIsAnalyzing(false);
      setTimeout(() => setProgress(0), 1000);
    }
  }, []);

  return {
    analyzeVideo,
    isAnalyzing,
    result,
    progress,
    setResult
  };
};