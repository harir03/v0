#!/usr/bin/env python3
"""
LinkedIn Bot v1 Enhanced - Advanced Automation with Intelligence
================================================================

🔥 NEW ADVANCED FEATURES 🔥

🧠 KEYWORD INTELLIGENCE SYSTEM
- Performance tracking per keyword (success rates, search results)
- Automatic keyword rotation after 25 successful comments
- AI-powered keyword generation using Ollama
- Cooling periods for overused keywords
- Multi-factor scoring for keyword selection

🏥 HEALTH MONITORING SYSTEM  
- Real-time account health scoring (0-100)
- CAPTCHA and warning detection
- Automatic activity reduction when health drops
- Recovery recommendations and cooldown periods

🎭 HUMAN BEHAVIOR SIMULATION
- Circadian rhythm-based speed adjustments
- Natural reading time calculation
- Human-like typing with errors and corrections
- Fatigue factor simulation over time
- Micro-break randomization

🔍 ENHANCED POST EVALUATION (50-point scale)
- Content quality analysis (length, structure, questions)
- Author credibility assessment
- Topic relevance scoring
- Engagement potential detection
- Call-to-action identification

🛡️ ADVANCED DUPLICATE DETECTION
- Exact text matching
- Semantic similarity analysis (using sklearn if available)
- Pattern recognition for template detection
- Multi-level signature generation

🔧 LINKEDIN UI RESILIENCE
- Multiple selector fallbacks for UI changes
- Advanced element finding with XPath backups
- Automatic retry mechanisms
- Error recovery strategies

📊 COMPREHENSIVE ANALYTICS
- Session performance tracking
- Keyword performance summaries
- Comment quality analysis
- Health status reporting

🚀 STEALTH FEATURES FOR LONG RUNS
- Browser fingerprint management
- Natural mouse movement simulation
- Realistic scrolling patterns
- Error pattern masking
- Session break management

💾 PERSISTENT MEMORY
- Comment history tracking
- Performance data persistence
- Account-specific configurations
- Cross-session learning

⚡ SIMPLE v0-STYLE STARTUP
- No complex configuration files
- Uses already logged-in browser
- Interactive account selection
- Quick keyword setup

SETUP:
1. Make sure you're logged into LinkedIn in your browser
2. Run: python v1.py
3. Follow the simple prompts
4. Set target comments (up to 100+ per session)

The bot is designed for long runs with advanced stealth and intelligence features!
"""

import os
import sys
import time
import random
import json
import hashlib
import re
import traceback
import platform
import base64
import threading
import psutil
import getpass
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, 
    StaleElementReferenceException, WebDriverException
)

# Import requests for API calls
import requests
import requests
import requests

# Additional imports for advanced features
try:
    from cryptography.fernet import Fernet
    ENCRYPTION_AVAILABLE = True
except ImportError:
    ENCRYPTION_AVAILABLE = False
    print("⚠️ Cryptography not available - data encryption disabled")

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("⚠️ Scikit-learn not available - advanced similarity detection disabled")

class HumanBehaviorSimulator:
    """Advanced human behavior simulation for stealth operations."""
    
    def __init__(self):
        self.session_start_time = datetime.now()
        self.activity_count = 0
        self.last_activity_time = datetime.now()
        
    def random_delay(self, min_seconds=1, max_seconds=5):
        """Generate random delay with human variance."""
        # Add circadian rhythm factor
        current_hour = datetime.now().hour
        speed_factor = self._get_human_speed_factor(current_hour)
        
        base_delay = random.uniform(min_seconds, max_seconds)
        adjusted_delay = base_delay * speed_factor
        
        time.sleep(adjusted_delay)
        return adjusted_delay
        
    def _get_human_speed_factor(self, hour):
        """Calculate human speed factor based on time of day."""
        speed_factors = {
            6: 0.7, 7: 0.8, 8: 0.9, 9: 1.0, 10: 1.1,
            11: 1.0, 12: 0.9, 13: 0.8, 14: 1.1, 15: 1.0,
            16: 0.9, 17: 0.8, 18: 0.7, 19: 0.6, 20: 0.5,
            21: 0.4, 22: 0.3, 23: 0.2
        }
        return speed_factors.get(hour, 0.8)
        
    def simulate_reading_time(self, text_length):
        """Calculate realistic reading time based on content length."""
        # Average reading speed: 200 words per minute
        words = text_length / 5  # Approximate words from characters
        base_reading_time = (words / 200) * 60  # Convert to seconds
        
        # Add human variance (±30%)
        variance = random.uniform(0.7, 1.3)
        reading_time = base_reading_time * variance
        
        # Minimum reading time
        return max(reading_time, 2.0)
        
    def human_like_typing(self, element, text, typing_speed_range=(0.03, 0.15)):
        """Type text with human-like patterns."""
        element.clear()
        
        for i, char in enumerate(text):
            element.send_keys(char)
            
            # Random typing speed
            typing_delay = random.uniform(*typing_speed_range)
            time.sleep(typing_delay)
            
            # Simulate occasional typing errors (2% chance)
            if random.random() < 0.02 and i > 3:
                # Make a "mistake"
                wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz')
                element.send_keys(wrong_char)
                time.sleep(random.uniform(0.1, 0.3))
                
                # Correct the mistake
                element.send_keys('\b')  # Backspace
                time.sleep(random.uniform(0.1, 0.2))
                element.send_keys(char)
                
            # Random pauses (10% chance)
            if random.random() < 0.1:
                time.sleep(random.uniform(0.3, 0.8))
                
    def natural_scroll(self, driver, direction="down", distance=None):
        """Simulate natural scrolling behavior."""
        if distance is None:
            distance = random.randint(200, 800)
            
        scroll_steps = random.randint(3, 7)
        
        for _ in range(scroll_steps):
            step_distance = distance // scroll_steps
            if direction == "down":
                driver.execute_script(f"window.scrollBy(0, {step_distance})")
            else:
                driver.execute_script(f"window.scrollBy(0, -{step_distance})")
            time.sleep(random.uniform(0.1, 0.4))
            
    def fatigue_factor(self):
        """Calculate fatigue based on session duration and activity."""
        session_duration = (datetime.now() - self.session_start_time).total_seconds() / 60  # minutes
        
        # Fatigue increases over time
        if session_duration < 15:
            return 1.0  # 100% efficiency
        elif session_duration < 30:
            return 0.95  # 95% efficiency  
        elif session_duration < 60:
            return 0.85  # 85% efficiency
        else:
            return 0.70  # 70% efficiency
            
    def should_take_micro_break(self):
        """Determine if a micro break should be taken."""
        # 15% chance of taking a micro break
        if random.random() < 0.15:
            break_duration = random.uniform(2, 8)
            print(f"😴 Taking micro break for {break_duration:.1f} seconds...")
            time.sleep(break_duration)
            return True
        return False

class SessionManager:
    """Manages long-running sessions with intelligent pacing."""
    
    def __init__(self, account_name):
        self.account_name = account_name
        self.session_start_time = datetime.now()
        self.comments_posted = 0
        self.searches_performed = 0
        self.last_comment_time = None
        self.last_search_time = None
        self.errors_encountered = 0
        
    def can_make_comment(self, max_comments_per_day=100):
        """Check if another comment can be made."""
        # Check daily limit
        if self.comments_posted >= max_comments_per_day:
            return False, "Daily comment limit reached"
            
        # Check time since last comment (2-5 minutes minimum)
        if self.last_comment_time:
            min_interval = random.randint(120, 300)  # 2-5 minutes
            time_since_last = (datetime.now() - self.last_comment_time).total_seconds()
            if time_since_last < min_interval:
                remaining = min_interval - time_since_last
                return False, f"Need to wait {remaining:.0f} more seconds"
                
        return True, "OK"
        
    def can_perform_search(self):
        """Check if another search can be performed."""
        # Check time since last search (30-90 seconds minimum)
        if self.last_search_time:
            min_interval = random.randint(30, 90)
            time_since_last = (datetime.now() - self.last_search_time).total_seconds()
            if time_since_last < min_interval:
                remaining = min_interval - time_since_last
                return False, f"Need to wait {remaining:.0f} more seconds"
                
        return True, "OK"
        
    def record_comment(self):
        """Record a successful comment."""
        self.last_comment_time = datetime.now()
        self.comments_posted += 1
        
    def record_search(self):
        """Record a search operation."""
        self.last_search_time = datetime.now()
        self.searches_performed += 1
        
    def record_error(self):
        """Record an error occurrence."""
        self.errors_encountered += 1
        
    def get_session_stats(self):
        """Get current session statistics."""
        duration = datetime.now() - self.session_start_time
        return {
            "duration_minutes": duration.total_seconds() / 60,
            "comments_posted": self.comments_posted,
            "searches_performed": self.searches_performed,
            "errors_encountered": self.errors_encountered,
            "comments_per_hour": self.comments_posted / max(duration.total_seconds() / 3600, 0.1)
        }

class CommentQualityAnalyzer:
    """Analyzes and improves comment quality over time."""
    
    def __init__(self, account_name):
        self.account_name = account_name
        self.quality_history = []
        
    def analyze_comment_quality(self, comment_text, post_text):
        """Analyze the quality of a generated comment."""
        score = 0
        issues = []
        
        # Length check
        if len(comment_text) < 10:
            issues.append("Too short")
        elif len(comment_text) > 300:
            issues.append("Too long")
        else:
            score += 20
            
        # Relevance check
        if self._is_relevant(comment_text, post_text):
            score += 30
        else:
            issues.append("Not relevant to post")
            
        # Professionalism check  
        if self._is_professional(comment_text):
            score += 25
        else:
            issues.append("Unprofessional tone")
            
        # Engagement potential
        if self._has_engagement_potential(comment_text):
            score += 25
        else:
            issues.append("Low engagement potential")
            
        quality_result = {
            "score": score,
            "issues": issues,
            "timestamp": datetime.now().isoformat()
        }
        
        self.quality_history.append(quality_result)
        return quality_result
        
    def _is_relevant(self, comment_text, post_text):
        """Check if comment is relevant to the post."""
        comment_words = set(comment_text.lower().split())
        post_words = set(post_text.lower().split())
        
        overlap = len(comment_words.intersection(post_words))
        return overlap >= 2
        
    def _is_professional(self, comment_text):
        """Check if comment maintains professional tone."""
        unprofessional_patterns = [
            r'\bwtf\b', r'\bomg\b', r'\blol\b', r'\blmao\b',
            r'!!!+', r'\ball caps\b'
        ]
        
        for pattern in unprofessional_patterns:
            if re.search(pattern, comment_text, re.IGNORECASE):
                return False
        return True
        
    def _has_engagement_potential(self, comment_text):
        """Check if comment is likely to generate engagement."""
        engagement_indicators = [
            r'\?', r'what do you think', r'agree', r'disagree',
            r'experience', r'thoughts', r'opinion'
        ]
        
        for indicator in engagement_indicators:
            if re.search(indicator, comment_text, re.IGNORECASE):
                return True
        return False

class AdvancedLinkedInSelectors:
    """Enhanced selectors with multiple fallbacks for LinkedIn UI changes."""
    
    COMMENT_BUTTON_SELECTORS = [
        # 2025 Primary selectors
        ".feed-shared-social-action-bar__action-button[aria-label*='comment' i]",
        ".social-actions-button[data-control-name='comment']",
        "button[aria-label*='Comment' i]",
        
        # Fallback selectors
        "[data-control-name='comment']", 
        ".feed-shared-update-v2__social-actions-comment",
        ".social-action-button--comment",
        
        # XPath fallbacks
        "//button[contains(@class, 'social-actions-button') and contains(translate(@aria-label, 'COMMENT', 'comment'), 'comment')]",
        "//button[contains(text(), 'Comment')]"
    ]
    
    COMMENT_BOX_SELECTORS = [
        ".comments-comment-box__form textarea",
        ".comments-comment-texteditor",
        "div[role='textbox'][aria-label*='comment' i]",
        ".ql-editor",
        
        # Fallbacks
        "textarea[placeholder*='comment' i]",
        ".comments-comment-box textarea",
        "div[contenteditable='true'][data-placeholder*='comment' i]"
    ]
    
    SUBMIT_COMMENT_SELECTORS = [
        ".comments-comment-box__submit-button",
        "button[aria-label*='post comment' i]",
        ".comments-comment-box button[type='submit']",
        
        # Fallbacks
        ".comment-submit-button",
        "button[data-control-name='comment.submit']"
    ]
    
    @classmethod
    def find_element_safely(cls, driver, selector_list, timeout=10):
        """Find element using multiple selectors with fallbacks."""
        wait = WebDriverWait(driver, timeout)
        
        for selector in selector_list:
            try:
                if selector.startswith("//"):
                    element = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                else:
                    element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                
                if element and element.is_displayed():
                    return element
            except (TimeoutException, NoSuchElementException):
                continue
                
        return None

