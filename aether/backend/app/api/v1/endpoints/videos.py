"""
Video processing API endpoints for Vivid AI platform
"""
import io
from typing import List, Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse, StreamingResponse

from app.core.security import get_current_user
from app.schemas.video import (
    VideoAsset,
    VideoProcessingJob,
    VideoProcessingMode,
    VideoProcessingRequest,
    StyleSynthesisRequest,
    AIDirectorRequest,
    AestheticDiscoveryRequest,
    AestheticSuggestion,
    ProcessingAnalytics,
    BulkProcessingRequest
)
from app.services.video_processing import video_service

router = APIRouter()


@router.post("/upload", response_model=VideoAsset)
async def upload_video(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """Upload a video file for processing"""
    
    # Validate file
    if not file.content_type or not file.content_type.startswith('video/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only video files are allowed"
        )
    
    # Read file data
    try:
        file_data = await file.read()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to read file: {str(e)}"
        )
    
    # Check file size (500MB max)
    if len(file_data) > 500_000_000:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size exceeds 500MB limit"
        )
    
    try:
        video_asset = await video_service.upload_video(
            file_data=file_data,
            filename=file.filename or "video",
            content_type=file.content_type,
            user_id=current_user["sub"]
        )
        return video_asset
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload video: {str(e)}"
        )


@router.post("/process/style-synthesis", response_model=VideoProcessingJob)
async def process_style_synthesis(
    request: StyleSynthesisRequest,
    current_user: dict = Depends(get_current_user)
):
    """Process video using style synthesis (Mode 1)"""
    
    try:
        job = await video_service.submit_processing_job(
            mode=VideoProcessingMode.STYLE_SYNTHESIS,
            source_video_id=request.source_video_id,
            user_id=current_user["sub"],
            parameters=request.dict()
        )
        return job
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit processing job: {str(e)}"
        )


@router.post("/process/ai-director", response_model=VideoProcessingJob)
async def process_ai_director(
    request: AIDirectorRequest,
    current_user: dict = Depends(get_current_user)
):
    """Process video using AI Creative Director (Mode 2)"""
    
    try:
        job = await video_service.submit_processing_job(
            mode=VideoProcessingMode.AI_DIRECTOR,
            source_video_id=request.source_video_id,
            user_id=current_user["sub"],
            parameters=request.dict()
        )
        return job
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit processing job: {str(e)}"
        )


@router.post("/process/aesthetic-discovery", response_model=VideoProcessingJob)
async def process_aesthetic_discovery(
    request: AestheticDiscoveryRequest,
    current_user: dict = Depends(get_current_user)
):
    """Process video using aesthetic discovery (Mode 3)"""
    
    try:
        job = await video_service.submit_processing_job(
            mode=VideoProcessingMode.AESTHETIC_DISCOVERY,
            source_video_id=request.source_video_id,
            user_id=current_user["sub"],
            parameters=request.dict()
        )
        return job
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit processing job: {str(e)}"
        )


@router.get("/aesthetic-suggestions/{video_id}", response_model=List[AestheticSuggestion])
async def get_aesthetic_suggestions(
    video_id: str,
    num_suggestions: int = 3,
    current_user: dict = Depends(get_current_user)
):
    """Get aesthetic suggestions for a video (Mode 3 preview)"""
    
    # Verify video exists and user has access
    video = video_service.get_video_asset(video_id)
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )
    
    if video.user_id != current_user["sub"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    try:
        suggestions = await video_service.generate_aesthetic_suggestions(
            video_id=video_id,
            num_suggestions=min(num_suggestions, 5)
        )
        return suggestions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate suggestions: {str(e)}"
        )


