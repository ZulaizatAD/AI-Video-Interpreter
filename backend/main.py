import os
import base64
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import tempfile
import aiofiles

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AI Video Interpreter",
    description="Analyze videos using Google's Gemini AI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp", 
    api_key=os.getenv("GEMINI_API_KEY")
)

# Pydantic models
class VideoAnalysisRequest(BaseModel):
    analysis_type: str
    video_base64: str
    mime_type: str = "video/mp4"

class VideoAnalysisResponse(BaseModel):
    analysis_type: str
    analysis_description: str
    result: str
    success: bool

# Analysis options
ANALYSIS_OPTIONS = {
    "detailed_summary": "Give a detailed summary of this video. Include information about the setting, people involved, actions taking place, objects visible, and any dialogue or audio elements.",
    "bullet_summary": "Summarize this video in a few short bullets. Focus on the key events and main points only.",
    "timestamped_summary": "Generate a paragraph that summarizes this video, with corresponding timecodes. Break down what happens at different time intervals and provide a comprehensive overview.",
    "quiz_generation": "Summarize this video in detail. Then create a quiz with 5-7 questions based on the information in this video. Include multiple choice, true/false, and short answer questions. Provide a complete answer key with explanations.",
    "technical_analysis": "Analyze the technical aspects of this video including camera work, lighting, editing techniques, and overall production quality.",
    "object_identification": "Identify and describe all the objects, people, and text visible in this video. Provide a comprehensive inventory of visual elements."
}

# Create prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert video analyst. Analyze videos carefully and provide detailed descriptions."),
    ("human", [
        {
            "type": "text",
            "text": "{analysis_request}"
        },
        {
            "type": "media",
            "data": "{video_data}",
            "mime_type": "{mime_type}"
        }
    ])
])

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "AI Video Interpreter API",
        "version": "1.0.0",
        "endpoints": {
            "analyze_video": "/analyze-video",
            "analyze_video_file": "/analyze-video-file",
            "get_analysis_options": "/analysis-options"
        }
    }

@app.get("/analysis-options")
async def get_analysis_options():
    """Get available analysis options"""
    return {
        "analysis_options": {
            key: {
                "key": key,
                "description": value[:100] + "..." if len(value) > 100 else value
            }
            for key, value in ANALYSIS_OPTIONS.items()
        }
    }

@app.post("/analyze-video", response_model=VideoAnalysisResponse)
async def analyze_video(request: VideoAnalysisRequest):
    """Analyze video from base64 encoded data"""
    try:
        # Validate analysis type
        if request.analysis_type not in ANALYSIS_OPTIONS:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid analysis type. Available options: {list(ANALYSIS_OPTIONS.keys())}"
            )
        
        # Create chain
        chain = prompt | llm
        
        # Invoke the chain
        response = chain.invoke({
            "analysis_request": ANALYSIS_OPTIONS[request.analysis_type],
            "video_data": request.video_base64,
            "mime_type": request.mime_type
        })
        
        return VideoAnalysisResponse(
            analysis_type=request.analysis_type,
            analysis_description=ANALYSIS_OPTIONS[request.analysis_type],
            result=response.content,
            success=True
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/analyze-video-file")
async def analyze_video_file(
    file: UploadFile = File(...),
    analysis_type: str = Form(...)
):
    """Analyze video from uploaded file"""
    try:
        # Validate file type
        if not file.content_type.startswith('video/'):
            raise HTTPException(status_code=400, detail="File must be a video")
        
        # Validate analysis type
        if analysis_type not in ANALYSIS_OPTIONS:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid analysis type. Available options: {list(ANALYSIS_OPTIONS.keys())}"
            )
        
        # Read and encode video file
        video_content = await file.read()
        encoded_video = base64.b64encode(video_content).decode()
        
        # Create chain
        chain = prompt | llm
        
        # Invoke the chain
        response = chain.invoke({
            "analysis_request": ANALYSIS_OPTIONS[analysis_type],
            "video_data": encoded_video,
            "mime_type": file.content_type
        })
        
        return VideoAnalysisResponse(
            analysis_type=analysis_type,
            analysis_description=ANALYSIS_OPTIONS[analysis_type],
            result=response.content,
            success=True
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/analyze-local-video")
async def analyze_local_video(
    file_path: str = Form(...),
    analysis_type: str = Form(...)
):
    """Analyze video from local file path (for development/testing)"""
    try:
        # Validate analysis type
        if analysis_type not in ANALYSIS_OPTIONS:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid analysis type. Available options: {list(ANALYSIS_OPTIONS.keys())}"
            )
        
        # Check if file exists
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Video file not found")
        
        # Read and encode video file
        with open(file_path, "rb") as video_file:
            encoded_video = base64.b64encode(video_file.read()).decode()
        
        # Create chain
        chain = prompt | llm
        
        # Invoke the chain
        response = chain.invoke({
            "analysis_request": ANALYSIS_OPTIONS[analysis_type],
            "video_data": encoded_video,
            "mime_type": "video/mp4"  # Default to mp4, could be enhanced to detect actual type
        })
        
        return VideoAnalysisResponse(
            analysis_type=analysis_type,
            analysis_description=ANALYSIS_OPTIONS[analysis_type],
            result=response.content,
            success=True
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "AI Video Interpreter"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)