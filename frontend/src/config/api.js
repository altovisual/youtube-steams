// API Configuration
export const API_BASE_URL = import.meta.env.VITE_API_URL || 
  (import.meta.env.MODE === 'production' 
    ? 'https://youtube-steams-backend.onrender.com'
    : 'http://localhost:8000');

export const API_ENDPOINTS = {
  videoInfo: `${API_BASE_URL}/api/video-info`,
  download: `${API_BASE_URL}/api/download`,
  downloadVideo: `${API_BASE_URL}/api/download-video`,
  separateStems: `${API_BASE_URL}/api/separate-stems`,
  downloadFile: (fileId) => `${API_BASE_URL}/api/download-file/${fileId}`,
  downloadVideoFile: (fileId) => `${API_BASE_URL}/api/download-video-file/${fileId}`,
  downloadStem: (fileId, stemName) => `${API_BASE_URL}/api/download-stem/${fileId}/${stemName}`
};
