"""
Video processing schemas for Vivid AI platform
"""
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, validator


class VideoProcessingMode(str, Enum):
    """Video processing modes"""
    STYLE_SYNTHESIS = "style_synthesis"  # Mode 1: Video-to-video style transfer
    AI_DIRECTOR = "ai_director"          # Mode 2: Text-to-video effects
    AESTHETIC_DISCOVERY = "aesthetic_discovery"  # Mode 3: AI brainstorming


class VideoProcessingStatus(str, Enum):
    """Video processing status"""
    PENDING = "pending"
    UPLOADING = "uploading"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class VideoUploadRequest(BaseModel):
    """Request schema for video upload"""
    filename: str = Field(..., description="Original filename")
    content_type: str = Field(..., description="MIME type of the video")
    file_size: int = Field(..., description="File size in bytes", gt=0, le=500_000_000)  # 500MB max
    
    @validator('content_type')
    def validate_content_type(cls, v):
        allowed_types = ['video/mp4', 'video/avi', 'video/mov', 'video/mkv', 'video/webm']
        if v not in allowed_types:
            raise ValueError(f'Content type must be one of: {allowed_types}')
        return v


class StyleSynthesisRequest(BaseModel):
    """Request schema for style synthesis (Mode 1)"""
    source_video_id: str = Field(..., description="ID of the source video to edit")
    style_video_id: str = Field(..., description="ID of the style reference video")
    intensity: float = Field(0.8, description="Style transfer intensity", ge=0.0, le=1.0)
    preserve_motion: bool = Field(True, description="Whether to preserve original motion")
    output_quality: str = Field("high", description="Output quality", pattern="^(low|medium|high|ultra)$")


class AIDirectorRequest(BaseModel):
    """Request schema for AI Creative Director (Mode 2)"""
    source_video_id: str = Field(..., description="ID of the source video to edit")
    creative_prompt: str = Field(..., description="Text prompt describing desired aesthetic", min_length=10, max_length=500)
    style_strength: float = Field(0.7, description="How strongly to apply the style", ge=0.0, le=1.0)
    sync_to_audio: bool = Field(False, description="Whether to sync effects to audio beats")
    duration_adjustment: bool = Field(False, description="Allow duration changes for better pacing")
    output_quality: str = Field("high", description="Output quality", pattern="^(low|medium|high|ultra)$")


class AestheticDiscoveryRequest(BaseModel):
    """Request schema for aesthetic discovery (Mode 3)"""
    source_video_id: str = Field(..., description="ID of the source video to edit")
    surprise_level: float = Field(0.5, description="How unexpected the suggestions should be", ge=0.0, le=1.0)
    content_type: str = Field("auto", description="Content type hint", pattern="^(auto|travel|portrait|action|landscape|event)$")
    num_suggestions: int = Field(3, description="Number of aesthetic suggestions to generate", ge=1, le=5)


class VideoProcessingRequest(BaseModel):
    """Base request schema for video processing"""
    mode: VideoProcessingMode = Field(..., description="Processing mode")
    user_id: str = Field(..., description="User ID")
    
    # Mode-specific parameters (optional, validated based on mode)
    style_synthesis: Optional[StyleSynthesisRequest] = None
    ai_director: Optional[AIDirectorRequest] = None
    aesthetic_discovery: Optional[AestheticDiscoveryRequest] = None
    
    @validator('style_synthesis', 'ai_director', 'aesthetic_discovery', pre=True)
    def validate_mode_parameters(cls, v, values):
        mode = values.get('mode')
        if mode == VideoProcessingMode.STYLE_SYNTHESIS and not values.get('style_synthesis'):
            raise ValueError('style_synthesis parameters required for STYLE_SYNTHESIS mode')
        elif mode == VideoProcessingMode.AI_DIRECTOR and not values.get('ai_director'):
            raise ValueError('ai_director parameters required for AI_DIRECTOR mode')
        elif mode == VideoProcessingMode.AESTHETIC_DISCOVERY and not values.get('aesthetic_discovery'):
            raise ValueError('aesthetic_discovery parameters required for AESTHETIC_DISCOVERY mode')
        return v


