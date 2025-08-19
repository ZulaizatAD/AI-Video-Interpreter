# AI-Video-Interpreter
A web application that uses AI technology to analyze and interpret video content. Upload any video file and get detailed insights, summaries, technical analysis, and more using Google's Gemini AI.


AI Video Interpreter
React
FastAPI
Tailwind CSS

🎯 Features

Drag & Drop Video Upload - Easy file upload with support for multiple video formats
Multiple Analysis Types - Choose from 6 different analysis options:

Detailed Summary
Bullet Point Summary  
Timestamped Summary
Quiz Generation
Technical Analysis
Object Identification

Real-time Processing - Live analysis with loading indicators
Copy Results - One-click copy functionality for analysis results
Responsive Design - Works seamlessly on desktop and mobile devices

🛠️ Tech Stack

Frontend

React 19.1.1 - Modern JavaScript library for building user interfaces
Vite 7.1.2 - Fast build tool and development server
Tailwind CSS 3.4.1 - Utility-first CSS framework for styling
Axios - HTTP client for API communication
React Dropzone - Drag and drop file upload component
Lucide React - Beautiful icon library

Backend

FastAPI - Modern, fast Python web framework for building APIs
LangChain - Framework for developing applications with language models
Google Gemini AI - Advanced AI model for video analysis
Python-multipart - File upload handling
Uvicorn - ASGI server for running FastAPI applications

Development Tools

ESLint - Code linting and formatting
PostCSS - CSS processing tool
Autoprefixer - CSS vendor prefix automation

🔧 API Endpoints

Backend API (Port 8000)

GET / - API information and available endpoints
GET /analysis-options - Get available analysis types
POST /analyze-video-file - Analyze uploaded video file
POST /analyze-video - Analyze base64 encoded video
POST /analyze-local-video - Analyze video from local path
GET /health - Health check endpoint

Frontend Development Server (Port 3000)

Main application interface
Real-time communication with backend API

Preview
<img width="1100" height="945" alt="image" src="https://github.com/user-attachments/assets/40e58b13-c683-4dc6-8102-c8830b10bd16" />
