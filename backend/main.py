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

load_dotenv()

app = FastAPI(
    title="AI Video Interpreter",
    description="Analyze videos using Google's Gemini AI",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LLM
try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp", api_key=os.getenv("GEMINI_API_KEY")
    )
except Exception as e:
    raise HTTPException(
        status_code=500, detail=f"Failed to initialize AI model: {str(e)}"
    )


# Pydantic models
class VideoAnalysisRequest(BaseModel):
    analysis_type: str
    custom_prompt: Optional[str] = None


class VideoAnalysisResponse(BaseModel):
    analysis_type: str
    analysis_description: str
    result: str
    success: bool
    error: Optional[str] = None


# Analysis options
analysis_options = {
    "detailed_summary": "Give a detailed summary of this video. Include information about the setting, people involved, actions taking place, objects visible, and any dialogue or audio elements.",
    "bullet_summary": "Summarize this video in a few short bullets. Focus on the key events and main points only.",
    "timestamped_summary": "Generate a paragraph that summarizes this video, with corresponding timecodes. Break down what happens at different time intervals and provide a comprehensive overview.",
    "quiz_generation": "Summarize this video in detail. Then create a quiz with 5-7 questions based on the information in this video. Include multiple choice, true/false, and short answer questions. Provide a complete answer key with explanations.",
    "technical_analysis": "Analyze the technical aspects of this video including camera work, lighting, editing techniques, and overall production quality.",
    "object_identification": "Identify and describe all the objects, people, and text visible in this video. Provide a comprehensive inventory of visual elements.",
    "custom": "Custom analysis based on user input",
}

# Create prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert video analyst. Analyze videos carefully and provide detailed descriptions.",
        ),
        (
            "human",
            [
                {"type": "text", "text": "{analysis_request}"},
                {"type": "media", "data": "{video_data}", "mime_type": "{mime_type}"},
            ],
        ),
    ]
)


def encode_video(video_content: bytes) -> str:
    """Encode video content to base64"""
    return base64.b64encode(video_content).decode()


def get_mime_type(filename: str) -> str:
    """Get MIME type based on file extension"""
    extension = filename.lower().split(".")[-1]
    mime_types = {
        "mp4": "video/mp4",
        "avi": "video/x-msvideo",
        "mov": "video/quicktime",
        "wmv": "video/x-ms-wmv",
        "flv": "video/x-flv",
        "webm": "video/webm",
        "mkv": "video/x-matroska",
    }
    return mime_types.get(extension, "video/mp4")


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "AI Video Interpreter API",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/analyze-video",
            "options": "/analysis-options",
            "health": "/health",
        },
    }


@app.get("/analysis-options")
async def get_analysis_options():
    """Get available analysis options"""
    return {
        "options": analysis_options,
        "usage": "Use the key (e.g., 'detailed_summary') as analysis_type in your request",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test if the AI model is accessible
        test_response = "AI Video Interpreter is healthy"
        return {"status": "healthy", "message": test_response}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")


@app.post("/analyze-video", response_model=VideoAnalysisResponse)
async def analyze_video(
    video_file: UploadFile = File(...),
    analysis_type: str = Form(...),
    custom_prompt: Optional[str] = Form(None),
):
    """
    Analyze a video file using AI

    - **video_file**: Video file to analyze (mp4, avi, mov, etc.)
    - **analysis_type**: Type of analysis to perform
    - **custom_prompt**: Custom prompt for analysis (required if analysis_type is 'custom')
    """

    # Validate analysis type
    if analysis_type not in analysis_options:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid analysis_type. Choose from: {list(analysis_options.keys())}",
        )

    # Validate custom prompt for custom analysis
    if analysis_type == "custom" and not custom_prompt:
        raise HTTPException(
            status_code=400,
            detail="custom_prompt is required when analysis_type is 'custom'",
        )

    try:
        # Read video content
        video_content = await video_file.read()

        # Check file size (limit to 50MB for example)
        max_size = 50 * 1024 * 1024  # 50MB
        if len(video_content) > max_size:
            raise HTTPException(
                status_code=413, detail="Video file too large. Maximum size is 50MB"
            )

        # Encode video
        encoded_video = encode_video(video_content)

        # Get MIME type
        mime_type = get_mime_type(video_file.filename)

        # Prepare analysis request
        if analysis_type == "custom":
            analysis_request = custom_prompt
        else:
            analysis_request = analysis_options[analysis_type]

        # Create chain and analyze
        chain = prompt | llm

        response = chain.invoke(
            {
                "analysis_request": analysis_request,
                "video_data": encoded_video,
                "mime_type": mime_type,
            }
        )

        return VideoAnalysisResponse(
            analysis_type=analysis_type,
            analysis_description=analysis_options.get(analysis_type, custom_prompt),
            result=response.content,
            success=True,
        )

    except HTTPException:
        raise
    except Exception as e:
        return VideoAnalysisResponse(
            analysis_type=analysis_type,
            analysis_description=analysis_options.get(
                analysis_type, custom_prompt or ""
            ),
            result="",
            success=False,
            error=str(e),
        )


@app.post("/analyze-video-from-path")
async def analyze_video_from_path(
    video_path: str = Form(...),
    analysis_type: str = Form(...),
    custom_prompt: Optional[str] = Form(None),
):
    """
    Analyze a video file from a local path (for development/testing)

    - **video_path**: Local path to video file
    - **analysis_type**: Type of analysis to perform
    - **custom_prompt**: Custom prompt for analysis (required if analysis_type is 'custom')
    """

    # Validate analysis type
    if analysis_type not in analysis_options:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid analysis_type. Choose from: {list(analysis_options.keys())}",
        )

    # Validate custom prompt for custom analysis
    if analysis_type == "custom" and not custom_prompt:
        raise HTTPException(
            status_code=400,
            detail="custom_prompt is required when analysis_type is 'custom'",
        )

    # Check if file exists
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video file not found")

    try:
        # Read video file
        with open(video_path, "rb") as video_file:
            video_content = video_file.read()

        # Encode video
        encoded_video = encode_video(video_content)

        # Get MIME type
        mime_type = get_mime_type(video_path)

        # Prepare analysis request
        if analysis_type == "custom":
            analysis_request = custom_prompt
        else:
            analysis_request = analysis_options[analysis_type]

        # Create chain and analyze
        chain = prompt | llm

        response = chain.invoke(
            {
                "analysis_request": analysis_request,
                "video_data": encoded_video,
                "mime_type": mime_type,
            }
        )

        return VideoAnalysisResponse(
            analysis_type=analysis_type,
            analysis_description=analysis_options.get(analysis_type, custom_prompt),
            result=response.content,
            success=True,
        )

    except Exception as e:
        return VideoAnalysisResponse(
            analysis_type=analysis_type,
            analysis_description=analysis_options.get(
                analysis_type, custom_prompt or ""
            ),
            result="",
            success=False,
            error=str(e),
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
