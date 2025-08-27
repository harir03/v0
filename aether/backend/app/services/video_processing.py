"""
Video processing service for Vivid AI platform
"""
import asyncio
import json
import os
import subprocess
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
import hashlib
import tempfile

from app.schemas.video import (
    VideoProcessingMode,
    VideoProcessingStatus,
    VideoProcessingJob,
    VideoAsset,
    VideoMetadata,
    ProcessingProgress,
    ViralPrediction,
    AestheticSuggestion,
    StyleSynthesisRequest,
    AIDirectorRequest,
    AestheticDiscoveryRequest
)
from app.services.content_moderation import content_moderation


class VideoProcessingService:
    """Service for processing videos with AI"""
    
    def __init__(self):
        self.storage_path = Path("/tmp/vivid_ai_videos")
        self.storage_path.mkdir(exist_ok=True)
        
        # In-memory storage for demo (replace with database in production)
        self.jobs: Dict[str, VideoProcessingJob] = {}
        self.videos: Dict[str, VideoAsset] = {}
        self.processing_queue = asyncio.Queue()
        self.workers_started = False
        
        # Style templates for quick generation
        self.style_templates = {
            "cinematic": {
                "color_grading": "dramatic_shadows",
                "motion": "smooth_tracking",
                "effects": ["lens_flare", "depth_of_field"]
            },
            "vintage": {
                "color_grading": "sepia_warm",
                "motion": "film_grain",
                "effects": ["light_leaks", "vignette"]
            },
            "cyberpunk": {
                "color_grading": "neon_blue_purple",
                "motion": "glitch_transitions",
                "effects": ["digital_noise", "chromatic_aberration"]
            },
            "travel_vlog": {
                "color_grading": "vibrant_saturation",
                "motion": "dynamic_cuts",
                "effects": ["time_lapse", "transitions"]
            },
            "aesthetic_dream": {
                "color_grading": "pastel_soft",
                "motion": "slow_motion",
                "effects": ["bokeh", "soft_focus"]
            }
        }
    
    async def start_processing_workers(self):
        """Start background workers for video processing"""
        if not self.workers_started:
            # Start 3 concurrent workers
            for i in range(3):
                asyncio.create_task(self._processing_worker(f"worker-{i}"))
            self.workers_started = True
    
    async def _processing_worker(self, worker_name: str):
        """Background worker for processing video jobs"""
        while True:
            try:
                job_id = await self.processing_queue.get()
                await self._process_video_job(job_id)
                self.processing_queue.task_done()
            except Exception as e:
                print(f"Worker {worker_name} error: {e}")
                await asyncio.sleep(1)
    
    async def upload_video(self, file_data: bytes, filename: str, content_type: str, user_id: str) -> VideoAsset:
        """Upload and store a video file"""
        
        # Check rate limits
        rate_check = await content_moderation.check_rate_limits(user_id, 'video_upload')
        if not rate_check['allowed']:
            raise ValueError(f"Rate limit exceeded: {rate_check['message']}")
        
        video_id = str(uuid.uuid4())
        file_extension = Path(filename).suffix.lower()
        
        # Create secure file path
        file_path = self.storage_path / f"{video_id}{file_extension}"
        
        # Save file temporarily for content analysis
        with open(file_path, "wb") as f:
            f.write(file_data)
        
        # Content moderation - check for inappropriate content
        moderation_result = await content_moderation.moderate_video_content(str(file_path), user_id)
        
        if not moderation_result['approved']:
            # Remove the file and reject upload
            os.remove(file_path)
            violation_details = moderation_result.get('violations', [])
            raise ValueError(f"Content rejected: {violation_details}")
        
        # Deepfake detection
        deepfake_result = await content_moderation.detect_deepfake(str(file_path))
        if deepfake_result['flagged']:
            os.remove(file_path)
            raise ValueError("Potential deepfake content detected")
        
        # Extract video metadata
        metadata = await self._extract_video_metadata(file_path)
        
        # Generate thumbnail
        thumbnail_url = await self._generate_thumbnail(file_path, video_id)
        
        # Apply watermark for traceability
        watermarked_path = self.storage_path / f"{video_id}_watermarked{file_extension}"
        watermark_result = await content_moderation.apply_watermark(str(file_path), str(watermarked_path))
        
        # Use watermarked version if watermarking was successful
        final_path = watermarked_path if watermark_result['watermarked'] else file_path
        if watermark_result['watermarked'] and file_path != watermarked_path:
            # Copy original to watermarked path (in production, actual watermarking would occur)
            import shutil
            shutil.copy2(file_path, watermarked_path)
        
        # Create video asset
        video_asset = VideoAsset(
            id=video_id,
            user_id=user_id,
            filename=filename,
            file_path=str(final_path),
            file_size=len(file_data),
            content_type=content_type,
            metadata=metadata,
            thumbnail_url=thumbnail_url,
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=30)  # 30-day expiration
        )
        
        self.videos[video_id] = video_asset
        return video_asset
    
    async def submit_processing_job(
        self,
        mode: VideoProcessingMode,
        source_video_id: str,
        user_id: str,
        parameters: Dict[str, Any]
    ) -> VideoProcessingJob:
        """Submit a video processing job"""
        
        # Check rate limits
        rate_check = await content_moderation.check_rate_limits(user_id, 'video_process')
        if not rate_check['allowed']:
            raise ValueError(f"Rate limit exceeded: {rate_check['message']}")
        
        job_id = str(uuid.uuid4())
        
        # Validate source video exists
        if source_video_id not in self.videos:
            raise ValueError(f"Source video {source_video_id} not found")
        
        # Content moderation for AI Director prompts
        if mode == VideoProcessingMode.AI_DIRECTOR:
            creative_prompt = parameters.get('creative_prompt', '')
            if creative_prompt:
                moderation_result = await content_moderation.moderate_text_content(creative_prompt, user_id)
                if not moderation_result['approved']:
                    violation_details = moderation_result.get('violations', [])
                    raise ValueError(f"Prompt rejected: {violation_details}")
        
        # Create processing job
        job = VideoProcessingJob(
            id=job_id,
            user_id=user_id,
            mode=mode,
            status=VideoProcessingStatus.PENDING,
            source_video_id=source_video_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        self.jobs[job_id] = job
        
        # Start workers if needed
        await self.start_processing_workers()
        
        # Add to processing queue
        await self.processing_queue.put(job_id)
        
        return job
    
    async def _process_video_job(self, job_id: str):
        """Process a video job based on its mode"""
        job = self.jobs.get(job_id)
        if not job:
            return
        
        try:
            # Update status to processing
            job.status = VideoProcessingStatus.PROCESSING
            job.updated_at = datetime.utcnow()
            
            # Update progress
            await self._update_progress(job_id, "Starting processing", 0)
            
            # Process based on mode
            if job.mode == VideoProcessingMode.STYLE_SYNTHESIS:
                output_video_id = await self._process_style_synthesis(job)
            elif job.mode == VideoProcessingMode.AI_DIRECTOR:
                output_video_id = await self._process_ai_director(job)
            elif job.mode == VideoProcessingMode.AESTHETIC_DISCOVERY:
                output_video_id = await self._process_aesthetic_discovery(job)
            else:
                raise ValueError(f"Unknown processing mode: {job.mode}")
            
            # Generate viral prediction
            viral_prediction = await self._generate_viral_prediction(output_video_id)
            
            # Update job as completed
            job.status = VideoProcessingStatus.COMPLETED
            job.output_video_id = output_video_id
            job.viral_prediction = viral_prediction
            job.completed_at = datetime.utcnow()
            job.processing_time_seconds = (job.completed_at - job.created_at).total_seconds()
            job.updated_at = datetime.utcnow()
            
            await self._update_progress(job_id, "Processing complete", 100)
            
        except Exception as e:
            # Update job as failed
            job.status = VideoProcessingStatus.FAILED
            job.error_message = str(e)
            job.updated_at = datetime.utcnow()
            print(f"Job {job_id} failed: {e}")
    
    async def _process_style_synthesis(self, job: VideoProcessingJob) -> str:
        """Process style synthesis (Mode 1)"""
        await self._update_progress(job.id, "Analyzing source video", 10)
        await asyncio.sleep(2)  # Simulate processing
        
        await self._update_progress(job.id, "Analyzing style reference", 25)
        await asyncio.sleep(2)
        
        await self._update_progress(job.id, "Applying style transfer", 50)
        await asyncio.sleep(3)
        
        await self._update_progress(job.id, "Optimizing temporal consistency", 75)
        await asyncio.sleep(2)
        
        await self._update_progress(job.id, "Finalizing output", 90)
        
        # Create output video (simulated)
        output_video = await self._create_processed_video(job, "style_synthesis")
        return output_video.id
    
    async def _process_ai_director(self, job: VideoProcessingJob) -> str:
        """Process AI Creative Director (Mode 2)"""
        await self._update_progress(job.id, "Understanding creative prompt", 10)
        await asyncio.sleep(1)
        
        await self._update_progress(job.id, "Analyzing video content", 25)
        await asyncio.sleep(2)
        
        await self._update_progress(job.id, "Generating effects plan", 40)
        await asyncio.sleep(2)
        
        await self._update_progress(job.id, "Applying AI-generated effects", 70)
        await asyncio.sleep(4)  # AI processing takes longer
        
        await self._update_progress(job.id, "Audio synchronization", 85)
        await asyncio.sleep(1)
        
        await self._update_progress(job.id, "Finalizing masterpiece", 95)
        await asyncio.sleep(1)
        
        # Create output video (simulated)
        output_video = await self._create_processed_video(job, "ai_director")
        return output_video.id
    
    async def _process_aesthetic_discovery(self, job: VideoProcessingJob) -> str:
        """Process aesthetic discovery (Mode 3)"""
        await self._update_progress(job.id, "Analyzing video aesthetics", 15)
        await asyncio.sleep(2)
        
        await self._update_progress(job.id, "Exploring style latent space", 35)
        await asyncio.sleep(3)
        
        await self._update_progress(job.id, "Generating novel combinations", 60)
        await asyncio.sleep(3)
        
        await self._update_progress(job.id, "Ranking aesthetic suggestions", 80)
        await asyncio.sleep(2)
        
        await self._update_progress(job.id, "Creating preview variants", 95)
        await asyncio.sleep(1)
        
        # Create output video (simulated)
        output_video = await self._create_processed_video(job, "aesthetic_discovery")
        return output_video.id
    
    async def _create_processed_video(self, job: VideoProcessingJob, suffix: str) -> VideoAsset:
        """Create a processed video asset (simulated)"""
        source_video = self.videos[job.source_video_id]
        output_id = str(uuid.uuid4())
        
        # In a real implementation, this would save the actual processed video
        # For now, we'll copy the source file with a new ID
        source_path = Path(source_video.file_path)
        output_path = self.storage_path / f"{output_id}_{suffix}{source_path.suffix}"
        
        # Copy source file as placeholder
        import shutil
        shutil.copy2(source_path, output_path)
        
        # Create output video asset
        output_video = VideoAsset(
            id=output_id,
            user_id=job.user_id,
            filename=f"processed_{suffix}_{source_video.filename}",
            file_path=str(output_path),
            file_size=source_video.file_size,
            content_type=source_video.content_type,
            metadata=source_video.metadata,
            thumbnail_url=await self._generate_thumbnail(output_path, output_id),
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=30)
        )
        
        self.videos[output_id] = output_video
        return output_video
    
    async def _extract_video_metadata(self, file_path: Path) -> VideoMetadata:
        """Extract video metadata using ffprobe (simulated)"""
        # In production, use ffprobe or similar tool
        return VideoMetadata(
            duration=30.5,  # Simulated values
            resolution={"width": 1920, "height": 1080},
            fps=30.0,
            codec="h264",
            bitrate=5000,
            has_audio=True,
            audio_codec="aac"
        )
    
    async def _generate_thumbnail(self, file_path: Path, video_id: str) -> str:
        """Generate video thumbnail (simulated)"""
        # In production, use ffmpeg to extract frame
        return f"/api/v1/videos/{video_id}/thumbnail"
    
    async def _update_progress(self, job_id: str, step: str, progress: float):
        """Update job progress"""
        job = self.jobs.get(job_id)
        if job:
            job.progress = ProcessingProgress(
                step=step,
                progress=progress,
                eta_seconds=max(0, (100 - progress) * 2),  # Rough ETA
                message=f"Processing: {step}"
            )
            job.updated_at = datetime.utcnow()
    
    async def _generate_viral_prediction(self, video_id: str) -> ViralPrediction:
        """Generate viral potential prediction (AI-powered)"""
        # Simulated viral prediction based on video analysis
        import random
        
        base_score = random.uniform(65, 95)
        
        factors = {
            "visual_appeal": random.uniform(0.7, 0.95),
            "trend_alignment": random.uniform(0.6, 0.9),
            "engagement_potential": random.uniform(0.65, 0.9),
            "uniqueness": random.uniform(0.5, 0.85),
            "audio_quality": random.uniform(0.7, 0.95),
            "pacing": random.uniform(0.6, 0.9)
        }
        
        suggestions = [
            "Consider adding captions for better accessibility",
            "The opening 3 seconds could be more engaging",
            "Color saturation could be increased by 15% for social media",
            "Adding trending audio could boost viral potential",
            "Consider creating a shorter version for TikTok/Reels"
        ]
        
        return ViralPrediction(
            score=base_score,
            factors=factors,
            suggestions=random.sample(suggestions, 3),
            confidence=random.uniform(0.8, 0.95)
        )
    
    async def generate_aesthetic_suggestions(self, video_id: str, num_suggestions: int = 3) -> List[AestheticSuggestion]:
        """Generate aesthetic suggestions for discovery mode"""
        suggestions = []
        
        style_options = [
            ("Dreamy Nostalgic", "Soft vintage film aesthetic with warm light leaks"),
            ("Cyberpunk Neon", "Futuristic neon-soaked digital landscape"),
            ("Golden Hour Magic", "Warm cinematic glow with dramatic shadows"),
            ("Retro Synthwave", "80s-inspired purple and pink aesthetic"),
            ("Minimalist Clean", "Modern clean lines with subtle color grading"),
            ("Film Noir Classic", "High contrast black and white with dramatic lighting"),
            ("Tropical Vibrant", "Saturated colors with beach/vacation vibes"),
            ("Arctic Blue", "Cool blue tones with crisp, clean aesthetics")
        ]
        
        import random
        selected_styles = random.sample(style_options, min(num_suggestions, len(style_options)))
        
        for i, (title, description) in enumerate(selected_styles):
            suggestion = AestheticSuggestion(
                id=f"aesthetic_{uuid.uuid4().hex[:8]}",
                title=title,
                description=description,
                style_tags=[tag.lower() for tag in title.split()],
                preview_thumbnail=f"/api/v1/aesthetic/preview/{uuid.uuid4().hex[:8]}",
                novelty_score=random.uniform(0.6, 0.95),
                estimated_processing_time=random.randint(45, 180)
            )
            suggestions.append(suggestion)
        
        return suggestions
    
    def get_job_status(self, job_id: str) -> Optional[VideoProcessingJob]:
        """Get processing job status"""
        return self.jobs.get(job_id)
    
    def get_video_asset(self, video_id: str) -> Optional[VideoAsset]:
        """Get video asset by ID"""
        return self.videos.get(video_id)
    
    def get_user_videos(self, user_id: str) -> List[VideoAsset]:
        """Get all videos for a user"""
        return [video for video in self.videos.values() if video.user_id == user_id]
    
    def get_user_jobs(self, user_id: str) -> List[VideoProcessingJob]:
        """Get all processing jobs for a user"""
        return [job for job in self.jobs.values() if job.user_id == user_id]


# Global service instance
video_service = VideoProcessingService()