class VideoMetadata(BaseModel):
    """Video metadata schema"""
    duration: float = Field(..., description="Video duration in seconds")
    resolution: Dict[str, int] = Field(..., description="Video resolution (width, height)")
    fps: float = Field(..., description="Frames per second")
    codec: str = Field(..., description="Video codec")
    bitrate: Optional[int] = Field(None, description="Video bitrate in kbps")
    has_audio: bool = Field(False, description="Whether video has audio track")
    audio_codec: Optional[str] = Field(None, description="Audio codec if present")


class ProcessingProgress(BaseModel):
    """Processing progress schema"""
    step: str = Field(..., description="Current processing step")
    progress: float = Field(..., description="Progress percentage", ge=0.0, le=100.0)
    eta_seconds: Optional[float] = Field(None, description="Estimated time to completion")
    message: Optional[str] = Field(None, description="Progress message")


class ViralPrediction(BaseModel):
    """Viral performance prediction schema"""
    score: float = Field(..., description="Viral potential score", ge=0.0, le=100.0)
    factors: Dict[str, float] = Field(..., description="Contributing factors to viral score")
    suggestions: List[str] = Field(..., description="Optimization suggestions")
    confidence: float = Field(..., description="Prediction confidence", ge=0.0, le=1.0)


class VideoProcessingJob(BaseModel):
    """Video processing job response schema"""
    id: str = Field(..., description="Job ID")
    user_id: str = Field(..., description="User ID")
    mode: VideoProcessingMode = Field(..., description="Processing mode")
    status: VideoProcessingStatus = Field(..., description="Current status")
    source_video_id: str = Field(..., description="Source video ID")
    output_video_id: Optional[str] = Field(None, description="Output video ID if completed")
    progress: Optional[ProcessingProgress] = Field(None, description="Current progress")
    viral_prediction: Optional[ViralPrediction] = Field(None, description="Viral potential prediction")
    created_at: datetime = Field(..., description="Job creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    completed_at: Optional[datetime] = Field(None, description="Job completion timestamp")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    processing_time_seconds: Optional[float] = Field(None, description="Total processing time")


class VideoAsset(BaseModel):
    """Video asset schema"""
    id: str = Field(..., description="Video asset ID")
    user_id: str = Field(..., description="Owner user ID")
    filename: str = Field(..., description="Original filename")
    file_path: str = Field(..., description="Storage file path")
    file_size: int = Field(..., description="File size in bytes")
    content_type: str = Field(..., description="MIME type")
    metadata: VideoMetadata = Field(..., description="Video metadata")
    thumbnail_url: Optional[str] = Field(None, description="Thumbnail URL")
    preview_url: Optional[str] = Field(None, description="Preview video URL")
    is_public: bool = Field(False, description="Whether video is publicly accessible")
    created_at: datetime = Field(..., description="Upload timestamp")
    expires_at: Optional[datetime] = Field(None, description="Expiration timestamp")


class AestheticSuggestion(BaseModel):
    """Aesthetic suggestion schema for discovery mode"""
    id: str = Field(..., description="Suggestion ID")
    title: str = Field(..., description="Suggestion title")
    description: str = Field(..., description="Detailed description")
    style_tags: List[str] = Field(..., description="Style tags")
    preview_thumbnail: str = Field(..., description="Preview thumbnail URL")
    novelty_score: float = Field(..., description="How novel/unique this style is", ge=0.0, le=1.0)
    estimated_processing_time: int = Field(..., description="Estimated processing time in seconds")


class BulkProcessingRequest(BaseModel):
    """Request schema for bulk video processing"""
    video_ids: List[str] = Field(..., description="List of video IDs to process", min_items=1, max_items=10)
    mode: VideoProcessingMode = Field(..., description="Processing mode for all videos")
    common_parameters: Dict[str, Any] = Field(..., description="Parameters to apply to all videos")
    priority: str = Field("normal", description="Processing priority", pattern="^(low|normal|high|urgent)$")


class ProcessingAnalytics(BaseModel):
    """Processing analytics schema"""
    total_jobs: int = Field(..., description="Total number of jobs processed")
    success_rate: float = Field(..., description="Success rate percentage", ge=0.0, le=100.0)
    average_processing_time: float = Field(..., description="Average processing time in seconds")
    popular_modes: Dict[str, int] = Field(..., description="Usage count by processing mode")
    performance_metrics: Dict[str, float] = Field(..., description="Various performance metrics")