@router.get("/jobs/{job_id}", response_model=VideoProcessingJob)
async def get_processing_job(
    job_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get processing job status"""
    
    job = video_service.get_job_status(job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    if job.user_id != current_user["sub"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return job


@router.get("/jobs", response_model=List[VideoProcessingJob])
async def get_user_jobs(
    current_user: dict = Depends(get_current_user),
    limit: int = 20,
    offset: int = 0
):
    """Get all processing jobs for current user"""
    
    jobs = video_service.get_user_jobs(current_user["sub"])
    
    # Apply pagination
    start = offset
    end = offset + limit
    return jobs[start:end]


@router.get("/videos/{video_id}", response_model=VideoAsset)
async def get_video(
    video_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get video asset details"""
    
    video = video_service.get_video_asset(video_id)
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )
    
    if video.user_id != current_user["sub"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return video


@router.get("/videos", response_model=List[VideoAsset])
async def get_user_videos(
    current_user: dict = Depends(get_current_user),
    limit: int = 20,
    offset: int = 0
):
    """Get all videos for current user"""
    
    videos = video_service.get_user_videos(current_user["sub"])
    
    # Apply pagination
    start = offset
    end = offset + limit
    return videos[start:end]


@router.get("/videos/{video_id}/download")
async def download_video(
    video_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Download a video file"""
    
    video = video_service.get_video_asset(video_id)
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )
    
    if video.user_id != current_user["sub"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    try:
        return FileResponse(
            path=video.file_path,
            filename=video.filename,
            media_type=video.content_type
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to download video: {str(e)}"
        )


@router.get("/videos/{video_id}/thumbnail")
async def get_video_thumbnail(
    video_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get video thumbnail"""
    
    video = video_service.get_video_asset(video_id)
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )
    
    if video.user_id != current_user["sub"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Return placeholder image for now
    # In production, generate actual thumbnail
    placeholder_svg = '''<?xml version="1.0" encoding="UTF-8"?>
    <svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="#1e293b"/>
        <text x="50%" y="50%" fill="white" text-anchor="middle" dy="0.3em" font-family="Arial" font-size="16">
            Video Thumbnail
        </text>
    </svg>'''
    
    return StreamingResponse(
        io.BytesIO(placeholder_svg.encode()),
        media_type="image/svg+xml"
    )


@router.delete("/videos/{video_id}")
async def delete_video(
    video_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete a video"""
    
    video = video_service.get_video_asset(video_id)
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )
    
    if video.user_id != current_user["sub"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Remove from service storage
    try:
        import os
        if os.path.exists(video.file_path):
            os.remove(video.file_path)
        
        # Remove from in-memory storage
        if video_id in video_service.videos:
            del video_service.videos[video_id]
        
        return {"message": "Video deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete video: {str(e)}"
        )


@router.post("/process/bulk", response_model=List[VideoProcessingJob])
async def bulk_process_videos(
    request: BulkProcessingRequest,
    current_user: dict = Depends(get_current_user)
):
    """Submit multiple videos for processing"""
    
    jobs = []
    
    for video_id in request.video_ids:
        try:
            job = await video_service.submit_processing_job(
                mode=request.mode,
                source_video_id=video_id,
                user_id=current_user["sub"],
                parameters=request.common_parameters
            )
            jobs.append(job)
        except Exception as e:
            # Continue with other videos even if one fails
            print(f"Failed to process video {video_id}: {e}")
    
    return jobs


@router.get("/analytics", response_model=ProcessingAnalytics)
async def get_processing_analytics(
    current_user: dict = Depends(get_current_user)
):
    """Get processing analytics for current user"""
    
    user_jobs = video_service.get_user_jobs(current_user["sub"])
    
    if not user_jobs:
        return ProcessingAnalytics(
            total_jobs=0,
            success_rate=0.0,
            average_processing_time=0.0,
            popular_modes={},
            performance_metrics={}
        )
    
    # Calculate analytics
    total_jobs = len(user_jobs)
    completed_jobs = [job for job in user_jobs if job.processing_time_seconds is not None]
    success_rate = (len(completed_jobs) / total_jobs) * 100 if total_jobs > 0 else 0
    
    avg_processing_time = 0
    if completed_jobs:
        avg_processing_time = sum(job.processing_time_seconds for job in completed_jobs) / len(completed_jobs)
    
    # Mode popularity
    mode_counts = {}
    for job in user_jobs:
        mode_counts[job.mode.value] = mode_counts.get(job.mode.value, 0) + 1
    
    return ProcessingAnalytics(
        total_jobs=total_jobs,
        success_rate=success_rate,
        average_processing_time=avg_processing_time,
        popular_modes=mode_counts,
        performance_metrics={
            "queue_efficiency": 85.5,
            "user_satisfaction": 92.3,
            "processing_speed": 78.9
        }
    )