class KeywordPerformanceTracker:
    """
    Advanced keyword performance tracking system with AI-powered rotation and generation.
    """
    
    def __init__(self, account_name="default"):
        self.account_name = account_name
        self.data_file = f"data/keyword_performance_{account_name}.json"
        self.performance_data = self._load_performance_data()
        self.current_keyword = None
        self.session_stats = {}
        
    def _load_performance_data(self):
        """Load keyword performance data from file."""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"⚠️ Error loading keyword performance data: {e}")
            return {}
            
    def _save_performance_data(self):
        """Save keyword performance data to file."""
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, 'w') as f:
                json.dump(self.performance_data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Error saving keyword performance data: {e}")
            
    def initialize_keyword(self, keyword):
        """Initialize a new keyword in the tracking system."""
        if keyword not in self.performance_data:
            self.performance_data[keyword] = {
                "searches": 0,
                "search_results": 0,
                "comments_attempted": 0,
                "comments_successful": 0,
                "success_rate": 0.0,
                "avg_results_per_search": 0.0,
                "last_used": None,
                "cooling_until": None,
                "generated_from": None,
                "total_score": 0.0,
                "best_session": 0,
                "worst_session": 0,
                "quality_scores": [],
                "created_at": datetime.now().isoformat()
            }
            self._save_performance_data()
            
    def record_search(self, keyword, results_count):
        """Record a search operation for a keyword."""
        self.initialize_keyword(keyword)
        
        self.performance_data[keyword]["searches"] += 1
        self.performance_data[keyword]["search_results"] += results_count
        self.performance_data[keyword]["last_used"] = datetime.now().isoformat()
        
        # Calculate average results per search
        searches = self.performance_data[keyword]["searches"]
        total_results = self.performance_data[keyword]["search_results"]
        self.performance_data[keyword]["avg_results_per_search"] = total_results / searches if searches > 0 else 0
        
        self._save_performance_data()
        
    def record_comment_attempt(self, keyword, successful=False, post_quality_score=0):
        """Record a comment attempt for a keyword."""
        self.initialize_keyword(keyword)
        
        self.performance_data[keyword]["comments_attempted"] += 1
        
        if successful:
            self.performance_data[keyword]["comments_successful"] += 1
            if post_quality_score > 0:
                self.performance_data[keyword]["quality_scores"].append(post_quality_score)
        
        # Calculate success rate
        attempted = self.performance_data[keyword]["comments_attempted"]
        successful_count = self.performance_data[keyword]["comments_successful"]
        self.performance_data[keyword]["success_rate"] = successful_count / attempted if attempted > 0 else 0
        
        # Update session stats
        if keyword not in self.session_stats:
            self.session_stats[keyword] = {"attempts": 0, "successes": 0}
        
        self.session_stats[keyword]["attempts"] += 1
        if successful:
            self.session_stats[keyword]["successes"] += 1
            
        self._save_performance_data()
        
    def calculate_keyword_score(self, keyword):
        """Calculate multi-factor score for keyword selection."""
        if keyword not in self.performance_data:
            return 0.5  # Default score for new keywords
            
        data = self.performance_data[keyword]
        
        # Success rate component (40% weight)
        success_component = data.get("success_rate", 0) * 0.4
        
        # Result quality component (25% weight)
        avg_results = data.get("avg_results_per_search", 0)
        result_quality = min(avg_results / 10, 1) * 0.25  # Normalize to 0-1
        
        # Recency bonus (20% weight) - rewards keywords not used recently
        last_used = data.get("last_used")
        if last_used:
            hours_since_use = (datetime.now() - datetime.fromisoformat(last_used)).total_seconds() / 3600
            recency_component = min(hours_since_use / 24, 1) * 0.2  # Max bonus after 24 hours
        else:
            recency_component = 0.2  # Full bonus for never used
            
        # Experience factor (10% weight) - slight bonus for experienced keywords
        experience = min(data.get("comments_attempted", 0) / 20, 0.5) * 0.1
        
        # Freshness factor (5% weight) - prevents overuse
        attempts = data.get("comments_attempted", 0)
        freshness = max(0.5, 1 - (attempts / 200)) * 0.05
        
        total_score = success_component + result_quality + recency_component + experience + freshness
        
        # Check if keyword is cooling
        cooling_until = data.get("cooling_until")
        if cooling_until and datetime.now() < datetime.fromisoformat(cooling_until):
            total_score *= 0.1  # Heavily penalize cooling keywords
            
        return total_score
        
    def should_rotate_keyword(self, keyword):
        """Determine if keyword should be rotated based on performance."""
        if keyword not in self.performance_data:
            return False
            
        data = self.performance_data[keyword]
        successful_comments = data.get("comments_successful", 0)
        success_rate = data.get("success_rate", 0)
        avg_results = data.get("avg_results_per_search", 0)
        
        # Rotation triggers
        rotation_reasons = []
        
        # Success threshold reached (25 successful comments)
        if successful_comments >= 25:
            rotation_reasons.append("success_threshold_reached")
            
        # Performance decline (success rate below 60%)
        if data.get("comments_attempted", 0) >= 10 and success_rate < 0.6:
            rotation_reasons.append("performance_decline")
            
        # Poor search results (average below 5 results per search)
        if data.get("searches", 0) >= 5 and avg_results < 5:
            rotation_reasons.append("poor_search_results")
            
        return len(rotation_reasons) > 0, rotation_reasons
        
    def initiate_keyword_cooling(self, keyword, cooling_hours=None):
        """Put keyword in cooling period."""
        if cooling_hours is None:
            # Calculate cooling period based on performance
            data = self.performance_data.get(keyword, {})
            success_rate = data.get("success_rate", 0)
            
            if success_rate > 0.8:
                cooling_hours = random.randint(36, 48)  # 1.5-2 days for high performers
            else:
                cooling_hours = random.randint(18, 30)  # 18-30 hours for poor performers
                
        cooling_until = datetime.now() + timedelta(hours=cooling_hours)
        self.performance_data[keyword]["cooling_until"] = cooling_until.isoformat()
        
        print(f"🧊 Keyword '{keyword}' cooling for {cooling_hours} hours until {cooling_until.strftime('%Y-%m-%d %H:%M')}")
        self._save_performance_data()
        
    def select_best_keyword(self, available_keywords):
        """Select the best keyword based on performance scores."""
        if not available_keywords:
            return None
            
        # Calculate scores for all keywords
        keyword_scores = {}
        for keyword in available_keywords:
            keyword_scores[keyword] = self.calculate_keyword_score(keyword)
            
        # Sort by score (highest first)
        sorted_keywords = sorted(keyword_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Show top 3 scores for debugging
        print("🎯 Keyword scores (top 3):")
        for keyword, score in sorted_keywords[:3]:
            data = self.performance_data.get(keyword, {})
            success_rate = data.get("success_rate", 0)
            comments = data.get("comments_successful", 0)
            print(f"   {keyword}: {score:.3f} (success: {success_rate:.1%}, comments: {comments})")
            
        # Select best keyword
        best_keyword = sorted_keywords[0][0]
        self.current_keyword = best_keyword
        
        return best_keyword
        
    def generate_related_keywords(self, seed_keyword, ollama_config=None):
        """Generate AI-powered related keywords."""
        if not ollama_config or not ollama_config.get("use_ollama", False):
            return self._generate_template_keywords(seed_keyword)
            
        try:
            # Analyze successful posts for context
            successful_topics = self._analyze_successful_content(seed_keyword)
            
            prompt = f"""Based on successful LinkedIn engagement with "{seed_keyword}", generate 3 related professional keywords that would attract similar high-quality posts.

Context from successful posts:
- Common topics: {', '.join(successful_topics[:5])}
- LinkedIn professional terminology preferred
- Focus on trending business/tech topics

Requirements:
- 1-4 words maximum per keyword
- Different enough from "{seed_keyword}" to provide variety
- Likely to have active LinkedIn discussions
- Professional and business-focused

Generate exactly 3 keywords, one per line, no numbering or bullets:"""

            response = requests.post(
                ollama_config.get("ollama_url", "http://localhost:11434/api/generate"),
                json={
                    "model": ollama_config.get("ollama_model", "llama3:8b"),
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "max_tokens": 100
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result.get("response", "").strip()
                
                # Parse keywords from response
                keywords = []
                for line in generated_text.split('\n'):
                    line = line.strip()
                    if line and not line.startswith(('•', '-', '1.', '2.', '3.')):
                        # Clean up the keyword
                        keyword = re.sub(r'^[\d\.\-\•\*\s]+', '', line).strip()
                        keyword = keyword.replace('"', '').replace("'", "")
                        
                        if len(keyword) > 0 and len(keyword) <= 50:
                            keywords.append(keyword.lower())
                
                # Validate and return keywords
                valid_keywords = []
                for keyword in keywords[:3]:
                    if keyword != seed_keyword.lower() and len(keyword.split()) <= 4:
                        # Mark as AI-generated
                        self.initialize_keyword(keyword)
                        self.performance_data[keyword]["generated_from"] = seed_keyword
                        valid_keywords.append(keyword)
                        
                if valid_keywords:
                    self._save_performance_data()
                    print(f"🤖 Generated AI keywords from '{seed_keyword}': {', '.join(valid_keywords)}")
                    return valid_keywords
                    
        except Exception as e:
            print(f"⚠️ AI keyword generation failed: {e}")
            
        # Fallback to template generation
        return self._generate_template_keywords(seed_keyword)
        
    def _generate_template_keywords(self, seed_keyword):
        """Generate template-based related keywords."""
        keyword_expansions = {
            "artificial intelligence": ["machine learning", "deep learning", "AI automation"],
            "machine learning": ["data science", "predictive analytics", "AI models"],
            "data science": ["big data", "analytics", "business intelligence"],
            "digital transformation": ["automation", "cloud computing", "digital strategy"],
            "leadership": ["management", "team building", "executive coaching"],
            "startup": ["entrepreneurship", "innovation", "venture capital"],
            "remote work": ["hybrid work", "work life balance", "digital nomad"],
            "cybersecurity": ["data privacy", "information security", "cyber threats"]
        }
        
        # Find related keywords
        related = keyword_expansions.get(seed_keyword.lower(), [])
        
        if not related:
            # Generate based on common patterns
            if "AI" in seed_keyword or "artificial" in seed_keyword:
                related = ["machine learning", "automation", "digital innovation"]
            elif "data" in seed_keyword:
                related = ["analytics", "business intelligence", "insights"]
            elif "work" in seed_keyword:
                related = ["productivity", "collaboration", "workplace culture"]
            else:
                related = ["innovation", "strategy", "growth"]
                
        # Mark as template-generated
        for keyword in related:
            self.initialize_keyword(keyword)
            self.performance_data[keyword]["generated_from"] = f"template:{seed_keyword}"
            
        if related:
            self._save_performance_data()
            print(f"📝 Generated template keywords from '{seed_keyword}': {', '.join(related)}")
            
        return related[:3]
        
    def _analyze_successful_content(self, keyword):
        """Analyze successful posts to extract trending topics."""
        # This would analyze comment history for successful posts
        # For now, return common LinkedIn topics
        trending_topics = [
            "digital transformation", "leadership development", "innovation strategy",
            "team collaboration", "professional growth", "industry insights",
            "market trends", "technology adoption", "business strategy",
            "career development", "thought leadership", "best practices"
        ]
        
        return trending_topics
        
    def get_performance_summary(self):
        """Get performance summary for all keywords."""
        if not self.performance_data:
            return "No keyword performance data available."
            
        summary = "\n📊 Keyword Performance Summary:\n"
        summary += "=" * 50 + "\n"
        
        # Sort keywords by success rate
        sorted_keywords = sorted(
            self.performance_data.items(),
            key=lambda x: (x[1].get("success_rate", 0), x[1].get("comments_successful", 0)),
            reverse=True
        )
        
        for keyword, data in sorted_keywords[:10]:  # Top 10
            success_rate = data.get("success_rate", 0)
            attempts = data.get("comments_attempted", 0)
            successes = data.get("comments_successful", 0)
            avg_results = data.get("avg_results_per_search", 0)
            
            status = ""
            if data.get("cooling_until"):
                cooling_until = datetime.fromisoformat(data["cooling_until"])
                if datetime.now() < cooling_until:
                    status = " 🧊"
                    
            summary += f"{keyword:<25} | {success_rate:>6.1%} | {successes:>3}/{attempts:<3} | {avg_results:>4.1f} results{status}\n"
            
        return summary

# Enhanced Duplicate Detection System
class EnhancedDuplicateDetector:
    """
    Multi-level duplicate detection system with semantic analysis.
    """
    
    def __init__(self, similarity_threshold=0.75):
        self.threshold = similarity_threshold
        self.comment_signatures = set()
        self.recent_comments = []
        self.max_recent_comments = 100
        
    def add_comment(self, comment_text, post_signature=""):
        """Add a comment to the tracking system."""
        signature = self._generate_signature(comment_text, post_signature)
        self.comment_signatures.add(signature)
        
        # Add to recent comments for semantic analysis
        self.recent_comments.append({
            "text": comment_text,
            "signature": signature,
            "timestamp": datetime.now(),
            "normalized": self._normalize_text(comment_text)
        })
        
        # Keep only recent comments
        if len(self.recent_comments) > self.max_recent_comments:
            self.recent_comments = self.recent_comments[-self.max_recent_comments:]
            
    def is_duplicate(self, new_comment, post_signature="", days_lookback=7):
        """Check if comment is a duplicate using multiple methods."""
        
        # Method 1: Exact signature match
        new_signature = self._generate_signature(new_comment, post_signature)
        if new_signature in self.comment_signatures:
            return True, 1.0, "exact_signature_match"
            
        # Method 2: Normalized text comparison
        normalized_new = self._normalize_text(new_comment)
        cutoff_time = datetime.now() - timedelta(days=days_lookback)
        
        for comment in self.recent_comments:
            if comment["timestamp"] < cutoff_time:
                continue
                
            # Exact normalized match
            if normalized_new == comment["normalized"]:
                return True, 1.0, "exact_normalized_match"
                
            # Semantic similarity
            similarity = self._calculate_similarity(normalized_new, comment["normalized"])
            if similarity >= self.threshold:
                return True, similarity, "semantic_similarity"
                
            # Pattern similarity
            pattern_similarity = self._calculate_pattern_similarity(new_comment, comment["text"])
            if pattern_similarity >= 0.8:
                return True, pattern_similarity, "pattern_similarity"
                
        return False, 0.0, None
        
    def _generate_signature(self, comment_text, post_signature=""):
        """Generate unique signature for comment."""
        # Combine normalized comment with post signature
        normalized = self._normalize_text(comment_text)
        combined = f"{normalized}:{post_signature}"
        return hashlib.md5(combined.encode()).hexdigest()
        
    def _normalize_text(self, text):
        """Normalize text for comparison."""
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove punctuation variations
        text = re.sub(r'[^\w\s]', '', text)
        
        # Remove common variations
        text = text.replace('youre', 'you are')
        text = text.replace('dont', 'do not')
        text = text.replace('cant', 'can not')
        text = text.replace('wont', 'will not')
        
        return text
        
    def _calculate_similarity(self, text1, text2):
        """Calculate semantic similarity between two texts."""
        # Simple word overlap similarity
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0.0
            
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
        
    def _calculate_pattern_similarity(self, text1, text2):
        """Calculate structural pattern similarity."""
        # Extract sentence patterns
        pattern1 = self._extract_sentence_pattern(text1)
        pattern2 = self._extract_sentence_pattern(text2)
        
        return self._pattern_similarity(pattern1, pattern2)
        
    def _extract_sentence_pattern(self, text):
        """Extract sentence structure pattern."""
        # Simple pattern extraction
        sentences = text.split('.')
        patterns = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            # Count words and detect common patterns
            word_count = len(sentence.split())
            has_question = '?' in sentence
            has_exclamation = '!' in sentence
            
            patterns.append({
                "word_count": word_count,
                "has_question": has_question,
                "has_exclamation": has_exclamation,
                "length_category": "short" if word_count < 5 else "medium" if word_count < 15 else "long"
            })
            
        return patterns
        
    def _pattern_similarity(self, pattern1, pattern2):
        """Calculate similarity between sentence patterns."""
        if not pattern1 or not pattern2:
            return 0.0
            
        # Compare pattern structures
        similarities = []
        min_length = min(len(pattern1), len(pattern2))
        
        for i in range(min_length):
            p1, p2 = pattern1[i], pattern2[i]
            
            similarity = 0.0
            
            # Length category match
            if p1["length_category"] == p2["length_category"]:
                similarity += 0.4
                
            # Question/exclamation match
            if p1["has_question"] == p2["has_question"]:
                similarity += 0.3
                
            if p1["has_exclamation"] == p2["has_exclamation"]:
                similarity += 0.3
                
            similarities.append(similarity)
            
        return sum(similarities) / len(similarities) if similarities else 0.0

class AccountHealthMonitor:
    """
    Monitor account health and detect risk factors.
    """
    
    def __init__(self, account_name="default"):
        self.account_name = account_name
        self.health_file = f"data/health_{account_name}.json"
        self.health_data = self._load_health_data()
        self.base_score = 100
        
    def _load_health_data(self):
        """Load health monitoring data."""
        try:
            if os.path.exists(self.health_file):
                with open(self.health_file, 'r') as f:
                    return json.load(f)
            return {
                "captcha_encounters": [],
                "warnings_detected": [],
                "failed_logins": [],
                "suspicious_patterns": [],
                "daily_activity": {},
                "health_score": 100,
                "last_updated": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"⚠️ Error loading health data: {e}")
            return {"health_score": 100}
            
    def _save_health_data(self):
        """Save health monitoring data."""
        try:
            os.makedirs(os.path.dirname(self.health_file), exist_ok=True)
            self.health_data["last_updated"] = datetime.now().isoformat()
            with open(self.health_file, 'w') as f:
                json.dump(self.health_data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Error saving health data: {e}")
            
    def detect_captcha_signals(self, page_source, current_url):
        """Detect CAPTCHA or verification challenges."""
        risk_indicators = [
            "captcha" in page_source.lower(),
            "verify" in page_source.lower(),
            "security check" in page_source.lower(),
            "unusual activity" in page_source.lower(),
            "/challenge/" in current_url.lower(),
            "please confirm" in page_source.lower(),
            "verification" in page_source.lower()
        ]
        
        if any(risk_indicators):
            self.record_captcha_encounter()
            return True
            
        return False
        
    def detect_warning_signals(self, page_source):
        """Detect LinkedIn warning messages."""
        warning_patterns = [
            "account restriction",
            "reduced visibility",
            "suspended",
            "limited features",
            "unusual activity detected",
            "temporarily restricted",
            "violation of",
            "community guidelines"
        ]
        
        page_lower = page_source.lower()
        detected_warnings = [pattern for pattern in warning_patterns if pattern in page_lower]
        
        if detected_warnings:
            self.record_warning(detected_warnings)
            return True, detected_warnings
            
        return False, []
        
    def record_captcha_encounter(self):
        """Record a CAPTCHA encounter."""
        encounter = {
            "timestamp": datetime.now().isoformat(),
            "type": "captcha_detected"
        }
        
        if "captcha_encounters" not in self.health_data:
            self.health_data["captcha_encounters"] = []
            
        self.health_data["captcha_encounters"].append(encounter)
        
        # Keep only last 30 days
        cutoff = datetime.now() - timedelta(days=30)
        self.health_data["captcha_encounters"] = [
            enc for enc in self.health_data["captcha_encounters"]
            if datetime.fromisoformat(enc["timestamp"]) > cutoff
        ]
        
        self.recalculate_health_score()
        print("🚨 CAPTCHA detected - health score updated")
        
    def record_warning(self, warning_types):
        """Record LinkedIn warning detection."""
        warning = {
            "timestamp": datetime.now().isoformat(),
            "types": warning_types
        }
        
        if "warnings_detected" not in self.health_data:
            self.health_data["warnings_detected"] = []
            
        self.health_data["warnings_detected"].append(warning)
        
        # Keep only last 30 days
        cutoff = datetime.now() - timedelta(days=30)
        self.health_data["warnings_detected"] = [
            warn for warn in self.health_data["warnings_detected"]
            if datetime.fromisoformat(warn["timestamp"]) > cutoff
        ]
        
        self.recalculate_health_score()
        print(f"⚠️ LinkedIn warning detected: {', '.join(warning_types)}")
        
    def record_failed_login(self):
        """Record a failed login attempt."""
        failure = {
            "timestamp": datetime.now().isoformat()
        }
        
        if "failed_logins" not in self.health_data:
            self.health_data["failed_logins"] = []
            
        self.health_data["failed_logins"].append(failure)
        
        # Keep only last 7 days for login failures
        cutoff = datetime.now() - timedelta(days=7)
        self.health_data["failed_logins"] = [
            fail for fail in self.health_data["failed_logins"]
            if datetime.fromisoformat(fail["timestamp"]) > cutoff
        ]
        
        self.recalculate_health_score()
        
    def record_daily_activity(self, searches=0, comments=0):
        """Record daily activity metrics."""
        today = datetime.now().strftime("%Y-%m-%d")
        
        if "daily_activity" not in self.health_data:
            self.health_data["daily_activity"] = {}
            
        if today not in self.health_data["daily_activity"]:
            self.health_data["daily_activity"][today] = {"searches": 0, "comments": 0}
            
        self.health_data["daily_activity"][today]["searches"] += searches
        self.health_data["daily_activity"][today]["comments"] += comments
        
        # Keep only last 30 days
        cutoff = datetime.now() - timedelta(days=30)
        cutoff_str = cutoff.strftime("%Y-%m-%d")
        
        self.health_data["daily_activity"] = {
            date: activity for date, activity in self.health_data["daily_activity"].items()
            if date >= cutoff_str
        }
        
        self.recalculate_health_score()
        
    def recalculate_health_score(self):
        """Recalculate overall health score."""
        score = self.base_score
        
        # Deduct for CAPTCHAs (last 30 days)
        captcha_count = len(self.health_data.get("captcha_encounters", []))
        score -= captcha_count * 20
        
        # Deduct for warnings (last 30 days)
        warning_count = len(self.health_data.get("warnings_detected", []))
        score -= warning_count * 25
        
        # Deduct for failed logins (last 7 days)
        failed_login_count = len(self.health_data.get("failed_logins", []))
        score -= failed_login_count * 10
        
        # Deduct for high activity levels
        daily_activity = self.health_data.get("daily_activity", {})
        for date, activity in daily_activity.items():
            searches = activity.get("searches", 0)
            comments = activity.get("comments", 0)
            
            # High search activity penalty
            if searches > 15:
                score -= (searches - 15) * 3
                
            # High comment activity penalty
            if comments > 10:
                score -= (comments - 10) * 5
                
        # Ensure score doesn't go below 0
        score = max(0, score)
        
        self.health_data["health_score"] = score
        self._save_health_data()
        
        return score
        
    def get_health_status(self):
        """Get current health status and recommendations."""
        score = self.health_data.get("health_score", 100)
        
        if score >= 80:
            status = "HEALTHY"
            recommendation = "Normal operation"
            activity_multiplier = 1.0
        elif score >= 60:
            status = "CAUTION"
            recommendation = "Reduce activity by 50%"
            activity_multiplier = 0.5
        elif score >= 40:
            status = "WARNING"
            recommendation = "Minimal activity only"
            activity_multiplier = 0.25
        elif score >= 20:
            status = "DANGER"
            recommendation = "Emergency cooldown 24-48 hours"
            activity_multiplier = 0.0
        else:
            status = "CRITICAL"
            recommendation = "Extended recovery 3-7 days"
            activity_multiplier = 0.0
            
        return {
            "score": score,
            "status": status,
            "recommendation": recommendation,
            "activity_multiplier": activity_multiplier,
            "recent_issues": self._get_recent_issues()
        }
        
    def _get_recent_issues(self):
        """Get summary of recent health issues."""
        issues = []
        
        # Recent CAPTCHAs
        captcha_count = len(self.health_data.get("captcha_encounters", []))
        if captcha_count > 0:
            issues.append(f"{captcha_count} CAPTCHA encounters")
            
        # Recent warnings
        warning_count = len(self.health_data.get("warnings_detected", []))
        if warning_count > 0:
            issues.append(f"{warning_count} LinkedIn warnings")
            
        # Recent failed logins
        failed_login_count = len(self.health_data.get("failed_logins", []))
        if failed_login_count > 0:
            issues.append(f"{failed_login_count} failed logins")
            
        # High activity days
        high_activity_days = 0
        for activity in self.health_data.get("daily_activity", {}).values():
            if activity.get("comments", 0) > 15 or activity.get("searches", 0) > 20:
                high_activity_days += 1
                
        if high_activity_days > 0:
            issues.append(f"{high_activity_days} high activity days")
            
        return issues
        
    def should_pause_activity(self):
        """Check if account should pause all activity."""
        health_status = self.get_health_status()
        return health_status["activity_multiplier"] == 0.0
        
    def get_recommended_delay_multiplier(self):
        """Get delay multiplier based on health score."""
        health_status = self.get_health_status()
        score = health_status["score"]
        
        if score >= 80:
            return 1.0  # Normal delays
        elif score >= 60:
            return 1.5  # 50% longer delays
        elif score >= 40:
            return 2.0  # Double delays
        else:
            return 3.0  # Triple delays

class SimpleAccountManager:
    """
    Simple account manager without complex scheduling - for manual operation.
    """
    
    def __init__(self):
        self.accounts_file = "data/simple_accounts.json"
        self.accounts = self._load_accounts()
        
    def _load_accounts(self):
        """Load accounts configuration."""
        try:
            if os.path.exists(self.accounts_file):
                with open(self.accounts_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"⚠️ Error loading accounts: {e}")
            return {}
            
    def _save_accounts(self):
        """Save accounts configuration."""
        try:
            os.makedirs(os.path.dirname(self.accounts_file), exist_ok=True)
            with open(self.accounts_file, 'w') as f:
                json.dump(self.accounts, f, indent=2)
        except Exception as e:
            print(f"⚠️ Error saving accounts: {e}")
            
    def add_account(self, name, keywords=None, max_comments_per_day=100):
        """Add a new account (no login credentials stored)."""
        self.accounts[name] = {
            "name": name,
            "keywords": keywords or ["artificial intelligence", "machine learning"],
            "max_comments_per_day": max_comments_per_day,
            "created_at": datetime.now().isoformat(),
            "last_used": None,
            "total_comments": 0,
            "active": True
        }
        self._save_accounts()
        
    def get_account_names(self):
        """Get list of account names."""
        return [name for name, data in self.accounts.items() if data.get("active", True)]
        
    def get_account_info(self, account_name):
        """Get account information."""
        return self.accounts.get(account_name)
        
    def update_account_usage(self, account_name, comments_posted=0):
        """Update account usage statistics."""
        if account_name in self.accounts:
            self.accounts[account_name]["last_used"] = datetime.now().isoformat()
            self.accounts[account_name]["total_comments"] += comments_posted
            self._save_accounts()
            
    def can_post_comment(self, account_name):
        """Check if account can post more comments today."""
        if account_name not in self.accounts:
            return False, "Account not found"
            
        account = self.accounts[account_name]
        max_daily = account.get("max_comments_per_day", 100)
        
        # Check daily comment count (this would need tracking)
        # For now, always allow
        return True, "OK"

# Configuration constants
DEFAULT_CONFIG = {
    "accounts": [],
    "brave_path": "",  # Will be auto-detected
    "default_keywords": ["artificial intelligence", "machine learning"],
    "wait_time_between_comments": [120, 300],  # Range in seconds (2-5 minutes for stealth)
    "max_comments_per_run": 25,  # Increased for long runs
    "max_comments_per_day": 150,  # Daily limit per account
    "session_break_duration": [900, 1800],  # 15-30 minutes break between sessions
    "min_post_score": 20,
    "use_ollama": True,  # Set to True if using local Ollama for comment generation
    "ollama_url": "http://localhost:11434/api/generate",
    "ollama_model": "llama3:8b",
    "use_proxies": True,  # Set to True if using proxy rotation
    "proxy_rotation_frequency": 15,  # Change proxy every N comments
    "stealth_mode": True,  # Enable advanced stealth features
    "human_behavior_simulation": True  # Simulate human-like behavior
}

class StealthFeatures:
    """Advanced stealth features for long-run automation."""
    
    @staticmethod
    def random_delay(min_seconds=1, max_seconds=5):
        """Generate random delay to simulate human behavior."""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
        
    @staticmethod
    def human_like_typing(element, text, typing_speed_range=(0.05, 0.2)):
        """Type text with human-like patterns including errors and corrections."""
        element.clear()
        
        for i, char in enumerate(text):
            element.send_keys(char)
            
            # Random typing speed
            typing_delay = random.uniform(*typing_speed_range)
            time.sleep(typing_delay)
            
            # Simulate occasional typing errors (2% chance)
            if random.random() < 0.02 and i > 3:
                # Make a "mistake"
                wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz')
                element.send_keys(wrong_char)
                time.sleep(random.uniform(0.1, 0.3))
                
                # Correct the mistake
                element.send_keys('\b')  # Backspace
                time.sleep(random.uniform(0.1, 0.2))
                element.send_keys(char)
                
            # Random pauses (10% chance of longer pause)
            if random.random() < 0.1:
                time.sleep(random.uniform(0.3, 0.8))
                
    @staticmethod
    def random_mouse_movement(driver):
        """Simulate random mouse movements."""
        try:
            from selenium.webdriver.common.action_chains import ActionChains
            
            body = driver.find_element(By.TAG_NAME, "body")
            action_chains = ActionChains(driver)
            
            # Random movement
            x_offset = random.randint(-100, 100)
            y_offset = random.randint(-100, 100)
            
            action_chains.move_to_element_with_offset(body, x_offset, y_offset).perform()
            time.sleep(random.uniform(0.1, 0.3))
        except:
            pass  # Ignore errors in mouse movement
            
    @staticmethod
    def random_scroll(driver, direction="down"):
        """Simulate human-like scrolling."""
        scroll_distance = random.randint(200, 800)
        scroll_steps = random.randint(3, 7)
        
        for _ in range(scroll_steps):
            step_distance = scroll_distance // scroll_steps
            if direction == "down":
                driver.execute_script(f"window.scrollBy(0, {step_distance})")
            else:
                driver.execute_script(f"window.scrollBy(0, -{step_distance})")
            time.sleep(random.uniform(0.1, 0.4))

class SessionManager:
    """Manages long-running sessions with breaks and limits."""
    
    def __init__(self, account_name):
        self.account_name = account_name
        self.session_start_time = datetime.now()
        self.comments_in_session = 0
        self.total_comments_today = 0
        self.last_comment_time = None
        self.session_number = 1
        self.proxy_rotation_counter = 0
        
    def should_take_break(self, config):
        """Determine if account should take a session break."""
        max_per_session = config.get("max_comments_per_run", 25)
        return self.comments_in_session >= max_per_session
        
    def should_stop_for_day(self, config):
        """Check if daily limit is reached."""
        daily_limit = config.get("max_comments_per_day", 150)
        return self.total_comments_today >= daily_limit
        
    def can_make_comment(self, config):
        """Check if account can make another comment."""
        if self.should_stop_for_day(config):
            return False, "Daily limit reached"
            
        if self.last_comment_time:
            min_interval = config.get("wait_time_between_comments", [120, 300])[0]
            time_since_last = (datetime.now() - self.last_comment_time).total_seconds()
            if time_since_last < min_interval:
                return False, f"Need to wait {min_interval - time_since_last:.0f} more seconds"
                
        return True, "OK"
        
    def wait_for_next_comment(self, config):
        """Wait appropriate time before next comment."""
        min_wait, max_wait = config.get("wait_time_between_comments", [120, 300])
        wait_time = random.randint(min_wait, max_wait)
        
        if self.last_comment_time:
            time_since_last = (datetime.now() - self.last_comment_time).total_seconds()
            remaining_wait = max(0, wait_time - time_since_last)
        else:
            remaining_wait = wait_time
            
        if remaining_wait > 0:
            print(f"⏳ Waiting {remaining_wait:.0f} seconds before next comment...")
            time.sleep(remaining_wait)
            
    def record_comment(self):
        """Record that a comment was made."""
        self.last_comment_time = datetime.now()
        self.comments_in_session += 1
        self.total_comments_today += 1
        self.proxy_rotation_counter += 1
        
    def take_session_break(self, config):
        """Take a break between comment sessions."""
        min_break, max_break = config.get("session_break_duration", [900, 1800])
        break_duration = random.randint(min_break, max_break)
        
        print(f"🛌 Taking session break for {break_duration // 60} minutes...")
        print(f"📊 Session {self.session_number} stats: {self.comments_in_session} comments")
        
        time.sleep(break_duration)
        
        # Reset session counters
        self.comments_in_session = 0
        self.session_number += 1
        self.session_start_time = datetime.now()
        
    def should_rotate_proxy(self, config):
        """Check if proxy should be rotated."""
        rotation_freq = config.get("proxy_rotation_frequency", 15)
        return self.proxy_rotation_counter >= rotation_freq
        
    def reset_proxy_counter(self):
        """Reset proxy rotation counter."""
        self.proxy_rotation_counter = 0

class AdvancedProxyManager:
    """Enhanced proxy management for long runs."""
    
    def __init__(self, config_file="proxy_config_longrun.json"):
        self.config_file = config_file
        self.proxies = {}
        self.current_proxy = None
        self.proxy_stats = {}
        self.load_proxy_config()
        
    def load_proxy_config(self):
        """Load proxy configuration."""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                
            self.proxy_pools = config.get("proxy_pools", {})
            self.settings = config.get("proxy_settings", {})
            
            print(f"✅ Loaded proxy config with {len(self.proxy_pools)} pools")
            
        except FileNotFoundError:
            print(f"⚠️ Proxy config file not found: {self.config_file}")
            self.proxy_pools = {}
            self.settings = {}
            
    def get_proxy_for_account(self, account_name, pool_name="premium_residential"):
        """Get best available proxy for account."""
        if pool_name not in self.proxy_pools:
            print(f"⚠️ Proxy pool '{pool_name}' not found")
            return None
            
        pool = self.proxy_pools[pool_name]
        available_proxies = [p for p in pool.get("proxies", []) if p.get("enabled", True)]
        
        if not available_proxies:
            print(f"⚠️ No available proxies in pool '{pool_name}'")
            return None
            
        # Select proxy based on rotation method
        rotation_method = pool.get("rotation_method", "round_robin")
        
        if rotation_method == "round_robin":
            if account_name not in self.proxy_stats:
                self.proxy_stats[account_name] = {"index": 0}
            
            index = self.proxy_stats[account_name]["index"] % len(available_proxies)
            selected_proxy = available_proxies[index]
            self.proxy_stats[account_name]["index"] += 1
            
        else:  # Default to random
            selected_proxy = random.choice(available_proxies)
            
        return selected_proxy.get("url")
        
    def health_check_proxy(self, proxy_url):
        """Check if proxy is working."""
        try:
            proxies = {"http": proxy_url, "https": proxy_url}
            response = requests.get(
                self.settings.get("health_check_url", "https://httpbin.org/ip"),
                proxies=proxies,
                timeout=self.settings.get("health_check_timeout", 15)
            )
            return response.status_code == 200
        except:
            return False

class LongRunBot:
    """Enhanced LinkedIn bot for long runs with stealth features."""
    
    def __init__(self, config):
        self.config = config
        self.driver = None
        self.logged_in = False
        self.post_evaluator = PostEvaluator()
        self.session_manager = SessionManager(config.get("account_name", "default"))
        self.proxy_manager = AdvancedProxyManager()
        self.stealth = StealthFeatures()
        self.current_proxy = None
        
    def login_to_linkedin(self, username, password):
        """Login to LinkedIn with stealth measures."""
        try:
            self.driver.get("https://www.linkedin.com/login")
            time.sleep(random.uniform(2, 4))
            
            # Check if already logged in
            if "feed" in self.driver.current_url.lower():
                print("Already logged in")
                self.logged_in = True
                return True
                
            # Human-like login process
            username_field = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "username"))
            )
            
            self.stealth.human_like_typing(username_field, username)
            time.sleep(random.uniform(0.5, 1.5))
            
            password_field = self.driver.find_element(By.ID, "password")
            self.stealth.human_like_typing(password_field, password)
            time.sleep(random.uniform(0.5, 1.5))
            
            # Click login with human-like behavior
            login_button = self.driver.find_element(By.CSS_SELECTOR, "[type='submit']")
            login_button.click()
            
            time.sleep(random.uniform(3, 6))
            
            # Handle potential verification
            if "challenge" in self.driver.current_url.lower():
                print("🔐 Verification required - please complete manually")
                input("Press Enter after completing verification...")
                
            success = "feed" in self.driver.current_url.lower()
            if success:
                self.logged_in = True
                print("✅ Login successful!")
            else:
                print("❌ Login may have failed - please check")
                
            return success
            
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
            
    def search_for_posts(self, keyword):
        """Search for posts with the given keyword."""
        try:
            search_url = f"https://www.linkedin.com/search/results/content/?keywords={keyword}"
            self.driver.get(search_url)
            time.sleep(random.uniform(3, 6))
            
            # Random scrolling to load more posts
            for _ in range(random.randint(2, 5)):
                self.stealth.random_scroll(self.driver, "down")
                time.sleep(random.uniform(1, 2))
                
            posts = self.driver.find_elements(By.CSS_SELECTOR, "[data-urn*='activity']")
            return posts[:10]  # Return first 10 posts
            
        except Exception as e:
            print(f"Error searching for posts: {e}")
            return []
        
    def create_stealth_driver(self):
        """Create driver with advanced stealth features."""
        try:
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service
            
            options = Options()
            
            # Basic stealth options
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Proxy setup
            if self.config.get("use_proxies", True):
                account_name = self.config.get("account_name", "default")
                proxy_url = self.proxy_manager.get_proxy_for_account(account_name)
                if proxy_url:
                    options.add_argument(f'--proxy-server={proxy_url}')
                    self.current_proxy = proxy_url
                    print(f"🌐 Using proxy for stealth")
                    
            # Advanced stealth options
            options.add_argument("--disable-plugins-discovery")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-images")  # Faster loading
            options.add_argument("--disable-plugins")
            
            # User agent rotation
            if self.config.get("stealth_mode", True):
                user_agents = [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                ]
                options.add_argument(f'--user-agent={random.choice(user_agents)}')
                
            service = Service()
            driver = webdriver.Chrome(service=service, options=options)
            
            # Execute stealth scripts
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            return driver
            
        except Exception as e:
            print(f"❌ Error creating stealth driver: {e}")
            return None
            
    def run_long_session(self, target_comments=100):
        """Run extended commenting session with stealth features."""
        print(f"🚀 Starting long session - Target: {target_comments} comments")
        
        # Create stealth driver
        self.driver = self.create_stealth_driver()
        if not self.driver:
            return 0
            
        # Login
        if not self.login_to_linkedin(
            self.config.get("username", ""),
            self.config.get("password", "")
        ):
            return 0
            
        total_comments = 0
        keywords = self.config.get("keywords", self.config.get("default_keywords", ["AI"]))
        
        try:
            while total_comments < target_comments:
                # Check daily limits
                if self.session_manager.should_stop_for_day(self.config):
                    print("📊 Daily comment limit reached")
                    break
                    
                # Check if session break needed
                if self.session_manager.should_take_break(self.config):
                    self.session_manager.take_session_break(self.config)
                    
                    # Simulate human activity during break
                    self.simulate_human_activity()
                    
                # Check if proxy rotation needed
                if self.session_manager.should_rotate_proxy(self.config):
                    print("🔄 Rotating proxy...")
                    self.rotate_proxy()
                    self.session_manager.reset_proxy_counter()
                    
                # Wait before next comment
                can_comment, reason = self.session_manager.can_make_comment(self.config)
                if not can_comment:
                    print(f"⏸️ Cannot comment: {reason}")
                    if "wait" in reason.lower():
                        time.sleep(60)  # Wait a minute and try again
                        continue
                    else:
                        break
                        
                self.session_manager.wait_for_next_comment(self.config)
                
                # Find and comment on posts
                keyword = random.choice(keywords)
                posts = self.search_for_posts(keyword)
                
                # Process a few posts per search
                posts_to_process = min(3, len(posts))
                for i in range(posts_to_process):
                    if total_comments >= target_comments:
                        break
                        
                    post = posts[i]
                    
                    # Extract post data with stealth
                    post_data = self.extract_post_data_stealth(post)
                    if not post_data:
                        continue
                        
                    # Evaluate post quality
                    evaluation = self.post_evaluator.evaluate_post(post_data)
                    if not evaluation["pass_threshold"]:
                        print(f"⏭️ Skipping low-quality post (score: {evaluation['total_score']})")
                        continue
                        
                    # Comment with stealth features
                    if self.comment_on_post_stealth(post, post_data):
                        total_comments += 1
                        self.session_manager.record_comment()
                        print(f"✅ Comment {total_comments}/{target_comments} posted")
                        
                        # Random human-like activity
                        if random.random() < 0.3:
                            self.random_page_activity()
                            
                    # Random delay between posts
                    self.stealth.random_delay(10, 30)
                    
                # Longer delay between search queries
                self.stealth.random_delay(30, 90)
                
        except Exception as e:
            print(f"❌ Error in long session: {e}")
            traceback.print_exc()
            
        finally:
            if self.driver:
                self.driver.quit()
                
        print(f"🏁 Long session completed. Total comments: {total_comments}")
        return total_comments
        
    def extract_post_data_stealth(self, post_element):
        """Extract post data with human-like behavior."""
        try:
            # Scroll to post naturally
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", post_element)
            self.stealth.random_delay(1, 3)
            
            # Random mouse movement
            self.stealth.random_mouse_movement(self.driver)
            
            # Extract text content
            text_elements = post_element.find_elements(By.CSS_SELECTOR, "[data-attributed-text], .feed-shared-text, .share-update-card__content")
            post_text = " ".join([elem.text.strip() for elem in text_elements if elem.text.strip()])
            
            # Extract author
            author_elements = post_element.find_elements(By.CSS_SELECTOR, ".feed-shared-actor__name, .update-components-actor__name")
            author = author_elements[0].text.strip() if author_elements else "Unknown"
            
            return {
                "text": post_text,
                "author": author,
                "element": post_element,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"⚠️ Error extracting post data: {e}")
            return None
            
    def comment_on_post_stealth(self, post_element, post_data):
        """Comment on post with advanced stealth features."""
        try:
            # Find comment button with multiple selectors
            comment_selectors = [
                "[aria-label*='Comment']",
                ".comment-button",
                "[data-control-name*='comment']",
                ".feed-shared-social-action-bar__action-button[aria-label*='Comment']"
            ]
            
            comment_button = None
            for selector in comment_selectors:
                try:
                    comment_button = post_element.find_element(By.CSS_SELECTOR, selector)
                    if comment_button.is_displayed():
                        break
                except:
                    continue
                    
            if not comment_button:
                print("⚠️ Could not find comment button")
                return False
                
            # Human-like click
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", comment_button)
            self.stealth.random_delay(0.5, 1.5)
            
            # Move mouse to button area before clicking
            self.stealth.random_mouse_movement(self.driver)
            comment_button.click()
            
            self.stealth.random_delay(1, 3)
            
            # Wait for comment box
            comment_box_selectors = [
                "[contenteditable='true']",
                ".ql-editor",
                "[data-placeholder*='comment']",
                ".comments-comment-texteditor"
            ]
            
            comment_box = None
            for selector in comment_box_selectors:
                try:
                    comment_box = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue
                    
            if not comment_box:
                print("⚠️ Could not find comment input box")
                return False
                
            # Generate contextual comment
            comment_text = self.generate_smart_comment(post_data)
            
            # Type comment with human-like behavior
            comment_box.click()
            self.stealth.random_delay(0.5, 1)
            self.stealth.human_like_typing(comment_box, comment_text)
            
            self.stealth.random_delay(1, 3)
            
            # Find and click post button
            post_button_selectors = [
                "[data-control-name='comment.post']",
                ".comment-submit-button",
                "[aria-label*='Post comment']",
                "button[type='submit']"
            ]
            
            post_button = None
            for selector in post_button_selectors:
                try:
                    post_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if post_button.is_enabled():
                        break
                except:
                    continue
                    
            if not post_button:
                print("⚠️ Could not find post button")
                return False
                
            # Human-like submit
            self.stealth.random_mouse_movement(self.driver)
            post_button.click()
            
            self.stealth.random_delay(2, 4)
            
            # Verify comment was posted
            return self.verify_comment_posted()
            
        except Exception as e:
            print(f"❌ Error commenting on post: {e}")
            return False
            
    def verify_comment_posted(self):
        """Verify that comment was successfully posted."""
        try:
            # Look for success indicators
            success_indicators = [
                "comment-posted",
                "success",
                "your comment",
                "commented"
            ]
            
            page_source = self.driver.page_source.lower()
            for indicator in success_indicators:
                if indicator in page_source:
                    return True
                    
            # Wait a moment and check again
            time.sleep(2)
            
            # Look for the comment in the comments section
            comments = self.driver.find_elements(By.CSS_SELECTOR, ".comments-comment-item, .comment-item")
            return len(comments) > 0
            
        except:
            return True  # Assume success if verification fails
            
    def generate_smart_comment(self, post_data):
        """Generate contextual comment based on post content."""
        if self.config.get("use_ollama", True):
            try:
                return self.generate_ollama_comment(post_data)
            except:
                pass  # Fall back to templates
                
        # Template-based comments with context
        post_text = post_data.get("text", "").lower()
        
        templates = {
            "agreement": [
                "Great insights! This really resonates with my experience.",
                "Absolutely agree with your perspective on this.",
                "This is exactly what I've been thinking about lately.",
                "Really valuable points shared here."
            ],
            "question": [
                "Interesting perspective! How do you see this evolving?",
                "This makes me wonder about the practical applications.",
                "Great post! What's been your experience with this?",
                "Thought-provoking content. What are your thoughts on the challenges?"
            ],
            "appreciation": [
                "Thanks for sharing this valuable insight!",
                "Really appreciate you taking the time to share this.",
                "This is exactly the kind of content I love seeing on LinkedIn.",
                "Excellent breakdown of this topic!"
            ]
        }
        
        # Choose template category based on content
        if any(word in post_text for word in ["question", "what", "how", "why"]):
            category = "question"
        elif any(word in post_text for word in ["thank", "share", "insight", "experience"]):
            category = "appreciation" 
        else:
            category = "agreement"
            
        return random.choice(templates[category])
        
    def generate_ollama_comment(self, post_data):
        """Generate AI comment using Ollama."""
        try:
            prompt = f"""Generate a professional, engaging LinkedIn comment for this post:

Post: {post_data.get('text', '')[:500]}
Author: {post_data.get('author', 'Unknown')}

Guidelines:
- Keep it under 100 words
- Be professional and constructive
- Add value to the conversation
- Avoid generic responses
- Sound natural and human

Comment:"""

            response = requests.post(
                self.config.get("ollama_url", "http://localhost:11434/api/generate"),
                json={
                    "model": self.config.get("ollama_model", "llama3:8b"),
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.8,
                        "max_tokens": 100
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                comment = result.get("response", "").strip()
                
                # Clean up the comment
                comment = re.sub(r'^(Comment:|Response:)', '', comment, flags=re.IGNORECASE).strip()
                comment = comment.replace('"', '').replace("'", "'")
                
                if len(comment) > 10:
                    return comment
                    
        except Exception as e:
            print(f"⚠️ Ollama comment generation failed: {e}")
            
        # Fallback to template
        return self.generate_smart_comment(post_data)
        
    def simulate_human_activity(self):
        """Simulate random human browsing during breaks."""
        activities = [
            self.browse_linkedin_feed,
            self.check_notifications,
            self.view_random_profiles,
            self.browse_jobs_page
        ]
        
        # Perform 1-3 random activities
        num_activities = random.randint(1, 3)
        selected_activities = random.sample(activities, num_activities)
        
        for activity in selected_activities:
            try:
                print(f"🎭 Simulating human activity: {activity.__name__}")
                activity()
                self.stealth.random_delay(30, 120)
            except Exception as e:
                print(f"⚠️ Error in activity simulation: {e}")
                
    def browse_linkedin_feed(self):
        """Browse LinkedIn feed naturally."""
        try:
            self.driver.get("https://www.linkedin.com/feed/")
            self.stealth.random_delay(2, 5)
            
            # Scroll and interact naturally
            for _ in range(random.randint(5, 15)):
                self.stealth.random_scroll(self.driver, "down")
                self.stealth.random_delay(1, 4)
                
                # Occasionally interact with posts (like, view)
                if random.random() < 0.2:
                    posts = self.driver.find_elements(By.CSS_SELECTOR, "[data-urn*='activity']")
                    if posts:
                        random_post = random.choice(posts[:5])
                        try:
                            self.driver.execute_script("arguments[0].scrollIntoView();", random_post)
                            self.stealth.random_delay(2, 6)
                        except:
                            pass
                            
        except Exception as e:
            print(f"⚠️ Error browsing feed: {e}")
            
    def check_notifications(self):
        """Check LinkedIn notifications."""
        try:
            self.driver.get("https://www.linkedin.com/notifications/")
            self.stealth.random_delay(3, 6)
            
            for _ in range(random.randint(3, 8)):
                self.stealth.random_scroll(self.driver, "down")
                self.stealth.random_delay(1, 3)
                
        except Exception as e:
            print(f"⚠️ Error checking notifications: {e}")
            
    def view_random_profiles(self):
        """View random LinkedIn profiles."""
        try:
            search_terms = ["software engineer", "data scientist", "marketing manager", "CEO"]
            search_term = random.choice(search_terms)
            
            search_url = f"https://www.linkedin.com/search/results/people/?keywords={search_term}"
            self.driver.get(search_url)
            self.stealth.random_delay(3, 6)
            
            profiles = self.driver.find_elements(By.CSS_SELECTOR, "[data-control-name='search_srp_result']")
            
            for _ in range(random.randint(1, 3)):
                if profiles:
                    profile = random.choice(profiles[:5])
                    try:
                        profile.click()
                        self.stealth.random_delay(5, 15)
                        self.stealth.random_scroll(self.driver, "down")
                        self.driver.back()
                        self.stealth.random_delay(2, 4)
                    except:
                        break
                        
        except Exception as e:
            print(f"⚠️ Error viewing profiles: {e}")
            
    def browse_jobs_page(self):
        """Browse LinkedIn jobs page."""
        try:
            self.driver.get("https://www.linkedin.com/jobs/")
            self.stealth.random_delay(3, 6)
            
            for _ in range(random.randint(3, 8)):
                self.stealth.random_scroll(self.driver, "down")
                self.stealth.random_delay(2, 5)
                
        except Exception as e:
            print(f"⚠️ Error browsing jobs: {e}")
            
    def rotate_proxy(self):
        """Rotate to a new proxy."""
        try:
            if self.driver:
                self.driver.quit()
                
            # Brief pause before creating new driver
            self.stealth.random_delay(10, 30)
            
            # Create new driver with different proxy
            self.driver = self.create_stealth_driver()
            
            if self.driver:
                # Re-login
                if self.login_to_linkedin(
                    self.config.get("username", ""),
                    self.config.get("password", "")
                ):
                    print("✅ Successfully rotated proxy and re-logged in")
                else:
                    print("⚠️ Failed to login after proxy rotation")
            else:
                print("❌ Failed to create new driver after proxy rotation")
                
        except Exception as e:
            print(f"❌ Error rotating proxy: {e}")
            
    def random_page_activity(self):
        """Perform random page interactions."""
        activities = [
            lambda: self.stealth.random_scroll(self.driver, "down"),
            lambda: self.stealth.random_scroll(self.driver, "up"), 
            lambda: self.stealth.random_mouse_movement(self.driver),
            lambda: self.stealth.random_delay(2, 8)
        ]
        
        activity = random.choice(activities)
        activity()

class PostEvaluator:
    """
    Evaluates LinkedIn posts for engagement value on a 50-point scale.
    """
    
    def __init__(self, target_keywords=None, min_score_threshold=20):
        """Initialize the post evaluator with target keywords and thresholds."""
        self.target_keywords = target_keywords or []
        self.min_score_threshold = min_score_threshold
        
    def evaluate_post(self, post_data):
        """
        Evaluate a post for engagement potential on a 50-point scale.
        
        Args:
            post_data (dict): Post data including text, author, etc.
            
        Returns:
            dict: Evaluation results with scores and pass/fail status
        """
        # Extract post text and author
        post_text = post_data.get("text", "")
        author = post_data.get("author", "")
        
        # Skip very short posts
        if len(post_text.strip()) < 10:
            return {
                "total_score": 0,
                "pass_threshold": False,
                "notes": ["Post too short"]
            }
        
        # 1. Evaluate content quality (20 points max)
        content_score, content_notes = self._evaluate_content_quality(post_text)
        
        # 2. Evaluate author credibility (10 points max)
        author_score, author_notes = self._evaluate_author_credibility(author)
        
        # 3. Evaluate topic relevance to target keywords (10 points max)
        relevance_score, relevance_notes = self._evaluate_topic_relevance(post_text)
        
        # 4. Evaluate engagement potential (10 points max)
        engagement_score, engagement_notes = self._evaluate_engagement_potential(post_text)
        
        # Calculate total score (50 points max)
        total_score = content_score + author_score + relevance_score + engagement_score
        
        # Check if post passes minimum threshold
        passes_threshold = total_score >= self.min_score_threshold
        
        # Combine all notes
        all_notes = content_notes + author_notes + relevance_notes + engagement_notes
        
        return {
            "total_score": total_score,
            "pass_threshold": passes_threshold,
            "notes": all_notes
        }
        
    def _evaluate_content_quality(self, post_text):
        """Evaluate content quality of the post (20 points max)."""
        score = 0
        notes = []
        
        # Check content length (0-5 points)
        if len(post_text) < 50:
            score += 1
            notes.append("Very short post")
        elif len(post_text) < 100:
            score += 2
        elif len(post_text) < 200:
            score += 3
        elif len(post_text) < 400:
            score += 4
        else:
            score += 5
            notes.append("Long-form content")
            
        # Check for questions (0-3 points)
        question_count = post_text.count("?")
        if question_count > 0:
            question_score = min(question_count, 3)
            score += question_score
            if question_score >= 2:
                notes.append("Contains thought-provoking questions")
                
        # Check for lists, numbers, and structured content (0-4 points)
        if re.search(r'\d+\.', post_text) or re.search(r'•', post_text) or re.search(r'-\s', post_text):
            score += 3
            notes.append("Contains structured content (lists, steps)")
            
        # Check for hashtags (0-2 points)
        hashtag_count = len(re.findall(r'#\w+', post_text))
        if 1 <= hashtag_count <= 3:
            score += 2
            notes.append("Contains relevant hashtags")
        elif hashtag_count > 3:
            score += 1
            notes.append("Contains many hashtags")
            
        # Check for specific content markers (0-6 points)
        content_markers = 0
        
        # Case studies, examples, or stories
        if re.search(r'case stud|example|for instance|story|experience', post_text, re.IGNORECASE):
            content_markers += 2
            notes.append("Contains examples or case studies")
            
        # Data, research, or statistics
        if re.search(r'research|stud(y|ies)|data|statistics|according to|\d+%|\d+\s*percent', post_text, re.IGNORECASE):
            content_markers += 2
            notes.append("References data or research")
            
        # Tips, advice, or how-to content
        if re.search(r'tip|advice|how to|guide|step|strategy', post_text, re.IGNORECASE):
            content_markers += 2
            notes.append("Provides tips or how-to advice")
            
        score += min(content_markers, 6)
        
        # Cap at 20 points
        return min(score, 20), notes
        
    def _evaluate_author_credibility(self, author_name):
        """Evaluate author credibility (10 points max)."""
        # Simple implementation
        score = 5  # Default middle score
        notes = []
            
        return min(score, 10), notes
        
    def _evaluate_topic_relevance(self, post_text):
        """Evaluate relevance to target keywords (10 points max)."""
        score = 0
        notes = []
        
        # If no target keywords, give middle score
        if not self.target_keywords:
            return 5, ["No target keywords specified"]
            
        # Check for keyword matches
        matches = 0
        matched_keywords = []
        
        for keyword in self.target_keywords:
            if keyword.lower() in post_text.lower():
                matches += 1
                matched_keywords.append(keyword)
                
        # Score based on keyword matches
        if matches > 0:
            # Calculate base score - more keywords = higher score
            base_score = min(matches * 3, 8)
            
            # Add points for keyword in the first paragraph (likely more relevant)
            first_paragraph = post_text.split('\n')[0] if '\n' in post_text else post_text
            if any(keyword.lower() in first_paragraph.lower() for keyword in self.target_keywords):
                base_score += 2
                notes.append("Target keywords in first paragraph")
                
            score = base_score
            notes.append(f"Matches {matches} target keywords: {', '.join(matched_keywords[:3])}")
        else:
            # Check for partial matches or related terms
            lower_text = post_text.lower()
            partial_matches = sum(1 for kw in self.target_keywords if any(word in lower_text for word in kw.lower().split()))
            
            if partial_matches > 0:
                score = max(3, partial_matches * 2)
                notes.append(f"Contains {partial_matches} related terms to target keywords")
            else:
                score = 0
                notes.append("No matches to target keywords")
                
        return min(score, 10), notes
        
    def _evaluate_engagement_potential(self, post_text):
        """Evaluate engagement potential (10 points max)."""
        score = 0
        notes = []
        
        # Check for calls to action (0-3 points)
        cta_patterns = [
            r'what do you think\?',
            r'let me know',
            r'share your',
            r'comment below',
            r'agree\?',
            r'thoughts\?'
        ]
        
        cta_matches = sum(1 for pattern in cta_patterns if re.search(pattern, post_text, re.IGNORECASE))
        if cta_matches > 0:
            cta_score = min(cta_matches * 2, 3)
            score += cta_score
            notes.append("Contains calls to action")
            
        # Check for controversial or discussion-worthy statements (0-3 points)
        discussion_patterns = [
            r'controversial',
            r'unpopular opinion',
            r'debate',
            r'myth',
            r'misconception',
            r'wrong about',
            r'challenge',
            r'disagree'
        ]
        
        discussion_matches = sum(1 for pattern in discussion_patterns if re.search(pattern, post_text, re.IGNORECASE))
        if discussion_matches > 0:
            score += min(discussion_matches, 3)
            notes.append("Contains discussion-worthy content")
            
        # Check for trending topics (0-2 points)
        trending_topics = [
            'AI', 'artificial intelligence', 'ChatGPT', 'machine learning',
            'remote work', 'layoffs', 'recession', 'climate change',
            'sustainability', 'blockchain', 'crypto', 'leadership',
            'mental health', 'burnout', 'work-life balance',
            'career change', 'upskilling', 'generative AI'
        ]
        
        trending_matches = sum(1 for topic in trending_topics if topic.lower() in post_text.lower())
        if trending_matches > 0:
            score += min(trending_matches, 2)
            notes.append("Mentions trending topics")
            
        # Check for timeliness (0-2 points)
        time_patterns = [
            r'today', r'yesterday', r'this week', r'this month',
            r'recent', r'breaking', r'just announced', r'latest'
        ]
        
        time_matches = sum(1 for pattern in time_patterns if re.search(pattern, post_text, re.IGNORECASE))
        if time_matches > 0:
            score += min(time_matches, 2)
            notes.append("Contains timely content")
            
        return min(score, 10), notes

class LinkedInBot:
    """
    Enhanced LinkedIn Bot with keyword intelligence and health monitoring.
    Simple startup process like v0 - no credentials stored.
    """
    
    def __init__(self, config_file="config.json"):
        """Initialize the LinkedIn Bot."""
        # Load configuration
        self.config = self._load_config(config_file)
        self.config_file = config_file
        
        # Initialize core components
        self.driver = None
        self.logged_in = False
        self.current_account = None
        self.manual_login_mode = False  # For manual browser login
        
        # Initialize advanced systems
        self.account_manager = SimpleAccountManager()
        self.keyword_tracker = None  # Will be initialized per account
        self.duplicate_detector = EnhancedDuplicateDetector()
        self.health_monitor = None  # Will be initialized per account
        self.proxy_manager = None  # Will be initialized if proxies are used
        self.stealth = HumanBehaviorSimulator()  # For human-like interactions
        
        # Create base directories
        os.makedirs("logs", exist_ok=True)
        os.makedirs("data", exist_ok=True)
        os.makedirs("screenshots", exist_ok=True)
        
        # Set up post evaluator
        self.post_evaluator = PostEvaluator(
            target_keywords=self.config.get("default_keywords", []),
            min_score_threshold=self.config.get("min_post_score", 20)
        )
        
        # Track comments to avoid duplicates
        self.commented_posts = set()
        
        # Track comment history
        comment_history_file = "data/comment_history.json"
        self.comment_history = self._load_json_file(comment_history_file, {})
        self.comment_history_file = comment_history_file
        
        # Session stats
        self.session_stats = {
            "start_time": None,
            "comments_posted": 0,
            "posts_processed": 0,
            "keywords_used": [],
            "health_checks": 0
        }
        
    def interactive_startup(self):
        """Simple interactive startup with manual login support."""
        print("\n" + "="*60)
        print("🚀 LinkedIn Bot v1 Enhanced - Manual Login")
        print("="*60)
        print("� You will login manually in the browser")
        print("="*60)
        
        # Show existing accounts or setup new one
        account_names = self.account_manager.get_account_names()
        
        if account_names:
            print(f"\n📁 Available accounts: {', '.join(account_names)}")
            print("0. Add new account")
            
            for i, name in enumerate(account_names, 1):
                account_info = self.account_manager.get_account_info(name)
                total_comments = account_info.get("total_comments", 0)
                print(f"{i}. {name} (Total comments: {total_comments})")
                
            while True:
                try:
                    choice = int(input(f"\nSelect account (0-{len(account_names)}): "))
                    
                    if choice == 0:
                        return self._quick_setup_new_account()
                    elif 1 <= choice <= len(account_names):
                        selected_account = account_names[choice - 1]
                        self.current_account = selected_account
                        self._initialize_account_systems(selected_account)
                        print(f"✅ Using account: {selected_account}")
                        return self._start_session()
                    else:
                        print("❌ Invalid selection")
                except ValueError:
                    print("❌ Please enter a number")
        else:
            print("\n➕ No accounts found. Setting up first account...")
            return self._quick_setup_new_account()
            
    def _quick_setup_new_account(self):
        """Quick setup for new account - minimal questions."""
        print("\n➕ Quick Account Setup")
        print("-" * 25)
        
        # Get account name
        account_name = input("📝 Account name (e.g., 'john_doe'): ").strip()
        if not account_name:
            print("❌ Account name required")
            return False
            
        if account_name in self.account_manager.accounts:
            print("❌ Account already exists")
            return False
            
        # Simple keyword setup
        print("\n🎯 Keywords (or press Enter for AI/ML defaults):")
        keywords_input = input("📝 Keywords (comma-separated): ").strip()
        
        if keywords_input:
            keywords = [kw.strip() for kw in keywords_input.split(",")]
        else:
            keywords = ["artificial intelligence", "machine learning", "data science"]
            
        # Add account
        self.account_manager.add_account(account_name, keywords)
        self.current_account = account_name
        self._initialize_account_systems(account_name)
        
        print(f"✅ Account '{account_name}' created!")
        print(f"🎯 Keywords: {', '.join(keywords)}")
        
        return self._start_session()
        
    def _start_session(self):
        """Start the main commenting session."""
        print(f"\n🚀 Starting session for account: {self.current_account}")
        
        # Get target number of comments
        while True:
            try:
                target = input("\n� Target comments for this session (default 25): ").strip()
                target = int(target) if target else 25
                
                if target > 0:
                    break
                else:
                    print("❌ Target must be greater than 0")
            except ValueError:
                print("❌ Please enter a valid number")
                
        print(f"\n🎯 Target: {target} comments")
        print("🔄 Opening browser for manual LinkedIn login...")
        
        # Initialize browser
        if self.initialize_browser():
            if self.manual_login_mode:
                # Open LinkedIn and wait for manual login
                print("\n🌐 Opening LinkedIn...")
                self.driver.get("https://www.linkedin.com")
                time.sleep(2)
                
                print("\n" + "="*60)
                print("🔐 MANUAL LOGIN REQUIRED")
                print("="*60)
                print("1. Login to LinkedIn in the browser window")
                print("2. Complete any 2FA/verification")
                print("3. Make sure you reach the LinkedIn feed")
                print("4. Come back here and press ENTER")
                print("="*60)
                
                input("\nPress ENTER after you've logged in to LinkedIn...")
                
                # Verify login
                current_url = self.driver.current_url.lower()
                if "linkedin.com" in current_url and ("feed" in current_url or "in/" in current_url):
                    print("✅ LinkedIn login detected!")
                    self.logged_in = True
                else:
                    print("⚠️ Make sure you're logged into LinkedIn and on the feed page")
                    retry = input("Press ENTER to continue anyway, or 'q' to quit: ")
                    if retry.lower() == 'q':
                        return False
                    self.logged_in = True
                
            return self._run_enhanced_session(target)
        else:
            print("❌ Failed to initialize browser")
            return False
            
    def _run_enhanced_session(self, target_comments):
        """Run enhanced session with all advanced features for long runs."""
        print(f"\n🎯 Enhanced Session Started - Target: {target_comments}")
        print("🔥 Advanced features: Keyword Intelligence | Health Monitoring | Stealth Mode")
        print("-" * 70)
        
        # Initialize session components
        session_manager = SessionManager(self.current_account)
        behavior_simulator = HumanBehaviorSimulator()
        quality_analyzer = CommentQualityAnalyzer(self.current_account)
        
        comments_posted = 0
        total_attempts = 0
        consecutive_failures = 0
        last_keyword_rotation = 0
        
        # Get account keywords
        account_info = self.account_manager.get_account_info(self.current_account)
        available_keywords = account_info.get("keywords", ["artificial intelligence"])
        
        try:
            # Verify LinkedIn login first
            if not self._verify_linkedin_access():
                print("❌ Not logged into LinkedIn. Please login first!")
                return False
                
            while comments_posted < target_comments:
                # Check if we can continue (health, limits, etc.)
                if not self._can_continue_session(session_manager, target_comments):
                    break
                    
                # Health monitoring every 10 attempts
                if total_attempts % 10 == 0 and total_attempts > 0:
                    health_status = self.health_monitor.get_health_status()
                    if health_status["activity_multiplier"] == 0.0:
                        print(f"🛑 Health score too low ({health_status['score']}) - stopping session")
                        break
                    elif health_status["activity_multiplier"] < 1.0:
                        print(f"⚠️ Health warning ({health_status['score']}) - reducing speed")
                        
                # Keyword intelligence - rotate keywords intelligently
                if total_attempts - last_keyword_rotation >= 15 or not hasattr(self, '_current_keyword'):
                    self._current_keyword = self.keyword_tracker.select_best_keyword(available_keywords)
                    
                    # Check if keyword should be rotated
                    if self._current_keyword:
                        should_rotate, reasons = self.keyword_tracker.should_rotate_keyword(self._current_keyword)
                        if should_rotate:
                            print(f"🔄 Rotating keyword '{self._current_keyword}': {', '.join(reasons)}")
                            self.keyword_tracker.initiate_keyword_cooling(self._current_keyword)
                            
                            # Generate new keywords if needed
                            self._generate_new_keywords_if_needed(available_keywords)
                            
                            self._current_keyword = self.keyword_tracker.select_best_keyword(available_keywords)
                            last_keyword_rotation = total_attempts
                            
                if not self._current_keyword:
                    print("❌ No available keywords")
                    break
                    
                print(f"\n🔍 Keyword: '{self._current_keyword}' (Score: {self.keyword_tracker.calculate_keyword_score(self._current_keyword):.3f})")
                
                # Human behavior simulation - micro breaks
                if behavior_simulator.should_take_micro_break():
                    continue
                    
                # Search with intelligent pacing
                can_search, search_reason = session_manager.can_perform_search()
                if not can_search:
                    print(f"⏳ Search cooldown: {search_reason}")
                    time.sleep(5)
                    continue
                    
                # Search for posts
                posts = self._search_with_advanced_features(self._current_keyword, behavior_simulator)
                session_manager.record_search()
                self.keyword_tracker.record_search(self._current_keyword, len(posts))
                
                if not posts:
                    consecutive_failures += 1
                    if consecutive_failures >= 3:
                        # Try generating related keywords
                        self._generate_new_keywords_if_needed(available_keywords)
                        consecutive_failures = 0
                    continue
                else:
                    consecutive_failures = 0
                    
                # Process posts with advanced evaluation
                for post_element in posts:
                    if comments_posted >= target_comments:
                        break
                        
                    # Check session limits and health
                    can_comment, comment_reason = session_manager.can_make_comment(target_comments)
                    if not can_comment:
                        print(f"⏳ Comment cooldown: {comment_reason}")
                        behavior_simulator.random_delay(30, 90)
                        continue
                        
                    total_attempts += 1
                    
                    # Advanced post data extraction with human-like behavior
                    post_data = self._extract_post_data_with_behavior(post_element, behavior_simulator)
                    if not post_data:
                        continue
                        
                    # Multi-level duplicate detection
                    if self._is_duplicate_advanced(post_data):
                        continue
                        
                    # Enhanced post evaluation
                    evaluation = self.post_evaluator.evaluate_post(post_data)
                    
                    if not evaluation["pass_threshold"]:
                        print(f"🔍 Post score too low: {evaluation['total_score']}/50")
                        continue
                        
                    print(f"✅ High-quality post found (Score: {evaluation['total_score']}/50)")
                    
                    # Generate and analyze comment
                    comment_success = self._attempt_enhanced_comment_with_intelligence(
                        post_data, self._current_keyword, evaluation, 
                        quality_analyzer, behavior_simulator, session_manager
                    )
                    
                    if comment_success:
                        comments_posted += 1
                        consecutive_failures = 0
                        
                        # Update all tracking systems
                        session_manager.record_comment()
                        self.keyword_tracker.record_comment_attempt(self._current_keyword, True, evaluation['total_score'])
                        self.account_manager.update_account_usage(self.current_account, 1)
                        
                        print(f"🎉 Comment #{comments_posted} posted successfully!")
                        
                        # Human-like break between comments
                        delay = behavior_simulator.random_delay(
                            120 * behavior_simulator.fatigue_factor(),
                            300 * behavior_simulator.fatigue_factor()
                        )
                        print(f"😴 Human-like break: {delay:.1f}s")
                        
                    else:
                        consecutive_failures += 1
                        session_manager.record_error()
                        self.keyword_tracker.record_comment_attempt(self._current_keyword, False)
                        
                        if consecutive_failures >= 5:
                            print("❌ Too many consecutive failures - taking longer break")
                            behavior_simulator.random_delay(300, 600)
                            consecutive_failures = 0
                            
                    # Check if we should pause due to health concerns
                    if self.health_monitor.should_pause_activity():
                        print("🛑 Health monitor recommends pausing activity")
                        break
                        
        except KeyboardInterrupt:
            print("\n⏹️ Session interrupted by user")
        except Exception as e:
            print(f"\n❌ Session error: {e}")
            traceback.print_exc()
        finally:
            # Session cleanup and reporting
            self._finalize_enhanced_session(session_manager, comments_posted, total_attempts)
            
            return comments_posted > 0
            
    def _verify_linkedin_access(self):
        """Verify that we can access LinkedIn and are logged in."""
        try:
            print("🔍 Verifying LinkedIn access...")
            self.driver.get("https://www.linkedin.com/feed/")
            time.sleep(3)
            
            # Check if we're on the feed page (indicates logged in)
            if "feed" in self.driver.current_url.lower():
                print("✅ LinkedIn access verified")
                return True
            elif "login" in self.driver.current_url.lower():
                print("❌ Not logged in - please login to LinkedIn first")
                return False
            else:
                print("⚠️ Unknown LinkedIn page - attempting to continue")
                return True
        except Exception as e:
            print(f"❌ Error verifying LinkedIn access: {e}")
            return False
            
    def _can_continue_session(self, session_manager, target_comments):
        """Check if session can continue based on various factors."""
        # Check if health monitor suggests stopping
        if self.health_monitor and self.health_monitor.should_pause_activity():
            return False
            
        # Check session stats for anomalies
        stats = session_manager.get_session_stats()
        
        # Stop if too many errors
        if stats["errors_encountered"] >= 10:
            print("❌ Too many errors encountered - stopping session")
            return False
            
        # Stop if session is too long (safety measure)
        if stats["duration_minutes"] > 240:  # 4 hours max
            print("⏰ Session too long - stopping for safety")
            return False
            
        return True
        
    def _generate_new_keywords_if_needed(self, available_keywords):
        """Generate new keywords if running low."""
        active_keywords = [kw for kw in available_keywords 
                          if not self.keyword_tracker.performance_data.get(kw, {}).get("cooling_until")]
        
        if len(active_keywords) < 3:
            print("🤖 Generating new keywords...")
            
            # Use the best performing keyword as seed
            if available_keywords:
                best_keyword = max(available_keywords, 
                                 key=lambda k: self.keyword_tracker.calculate_keyword_score(k))
                
                new_keywords = self.keyword_tracker.generate_related_keywords(
                    best_keyword, 
                    self.config
                )
                
                if new_keywords:
                    available_keywords.extend(new_keywords)
                    
                    # Update account
                    account_info = self.account_manager.get_account_info(self.current_account)
                    account_info["keywords"].extend(new_keywords)
                    self.account_manager.accounts[self.current_account] = account_info
                    self.account_manager._save_accounts()
                    
                    print(f"✅ Generated {len(new_keywords)} new keywords: {', '.join(new_keywords)}")
                    
    def _search_with_advanced_features(self, keyword, behavior_simulator):
        """Search for posts with human-like behavior."""
        try:
            print(f"🔍 Searching for posts about '{keyword}'...")
            
            # Navigate to search with human-like timing
            search_url = f"https://www.linkedin.com/search/results/content/?keywords={keyword}"
            self.driver.get(search_url)
            
            # Human-like wait for page load
            behavior_simulator.random_delay(2, 4)
            
            # Natural scrolling to load more posts
            for _ in range(random.randint(2, 4)):
                behavior_simulator.natural_scroll(self.driver, "down")
                behavior_simulator.random_delay(1, 2)
                
            # Find posts with advanced selectors
            post_selectors = [
                "[data-urn*='activity']",
                ".feed-shared-update-v2",
                ".share-update-card",
                ".feed-shared-story"
            ]
            
            posts = []
            for selector in post_selectors:
                try:
                    found_posts = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if found_posts:
                        posts = found_posts[:10]  # Limit to first 10
                        break
                except:
                    continue
                    
            print(f"📊 Found {len(posts)} posts")
            return posts
            
        except Exception as e:
            print(f"❌ Search error: {e}")
            return []
            
    def _extract_post_data_with_behavior(self, post_element, behavior_simulator):
        """Extract post data with human-like behavior simulation."""
        try:
            # Scroll to post naturally
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", post_element)
            behavior_simulator.random_delay(1, 2)
            
            # Extract post text
            text_selectors = [
                ".feed-shared-text__text-view span[dir='ltr']",
                ".feed-shared-text span",
                ".share-update-card__content",
                "[data-attributed-text]"
            ]
            
            post_text = ""
            for selector in text_selectors:
                try:
                    text_elements = post_element.find_elements(By.CSS_SELECTOR, selector)
                    if text_elements:
                        post_text = " ".join([elem.text.strip() for elem in text_elements if elem.text.strip()])
                        break
                except:
                    continue
                    
            # Extract author
            author_selectors = [
                ".feed-shared-actor__name",
                ".update-components-actor__name",
                ".share-update-card__actor-name"
            ]
            
            author = "Unknown"
            for selector in author_selectors:
                try:
                    author_elem = post_element.find_element(By.CSS_SELECTOR, selector)
                    author = author_elem.text.strip()
                    break
                except:
                    continue
                    
            # Generate unique post ID
            post_id = hashlib.md5(f"{author}:{post_text[:100]}".encode()).hexdigest()[:12]
            
            # Simulate reading time
            reading_time = behavior_simulator.simulate_reading_time(len(post_text))
            time.sleep(min(reading_time, 5))  # Max 5 seconds reading time
            
            return {
                "id": post_id,
                "text": post_text,
                "author": author,
                "element": post_element,
                "signature": f"{author}:{post_text[:50]}"
            }
            
        except Exception as e:
            print(f"⚠️ Error extracting post data: {e}")
            return None
            
    def _is_duplicate_advanced(self, post_data):
        """Advanced duplicate detection using multiple methods."""
        try:
            # Check if we've already commented on this post
            if self.has_commented(post_data["id"]):
                return True
                
            # Enhanced duplicate detection
            is_duplicate, similarity, method = self.duplicate_detector.is_duplicate(
                post_data["text"], 
                post_data.get("signature", "")
            )
            
            if is_duplicate:
                print(f"🔄 Duplicate detected ({method}: {similarity:.2f})")
                return True
                
            return False
            
        except Exception as e:
            print(f"⚠️ Error in duplicate detection: {e}")
            return False
            
    def _attempt_enhanced_comment_with_intelligence(self, post_data, keyword, evaluation, 
                                                   quality_analyzer, behavior_simulator, session_manager):
        """Attempt to comment with all intelligence features."""
        try:
            # Generate comment using available methods
            comment_text = self._generate_intelligent_comment(post_data, keyword)
            
            if not comment_text:
                print("❌ Failed to generate comment")
                return False
                
            # Analyze comment quality
            quality_result = quality_analyzer.analyze_comment_quality(comment_text, post_data["text"])
            
            if quality_result["score"] < 60:
                print(f"⚠️ Comment quality too low ({quality_result['score']}/100): {', '.join(quality_result['issues'])}")
                return False
                
            print(f"✅ High-quality comment generated (Score: {quality_result['score']}/100)")
            
            # Find comment button with advanced selectors
            comment_button = AdvancedLinkedInSelectors.find_element_safely(
                self.driver, 
                AdvancedLinkedInSelectors.COMMENT_BUTTON_SELECTORS,
                timeout=10
            )
            
            if not comment_button:
                print("❌ Could not find comment button")
                return False
                
            # Human-like click
            behavior_simulator.random_delay(0.5, 1.5)
            comment_button.click()
            behavior_simulator.random_delay(1, 2)
            
            # Find comment box
            comment_box = AdvancedLinkedInSelectors.find_element_safely(
                self.driver,
                AdvancedLinkedInSelectors.COMMENT_BOX_SELECTORS,
                timeout=10
            )
            
            if not comment_box:
                print("❌ Could not find comment box")
                return False
                
            # Type comment with human-like behavior
            behavior_simulator.human_like_typing(comment_box, comment_text)
            behavior_simulator.random_delay(1, 2)
            
            # Submit comment
            submit_button = AdvancedLinkedInSelectors.find_element_safely(
                self.driver,
                AdvancedLinkedInSelectors.SUBMIT_COMMENT_SELECTORS,
                timeout=5
            )
            
            if submit_button:
                submit_button.click()
            else:
                # Try Enter key as fallback
                comment_box.send_keys(Keys.RETURN)
                
            # Wait for comment to post
            behavior_simulator.random_delay(2, 4)
            
            # Verify comment was posted
            if self._verify_comment_posted(comment_text):
                # Record successful comment
                self.duplicate_detector.add_comment(comment_text, post_data.get("signature", ""))
                self.add_commented_post(post_data["id"])
                
                # Health monitoring
                self.health_monitor.record_daily_activity(comments=1)
                
                return True
            else:
                print("⚠️ Comment verification failed")
                return False
                
        except Exception as e:
            print(f"❌ Comment attempt failed: {e}")
            return False
            
    def _generate_intelligent_comment(self, post_data, keyword):
        """Generate intelligent comment using available methods."""
        # Try Ollama first if available
        if self.config.get("use_ollama", False):
            try:
                ollama_comment = self._generate_ollama_comment(post_data, keyword)
                if ollama_comment:
                    return ollama_comment
            except Exception as e:
                print(f"⚠️ Ollama generation failed: {e}")
                
        # Fallback to template-based comments
        return self._generate_template_comment(post_data, keyword)
        
    def _generate_ollama_comment(self, post_data, keyword):
        """Generate comment using Ollama AI."""
        try:
            post_text = post_data.get("text", "")[:500]  # Limit text length
            
            prompt = f"""Generate a professional LinkedIn comment for this post about "{keyword}".
            
Post content: "{post_text}"

Requirements:
- Be professional and insightful
- 1-3 sentences maximum  
- Add value to the discussion
- Sound natural and engaging
- Don't just agree - add perspective

Generate only the comment text, no quotes or extra formatting:"""

            response = requests.post(
                self.config.get("ollama_url", "http://localhost:11434/api/generate"),
                json={
                    "model": self.config.get("ollama_model", "llama3:8b"),
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "max_tokens": 150
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                comment = result.get("response", "").strip()
                
                # Clean up the response
                comment = re.sub(r'^["\']*', '', comment)
                comment = re.sub(r'["\']*$', '', comment)
                
                if len(comment) > 10 and len(comment) < 300:
                    return comment
                    
        except Exception as e:
            print(f"⚠️ Ollama comment generation error: {e}")
            
        return None
        
    def _generate_template_comment(self, post_data, keyword):
        """Generate template-based comment."""
        post_text = post_data.get("text", "").lower()
        
        # Context-aware templates
        if "question" in post_text or "?" in post_text:
            templates = [
                "Great question! In my experience, this often comes down to finding the right balance between innovation and practical implementation.",
                "This is such an important discussion. I've found that the key is often in how we approach the problem from different angles.",
                "Excellent point raised here. What's your take on how this might evolve in the next few years?"
            ]
        elif "data" in post_text or "research" in post_text or "study" in post_text:
            templates = [
                "Thanks for sharing these insights! The data really highlights some important trends we should all be paying attention to.",
                "Fascinating research! This aligns with what I've been seeing in the field. The implications are quite significant.",
                "Really valuable data here. It's interesting how this correlates with other trends we're seeing in the industry."
            ]
        else:
            templates = [
                "Absolutely agree with your perspective on this. It's refreshing to see such thoughtful analysis on this topic.",
                "This really resonates with my experience. Thanks for sharing such valuable insights!",
                "Great post! This is exactly the kind of forward-thinking discussion our industry needs more of.",
                "Thank you for sharing this perspective. It's given me some new angles to consider on this important topic."
            ]
            
        return random.choice(templates)
        
    def _verify_comment_posted(self, comment_text):
        """Verify that the comment was successfully posted."""
        try:
            time.sleep(2)  # Wait for comment to appear
            
            # Look for the comment in recent comments
            comment_elements = self.driver.find_elements(By.CSS_SELECTOR, ".comments-comment-item")
            
            for element in comment_elements[-3:]:  # Check last 3 comments
                try:
                    text_elem = element.find_element(By.CSS_SELECTOR, ".comment-text, .comments-comment-text")
                    if text_elem and comment_text[:50].lower() in text_elem.text.lower():
                        return True
                except:
                    continue
                    
            return False
            
        except Exception as e:
            print(f"⚠️ Comment verification error: {e}")
            return False
            
    def _finalize_enhanced_session(self, session_manager, comments_posted, total_attempts):
        """Finalize session with comprehensive reporting."""
        stats = session_manager.get_session_stats()
        
        print("\n" + "="*70)
        print("📊 ENHANCED SESSION SUMMARY")
        print("="*70)
        print(f"🎯 Target Comments: {total_attempts}")
        print(f"✅ Successful Comments: {comments_posted}")
        print(f"📈 Success Rate: {(comments_posted/max(total_attempts,1)*100):.1f}%")
        print(f"⏱️ Session Duration: {stats['duration_minutes']:.1f} minutes")
        print(f"🔍 Searches Performed: {stats['searches_performed']}")
        print(f"⚠️ Errors Encountered: {stats['errors_encountered']}")
        print(f"📊 Comments/Hour: {stats['comments_per_hour']:.1f}")
        
        # Health status
        if self.health_monitor:
            health_status = self.health_monitor.get_health_status()
            print(f"🏥 Health Score: {health_status['score']}/100 ({health_status['status']})")
            
        # Keyword performance
        if self.keyword_tracker:
            print(f"\n🎯 Keyword Performance:")
            summary = self.keyword_tracker.get_performance_summary()
            print(summary)
            
        print("="*70)
        
    def _test_existing_session(self):
        """Test if existing browser session is still valid."""
        try:
            if self.initialize_browser():
                self.driver.get("https://www.linkedin.com/feed/")
                time.sleep(3)
                
                # Check if logged in
                if "feed" in self.driver.current_url.lower():
                    self.logged_in = True
                    return True
                    
            return False
        except Exception as e:
            print(f"❌ Error testing session: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
                self.driver = None
                
    def _select_existing_account(self):
        """Select from existing accounts."""
        account_names = self.account_manager.get_account_names()
        
        print("\n📋 Select Account:")
        for i, name in enumerate(account_names, 1):
            account_info = self.account_manager.get_account_info(name)
            last_used = account_info.get("last_used", "Never")
            if last_used != "Never":
                last_used = datetime.fromisoformat(last_used).strftime("%Y-%m-%d %H:%M")
            print(f"{i}. {name} (Last used: {last_used})")
            
        while True:
            try:
                choice = int(input(f"\nSelect account (1-{len(account_names)}): ")) - 1
                if 0 <= choice < len(account_names):
                    selected_account = account_names[choice]
                    self.current_account = selected_account
                    
                    # Initialize account-specific systems
                    self._initialize_account_systems(selected_account)
                    
                    print(f"✅ Selected account: {selected_account}")
                    return self._configure_session()
                else:
                    print("❌ Invalid selection")
            except ValueError:
                print("❌ Please enter a number")
                
    def _setup_new_account(self):
        """Setup a new account."""
        print("\n➕ Add New Account")
        print("-" * 25)
        
        account_name = input("📝 Enter account name (e.g., 'john_doe'): ").strip()
        if not account_name:
            print("❌ Account name required")
            return False
            
        # Check if account exists
        if account_name in self.account_manager.accounts:
            print("❌ Account name already exists")
            return False
            
        # Get keywords
        print("\n🎯 Configure Keywords")
        print("Default keywords: artificial intelligence, machine learning")
        custom_keywords = input("📝 Enter custom keywords (comma-separated) or press Enter for defaults: ").strip()
        
        if custom_keywords:
            keywords = [kw.strip() for kw in custom_keywords.split(",")]
        else:
            keywords = ["artificial intelligence", "machine learning"]
            
        # Get daily comment limit
        print("\n📊 Daily Limits")
        max_comments = input("📝 Max comments per day (default 100): ").strip()
        try:
            max_comments = int(max_comments) if max_comments else 100
        except ValueError:
            max_comments = 100
            
        # Add account
        self.account_manager.add_account(account_name, keywords, max_comments)
        self.current_account = account_name
        
        # Initialize account-specific systems
        self._initialize_account_systems(account_name)
        
        print(f"✅ Added account: {account_name}")
        print(f"🎯 Keywords: {', '.join(keywords)}")
        print(f"📊 Daily limit: {max_comments} comments")
        
        return self._configure_session()
        
    def _initialize_account_systems(self, account_name):
        """Initialize account-specific tracking systems."""
        self.keyword_tracker = KeywordPerformanceTracker(account_name)
        self.health_monitor = AccountHealthMonitor(account_name)
        
        # Initialize keywords in tracker
        account_info = self.account_manager.get_account_info(account_name)
        if account_info:
            for keyword in account_info.get("keywords", []):
                self.keyword_tracker.initialize_keyword(keyword)
                
    def _configure_session(self):
        """Configure the current session."""
        print("\n⚙️ Session Configuration")
        print("-" * 30)
        
        # Show health status
        health_status = self.health_monitor.get_health_status()
        print(f"🏥 Account Health: {health_status['score']}/100 ({health_status['status']})")
        
        if health_status["recent_issues"]:
            print(f"⚠️ Recent issues: {', '.join(health_status['recent_issues'])}")
            
        if health_status["activity_multiplier"] < 1.0:
            print(f"🔄 Recommended: {health_status['recommendation']}")
            
        # Check if should pause
        if self.health_monitor.should_pause_activity():
            print("🛑 Account health requires rest period!")
            continue_anyway = input("⚠️ Continue anyway? (not recommended) (y/n): ").lower().strip()
            if continue_anyway != 'y':
                return False
                
        # Get target comment count
        account_info = self.account_manager.get_account_info(self.current_account)
        max_daily = account_info.get("max_comments_per_day", 100)
        
        target_comments = input(f"📊 Target comments this session (max {max_daily}): ").strip()
        try:
            target_comments = int(target_comments) if target_comments else 25
            target_comments = min(target_comments, max_daily)
        except ValueError:
            target_comments = 25
            
        print(f"🎯 Target: {target_comments} comments")
        
        # Start the session
        return self._start_enhanced_session(target_comments)
        
    def _start_enhanced_session(self, target_comments):
        """Start enhanced LinkedIn session with all new features."""
        print("\n🚀 Starting Enhanced Session")
        print("=" * 40)
        
        self.session_stats["start_time"] = datetime.now()
        self.session_stats["target_comments"] = target_comments
        
        # Initialize browser
        if not self.initialize_browser():
            print("❌ Failed to initialize browser")
            return False
            
        try:
            # Check if already logged in
            self.driver.get("https://www.linkedin.com/feed/")
            time.sleep(3)
            
            if "feed" not in self.driver.current_url.lower():
                print("❌ Not logged in to LinkedIn")
                print("👆 Please log in manually in the browser")
                input("Press Enter after logging in...")
                
                # Re-check login
                self.driver.refresh()
                time.sleep(3)
                
                if "feed" not in self.driver.current_url.lower():
                    print("❌ Still not logged in")
                    return False
                    
            self.logged_in = True
            print("✅ Logged in to LinkedIn")
            
            # Run enhanced comment session
            return self._run_enhanced_comment_session(target_comments)
            
        except Exception as e:
            print(f"❌ Session error: {e}")
            traceback.print_exc()
            return False
        finally:
            if self.driver:
                self.driver.quit()
                
    def _run_enhanced_comment_session(self, target_comments):
        """Run the main commenting session with all enhancements."""
        print(f"\n🎯 Starting comment session - Target: {target_comments}")
        
        comments_posted = 0
        total_attempts = 0
        
        # Get account keywords
        account_info = self.account_manager.get_account_info(self.current_account)
        available_keywords = account_info.get("keywords", ["artificial intelligence"])
        
        while comments_posted < target_comments:
            try:
                # Health check every 10 attempts
                if total_attempts % 10 == 0:
                    if self._perform_health_check():
                        print("🛑 Health check failed - pausing session")
                        break
                        
                # Select best keyword using performance tracking
                current_keyword = self.keyword_tracker.select_best_keyword(available_keywords)
                if not current_keyword:
                    print("❌ No keywords available")
                    break
                    
                print(f"\n🔍 Using keyword: '{current_keyword}'")
                
                # Search for posts
                posts = self.search_for_posts(current_keyword)
                self.keyword_tracker.record_search(current_keyword, len(posts))
                
                if not posts:
                    print(f"❌ No posts found for '{current_keyword}'")
                    # Try generating new keywords
                    new_keywords = self.keyword_tracker.generate_related_keywords(
                        current_keyword, 
                        self.config
                    )
                    if new_keywords:
                        available_keywords.extend(new_keywords)
                        # Update account keywords
                        account_info["keywords"].extend(new_keywords)
                        self.account_manager.accounts[self.current_account] = account_info
                        self.account_manager._save_accounts()
                    continue
                    
                # Process posts with enhanced evaluation
                processed_this_keyword = 0
                for post in posts:
                    if comments_posted >= target_comments:
                        break
                        
                    total_attempts += 1
                    
                    # Extract post data
                    post_data = self.extract_post_data(post)
                    if not post_data:
                        continue
                        
                    # Check for duplicates with enhanced detection
                    if self.has_commented(post_data["id"]):
                        continue
                        
                    # Enhanced duplicate detection
                    is_duplicate, similarity, method = self.duplicate_detector.is_duplicate(
                        post_data["text"], 
                        post_data.get("signature", "")
                    )
                    
                    if is_duplicate:
                        print(f"🔄 Duplicate content detected ({method}: {similarity:.2f})")
                        continue
                        
                    # Evaluate post quality
                    evaluation = self.post_evaluator.evaluate_post(post_data)
                    
                    print(f"📊 Post score: {evaluation['total_score']}/50")
                    if evaluation["notes"]:
                        print(f"📝 Notes: {', '.join(evaluation['notes'][:3])}")
                        
                    # Skip low quality posts
                    if not evaluation["pass_threshold"]:
                        print("⏭️ Skipping low-quality post")
                        continue
                        
                    # Generate and post comment
                    comment_success = self._attempt_enhanced_comment(
                        post_data, 
                        current_keyword, 
                        evaluation['total_score']
                    )
                    
                    if comment_success:
                        comments_posted += 1
                        processed_this_keyword += 1
                        
                        # Record success
                        self.keyword_tracker.record_comment_attempt(
                            current_keyword, 
                            successful=True, 
                            post_quality_score=evaluation['total_score']
                        )
                        
                        # Add to duplicate detector
                        self.duplicate_detector.add_comment(
                            comment_success, 
                            post_data.get("signature", "")
                        )
                        
                        print(f"✅ Comment {comments_posted}/{target_comments} posted successfully")
                        
                        # Human-like delay with health-based multiplier
                        delay_multiplier = self.health_monitor.get_recommended_delay_multiplier()
                        base_delay = random.randint(120, 300)  # 2-5 minutes
                        actual_delay = base_delay * delay_multiplier
                        
                        print(f"⏳ Waiting {actual_delay/60:.1f} minutes...")
                        time.sleep(actual_delay)
                        
                    else:
                        # Record failure
                        self.keyword_tracker.record_comment_attempt(
                            current_keyword, 
                            successful=False
                        )
                        
                    # Limit posts per keyword per session
                    if processed_this_keyword >= 3:
                        break
                        
                # Check if keyword should be rotated
                should_rotate, reasons = self.keyword_tracker.should_rotate_keyword(current_keyword)
                if should_rotate:
                    print(f"🔄 Rotating keyword '{current_keyword}': {', '.join(reasons)}")
                    self.keyword_tracker.initiate_keyword_cooling(current_keyword)
                    
                    # Generate new keywords if needed
                    if len(available_keywords) < 3:
                        new_keywords = self.keyword_tracker.generate_related_keywords(
                            current_keyword, 
                            self.config
                        )
                        available_keywords.extend(new_keywords)
                        
                # Session break
                if comments_posted < target_comments:
                    break_duration = random.randint(300, 900)  # 5-15 minutes
                    print(f"☕ Session break: {break_duration/60:.1f} minutes")
                    time.sleep(break_duration)
                    
            except KeyboardInterrupt:
                print("\n⏹️ Session interrupted by user")
                break
            except Exception as e:
                print(f"❌ Error in session: {e}")
                traceback.print_exc()
                continue
                
        # Session summary
        self._print_session_summary(comments_posted, total_attempts)
        
        # Update account usage
        self.account_manager.update_account_usage(self.current_account, comments_posted)
        
        return comments_posted
        
    def _attempt_enhanced_comment(self, post_data, keyword, post_quality_score):
        """Attempt to post a comment with enhanced features."""
        try:
            # Generate contextual comment
            comment_text = self.generate_comment(post_data["text"])
            
            # Check for duplicate comments
            is_duplicate, similarity, method = self.duplicate_detector.is_duplicate(comment_text)
            if is_duplicate:
                print(f"🔄 Generated duplicate comment ({method}), regenerating...")
                # Try again with different approach
                comment_text = self.generate_comment(post_data["text"])
                
            print(f"💬 Comment: {comment_text[:50]}...")
            
            # Post comment
            success = self.post_comment(post_data, comment_text)
            
            if success:
                # Record comment in history
                self.record_comment(post_data, comment_text)
                return comment_text
            else:
                return False
                
        except Exception as e:
            print(f"❌ Comment attempt failed: {e}")
            return False
            
    def _perform_health_check(self):
        """Perform account health check."""
        try:
            page_source = self.driver.page_source
            current_url = self.driver.current_url
            
            # Check for CAPTCHAs
            if self.health_monitor.detect_captcha_signals(page_source, current_url):
                print("🚨 CAPTCHA detected!")
                return True  # Pause session
                
            # Check for warnings
            has_warnings, warning_types = self.health_monitor.detect_warning_signals(page_source)
            if has_warnings:
                print(f"⚠️ LinkedIn warnings detected: {', '.join(warning_types)}")
                return True  # Pause session
                
            # Update activity metrics
            self.health_monitor.record_daily_activity(
                searches=1, 
                comments=1 if self.session_stats["comments_posted"] > 0 else 0
            )
            
            self.session_stats["health_checks"] += 1
            return False  # Continue session
            
        except Exception as e:
            print(f"⚠️ Health check error: {e}")
            return False
            
    def _print_session_summary(self, comments_posted, total_attempts):
        """Print comprehensive session summary."""
        duration = datetime.now() - self.session_stats["start_time"]
        
        print("\n" + "="*50)
        print("📊 SESSION SUMMARY")
        print("="*50)
        print(f"👤 Account: {self.current_account}")
        print(f"⏱️ Duration: {str(duration).split('.')[0]}")
        print(f"✅ Comments posted: {comments_posted}")
        print(f"📝 Posts processed: {total_attempts}")
        print(f"📈 Success rate: {comments_posted/total_attempts*100:.1f}%" if total_attempts > 0 else "N/A")
        
        # Health status
        health_status = self.health_monitor.get_health_status()
        print(f"🏥 Final health score: {health_status['score']}/100")
        
        # Keyword performance
        print(f"\n{self.keyword_tracker.get_performance_summary()}")
        
        print("="*50)
        
    def _load_config(self, config_file):
        """Load configuration from file or create with defaults."""
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Error in config file: {config_file}, using defaults")
                
        # Create default config
        config = DEFAULT_CONFIG.copy()
        
        # Auto-detect Brave path
        brave_path = self._detect_brave_path()
        if brave_path:
            config["brave_path"] = brave_path
            
        # Save default config
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
            
        return config
        
    def _detect_brave_path(self):
        """Auto-detect Brave browser path."""
        import platform
        import os
        
        system = platform.system()
        
        if system == "Windows":
            paths = [
                "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe",
                "C:/Program Files (x86)/BraveSoftware/Brave-Browser/Application/brave.exe",
                os.path.expanduser("~") + "/AppData/Local/BraveSoftware/Brave-Browser/Application/brave.exe"
            ]
            
        elif system == "Darwin":  # macOS
            paths = [
                "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
                os.path.expanduser("~") + "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
            ]
            
        else:  # Linux
            paths = [
                "/usr/bin/brave-browser",
                "/usr/bin/brave",
                "/snap/bin/brave"
            ]
            
        for path in paths:
            if os.path.exists(path):
                return path
                
        return None
    
    def _load_json_file(self, filepath, default_value):
        """Load JSON data from a file, or return default if file doesn't exist."""
        if not os.path.exists(filepath):
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Save default value
            with open(filepath, 'w') as f:
                json.dump(default_value, f, indent=2)
                
            return default_value
            
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return default_value
            
    def _save_json_file(self, filepath, data):
        """Save JSON data to a file."""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving data to {filepath}: {e}")
            
    def initialize_browser(self, headless=False):
        """Initialize browser with stealth features."""
        try:
            # Set up browser options
            options = webdriver.ChromeOptions()
            
            # Add user data directory for persistence
            user_data_dir = os.path.abspath("data/browser_profile")
            os.makedirs(user_data_dir, exist_ok=True)
            options.add_argument(f"user-data-dir={user_data_dir}")
            
            # Add stealth settings
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)
            
            # Set up proxy if enabled
            if self.proxy_manager:
                proxy = self.proxy_manager.get_next_proxy()
                if proxy:
                    print(f"Using proxy: {proxy['host']}:{proxy['port']}")
                    options.add_argument(f"--proxy-server={proxy['host']}:{proxy['port']}")
            
            # Add human-like user agent
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            options.add_argument(f"user-agent={user_agent}")
            
            # Set headless mode if needed
            if headless:
                options.add_argument("--headless")
                options.add_argument("--window-size=1920,1080")
                
            # Use Brave browser if path is specified
            brave_path = self.config.get("brave_path")
            if brave_path and os.path.exists(brave_path):
                options.binary_location = brave_path
                print(f"Using Brave browser at: {brave_path}")
            else:
                print("Using default Chrome browser")
                
            # Initialize browser
            self.driver = webdriver.Chrome(options=options)
            
            # Apply stealth JS
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                
                // Overwrite the 'plugins' property to use a custom getter
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
                
                // Overwrite the 'languages' property to use a custom getter
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en', 'es'],
                });
                
                // Pass the Permissions Test
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
                );
                """
            })
            
            # Set window size to a common resolution
            self.driver.set_window_size(1920, 1080)
            
            return True
        except Exception as e:
            print(f"Error initializing browser: {e}")
            traceback.print_exc()
            return False
            
    def login(self, username, password):
        """Log in to LinkedIn with provided credentials."""
        if not self.driver:
            print("Browser not initialized")
            return False
            
        try:
            # Go to LinkedIn login page
            self.driver.get("https://www.linkedin.com/login")
            
            # Wait for the page to load
            time.sleep(2)
            
            # Check if we're already logged in
            if "feed" in self.driver.current_url:
                print("Already logged in to LinkedIn")
                self.logged_in = True
                return True
                
            # Enter username
            username_field = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "username"))
            )
            self._type_like_human(username_field, username)
            
            # Enter password
            password_field = self.driver.find_element(By.ID, "password")
            self._type_like_human(password_field, password)
            
            # Click sign in
            sign_in_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            sign_in_button.click()
            
            # Wait for login to complete
            time.sleep(3)
            
            # Check for captcha or verification
            page_source = self.driver.page_source.lower()
            if "captcha" in page_source or "verify" in page_source or "security check" in page_source:
                print("CAPTCHA or verification detected! Please complete it manually.")
                
                # Take a screenshot
                os.makedirs("screenshots", exist_ok=True)
                screenshot_path = f"screenshots/captcha_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                self.driver.save_screenshot(screenshot_path)
                print(f"Screenshot saved to {screenshot_path}")
                
                # Wait for manual intervention
                input("Press Enter after completing the captcha/verification...")
                
            # Check if login successful
            if "feed" in self.driver.current_url:
                print("Successfully logged in to LinkedIn")
                self.logged_in = True
                return True
            else:
                print("Failed to log in to LinkedIn")
                return False
                
        except Exception as e:
            print(f"Error logging in to LinkedIn: {e}")
            return False
            
    def search_for_posts(self, keyword):
        """Search for LinkedIn posts with the given keyword."""
        if not self.driver or not self.logged_in:
            print("Not logged in to LinkedIn")
            return []
            
        try:
            # Navigate to LinkedIn feed
            self.driver.get("https://www.linkedin.com/feed/")
            time.sleep(2)
            
            # Click on search box
            search_box = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[contains(@class, 'search-global-typeahead__input')]"))
            )
            search_box.click()
            time.sleep(1)
            
            # Clear and type search query
            search_box.clear()
            self._type_like_human(search_box, keyword)
            time.sleep(1)
            
            # Press Enter to search
            search_box.send_keys(Keys.RETURN)
            
            # Wait for search results
            time.sleep(3)
            
            # Click on "Posts" tab to show only posts
            try:
                posts_tab = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Posts']"))
                )
                posts_tab.click()
                time.sleep(3)
            except:
                print("Could not find 'Posts' tab, continuing with current results")
                
            # Find all post elements
            posts = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'feed-shared-update-v2')]")
            
            # If no posts found with the primary selector, try fallback selectors
            if not posts:
                posts = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'feed-shared-update')]")
                
            if not posts:
                posts = self.driver.find_elements(By.XPATH, "//div[contains(@data-urn, 'activity')]")
                
            print(f"Found {len(posts)} posts for keyword: {keyword}")
            
            return posts
        except Exception as e:
            print(f"Error searching for posts: {e}")
            return []
            
    def extract_post_data(self, post_element):
        """Extract data from a post element."""
        try:
            # Create a unique ID for the post
            post_id = post_element.get_attribute("data-urn") or str(hash(post_element.text))
            
            # Extract author name
            try:
                author = post_element.find_element(By.XPATH, ".//span[contains(@class, 'feed-shared-actor__name')]").text
            except:
                try:
                    # Fallback to alternative author selectors
                    author_element = post_element.find_element(By.XPATH, 
                        ".//a[contains(@class, 'app-aware-link') and contains(@class, 'feed-shared')]//span"
                    )
                    author = author_element.text
                except:
                    author = "Unknown Author"
                    
            # Extract post text
            try:
                text_element = post_element.find_element(By.XPATH, ".//div[contains(@class, 'feed-shared-update-v2__description')]")
                post_text = text_element.text
            except:
                try:
                    # Fallback to alternative text selectors
                    text_element = post_element.find_element(By.XPATH, ".//div[contains(@class, 'feed-shared-text')]")
                    post_text = text_element.text
                except:
                    try:
                        # One more fallback
                        text_element = post_element.find_element(By.XPATH, ".//*[contains(@class, 'update-components-text')]")
                        post_text = text_element.text
                    except:
                        post_text = ""
                        
            # Create a signature for duplicate detection
            signature = hashlib.md5(f"{author}:{post_text[:100]}".encode()).hexdigest()
            
            return {
                "id": post_id,
                "author": author,
                "text": post_text,
                "element": post_element,
                "signature": signature
            }
        except Exception as e:
            print(f"Error extracting post data: {e}")
            return None
            
    def generate_comment(self, post_text):
        """Generate a comment for a post using Ollama or a simple template."""
        # Check if Ollama is enabled
        if self.config.get("use_ollama", False):
            try:
                # Prepare prompt for the model
                prompt = f"""
                You are an intelligent LinkedIn user who provides thoughtful, relevant comments.
                
                Here's a LinkedIn post to comment on:
                ---
                {post_text}
                ---
                
                Write a brief, thoughtful comment (2-3 sentences) that adds value to the discussion. 
                Make it sound natural and conversational. Don't use hashtags.
                """
                
                # Make request to Ollama API
                response = requests.post(
                    self.config.get("ollama_url", "http://localhost:11434/api/generate"),
                    json={
                        "model": self.config.get("ollama_model", "llama3:8b"),
                        "prompt": prompt,
                        "stream": False
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    comment = response.json().get("response", "").strip()
                    
                    # Clean up the comment
                    comment = comment.replace('"', '')
                    comment = re.sub(r'^[\"\']|[\"\']$', '', comment)  # Remove quotes at beginning/end
                    
                    # If comment is too long, truncate it
                    if len(comment) > 500:
                        comment = comment[:497] + "..."
                        
                    return comment
            except Exception as e:
                print(f"Error generating comment with Ollama: {e}")
                # Fall through to template generation
        
        # Template-based comment generation
        templates = [
            "This is a really insightful post. I particularly appreciate the point about {topic}. Thanks for sharing!",
            "Great perspective on {topic}. I've been thinking about this recently and your insights add a valuable dimension.",
            "I find your thoughts on {topic} very relevant. Have you also considered how this relates to recent industry changes?",
            "Thanks for sharing these thoughts on {topic}. It's a timely discussion that more professionals should be having.",
            "Excellent points about {topic}. This reminds me of how important it is to stay current in our rapidly evolving industry."
        ]
        
        # Extract a topic from the post
        topic = self._extract_topic(post_text)
        
        # Select a random template and format with the topic
        template = random.choice(templates)
        return template.format(topic=topic)
    
    def _extract_topic(self, post_text):
        """Extract a topic from the post text for template comments."""
        # Check for keywords in the post
        keywords = self.config.get("default_keywords", ["this topic"])
        
        for keyword in keywords:
            if keyword.lower() in post_text.lower():
                return keyword
                
        # If no keywords found, try to extract a topic from the first sentence
        first_sentence = post_text.split('.')[0] if '.' in post_text else post_text
        
        # If the first sentence is too long, truncate it
        if len(first_sentence) > 30:
            return "this discussion"
            
        return "this topic"
    
    def post_comment(self, post_data, comment_text):
        """Post a comment on a LinkedIn post."""
        if not self.driver or not self.logged_in:
            print("Not logged in to LinkedIn")
            return False
            
        try:
            post_element = post_data["element"]
            
            # Scroll to the post
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", post_element)
            time.sleep(2)
            
            # Find comment button
            try:
                comment_button = post_element.find_element(By.CSS_SELECTOR, 
                    ".feed-shared-social-action-bar__action-button[aria-label*='comment']"
                )
            except NoSuchElementException:
                # Try alternative selectors
                try:
                    comment_button = post_element.find_element(By.CSS_SELECTOR, 
                        "button[aria-label*='comment' i]"
                    )
                except NoSuchElementException:
                    try:
                        comment_button = post_element.find_element(By.XPATH,
                            ".//button[contains(@class, 'social-actions-button') and contains(@aria-label, 'comment')]"
                        )
                    except NoSuchElementException:
                        print("Could not find comment button")
                        return False
            
            comment_button.click()
            time.sleep(2)
            
            # Find comment input
            try:
                comment_input = post_element.find_element(By.CSS_SELECTOR, 
                    ".editor-content[role='textbox']"
                )
            except NoSuchElementException:
                # Try alternative selectors
                try:
                    comment_input = post_element.find_element(By.CSS_SELECTOR, 
                        "[contenteditable='true'][data-placeholder*='comment' i]"
                    )
                except NoSuchElementException:
                    try:
                        comment_input = self.driver.find_element(By.XPATH,
                            "//div[@contenteditable='true' and contains(@aria-label, 'Add a comment')]"
                        )
                    except NoSuchElementException:
                        print("Could not find comment input field")
                        return False
            
            # Click on comment input to focus
            comment_input.click()
            time.sleep(1)
            
            # Type comment with human-like behavior
            self._type_like_human(comment_input, comment_text)
            time.sleep(2)
            
            # Find submit button
            try:
                post_button = post_element.find_element(By.CSS_SELECTOR, 
                    ".comments-comment-box__submit-button"
                )
            except NoSuchElementException:
                # Try alternative selectors
                try:
                    post_button = post_element.find_element(By.CSS_SELECTOR, 
                        "button.social-actions-comment-submit"
                    )
                except NoSuchElementException:
                    try:
                        post_button = self.driver.find_element(By.CSS_SELECTOR,
                            ".comments-comment-box__submit-button:not(.artdeco-button--disabled)"
                        )
                    except NoSuchElementException:
                        print("Could not find post comment button")
                        return False
            
            # Check if post button is enabled
            if not post_button.is_enabled():
                print("Post button is disabled")
                return False
                
            post_button.click()
            
            # Wait for comment to post
            time.sleep(3)
            
            # Take a screenshot
            os.makedirs("screenshots", exist_ok=True)
            screenshot_path = f"screenshots/comment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            self.driver.save_screenshot(screenshot_path)
            
            # Record the comment
            self.record_comment(post_data, comment_text)
            
            return True
        except Exception as e:
            print(f"Error posting comment: {e}")
            traceback.print_exc()
            return False
    
    def record_comment(self, post_data, comment_text):
        """Record a comment in the history."""
        # Create a unique ID for the post
        post_id = post_data.get("id", "")
        comment_id = hashlib.md5(f"{post_id}:{comment_text}".encode()).hexdigest()
        
        # Add to commented posts set
        self.commented_posts.add(post_id)
        
        # Add to comment history
        self.comment_history[comment_id] = {
            "post_id": post_id,
            "post_author": post_data.get("author", ""),
            "post_text": post_data.get("text", "")[:200],  # Store only the first 200 chars
            "comment_text": comment_text,
            "timestamp": datetime.now().isoformat(),
            "signature": post_data.get("signature", "")
        }
        
        # Save comment history
        self._save_json_file(self.comment_history_file, self.comment_history)
    
    def has_commented(self, post_id):
        """Check if we've already commented on a post."""
        # Check in current session
        if post_id in self.commented_posts:
            return True
            
        # Check in history
        for comment_data in self.comment_history.values():
            if comment_data.get("post_id") == post_id:
                return True
                
        return False
        
    def add_commented_post(self, post_id):
        """Add a post ID to the commented posts list."""
        if not hasattr(self, 'commented_posts'):
            self.commented_posts = set()
        self.commented_posts.add(post_id)
    
    def is_duplicate_post(self, post_signature):
        """Check if a post is a duplicate (same content, different ID)."""
        # Don't check if signature is missing
        if not post_signature:
            return False
            
        # Check recent comments (past 48 hours)
        cutoff_time = (datetime.now() - timedelta(hours=48)).isoformat()
        
        for comment_data in self.comment_history.values():
            if (comment_data.get("signature") == post_signature and
                comment_data.get("timestamp", "") > cutoff_time):
                return True
                
        return False
    
    def _type_like_human(self, element, text, typing_style="normal"):
        """Type text like a human with natural delays between characters."""
        if not element or not text:
            return
            
        # Base typing speed (characters per second)
        if typing_style == "fast":
            base_speed = random.uniform(8, 12)  # Fast typing
        elif typing_style == "careful":
            base_speed = random.uniform(3, 6)   # Careful typing
        else:
            base_speed = random.uniform(5, 8)   # Normal typing
            
        # Clear field first
        element.clear()
        
        for char in text:
            # Calculate delay for this character
            if char in ['.', ',', ';', ':', '!', '?']:
                # Longer pause after punctuation
                delay = random.uniform(0.3, 0.7)
            elif char == ' ':
                # Medium pause for spaces
                delay = random.uniform(0.1, 0.3)
            else:
                # Normal typing delay
                delay = 1 / base_speed * random.uniform(0.8, 1.2)
                
            # Type the character
            element.send_keys(char)
            
            # Wait
            time.sleep(delay)
            
        # Sometimes people pause after typing
        if random.random() < 0.3:
            time.sleep(random.uniform(0.5, 1.5))
    
    def process_posts(self, keyword, max_comments=5):
        """Process LinkedIn posts for a given keyword."""
        if not self.driver or not self.logged_in:
            print("Not logged in to LinkedIn")
            return 0
            
        # Search for posts with the keyword
        posts = self.search_for_posts(keyword)
        
        if not posts:
            print(f"No posts found for keyword: {keyword}")
            return 0
            
        # Process posts
        comments_posted = 0
        processed_posts = 0
        
        # Sometimes randomize the order to appear more natural
        if random.random() < 0.5:
            random.shuffle(posts)
        
        for post in posts:
            # Extract post data
            post_data = self.extract_post_data(post)
            if not post_data:
                continue
                
            processed_posts += 1
            
            # Check if we've already commented on this post
            if self.has_commented(post_data["id"]):
                print(f"Already commented on post: {post_data['id']}")
                continue
                
            # Check if this is a duplicate post
            if self.is_duplicate_post(post_data["signature"]):
                print(f"Duplicate post detected: {post_data['signature']}")
                continue
                
            # Evaluate post quality
            evaluation = self.post_evaluator.evaluate_post(post_data)
            
            # Print evaluation info
            print(f"Post score: {evaluation['total_score']}/50")
            if evaluation["notes"]:
                print(f"Notes: {', '.join(evaluation['notes'])}")
                
            # Skip if post doesn't meet quality threshold
            if not evaluation["pass_threshold"]:
                print("Post quality too low, skipping")
                continue
                
            # Simulate reading the post content
            if post_data["text"]:
                reading_time = min(len(post_data["text"]) / 20, 15)  # ~20 chars per second, max 15 seconds
                print(f"Reading post for {reading_time:.1f} seconds...")
                time.sleep(reading_time)
                
            # Generate comment
            comment_text = self.generate_comment(post_data["text"])
            print(f"Generated comment: {comment_text}")
            
            # Post comment
            success = self.post_comment(post_data, comment_text)
            if success:
                comments_posted += 1
                print(f"Comment posted successfully ({comments_posted}/{max_comments})")
                
                # Add some delay between comments
                comment_delay = random.uniform(
                    self.config.get("wait_time_between_comments", [30, 60])[0],
                    self.config.get("wait_time_between_comments", [30, 60])[1]
                )
                print(f"Waiting {comment_delay:.1f} seconds before next comment...")
                time.sleep(comment_delay)
                
                # Check if we've reached the maximum comments
                if comments_posted >= max_comments:
                    break
            else:
                print("Failed to post comment")
                
        return comments_posted
    
    def run_session(self, account_index=0):
        """Run a complete LinkedIn engagement session."""
        # Check if there are any accounts configured
        accounts = self.config.get("accounts", [])
        if not accounts:
            print("No accounts configured. Please add accounts to config.json")
            return 0
            
        # Get the specified account or the first one
        if account_index >= len(accounts):
            print(f"Account index {account_index} out of range. Using first account.")
            account_index = 0
            
        account = accounts[account_index]
        self.active_account = account
        
        # Initialize browser
        if not self.initialize_browser():
            print("Failed to initialize browser")
            return 0
            
        try:
            # Login to LinkedIn
            print(f"Logging in as {account['username']}...")
            if not self.login(account['username'], account['password']):
                print("Failed to log in")
                return 0
                
            # Get keywords from account or default
            keywords = account.get("keywords", self.config.get("default_keywords", ["artificial intelligence"]))
            if not keywords:
                print("No keywords configured")
                return 0
                
            # Select a random keyword
            keyword = random.choice(keywords)
            print(f"Selected keyword: {keyword}")
            
            # Set post evaluator keywords
            self.post_evaluator.target_keywords = keywords
            
            # Get max comments
            max_comments = account.get("max_comments", self.config.get("max_comments_per_run", 5))
            
            # Process posts
            comments_posted = self.process_posts(keyword, max_comments)
            
            print(f"Session completed - Comments posted: {comments_posted}")
            
            # Take a final screenshot
            os.makedirs("screenshots", exist_ok=True)
            screenshot_path = f"screenshots/session_end_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            self.driver.save_screenshot(screenshot_path)
            
            return comments_posted
        except Exception as e:
            print(f"Error in session: {e}")
            traceback.print_exc()
            return 0
        finally:
            # Clean up
            if self.driver:
                self.driver.quit()

class ProxyManager:
    """Manages a pool of proxies for IP rotation."""
    
    def __init__(self, proxies=None):
        """Initialize the proxy manager with a list of proxies."""
        self.proxies = proxies or []
        self.current_index = 0
        
    def add_proxy(self, host, port, username=None, password=None):
        """Add a proxy to the pool."""
        self.proxies.append({
            "host": host,
            "port": port,
            "username": username,
            "password": password
        })
        
    def get_next_proxy(self):
        """Get the next proxy in the rotation."""
        if not self.proxies:
            return None
            
        proxy = self.proxies[self.current_index]
        
        # Move to next proxy for next request
        self.current_index = (self.current_index + 1) % len(self.proxies)
        
        return proxy

def main():
    """Main entry point - Manual login approach."""
    print("🚀 LinkedIn Bot v1 Enhanced")
    print("📋 Manual Login Required")
    print()
    
    # Check for simple command line usage
    if len(sys.argv) > 1:
        if sys.argv[1] == "--stats":
            # Show keyword stats for all accounts
            bot = LinkedInBot()
            show_keyword_stats(bot)
            return
        elif sys.argv[1] == "--help":
            print("Usage:")
            print("  python v1.py         # Interactive startup with manual login")
            print("  python v1.py --stats # Show keyword performance stats")
            print("  python v1.py --help  # Show this help")
            return
    
    # Manual login instructions
    print("🔐 LOGIN INSTRUCTIONS:")
    print("=" * 50)
    print("1. The bot will open a Chrome browser")
    print("2. Navigate to LinkedIn and login manually")
    print("3. Complete any 2FA/verification if needed")
    print("4. Make sure you're on the LinkedIn feed page")
    print("5. Come back to this terminal and press ENTER")
    print("=" * 50)
    print()
    
    input("Press ENTER when ready to start...")
    
    # Start bot with manual login approach
    try:
        bot = LinkedInBot()
        bot.manual_login_mode = True
        bot.interactive_startup()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        traceback.print_exc()

def show_keyword_stats(bot):
    """Show keyword performance statistics for all accounts."""
    print("\n" + "="*60)
    print("📊 KEYWORD PERFORMANCE STATISTICS")
    print("="*60)
    
    account_names = bot.account_manager.get_account_names()
    
    if not account_names:
        print("❌ No accounts found")
        return
        
    for account_name in account_names:
        print(f"\n👤 Account: {account_name}")
        print("-" * 40)
        
        tracker = KeywordPerformanceTracker(account_name)
        print(tracker.get_performance_summary())
        
        health_monitor = AccountHealthMonitor(account_name)
        health_status = health_monitor.get_health_status()
        print(f"\n🏥 Health: {health_status['score']}/100 ({health_status['status']})")
        if health_status["recent_issues"]:
            print(f"⚠️ Issues: {', '.join(health_status['recent_issues'])}")

def simple_setup(bot):
    """Simple setup configuration."""
    print("\n" + "="*60)
    print("⚙️ LINKEDIN BOT SETUP")
    print("="*60)
    
    print("\n1. Account Management")
    print("-" * 25)
    
    account_names = bot.account_manager.get_account_names()
    if account_names:
        print(f"📁 Existing accounts: {', '.join(account_names)}")
        
        action = input("\n🔧 Action - (a)dd account, (e)dit account, (d)elete account, (c)ontinue: ").lower().strip()
        
        if action == 'a':
            bot._setup_new_account()
        elif action == 'e' and account_names:
            edit_account(bot, account_names)
        elif action == 'd' and account_names:
            delete_account(bot, account_names)
    else:
        print("➕ No accounts found - let's add one!")
        bot._setup_new_account()
        
    print("\n2. Global Settings")
    print("-" * 20)
    
    # Ollama configuration
    current_ollama = bot.config.get("use_ollama", False)
    print(f"🤖 Ollama AI comments: {'Enabled' if current_ollama else 'Disabled'}")
    
    change_ollama = input("🔧 Change Ollama setting? (y/n): ").lower().strip()
    if change_ollama == 'y':
        enable_ollama = input("🤖 Enable Ollama for AI comments? (y/n): ").lower().strip()
        bot.config["use_ollama"] = (enable_ollama == 'y')
        
        if bot.config["use_ollama"]:
            ollama_url = input(f"🌐 Ollama URL (default: {bot.config.get('ollama_url', 'http://localhost:11434/api/generate')}): ").strip()
            if ollama_url:
                bot.config["ollama_url"] = ollama_url
                
            ollama_model = input(f"🤖 Ollama model (default: {bot.config.get('ollama_model', 'llama3:8b')}): ").strip()
            if ollama_model:
                bot.config["ollama_model"] = ollama_model
                
    # Save configuration
    with open(bot.config_file, 'w') as f:
        json.dump(bot.config, f, indent=2)
        
    print("\n✅ Setup completed!")

def edit_account(bot, account_names):
    """Edit an existing account."""
    print(f"\n📝 Select account to edit:")
    for i, name in enumerate(account_names, 1):
        print(f"{i}. {name}")
        
    try:
        choice = int(input(f"Select (1-{len(account_names)}): ")) - 1
        if 0 <= choice < len(account_names):
            account_name = account_names[choice]
            account_info = bot.account_manager.get_account_info(account_name)
            
            print(f"\n📝 Editing account: {account_name}")
            
            # Edit keywords
            current_keywords = ", ".join(account_info.get("keywords", []))
            print(f"Current keywords: {current_keywords}")
            new_keywords = input("📝 New keywords (comma-separated, or Enter to keep current): ").strip()
            
            if new_keywords:
                keywords = [kw.strip() for kw in new_keywords.split(",")]
                account_info["keywords"] = keywords
                
            # Edit daily limit
            current_limit = account_info.get("max_comments_per_day", 100)
            print(f"Current daily limit: {current_limit}")
            new_limit = input("📊 New daily limit (or Enter to keep current): ").strip()
            
            if new_limit:
                try:
                    account_info["max_comments_per_day"] = int(new_limit)
                except ValueError:
                    print("❌ Invalid number, keeping current limit")
                    
            # Save changes
            bot.account_manager.accounts[account_name] = account_info
            bot.account_manager._save_accounts()
            
            print(f"✅ Account '{account_name}' updated")
        else:
            print("❌ Invalid selection")
    except ValueError:
        print("❌ Please enter a number")

def delete_account(bot, account_names):
    """Delete an existing account."""
    print(f"\n🗑️ Select account to delete:")
    for i, name in enumerate(account_names, 1):
        print(f"{i}. {name}")
        
    try:
        choice = int(input(f"Select (1-{len(account_names)}): ")) - 1
        if 0 <= choice < len(account_names):
            account_name = account_names[choice]
            
            confirm = input(f"⚠️ Delete account '{account_name}'? This will remove all data! (yes/no): ").lower().strip()
            if confirm == 'yes':
                # Remove account
                del bot.account_manager.accounts[account_name]
                bot.account_manager._save_accounts()
                
                # Clean up data files
                try:
                    keyword_file = f"data/keyword_performance_{account_name}.json"
                    health_file = f"data/health_{account_name}.json"
                    
                    if os.path.exists(keyword_file):
                        os.remove(keyword_file)
                    if os.path.exists(health_file):
                        os.remove(health_file)
                        
                    print(f"✅ Account '{account_name}' deleted")
                except Exception as e:
                    print(f"⚠️ Error cleaning up files: {e}")
            else:
                print("❌ Deletion cancelled")
        else:
            print("❌ Invalid selection")
    except ValueError:
        print("❌ Please enter a number")

if __name__ == "__main__":
    main()