import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000, // 5 minutes timeout for video analysis
});

export const getAnalysisOptions = async () => {
  try {
    const response = await api.get('/analysis-options');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch analysis options');
  }
};

export const analyzeVideoFile = async (file, analysisType) => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('analysis_type', analysisType);

    const response = await api.post('/analyze-video-file', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to analyze video');
  }
};

export const analyzeVideoBase64 = async (videoBase64, analysisType, mimeType = 'video/mp4') => {
  try {
    const response = await api.post('/analyze-video', {
      analysis_type: analysisType,
      video_base64: videoBase64,
      mime_type: mimeType,
    });

    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to analyze video');
  }
};

export const checkHealth = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    throw new Error('API health check failed');
  }
};