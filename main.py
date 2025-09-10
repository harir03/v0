#!/usr/bin/env python3
import os
import time
import random
import json
import logging
import hashlib
import re
import string
import math
import sqlite3
import base64
import traceback
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Union, Optional, Any
from collections import defaultdict

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, 
    StaleElementReferenceException, WebDriverException
)

try:
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False
    print("NLTK not available. Simple text comparison will be used for duplicate detection.")
    
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("Scikit-learn not available. Simple text comparison will be used for duplicate detection.")

try:
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("Cryptography package not available. Encryption features will be disabled.")

#################################################
# LinkedIn UI Selectors
#################################################

class LinkedInSelectors:
    """
    Updated and comprehensive LinkedIn UI selectors with fallback options
    based on recent LinkedIn interface changes.
    """
    
    # Comment section selectors
    COMMENT_BUTTON_SELECTORS = [
        ".feed-shared-social-action-bar__action-button[aria-label*='comment']",
        ".feed-shared-social-action-bar__action-button[aria-label*='Comment']",
        "button[data-control-name='comment']",
        ".artdeco-button[data-control-name='comment']",
        "button[aria-label*='comment' i]",  # Case insensitive
        ".comments-comment-box__block",  # Area around the comment box
        ".feed-shared-update-v2__social-actions-comment", # Newest LinkedIn selector (2025)
        "//button[contains(@class, 'social-actions-button') and contains(@aria-label, 'comment')]" # XPath fallback
    ]
    
    # Comment input field selectors
    COMMENT_INPUT_SELECTORS = [
        ".editor-content[role='textbox']",
        ".ql-editor[data-placeholder='Add a comment…']",
        ".comments-comment-box__content-editor",
        ".comments-comment-texteditor__content", 
        "[contenteditable='true'][data-placeholder*='comment' i]",
        "div[role='textbox'][aria-label*='comment' i]",
        "div[contenteditable='true'][aria-label*='Add a comment']",  # Latest LinkedIn selector (2025)
        "//div[@contenteditable='true' and contains(@aria-label, 'Add a comment')]" # XPath fallback
    ]
    
    # Comment post button selectors
    COMMENT_POST_BUTTON_SELECTORS = [
        ".comments-comment-box__submit-button",
        "button.comments-comment-box__submit-button",
        "button[data-control-name='post_comment']",
        ".artdeco-button--primary[type='submit']",
        ".comments-comment-box__submit-button:not(.artdeco-button--disabled)",
        "button.social-actions-comment-submit",  # Latest LinkedIn selector (2025)
        "//button[contains(@class, 'comments-comment-box__submit-button') or contains(@class, 'social-actions-comment-submit')]" # XPath fallback
    ]
    
    # Selectors for finding existing comments
    EXISTING_COMMENTS_SELECTORS = [
        ".comments-comments-list",
        ".comments-comments-list__comment-item",
        ".comments-comment-item",
        ".feed-shared-comment",
        ".feed-shared-comment-list__comment",  # Newest LinkedIn selector (2025)
        "//div[contains(@class, 'comments-comment-item') or contains(@class, 'feed-shared-comment')]"  # XPath fallback
    ]
    
    # Selector for comment text within existing comments
    COMMENT_TEXT_SELECTORS = [
        ".comments-comment-item-content-body",
        ".comments-comment-item__main-content",
        ".feed-shared-comment__content-body",
        ".feed-shared-text",
        ".feed-shared-comment-text",  # Latest LinkedIn selector (2025)
        "//div[contains(@class, 'comments-comment-item__main-content') or contains(@class, 'feed-shared-comment-text')]" # XPath fallback
    ]
    
    # Delete comment button selectors
    COMMENT_DELETE_BUTTON_SELECTORS = [
        ".comments-comment-item__delete-button",
        ".feed-shared-comment-actions__action-button[aria-label*='Delete']",
        ".artdeco-dropdown__item[aria-label*='Delete']",
        ".feed-shared-comment-menu-item--delete",  # Latest LinkedIn selector (2025)
        "//button[contains(@aria-label, 'Delete this comment')]",
        "//li[contains(@class, 'feed-shared-comment-menu-item--delete')]",  # XPath fallback
        "//span[text()='Delete']//ancestor::button"  # Text-based XPath fallback
    ]
    
    # Comment options menu selectors (to access delete option)
    COMMENT_OPTIONS_MENU_SELECTORS = [
        ".feed-shared-comment-actions__action-button[aria-label*='More actions']",
        ".artdeco-dropdown__trigger.artdeco-dropdown__trigger--placement-bottom",
        ".feed-shared-control-menu__trigger",
        ".comment-options-trigger",  # Latest LinkedIn selector (2025)
        "//button[contains(@aria-label, 'More actions')]",
        "//button[contains(@class, 'feed-shared-control-menu__trigger')]"  # XPath fallback
    ]
    
    # Confirm delete dialog button selectors
    CONFIRM_DELETE_BUTTON_SELECTORS = [
        ".artdeco-modal__confirm-dialog-btn[data-test-dialog-primary-btn]",
        ".artdeco-modal__confirm-dialog-btn--primary",
        ".artdeco-button--primary.artdeco-button--2",
        "//button[text()='Delete']",
        "//button[contains(@class, 'artdeco-button--primary') and contains(text(), 'Delete')]"  # XPath fallback
    ]
    
    @classmethod
    def find_element_with_fallbacks(cls, driver, selector_list, by_type="css"):
        """
        Try multiple selectors until one works.
        
        Args:
            driver: WebDriver instance
            selector_list: List of selectors to try
            by_type: Type of selector ('css' or 'xpath')
            
        Returns:
            WebElement if found, None otherwise
        """
        for selector in selector_list:
            try:
                if selector.startswith("//") or by_type == "xpath":
                    return driver.find_element(By.XPATH, selector)
                else:
                    return driver.find_element(By.CSS_SELECTOR, selector)
            except NoSuchElementException:
                continue
        
        return None
        
    @classmethod
    def find_elements_with_fallbacks(cls, driver, selector_list, by_type="css"):
        """
        Try multiple selectors until one returns elements.
        
        Args:
            driver: WebDriver instance
            selector_list: List of selectors to try
            by_type: Type of selector ('css' or 'xpath')
            
        Returns:
            List of WebElements if found, empty list otherwise
        """
        for selector in selector_list:
            try:
                if selector.startswith("//") or by_type == "xpath":
                    elements = driver.find_elements(By.XPATH, selector)
                else:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    
                if elements:
                    return elements
            except:
                continue
        
        return []

#################################################
# Comment History
#################################################

class CommentHistory:
    """
    Tracks comment history for a LinkedIn account, preventing duplicate
    comments and maintaining a searchable comment database.
    """
    
    def __init__(self, account_name, encryption_key=None, storage_dir="comment_history", retention_days=90):
        """
        Initialize comment history tracker.
        
        Args:
            account_name (str): Name of the account
            encryption_key (str): Optional encryption key for sensitive data
            storage_dir (str): Directory to store comment history
            retention_days (int): Days to retain comment history
        """
        self.account_name = account_name
        self.encryption_key = encryption_key
        self.storage_dir = storage_dir
        self.retention_days = retention_days
        self.comments = {}
        self.encrypter = None
        
        # Set up encryption if key provided and cryptography available
        if encryption_key and CRYPTO_AVAILABLE:
            # Generate a consistent key from the provided encryption key
            key_hash = hashlib.sha256(encryption_key.encode()).digest()[:32]
            self.encrypter = Fernet(base64.urlsafe_b64encode(key_hash))
        
        # Create storage directory
        os.makedirs(storage_dir, exist_ok=True)
        
        # Load comment history
        self.load_comments()
        
        # Clean up old comments
        self.cleanup_old_comments()
        
    def load_comments(self):
        """Load comment history from file."""
        filepath = os.path.join(self.storage_dir, f"{self.account_name}_comments.json")
        
        if not os.path.exists(filepath):
            self.comments = {}
            return
            
        try:
            with open(filepath, 'r') as f:
                encrypted_data = f.read()
                
            if self.encrypter and encrypted_data:
                # Decrypt the data if encryption is enabled
                try:
                    decrypted_data = self.encrypter.decrypt(encrypted_data.encode())
                    self.comments = json.loads(decrypted_data)
                except Exception as e:
                    print(f"Error decrypting comment history: {e}")
                    self.comments = {}
            else:
                # Load unencrypted data
                self.comments = json.loads(encrypted_data)
                
        except Exception as e:
            print(f"Error loading comment history: {e}")
            self.comments = {}
            
    def save_comments(self):
        """Save comment history to file."""
        filepath = os.path.join(self.storage_dir, f"{self.account_name}_comments.json")
        
        try:
            data = json.dumps(self.comments)
            
            if self.encrypter:
                # Encrypt the data if encryption is enabled
                encrypted_data = self.encrypter.encrypt(data.encode()).decode()
                with open(filepath, 'w') as f:
                    f.write(encrypted_data)
            else:
                # Save unencrypted data
                with open(filepath, 'w') as f:
                    f.write(data)
                    
        except Exception as e:
            print(f"Error saving comment history: {e}")
            
    def record_comment(self, post_data, comment_text):
        """
        Record a comment in the history.
        
        Args:
            post_data (dict): Post data including ID, author, etc.
            comment_text (str): Text of the comment
        """
        post_id = post_data.get("id", str(hash(post_data.get("text", ""))))
        comment_id = hashlib.md5(f"{post_id}:{comment_text}".encode()).hexdigest()
        
        self.comments[comment_id] = {
            "post_id": post_id,
            "post_author": post_data.get("author", ""),
            "post_text": post_data.get("text", ""),
            "comment_text": comment_text,
            "timestamp": datetime.now().isoformat(),
            "signature": post_data.get("signature", "")
        }
        
        self.save_comments()
        
    def has_commented(self, post_id):
        """
        Check if we've already commented on a post.
        
        Args:
            post_id (str): ID of the post
            
        Returns:
            bool: Whether we've commented on this post
        """
        for comment_data in self.comments.values():
            if comment_data.get("post_id") == post_id:
                return True
                
        return False
        
    def is_duplicate_post(self, post_signature):
        """
        Check if a post is a duplicate (same content, different ID).
        
        Args:
            post_signature (str): Signature of the post
            
        Returns:
            bool: Whether this post is a duplicate
        """
        if not post_signature:
            return False
            
        # Check recent comments (past 48 hours)
        cutoff_time = datetime.now() - timedelta(hours=48)
        
        for comment_data in self.comments.values():
            if (comment_data.get("signature") == post_signature and
                datetime.fromisoformat(comment_data.get("timestamp")) > cutoff_time):
                return True
                
        return False
        
    def is_duplicate_comment(self, comment_text, duplicate_detector=None, similarity_threshold=0.75):
        """
        Check if this comment is too similar to recent comments.
        Uses enhanced duplicate detector if provided, otherwise falls back to basic comparison.
        
        Args:
            comment_text (str): The comment to check
            duplicate_detector: Optional EnhancedDuplicateDetector instance
            similarity_threshold (float): Threshold for considering a comment duplicate (0-1)
            
        Returns:
            bool: True if the comment is too similar to recent comments
        """
        # Get comments from the past 24 hours
        recent_time = datetime.now() - timedelta(hours=24)
        recent_comments = [
            c["comment_text"] for c in self.comments.values()
            if datetime.fromisoformat(c["timestamp"]) > recent_time
        ]
        
        # Use enhanced duplicate detector if provided
        if duplicate_detector:
            for existing in recent_comments:
                is_duplicate, score, _ = duplicate_detector.is_duplicate(comment_text, existing)
                if is_duplicate:
                    return True
            return False
            
        # Otherwise use the original simple similarity check
        normalized_text = comment_text.lower().strip()
        
        for existing in recent_comments:
            existing_norm = existing.lower().strip()
            
            # Skip very short comments
            if len(normalized_text) < 10 or len(existing_norm) < 10:
                continue
                
            # Calculate Jaccard similarity between character sets
            set1 = set(normalized_text)
            set2 = set(existing_norm)
            
            intersection = len(set1.intersection(set2))
            union = len(set1.union(set2))
            
            # Calculate similarity ratio
            similarity = intersection / union if union > 0 else 0
            
            # Calculate sequence similarity (for word order)
            seq_similarity = self._sequence_similarity(normalized_text, existing_norm)
            
            # Combined similarity
            combined = (similarity + seq_similarity) / 2
            
            if combined > similarity_threshold:
                return True
                
        return False
        
    def _sequence_similarity(self, text1, text2):
        """
        Calculate similarity based on sequence of words.
        
        Args:
            text1 (str): First text
            text2 (str): Second text
            
        Returns:
            float: Sequence similarity score (0-1)
        """
        words1 = text1.split()
        words2 = text2.split()
        
        # Handle empty inputs
        if not words1 or not words2:
            return 0
            
        # Count common bigrams
        bigrams1 = set(zip(words1, words1[1:]))
        bigrams2 = set(zip(words2, words2[1:]))
        
        intersection = len(bigrams1.intersection(bigrams2))
        union = len(bigrams1.union(bigrams2))
        
        return intersection / union if union > 0 else 0
        
    def cleanup_old_comments(self):
        """Remove comments older than retention_days."""
        if not self.comments:
            return
            
        cutoff_time = datetime.now() - timedelta(days=self.retention_days)
        updated_comments = {}
        
        for comment_id, comment_data in self.comments.items():
            try:
                timestamp = datetime.fromisoformat(comment_data.get("timestamp"))
                if timestamp > cutoff_time:
                    updated_comments[comment_id] = comment_data
            except (ValueError, TypeError):
                # Keep comments with invalid timestamps for now
                updated_comments[comment_id] = comment_data
                
        self.comments = updated_comments
        self.save_comments()
        
    def get_recent_comments(self, hours=24):
        """
        Get recent comments.
        
        Args:
            hours (int): Hours to look back
            
        Returns:
            list: Recent comment data
        """
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent = []
        
        for comment_data in self.comments.values():
            try:
                timestamp = datetime.fromisoformat(comment_data.get("timestamp"))
                if timestamp > cutoff_time:
                    recent.append(comment_data)
            except (ValueError, TypeError):
                continue
                
        # Sort by timestamp, newest first
        recent.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return recent

#################################################
# Account Interests
#################################################

class AccountInterests:
    """
    Tracks and manages the interests of a LinkedIn account
    to personalize engagement with relevant content.
    """
    
    def __init__(self, account_name, storage_dir="data"):
        """
        Initialize account interests tracker.
        
        Args:
            account_name (str): Name of the account
            storage_dir (str): Directory to store interest data
        """
        self.account_name = account_name
        self.storage_dir = storage_dir
        self.storage_file = os.path.join(storage_dir, f"{account_name}_interests.json")
        
        # Interest data structure
        self.interests = {
            "topics": {},       # Topic interest scores
            "authors": {},      # Author interest scores
            "keywords": {},     # Keyword interest scores
            "interactions": []  # Recent interactions
        }
        
        # Create directory if it doesn't exist
        os.makedirs(storage_dir, exist_ok=True)
        
        # Load existing interests
        self.load_interests()
        
    def load_interests(self):
        """Load interest data from file."""
        if not os.path.exists(self.storage_file):
            return
            
        try:
            with open(self.storage_file, 'r') as f:
                self.interests = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # Keep default interests if file is invalid
            pass
            
    def save_interests(self):
        """Save interest data to file."""
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(self.interests, f, indent=2)
        except Exception as e:
            print(f"Error saving interests: {e}")
            
    def record_interaction(self, post_data):
        """
        Record an interaction with a post to update interests.
        
        Args:
            post_data (dict): Post data including text, author, etc.
        """
        # Extract data from post
        post_text = post_data.get("text", "")
        author = post_data.get("author", "")
        
        # Skip if no text
        if not post_text:
            return
            
        # Update author interest
        if author:
            self.interests["authors"][author] = self.interests["authors"].get(author, 0) + 1
            
        # Extract topics and keywords from post
        topics = self._extract_topics(post_text)
        keywords = self._extract_keywords(post_text)
        
        # Update topic interests
        for topic in topics:
            self.interests["topics"][topic] = self.interests["topics"].get(topic, 0) + 1
            
        # Update keyword interests
        for keyword in keywords:
            self.interests["keywords"][keyword] = self.interests["keywords"].get(keyword, 0) + 1
            
        # Add to recent interactions
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "author": author,
            "topics": topics,
            "keywords": keywords
        }
        
        self.interests["interactions"].append(interaction)
        
        # Limit interactions history to 100 most recent
        if len(self.interests["interactions"]) > 100:
            self.interests["interactions"] = self.interests["interactions"][-100:]
            
        # Save updated interests
        self.save_interests()
        
    def _extract_topics(self, text):
        """
        Extract topics from text.
        
        Args:
            text (str): Text to extract topics from
            
        Returns:
            list: Extracted topics
        """
        # Common LinkedIn content topics
        common_topics = [
            "artificial intelligence", "machine learning", "data science",
            "leadership", "management", "career development", "networking",
            "marketing", "sales", "entrepreneurship", "startups",
            "technology", "software development", "web development",
            "digital marketing", "social media", "content marketing",
            "business strategy", "finance", "investment", "cryptocurrency",
            "blockchain", "innovation", "remote work", "workplace culture",
            "personal development", "productivity", "mindfulness",
            "mental health", "work-life balance", "diversity", "inclusion",
            "sustainability", "climate change", "education", "e-learning"
        ]
        
        # Extract topics mentioned in the text
        found_topics = []
        lower_text = text.lower()
        
        for topic in common_topics:
            if topic in lower_text:
                found_topics.append(topic)
                
        return found_topics
        
    def _extract_keywords(self, text):
        """
        Extract keywords from text.
        
        Args:
            text (str): Text to extract keywords from
            
        Returns:
            list: Extracted keywords
        """
        # Simple keyword extraction
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        
        # Count word frequency
        word_counts = {}
        for word in words:
            if word not in self.get_stopwords():
                word_counts[word] = word_counts.get(word, 0) + 1
                
        # Get most frequent words
        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Return top keywords
        return [word for word, count in sorted_words[:10]]
        
    def get_stopwords(self):
        """Get English stopwords."""
        # Common English stopwords
        return {
            "the", "and", "that", "have", "for", "not", "with", "you", "this",
            "but", "his", "from", "they", "will", "would", "there", "their",
            "what", "about", "which", "when", "make", "like", "time", "just",
            "know", "take", "into", "year", "your", "good", "some", "could",
            "them", "than", "then", "look", "only", "come", "over", "think",
            "also", "back", "after", "work", "first", "well", "even", "want",
            "because", "these", "give", "most"
        }
        
    def get_top_interests(self, category="topics", limit=5):
        """
        Get top interests in a category.
        
        Args:
            category (str): Category to get interests from ('topics', 'authors', or 'keywords')
            limit (int): Maximum number of interests to return
            
        Returns:
            list: Top interests in the category
        """
        if category not in self.interests:
            return []
            
        # Sort by score (descending)
        sorted_interests = sorted(
            self.interests[category].items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        # Return top interests
        return [item[0] for item in sorted_interests[:limit]]
        
    def calculate_interest_score(self, text):
        """
        Calculate how interesting a text is based on account interests.
        
        Args:
            text (str): Text to evaluate
            
        Returns:
            float: Interest score (0-10)
        """
        if not text:
            return 0
            
        score = 0
        lower_text = text.lower()
        
        # Check for topics of interest
        topics = self._extract_topics(text)
        topic_score = 0
        
        for topic in topics:
            if topic in self.interests["topics"]:
                topic_score += min(self.interests["topics"][topic], 5)
                
        score += min(topic_score, 5)  # Cap at 5 points
        
        # Check for keywords of interest
        keywords = self._extract_keywords(text)
        keyword_score = 0
        
        for keyword in keywords:
            if keyword in self.interests["keywords"]:
                keyword_score += min(self.interests["keywords"][keyword], 3)
                
        score += min(keyword_score, 3)  # Cap at 3 points
        
        # Check for recent interaction topics
        recent_topics = set()
        for interaction in self.interests["interactions"][-10:]:  # Last 10 interactions
            recent_topics.update(interaction.get("topics", []))
            
        for topic in recent_topics:
            if topic in lower_text:
                score += 0.5  # Small boost for recently interacted topics
                
        return min(score, 10)  # Cap at 10
        
    def is_author_of_interest(self, author_name):
        """
        Check if an author is of interest.
        
        Args:
            author_name (str): Author name to check
            
        Returns:
            bool: Whether the author is of interest
        """
        if not author_name:
            return False
            
        return author_name in self.interests["authors"]

#################################################
# Health Monitor
#################################################

class AccountHealthMonitor:
    """
    Monitors the health of a LinkedIn account by tracking activity patterns,
    captchas, warnings, and other signals that may indicate risk.
    """
    
    def __init__(self, account_name, storage_dir="health_data"):
        """
        Initialize the account health monitor.
        
        Args:
            account_name (str): Name of the account to monitor
            storage_dir (str): Directory to store health data
        """
        self.account_name = account_name
        self.storage_dir = storage_dir
        
        # Create directories
        os.makedirs(storage_dir, exist_ok=True)
        
        # Define storage files
        self.activity_file = os.path.join(storage_dir, f"{account_name}_activity.json")
        self.captchas_file = os.path.join(storage_dir, f"{account_name}_captchas.json")
        self.warnings_file = os.path.join(storage_dir, f"{account_name}_warnings.json")
        
        # Load health data
        self.activity_data = self._load_json_file(self.activity_file, {"searches": {}, "comments": {}, "posts": {}})
        self.captchas_data = self._load_json_file(self.captchas_file, [])
        self.warnings_data = self._load_json_file(self.warnings_file, [])
        
    def _load_json_file(self, filepath, default_value):
        """
        Load JSON data from a file, or return default if file doesn't exist.
        
        Args:
            filepath (str): Path to the JSON file
            default_value: Default value if file doesn't exist
            
        Returns:
            object: Loaded JSON data or default value
        """
        if not os.path.exists(filepath):
            return default_value
            
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return default_value
            
    def _save_json_file(self, filepath, data):
        """
        Save JSON data to a file.
        
        Args:
            filepath (str): Path to the JSON file
            data: Data to save
        """
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving health data: {e}")
            
    def record_activity(self, activity_type):
        """
        Record an activity event.
        
        Args:
            activity_type (str): Type of activity ('searches', 'comments', or 'posts')
        """
        if activity_type not in ["searches", "comments", "posts"]:
            return
            
        # Get today's date as string
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Initialize today's counter if it doesn't exist
        if today not in self.activity_data[activity_type]:
            self.activity_data[activity_type][today] = 0
            
        # Increment counter
        self.activity_data[activity_type][today] += 1
        
        # Save activity data
        self._save_json_file(self.activity_file, self.activity_data)
        
    def record_captcha_event(self, url, resolved=False, resolution_time=None):
        """
        Record a captcha event.
        
        Args:
            url (str): URL where captcha was encountered
            resolved (bool): Whether captcha was resolved
            resolution_time (int): Time taken to resolve in seconds
        """
        captcha_event = {
            "timestamp": datetime.now().isoformat(),
            "url": url,
            "resolved": resolved,
            "resolution_time": resolution_time
        }
        
        self.captchas_data.append(captcha_event)
        self._save_json_file(self.captchas_file, self.captchas_data)
        
    def record_warning_event(self, warning_type, description, screenshot_path=None):
        """
        Record a warning event.
        
        Args:
            warning_type (str): Type of warning
            description (str): Description of the warning
            screenshot_path (str): Path to screenshot of the warning
        """
        warning_event = {
            "timestamp": datetime.now().isoformat(),
            "type": warning_type,
            "description": description,
            "screenshot_path": screenshot_path
        }
        
        self.warnings_data.append(warning_event)
        self._save_json_file(self.warnings_file, self.warnings_data)
        
    def get_daily_activity_counts(self, days=7):
        """
        Get daily activity counts for the past n days.
        
        Args:
            days (int): Number of days to look back
            
        Returns:
            dict: Daily activity counts
        """
        # Calculate start date
        start_date = datetime.now() - timedelta(days=days)
        
        # Generate date strings for the past n days
        date_range = []
        current_date = start_date
        while current_date <= datetime.now():
            date_range.append(current_date.strftime("%Y-%m-%d"))
            current_date += timedelta(days=1)
            
        # Collect activity counts
        result = {
            "searches": {},
            "comments": {},
            "posts": {}
        }
        
        for activity_type in ["searches", "comments", "posts"]:
            for date_str in date_range:
                result[activity_type][date_str] = self.activity_data[activity_type].get(date_str, 0)
                
        return result
        
    def get_captcha_frequency(self, days=30):
        """
        Calculate captcha frequency over the past n days.
        
        Args:
            days (int): Number of days to look back
            
        Returns:
            float: Average captchas per day
        """
        # Calculate start time
        start_time = datetime.now() - timedelta(days=days)
        
        # Count captchas in time range
        captcha_count = 0
        
        for event in self.captchas_data:
            try:
                event_time = datetime.fromisoformat(event["timestamp"])
                if event_time >= start_time:
                    captcha_count += 1
            except (ValueError, KeyError):
                continue
                
        # Calculate average per day
        return captcha_count / days
        
    def get_warning_count(self, days=90):
        """
        Get warning count over the past n days.
        
        Args:
            days (int): Number of days to look back
            
        Returns:
            int: Number of warnings
        """
        # Calculate start time
        start_time = datetime.now() - timedelta(days=days)
        
        # Count warnings in time range
        warning_count = 0
        
        for event in self.warnings_data:
            try:
                event_time = datetime.fromisoformat(event["timestamp"])
                if event_time >= start_time:
                    warning_count += 1
            except (ValueError, KeyError):
                continue
                
        return warning_count
        
    def calculate_activity_safety(self):
        """
        Calculate activity safety score (0-100).
        
        Returns:
            int: Safety score (0-100)
        """
        # Get daily activity
        daily_activity = self.get_daily_activity_counts(days=7)
        
        # Calculate average daily activity
        avg_searches = sum(daily_activity["searches"].values()) / 7
        avg_comments = sum(daily_activity["comments"].values()) / 7
        
        # Calculate safety score based on activity levels
        safety_score = 100
        
        # Reduce score if average searches are too high
        if avg_searches > 15:
            safety_score -= min(30, (avg_searches - 15) * 3)
            
        # Reduce score if average comments are too high
        if avg_comments > 10:
            safety_score -= min(30, (avg_comments - 10) * 5)
            
        # Reduce score for captcha frequency
        captcha_freq = self.get_captcha_frequency(days=30)
        if captcha_freq > 0:
            safety_score -= min(40, captcha_freq * 20)
            
        # Reduce score for recent warnings
        warning_count = self.get_warning_count(days=30)
        if warning_count > 0:
            safety_score -= min(50, warning_count * 25)
            
        return max(0, int(safety_score))
        
    def get_health_summary(self):
        """
        Get a summary of account health.
        
        Returns:
            dict: Health summary
        """
        # Calculate health score
        health_score = self.calculate_activity_safety()
        
        # Get activity trends
        daily_activity = self.get_daily_activity_counts(days=7)
        
        # Get today's activity
        today = datetime.now().strftime("%Y-%m-%d")
        today_searches = daily_activity["searches"].get(today, 0)
        today_comments = daily_activity["comments"].get(today, 0)
        
        # Get recent captchas (past 7 days)
        recent_captchas = []
        start_time = datetime.now() - timedelta(days=7)
        
        for event in self.captchas_data:
            try:
                event_time = datetime.fromisoformat(event["timestamp"])
                if event_time >= start_time:
                    recent_captchas.append(event)
            except (ValueError, KeyError):
                continue
                
        # Get recent warnings (past 30 days)
        recent_warnings = []
        start_time = datetime.now() - timedelta(days=30)
        
        for event in self.warnings_data:
            try:
                event_time = datetime.fromisoformat(event["timestamp"])
                if event_time >= start_time:
                    recent_warnings.append(event)
            except (ValueError, KeyError):
                continue
                
        # Determine risk level
        if health_score >= 80:
            risk_level = "low"
        elif health_score >= 50:
            risk_level = "moderate"
        else:
            risk_level = "high"
            
        # Generate summary
        return {
            "health_score": health_score,
            "risk_level": risk_level,
            "today_activity": {
                "searches": today_searches,
                "comments": today_comments
            },
            "recent_captchas": len(recent_captchas),
            "recent_warnings": len(recent_warnings),
            "recommendations": self._generate_recommendations(health_score, daily_activity)
        }
        
    def _generate_recommendations(self, health_score, daily_activity):
        """
        Generate recommendations based on health score and activity.
        
        Args:
            health_score (int): Health score (0-100)
            daily_activity (dict): Daily activity counts
            
        Returns:
            list: Recommendations
        """
        recommendations = []
        
        # Calculate averages
        avg_searches = sum(daily_activity["searches"].values()) / 7
        avg_comments = sum(daily_activity["comments"].values()) / 7
        
        # Recommend cooling period if health score is low
        if health_score < 50:
            recommendations.append("Take a cooling period of 3-5 days before resuming activity")
            
        # Recommend reduced activity if averages are high
        if avg_searches > 15:
            recommendations.append(f"Reduce search frequency from {avg_searches:.1f} to 10-15 per day")
            
        if avg_comments > 8:
            recommendations.append(f"Reduce comment frequency from {avg_comments:.1f} to 5-8 per day")
            
        # Recommend more varied activity if health score is moderate
        if 50 <= health_score < 80:
            recommendations.append("Add more variety to your engagement (likes, views, profile visits)")
            recommendations.append("Space out activities throughout the day rather than in batches")
            
        # Standard recommendations
        if not recommendations:
            recommendations.append("Maintain current activity pattern")
            
        return recommendations
        
    def check_daily_limits(self, max_searches=20, max_comments=15):
        """
        Check if daily limits have been reached.
        
        Args:
            max_searches (int): Maximum searches per day
            max_comments (int): Maximum comments per day
            
        Returns:
            dict: Result indicating if limits have been reached
        """
        # Get today's activity
        today = datetime.now().strftime("%Y-%m-%d")
        today_searches = self.activity_data["searches"].get(today, 0)
        today_comments = self.activity_data["comments"].get(today, 0)
        
        # Check health score
        health_score = self.calculate_activity_safety()
        
        # Adjust limits based on health score
        if health_score < 50:
            max_searches = int(max_searches * 0.5)
            max_comments = int(max_comments * 0.5)
        elif health_score < 80:
            max_searches = int(max_searches * 0.8)
            max_comments = int(max_comments * 0.8)
            
        # Check if limits reached
        searches_limit_reached = today_searches >= max_searches
        comments_limit_reached = today_comments >= max_comments
        
        # Generate recommendations
        recommendations = []
        if searches_limit_reached:
            recommendations.append(f"Search limit reached ({today_searches}/{max_searches})")
        if comments_limit_reached:
            recommendations.append(f"Comment limit reached ({today_comments}/{max_comments})")
            
        limits_reached = searches_limit_reached or comments_limit_reached
        
        return {
            "limits_reached": limits_reached,
            "searches_limit_reached": searches_limit_reached,
            "comments_limit_reached": comments_limit_reached,
            "today_searches": today_searches,
            "today_comments": today_comments,
            "max_searches": max_searches,
            "max_comments": max_comments,
            "recommendations": recommendations
        }

#################################################
# Human Behavior Simulator
#################################################

class HumanBehaviorSimulator:
    """
    Simulates human-like behavior for browsing, typing, and interaction
    to avoid detection as an automated script.
    """
    
    def __init__(self):
        """Initialize the human behavior simulator."""
        self.driver = None
        
    def set_driver(self, driver):
        """
        Set the webdriver for the simulator.
        
        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
        
    def adaptive_delay(self, min_seconds, max_seconds=None):
        """
        Wait for a random amount of time.
        
        Args:
            min_seconds (float): Minimum seconds to wait
            max_seconds (float): Maximum seconds to wait
        """
        if max_seconds is None:
            max_seconds = min_seconds * 1.5
            
        # Add some randomness
        delay = random.uniform(min_seconds, max_seconds)
        
        # Adjust based on time of day (people are slower late at night)
        hour = datetime.now().hour
        if hour < 6 or hour > 22:  # Late night/early morning
            delay *= 1.2
        elif 12 <= hour <= 14:  # Lunch time
            delay *= 1.1
            
        time.sleep(delay)
        
    def simulate_reading(self, text_length):
        """
        Simulate reading time for a given text length.
        
        Args:
            text_length (int): Length of text
        """
        # Average reading speed (characters per second)
        # Slow: 10 chars/sec, Medium: 20 chars/sec, Fast: 30 chars/sec
        reading_speed = random.uniform(10, 30)
        
        # Calculate reading time
        read_time = text_length / reading_speed
        
        # Add some variability
        read_time *= random.uniform(0.8, 1.2)
        
        # Cap reading time (people skim long content)
        max_read_time = 20  # Maximum 20 seconds
        read_time = min(read_time, max_read_time)
        
        # Wait
        time.sleep(read_time)
        
    def type_like_human(self, element, text, typing_style="normal"):
        """
        Type text like a human with natural delays between characters.
        
        Args:
            element: Element to type into
            text (str): Text to type
            typing_style (str): Style of typing ('normal', 'fast', 'careful')
        """
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
            
    def simulate_browsing_behavior(self, scroll_range=(100, 500)):
        """
        Simulate natural browsing behavior with scrolling and pauses.
        
        Args:
            scroll_range (tuple): Range of pixels to scroll
        """
        if not self.driver:
            return
            
        # Number of scroll actions to perform
        scroll_count = random.randint(2, 5)
        
        for _ in range(scroll_count):
            # Random scroll amount
            scroll_amount = random.randint(scroll_range[0], scroll_range[1])
            
            # Scroll down smoothly
            self.scroll_smoothly(scroll_amount)
            
            # Pause to simulate reading content
            self.adaptive_delay(1.5, 4)
            
        # Sometimes scroll back up
        if random.random() < 0.3:
            self.scroll_smoothly(-random.randint(100, 300))
            self.adaptive_delay(1, 2)
            
    def scroll_smoothly(self, distance):
        """
        Scroll the page smoothly like a human.
        
        Args:
            distance (int): Distance to scroll in pixels
        """
        if not self.driver:
            return
            
        # Number of steps for smooth scrolling
        steps = 10
        step_distance = distance // steps
        
        for i in range(steps):
            # Gradually increase and then decrease speed for more natural motion
            if i < steps // 2:
                # Accelerate
                step_time = 0.01 + (0.02 * i)
            else:
                # Decelerate
                step_time = 0.01 + (0.02 * (steps - i))
                
            self.driver.execute_script(f"window.scrollBy(0, {step_distance});")
            time.sleep(step_time)
            
        # Small adjustment at the end
        adjustment = distance - (step_distance * steps)
        if adjustment != 0:
            self.driver.execute_script(f"window.scrollBy(0, {adjustment});")

#################################################
# Enhanced Logger
#################################################

class EnhancedLogger:
    """
    Enhanced logging system for LinkedIn bot with structured JSON logs,
    screenshot capture, and encrypted sensitive data.
    """
    
    def __init__(self, account_name, base_dir="logs", encryption_key=None):
        """
        Initialize the enhanced logger.
        
        Args:
            account_name (str): Name of the account
            base_dir (str): Base directory for logs
            encryption_key (str): Optional encryption key for sensitive data
        """
        self.account_name = account_name
        self.base_dir = base_dir
        self.encryption_key = encryption_key
        
        # Create account-specific log directory
        self.log_dir = os.path.join(base_dir, account_name)
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Create logs for today
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Set up rotating file handler
        log_file = os.path.join(self.log_dir, f"{self.today}_{self.session_id}.log")
        
        # Set up logger
        self.logger = logging.getLogger(f"linkedin_bot_{account_name}")
        self.logger.setLevel(logging.INFO)
        
        # Check if handlers already exist
        if not self.logger.handlers:
            # Add file handler
            file_handler = logging.FileHandler(log_file)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            
            # Add console handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
            
        # Current session data
        self.session_data = {
            "start_time": datetime.now().isoformat(),
            "account": account_name,
            "session_id": self.session_id,
            "events": [],
            "comments": [],
            "errors": [],
            "stats": {
                "searches": 0,
                "posts_viewed": 0,
                "comments_posted": 0,
                "errors": 0
            }
        }
        
    def log_event(self, event_type, details=None):
        """
        Log a structured event.
        
        Args:
            event_type (str): Type of event
            details (dict): Event details
        """
        if details is None:
            details = {}
            
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "details": details
        }
        
        self.session_data["events"].append(event)
        self.logger.info(f"Event: {event_type} - {json.dumps(details)}")
        
    def log_comment(self, post_data, comment_text, success=True):
        """
        Log a comment attempt.
        
        Args:
            post_data (dict): Post data
            comment_text (str): Comment text
            success (bool): Whether comment was successful
        """
        # Extract relevant post data
        post_info = {
            "id": post_data.get("id", ""),
            "author": post_data.get("author", ""),
            "text_snippet": post_data.get("text", "")[:100] if post_data.get("text") else ""
        }
        
        comment_log = {
            "timestamp": datetime.now().isoformat(),
            "post": post_info,
            "comment": comment_text,
            "success": success
        }
        
        self.session_data["comments"].append(comment_log)
        
        if success:
            self.session_data["stats"]["comments_posted"] += 1
            
        self.logger.info(f"Comment on post by {post_info['author']}: {'Success' if success else 'Failed'}")
        
    def log_error(self, error_type, error_message, context=None):
        """
        Log an error.
        
        Args:
            error_type (str): Type of error
            error_message (str): Error message
            context (dict): Error context
        """
        if context is None:
            context = {}
            
        error_log = {
            "timestamp": datetime.now().isoformat(),
            "type": error_type,
            "message": error_message,
            "context": context
        }
        
        self.session_data["errors"].append(error_log)
        self.session_data["stats"]["errors"] += 1
        
        self.logger.error(f"Error [{error_type}]: {error_message}")
        
    def log_session_end(self):
        """Log the end of a session and save session data."""
        self.session_data["end_time"] = datetime.now().isoformat()
        
        # Calculate duration
        start_time = datetime.fromisoformat(self.session_data["start_time"])
        end_time = datetime.fromisoformat(self.session_data["end_time"])
        duration_seconds = (end_time - start_time).total_seconds()
        
        self.session_data["duration_seconds"] = duration_seconds
        
        # Log session summary
        summary = f"Session ended: {self.session_data['stats']['comments_posted']} comments, {self.session_data['stats']['errors']} errors, {duration_seconds:.1f}s"
        self.logger.info(summary)
        
        # Save session data to JSON file
        self._save_session_data()
        
    def _save_session_data(self):
        """Save session data to a JSON file."""
        # Create sessions directory
        sessions_dir = os.path.join(self.log_dir, "sessions")
        os.makedirs(sessions_dir, exist_ok=True)
        
        # Save file path
        session_file = os.path.join(sessions_dir, f"{self.session_id}.json")
        
        try:
            with open(session_file, 'w') as f:
                json.dump(self.session_data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving session data: {e}")

#################################################
# Account Manager
#################################################

class AccountManager:
    """
    Manages multiple LinkedIn accounts with scheduling, rotation, and health tracking.
    """
    
    def __init__(self, config_file="accounts_config.json", encryption_key=None):
        """
        Initialize the account manager.
        
        Args:
            config_file (str): Path to accounts configuration file
            encryption_key (str): Optional encryption key for sensitive data
        """
        self.config_file = config_file
        self.encryption_key = encryption_key
        self.encrypter = None
        
        # Set up encryption if key provided and cryptography available
        if encryption_key and CRYPTO_AVAILABLE:
            # Generate a consistent key from the provided encryption key
            key_hash = hashlib.sha256(encryption_key.encode()).digest()[:32]
            self.encrypter = Fernet(base64.urlsafe_b64encode(key_hash))
            
        # Load accounts
        self.accounts = self._load_accounts()
        
        # Create account directories
        for account_name in self.accounts:
            self._create_account_directories(account_name)
            
    def _load_accounts(self):
        """
        Load accounts from configuration file.
        
        Returns:
            dict: Account configurations
        """
        if not os.path.exists(self.config_file):
            # Create empty config if it doesn't exist
            self._save_accounts({})
            return {}
            
        try:
            with open(self.config_file, 'r') as f:
                if self.encrypter:
                    # Decrypt file content
                    try:
                        encrypted_data = f.read()
                        decrypted_data = self.encrypter.decrypt(encrypted_data.encode())
                        accounts = json.loads(decrypted_data)
                    except Exception:
                        # If decryption fails, try reading as unencrypted
                        f.seek(0)
                        accounts = json.load(f)
                else:
                    # Read unencrypted
                    accounts = json.load(f)
                    
            return accounts
        except Exception as e:
            print(f"Error loading accounts: {e}")
            return {}
            
    def _save_accounts(self, accounts):
        """
        Save accounts to configuration file.
        
        Args:
            accounts (dict): Account configurations
        """
        try:
            if self.encrypter:
                # Encrypt data
                encrypted_data = self.encrypter.encrypt(json.dumps(accounts).encode())
                with open(self.config_file, 'w') as f:
                    f.write(encrypted_data.decode())
            else:
                # Save unencrypted
                with open(self.config_file, 'w') as f:
                    json.dump(accounts, f, indent=2)
        except Exception as e:
            print(f"Error saving accounts: {e}")
            
    def _create_account_directories(self, account_name):
        """
        Create directory structure for an account.
        
        Args:
            account_name (str): Name of the account
        """
        # Base directory
        account_dir = os.path.join("accounts", account_name)
        
        # Create subdirectories
        subdirs = ["logs", "data", "screenshots", "profile", "health"]
        
        for subdir in subdirs:
            path = os.path.join(account_dir, subdir)
            os.makedirs(path, exist_ok=True)
            
    def add_account(self, account_name, username, password, **kwargs):
        """
        Add a new account or update an existing one.
        
        Args:
            account_name (str): Name of the account
            username (str): LinkedIn username (email)
            password (str): LinkedIn password
            **kwargs: Additional account settings
            
        Returns:
            bool: Whether the account was added successfully
        """
        # Create account config
        account_config = {
            "username": username,
            "password": password,
            "enabled": kwargs.get("enabled", True),
            "health_score": kwargs.get("health_score", 100),
            "last_used": kwargs.get("last_used", None),
            "keywords": kwargs.get("keywords", ["artificial intelligence", "machine learning"]),
            "proxy": kwargs.get("proxy", {}),
            "schedule": kwargs.get("schedule", {
                "days": ["monday", "tuesday", "wednesday", "thursday", "friday"],
                "time_ranges": ["9:00-11:30", "13:00-16:30"],
                "max_comments_per_session": 5,
                "cooldown_minutes": 120
            })
        }
        
        # Add to accounts dict
        self.accounts[account_name] = account_config
        
        # Create directories
        self._create_account_directories(account_name)
        
        # Save accounts
        self._save_accounts(self.accounts)
        
        return True
        
    def get_account(self, account_name):
        """
        Get account configuration.
        
        Args:
            account_name (str): Name of the account
            
        Returns:
            dict: Account configuration or None if not found
        """
        return self.accounts.get(account_name)
        
    def get_enabled_accounts(self):
        """
        Get list of enabled accounts.
        
        Returns:
            list: Names of enabled accounts
        """
        return [name for name, config in self.accounts.items() 
                if config.get("enabled", True)]
                
    def get_account_directories(self, account_name):
        """
        Get directory paths for an account.
        
        Args:
            account_name (str): Name of the account
            
        Returns:
            dict: Directory paths
        """
        account_dir = os.path.join("accounts", account_name)
        
        return {
            "base": account_dir,
            "logs": os.path.join(account_dir, "logs"),
            "data": os.path.join(account_dir, "data"),
            "screenshots": os.path.join(account_dir, "screenshots"),
            "profile": os.path.join(account_dir, "profile"),
            "health": os.path.join(account_dir, "health")
        }
        
    def is_account_scheduled_now(self, account_name):
        """
        Check if an account is scheduled to run now.
        
        Args:
            account_name (str): Name of the account
            
        Returns:
            bool: Whether the account is scheduled for the current time
        """
        account = self.get_account(account_name)
        if not account or not account.get("enabled", False):
            return False
            
        # Get current day and time
        now = datetime.now()
        day_name = now.strftime("%A").lower()
        current_time = now.strftime("%H:%M")
        
        # Check if today is scheduled
        schedule = account.get("schedule", {})
        scheduled_days = [d.lower() for d in schedule.get("days", [])]
        
        if day_name not in scheduled_days:
            return False
            
        # Check if current time is within scheduled ranges
        time_ranges = schedule.get("time_ranges", [])
        for time_range in time_ranges:
            try:
                start_time, end_time = time_range.split("-")
                
                if start_time <= current_time <= end_time:
                    return True
            except ValueError:
                continue
                
        return False
        
    def get_scheduled_accounts(self):
        """
        Get list of accounts scheduled for the current time.
        
        Returns:
            list: Names of scheduled accounts
        """
        scheduled = []
        
        for name in self.get_enabled_accounts():
            if self.is_account_scheduled_now(name) and not self.check_cooldown(name):
                scheduled.append(name)
                
        return scheduled
        
    def select_next_account(self):
        """
        Select the next account to use based on scheduling and health.
        
        Returns:
            str: Name of the next account to use, or None if no accounts are available
        """
        # Get scheduled accounts
        scheduled = self.get_scheduled_accounts()
        
        if not scheduled:
            return None
            
        # Sort by health score and last used time
        account_scores = []
        
        for name in scheduled:
            account = self.get_account(name)
            health_score = account.get("health_score", 50)
            
            last_used = account.get("last_used")
            if last_used:
                try:
                    last_used_time = datetime.fromisoformat(last_used)
                    hours_since = (datetime.now() - last_used_time).total_seconds() / 3600
                    
                    # Boost score for accounts not used recently
                    time_bonus = min(50, hours_since)
                    adjusted_score = health_score + time_bonus
                except (ValueError, TypeError):
                    adjusted_score = health_score
            else:
                # No last used time - give a bonus
                adjusted_score = health_score + 30
                
            account_scores.append((name, adjusted_score))
            
        if not account_scores:
            return None
            
        # Sort by adjusted score (descending)
        account_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Select account with highest score
        return account_scores[0][0]
        
    def check_cooldown(self, account_name):
        """
        Check if an account is in cooldown period.
        
        Args:
            account_name (str): Name of the account
            
        Returns:
            bool: Whether the account is in cooldown
        """
        account = self.get_account(account_name)
        if not account:
            return False
            
        last_used = account.get("last_used")
        if not last_used:
            return False
            
        try:
            last_used_time = datetime.fromisoformat(last_used)
            cooldown_minutes = account.get("schedule", {}).get("cooldown_minutes", 120)
            
            # Check if cooldown period has passed
            cooldown_delta = timedelta(minutes=cooldown_minutes)
            return
                    # Check if cooldown period has passed
            cooldown_delta = timedelta(minutes=cooldown_minutes)
            return datetime.now() < last_used_time + cooldown_delta
        except (ValueError, TypeError):
            return False
            
    def update_account_last_used(self, account_name):
        """
        Update the last used timestamp for an account.
        
        Args:
            account_name (str): Name of the account
            
        Returns:
            bool: Whether the update was successful
        """
        if account_name not in self.accounts:
            return False
            
        self.accounts[account_name]["last_used"] = datetime.now().isoformat()
        self._save_accounts(self.accounts)
        
        return True
        
    def update_account_health(self, account_name, health_score):
        """
        Update the health score for an account.
        
        Args:
            account_name (str): Name of the account
            health_score (int): New health score
            
        Returns:
            bool: Whether the update was successful
        """
        if account_name not in self.accounts:
            return False
            
        self.accounts[account_name]["health_score"] = health_score
        self._save_accounts(self.accounts)
        
        return True
        
    def disable_account(self, account_name):
        """
        Disable an account.
        
        Args:
            account_name (str): Name of the account
            
        Returns:
            bool: Whether the update was successful
        """
        if account_name not in self.accounts:
            return False
            
        self.accounts[account_name]["enabled"] = False
        self._save_accounts(self.accounts)
        
        return True


#################################################
# Enhanced LinkedIn Bot
#################################################

class EnhancedLinkedInBot:
    """
    Enhanced LinkedIn bot with advanced features:
    - Multi-account support
    - Post quality scoring
    - Keyword intelligence
    - Human behavior mimicking
    - Comment history tracking
    - Account health monitoring
    - Enhanced duplicate detection
    - Secondary comment verification
    """
    
    def __init__(self, config_file="bot_config.json"):
        """
        Initialize the enhanced LinkedIn bot.
        
        Args:
            config_file (str): Path to configuration file
        """
        # Load configuration
        self.config = self._load_config(config_file)
        
        # Initialize account manager
        self.account_manager = AccountManager(
            config_file=self.config.get("accounts_config", "accounts_config.json"),
            encryption_key=self.config.get("master_key", None)
        )
        
        # Initialize components
        self.active_account = None
        self.driver = None
        self.keyword_tracker = None
        self.comment_history = None
        self.post_evaluator = None
        self.account_interests = None
        self.health_monitor = None
        self.behavior_simulator = None
        self.logger = None
        
        # Initialize LinkedIn-specific components
        self.linkedin_selectors = LinkedInSelectors()
        self.duplicate_detector = EnhancedDuplicateDetector(similarity_threshold=0.75)
        self.comment_verifier = None  # Will be initialized when driver is available
        
        # Create base directories
        os.makedirs("logs", exist_ok=True)
        os.makedirs("data", exist_ok=True)
        os.makedirs("accounts", exist_ok=True)
        
    def _load_config(self, config_file):
        """Load bot configuration from file."""
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Error loading config file: {config_file}")
                
        # Default configuration
        return {
            "accounts_config": "accounts_config.json",
            "default_comment_model": "llama3.2:3b",
            "ollama_url": "http://localhost:11434/api/generate",
            "min_post_score": 25,
            "default_keywords": ["artificial intelligence", "machine learning"],
            "session_cooldown_minutes": 120,
            "duplicate_similarity_threshold": 0.75,
            "comment_quality_threshold": 0.6
        }
        
    def setup_account(self, account_name):
        """
        Set up the bot for a specific account.
        
        Args:
            account_name (str): Name of the account to set up
            
        Returns:
            bool: Whether setup was successful
        """
        # Check if account exists
        account_data = self.account_manager.get_account(account_name)
        if not account_data:
            print(f"Account {account_name} not found.")
            return False
            
        # Check if account is enabled
        if not account_data.get("enabled", False):
            print(f"Account {account_name} is disabled.")
            return False
            
        # Check account health
        self.active_account = account_name
        self.health_monitor = AccountHealthMonitor(
            account_name=account_name,
            storage_dir=f"accounts/{account_name}/health"
        )
        
        health_summary = self.health_monitor.get_health_summary()
        if health_summary["health_score"] < 30:
            print(f"Account {account_name} health score too low ({health_summary['health_score']}). Skipping.")
            return False
            
        # Set up directories
        account_dirs = self.account_manager.get_account_directories(account_name)
        
        # Set up logger
        self.logger = EnhancedLogger(
            account_name=account_name,
            base_dir=account_dirs["logs"],
            encryption_key=self.config.get("master_key", None)
        )
        
        self.logger.logger.info(f"Setting up bot for account: {account_name}")
        
        # Set up keyword tracker
        keywords = account_data.get("keywords", self.config.get("default_keywords", ["artificial intelligence"]))
        initial_keyword = keywords[0] if keywords else "artificial intelligence"
        
        self.keyword_tracker = KeywordPerformanceTracker(
            initial_keyword=initial_keyword,
            storage_file=os.path.join(account_dirs["data"], "keyword_performance.json"),
            rotation_threshold=25,  # Changed from 50 to 25 successful comments
            ollama_url=self.config.get("ollama_url")
        )
        
        # Set up comment history
        self.comment_history = CommentHistory(
            account_name=account_name,
            encryption_key=self.config.get("master_key", None),
            storage_dir=os.path.join(account_dirs["data"], "comment_history"),
            retention_days=90
        )
        
        # Set up account interests
        self.account_interests = AccountInterests(
            account_name=account_name,
            storage_dir=account_dirs["data"]
        )
        
        # Set up post evaluator
        self.post_evaluator = PostEvaluator(
            target_keywords=keywords,
            min_score_threshold=self.config.get("min_post_score", 25),
            account_interests=self.account_interests
        )
        
        # Set up human behavior simulator
        self.behavior_simulator = HumanBehaviorSimulator()
        
        return True
        
    def initialize_browser(self, headless=False):
        """Initialize browser with proper profile and fingerprinting."""
        if self.active_account is None:
            self.logger.logger.error("No active account selected. Cannot initialize browser.")
            return False
            
        try:
            account_data = self.account_manager.get_account(self.active_account)
            account_dirs = self.account_manager.get_account_directories(self.active_account)
            
            # Browser profile directory
            profile_dir = os.path.join(account_dirs["profile"], "selenium")
            os.makedirs(profile_dir, exist_ok=True)
            
            # Set up browser options
            options = webdriver.ChromeOptions()
            options.add_argument(f"user-data-dir={profile_dir}")
            
            # Set up proxy if configured
            if "proxy" in account_data and account_data["proxy"].get("host"):
                proxy = account_data["proxy"]
                proxy_url = f"{proxy['host']}:{proxy['port']}"
                
                # Add proxy authentication if needed
                if "credentials" in proxy:
                    options.add_argument(f"--proxy-server={proxy_url}")
                    # Note: For authenticated proxies, you would need a proxy extension
                    # or browser automation to handle the authentication dialog
                else:
                    options.add_argument(f"--proxy-server={proxy_url}")
                    
            # Set headless mode if needed
            if headless:
                options.add_argument("--headless")
                options.add_argument("--window-size=1920,1080")
                
            # Add human-like fingerprinting
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            options.add_argument(f"user-agent={user_agent}")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)
            
            # For Brave browser, set the binary location if needed
            # Uncomment and adjust the path for your operating system:
            # For Windows:
            # brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
            # For Linux:
            # brave_path = "/usr/bin/brave-browser"
            # For macOS:
            # brave_path = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
            # options.binary_location = brave_path
            
            # Initialize browser
            self.driver = webdriver.Chrome(options=options)
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
                """
            })
            
            # Set window size to a common resolution
            self.driver.set_window_size(1920, 1080)
            
            # Set behavior simulator driver
            self.behavior_simulator.set_driver(self.driver)
            
            # Initialize comment verifier
            self.comment_verifier = CommentVerificationManager(
                self.driver,
                self.linkedin_selectors,
                self.duplicate_detector,
                self.logger,
                min_quality_score=self.config.get("comment_quality_threshold", 0.6)
            )
            
            self.logger.logger.info("Browser initialized successfully")
            return True
        except Exception as e:
            if hasattr(self, 'logger') and self.logger:
                self.logger.logger.error(f"Error initializing browser: {e}")
            else:
                print(f"Error initializing browser: {e}")
            return False
            
    def login_to_linkedin(self):
        """Log in to LinkedIn with the active account."""
        if not self.driver or not self.active_account:
            self.logger.logger.error("Browser or active account not initialized")
            return False
            
        try:
            account_data = self.account_manager.get_account(self.active_account)
            
            # Go to LinkedIn login page
            self.driver.get("https://www.linkedin.com/login")
            
            # Wait for the page to load
            self.behavior_simulator.adaptive_delay(2, 5)
            
            # Check if we're already logged in
            if "feed" in self.driver.current_url:
                self.logger.logger.info("Already logged in to LinkedIn")
                return True
                
            # Enter username
            username_field = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "username"))
            )
            self.behavior_simulator.type_like_human(username_field, account_data["username"])
            
            # Enter password
            password_field = self.driver.find_element(By.ID, "password")
            self.behavior_simulator.type_like_human(password_field, account_data["password"], typing_style="careful")
            
            # Click sign in
            sign_in_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            sign_in_button.click()
            
            # Wait for login to complete
            self.behavior_simulator.adaptive_delay(3, 7)
            
            # Check for captcha or verification
            page_source = self.driver.page_source.lower()
            if "captcha" in page_source or "verify" in page_source or "security check" in page_source:
                self.logger.logger.warning("Captcha or verification detected during login")
                
                # Take a screenshot
                screenshot_path = os.path.join(
                    self.account_manager.get_account_directories(self.active_account)["screenshots"],
                    f"captcha_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                )
                self.driver.save_screenshot(screenshot_path)
                
                # Record captcha event
                self.health_monitor.record_captcha_event(self.driver.current_url)
                
                # Notify about captcha
                print("CAPTCHA detected! Please complete it manually.")
                print("Bot will wait for 2 minutes...")
                
                # Wait for manual intervention
                time.sleep(120)
                
                # Check if we're logged in after manual intervention
                if "feed" in self.driver.current_url:
                    self.health_monitor.record_captcha_event(
                        self.driver.current_url, 
                        resolved=True, 
                        resolution_time=120
                    )
                    return True
                else:
                    return False
                    
            # Check if login successful
            if "feed" in self.driver.current_url or "checkpoint" in self.driver.current_url:
                self.logger.logger.info("Successfully logged in to LinkedIn")
                return True
            else:
                self.logger.logger.error("Failed to log in to LinkedIn")
                return False
                
        except Exception as e:
            self.logger.logger.error(f"Error logging in to LinkedIn: {e}")
            return False
            
    def search_for_posts(self, keyword):
        """
        Search for LinkedIn posts with the given keyword.
        
        Args:
            keyword (str): Search keyword
            
        Returns:
            list: List of post elements found
        """
        if not self.driver:
            return []
            
        try:
            # Record search activity
            self.health_monitor.record_activity("searches")
            
            # Navigate to LinkedIn feed
            self.driver.get("https://www.linkedin.com/feed/")
            self.behavior_simulator.adaptive_delay(2, 5)
            
            # Click on search box
            search_box = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[contains(@class, 'search-global-typeahead__input')]"))
            )
            search_box.click()
            self.behavior_simulator.adaptive_delay(0.5, 1.5)
            
            # Clear and type search query
            search_box.clear()
            self.behavior_simulator.type_like_human(search_box, keyword)
            self.behavior_simulator.adaptive_delay(0.5, 1.5)
            
            # Press Enter to search
            search_box.send_keys(Keys.RETURN)
            
            # Wait for search results
            self.behavior_simulator.adaptive_delay(2, 5)
            
            # Click on "Posts" tab to show only posts
            try:
                posts_tab = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Posts']"))
                )
                posts_tab.click()
                self.behavior_simulator.adaptive_delay(2, 5)
            except:
                self.logger.logger.warning("Could not find 'Posts' tab, continuing with current results")
                
            # Find all post elements
            posts = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'feed-shared-update-v2')]")
            
            # If no posts found with the primary selector, try fallback selectors
            if not posts:
                posts = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'feed-shared-update')]")
                
            if not posts:
                posts = self.driver.find_elements(By.XPATH, "//div[contains(@data-urn, 'activity')]")
                
            # Update keyword stats
            self.keyword_tracker.update_search_stats(keyword, len(posts))
            
            # Log search results
            self.logger.logger.info(f"Found {len(posts)} posts for keyword: {keyword}")
            
            # Simulate a delay between searching and processing
            self.behavior_simulator.adaptive_delay(1, 3)
            
            return posts
        except Exception as e:
            self.logger.logger.error(f"Error searching for posts: {e}")
            return []
            
    def extract_post_data(self, post_element):
        """
        Extract data from a post element.
        
        Args:
            post_element: Selenium element representing a LinkedIn post
            
        Returns:
            dict: Post data including text, author, etc.
        """
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
            
            # Create post data
            post_data = {
                "id": post_id,
                "author": author,
                "text": post_text,
                "element": post_element,
                "signature": signature,
                "timestamp": datetime.now().isoformat()
            }
            
            # Record viewing this post
            self.health_monitor.record_activity("posts")
            
            return post_data
        except Exception as e:
            self.logger.logger.error(f"Error extracting post data: {e}")
            traceback.print_exc()  # Print stack trace for debugging
            return None
            
    def generate_comment(self, post_data):
        """
        Generate a comment for a post.
        
        Args:
            post_data (dict): Post data
            
        Returns:
            str: Generated comment
        """
        # This would call your existing comment generation function
        # Assuming a function like generate_comment_ollama exists
        return self.generate_comment_ollama(post_data["text"])
        
    def generate_comment_ollama(self, post_text):
        """
        Generate a comment using Ollama API.
        Placeholder implementation - replace with actual implementation.
        
        Args:
            post_text (str): Post text to comment on
            
        Returns:
            str: Generated comment
        """
        try:
            import requests
            
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
                    "model": self.config.get("default_comment_model", "llama3.2:3b"),
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
            else:
                # Fallback comment if API fails
                return "This is an interesting perspective. Thanks for sharing your insights on this topic."
                
        except Exception as e:
            self.logger.logger.error(f"Error generating comment: {e}")
            # Return a generic fallback comment
            return "Thanks for sharing this insightful post. I appreciate the perspective you've provided."
            
    def is_duplicate_comment(self, comment_text):
        """
        Enhanced duplicate comment detection using our improved detector.
        
        Args:
            comment_text (str): Comment text to check
            
        Returns:
            bool: Whether the comment is a duplicate
        """
        # Get recent comments from history
        recent_comments = []
        for comment_data in list(self.comment_history.comments.values())[-30:]:
            recent_comments.append(comment_data.get("comment_text", ""))
            
        # Check if any of the recent comments are similar to this one
        for existing_comment in recent_comments:
            is_duplicate, score, method = self.duplicate_detector.is_duplicate(
                comment_text, existing_comment
            )
            
            if is_duplicate:
                self.logger.logger.warning(
                    f"Duplicate comment detected. Similarity score: {score:.2f}, method: {method}"
                )
                return True
                
        return False
            
    def post_comment(self, post_data, comment_text):
        """
        Enhanced method to post a comment on a LinkedIn post with advanced verification.
        
        Args:
            post_data (dict): Post data
            comment_text (str): Comment text to post
            
        Returns:
            bool: Whether comment was posted successfully
        """
        if not post_data or not comment_text:
            return False
            
        try:
            post_element = post_data["element"]
            
            # Scroll to the post
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", post_element)
            self.behavior_simulator.adaptive_delay(1, 3)
            
            # Find comment button using our enhanced selectors
            comment_button = self.linkedin_selectors.find_element_with_fallbacks(
                post_element, self.linkedin_selectors.COMMENT_BUTTON_SELECTORS
            )
            
            if not comment_button:
                self.logger.logger.error("Could not find comment button")
                return False
                
            comment_button.click()
            self.behavior_simulator.adaptive_delay(1, 3)
            
            # Find comment input using our enhanced selectors
            comment_input = self.linkedin_selectors.find_element_with_fallbacks(
                post_element, self.linkedin_selectors.COMMENT_INPUT_SELECTORS
            )
            
            if not comment_input:
                # Try finding in the entire driver context in case the comment box is in a different container
                comment_input = self.linkedin_selectors.find_element_with_fallbacks(
                    self.driver, self.linkedin_selectors.COMMENT_INPUT_SELECTORS
                )
                
            if not comment_input:
                self.logger.logger.error("Could not find comment input field")
                return False
                
            comment_input.click()
            self.behavior_simulator.adaptive_delay(0.5, 1.5)
            
            # Type comment
            self.behavior_simulator.type_like_human(comment_input, comment_text, typing_style="normal")
            self.behavior_simulator.adaptive_delay(1, 3)
            
            # Find submit button using our enhanced selectors
            post_button = self.linkedin_selectors.find_element_with_fallbacks(
                post_element, self.linkedin_selectors.COMMENT_POST_BUTTON_SELECTORS
            )
            
            if not post_button:
                # Try finding in the entire driver context
                post_button = self.linkedin_selectors.find_element_with_fallbacks(
                    self.driver, self.linkedin_selectors.COMMENT_POST_BUTTON_SELECTORS
                )
                
            if not post_button:
                self.logger.logger.error("Could not find post comment button")
                return False
                
            # Check if post button is enabled
            if not post_button.is_enabled():
                self.logger.logger.error("Post button is disabled")
                return False
                
            post_button.click()
            
            # Wait for comment to post
            self.behavior_simulator.adaptive_delay(2, 5)
            
            # Take a screenshot
            screenshot_path = os.path.join(
                self.account_manager.get_account_directories(self.active_account)["screenshots"],
                f"comment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            )
            self.driver.save_screenshot(screenshot_path)
            
            # Verify that the comment was actually posted
            comment_verified, comment_element = self.comment_verifier.verify_comment_posted(
                post_element, comment_text
            )
            
            if not comment_verified:
                self.logger.logger.warning("Failed to verify comment was posted")
                return False
                
            # Record the comment
            self.comment_history.record_comment(post_data, comment_text)
            
            # Record interaction with account interests
            self.account_interests.record_interaction(post_data)
            
            # Record comment activity
            self.health_monitor.record_activity("comments")
            
            # Log the comment
            self.logger.log_comment(post_data, comment_text, True)
            
            # Update keyword stats
            current_keyword = self.keyword_tracker.select_next_keyword()
            self.keyword_tracker.update_comment_stats(current_keyword, success=True)
            
            return True
        except Exception as e:
            self.logger.log_error("comment_error", str(e), {"post_id": post_data.get("id")})
            traceback.print_exc()  # Print stack trace for debugging
            return False
            
    def refresh_browser(self):
        """Refresh the browser to maintain session stability."""
        if self.driver:
            try:
                # Save current URL
                current_url = self.driver.current_url
                
                # Refresh the page
                self.driver.refresh()
                
                # Wait for page to load
                self.behavior_simulator.adaptive_delay(2, 5)
                
                self.logger.logger.info("Browser refreshed successfully")
                return True
            except Exception as e:
                self.logger.logger.error(f"Error refreshing browser: {e}")
                return False
        return False
        
    def process_posts(self, keyword, max_comments=5):
        """
        Process LinkedIn posts for a given keyword.
        
        Args:
            keyword (str): Search keyword
            max_comments (int): Maximum number of comments to post
            
        Returns:
            int: Number of comments posted
        """
        if not self.driver:
            return 0
            
        # Check account health first
        health_limits = self.health_monitor.check_daily_limits()
        if health_limits["limits_reached"]:
            self.logger.logger.warning(f"Daily limits reached: {health_limits['recommendations']}")
            return 0
            
        # Search for posts with the keyword
        posts = self.search_for_posts(keyword)
        posts_found = len(posts)
        
        if not posts:
            self.logger.logger.warning(f"No posts found for keyword: {keyword}")
            return 0
            
        # Simulate browsing behavior
        self.behavior_simulator.simulate_browsing_behavior((15, 40))
        
        # Process posts
        comments_posted = 0
        processed_posts = 0
        
        for post in posts:
            # Extract post data
            post_data = self.extract_post_data(post)
            if not post_data:
                continue
                
            processed_posts += 1
            
            # Check if we've already commented on this post
            if self.comment_history.has_commented(post_data["id"]):
                self.logger.logger.info(f"Already commented on post: {post_data['id']}")
                continue
                
            # Check if this is a duplicate post
            if self.comment_history.is_duplicate_post(post_data["signature"]):
                self.logger.logger.info(f"Duplicate post detected: {post_data['signature']}")
                continue
                
            # Evaluate post quality
            evaluation = self.post_evaluator.evaluate_post(post_data)
            self.logger.log_event("post_evaluation", {
                "post_id": post_data["id"],
                "score": evaluation["total_score"],
                "pass_threshold": evaluation["pass_threshold"]
            })
            
            # Skip if post doesn't meet quality threshold
            if not evaluation["pass_threshold"]:
                self.logger.logger.info(f"Post quality too low: {evaluation['total_score']}/50")
                continue
                
            # Simulate reading the post content
            if post_data["text"]:
                self.behavior_simulator.simulate_reading(len(post_data["text"]))
                
            # Generate comment
            comment_text = self.generate_comment(post_data)
            
            # Check if comment is a duplicate
            if self.is_duplicate_comment(comment_text):
                self.logger.logger.info("Generated comment too similar to recent comments, skipping")
                continue
                
            # Post comment
            success = self.post_comment(post_data, comment_text)
            if success:
                comments_posted += 1
                self.logger.logger.info(f"Comment posted successfully ({comments_posted}/{max_comments})")
                
                # Refresh browser after comment to increase stability
                self.refresh_browser()
                
                # Add some delay between comments
                comment_delay = random.uniform(10, 25)
                self.behavior_simulator.adaptive_delay(comment_delay, comment_delay + 10)
                
                # Check if we've reached the maximum comments
                if comments_posted >= max_comments:
                    break
            else:
                self.logger.logger.warning("Failed to post comment")
                
            # Check if we need to rotate keywords after 25 successful comments
            if self.keyword_tracker.should_rotate_keyword(keyword):
                self.logger.logger.info(f"Rotating keyword after {self.keyword_tracker.rotation_threshold} comments")
                break
                
        # Update keyword tracker stats
        self.keyword_tracker.update_search_stats(keyword, posts_found)
        
        return comments_posted
        
    def run_session(self):
        """Enhanced run_session with secondary comment verification."""
        # Select next account
        account_name = self.account_manager.select_next_account()
        if not account_name:
            print("No available accounts to use.")
            return False
            
        # Check if account is scheduled now
        if not self.account_manager.is_account_scheduled_now(account_name):
            print(f"Account {account_name} is not scheduled to run now.")
            return False
            
        # Set up account
        if not self.setup_account(account_name):
            print(f"Failed to set up account: {account_name}")
            return False
            
        try:
            # Initialize browser
            if not self.initialize_browser():
                return False
                
            # Login to LinkedIn
            if not self.login_to_linkedin():
                return False
                
            # Get account settings
            account_data = self.account_manager.get_account(account_name)
            max_comments_per_session = account_data.get("schedule", {}).get("max_comments_per_session", 5)
            
            # Select keyword
            current_keyword = self.keyword_tracker.select_next_keyword()
            self.logger.logger.info(f"Selected keyword: {current_keyword}")
            
            # Process posts with the keyword
            comments_posted = self.process_posts(current_keyword, max_comments_per_session)
            
            # Check if we need to rotate to a new keyword
            if self.keyword_tracker.should_rotate_keyword(current_keyword):
                new_keyword = self.keyword_tracker.select_next_keyword(current_keyword)
                self.logger.logger.info(f"Rotated to new keyword: {new_keyword}")
                
            # SECONDARY VERIFICATION: Check and manage comments after the session
            if comments_posted > 0:
                self.logger.logger.info("Running secondary comment verification...")
                verification_results = self.comment_verifier.check_and_manage_comments(
                    max_comments=max_comments_per_session * 2,  # Check twice as many comments as we posted
                    delete_duplicates=True,
                    delete_low_quality=True
                )
                
                self.logger.logger.info(
                    f"Comment verification results: {verification_results['comments_checked']} checked, "
                    f"{verification_results['duplicates_found']} duplicates, "
                    f"{verification_results['low_quality_found']} low quality, "
                    f"{verification_results['comments_deleted']} deleted"
                )
                
            # Log session stats
            self.logger.logger.info(f"Session completed - Comments posted: {comments_posted}")
            
            # Update account health
            health_summary = self.health_monitor.get_health_summary()
            self.account_manager.update_account_health(account_name, health_summary["health_score"])
            
            # End session logging
            if self.logger:
                self.logger.log_session_end()
                
            return True
        except Exception as e:
            if self.logger:
                self.logger.log_error("session_error", str(e))
            traceback.print_exc()  # Print stack trace for debugging
            return False
        finally:
            # Clean up
            if self.driver:
                self.driver.quit()
                
    def run_scheduled_session(self):
        """Run a session if scheduled, with proper timing."""
        # Get accounts scheduled for now
        scheduled_accounts = self.account_manager.get_scheduled_accounts()
        
        if not scheduled_accounts:
            print("No accounts scheduled to run now.")
            return False
            
        # Select one of the scheduled accounts (randomly to add variability)
        account_name = random.choice(scheduled_accounts)
        
        # Check cooldown
        if self.account_manager.check_cooldown(account_name):
            print(f"Account {account_name} is still in cooldown period.")
            return False
            
        # Run session with selected account
        print(f"Running scheduled session for account: {account_name}")
        return self.run_session()


#################################################
# Main Entry Point
#################################################

def run_bot_session():
    """Run a scheduled bot session."""
    bot = EnhancedLinkedInBot()
    success = bot.run_scheduled_session()
    
    if success:
        print("Session completed successfully.")
    else:
        print("Session did not complete successfully.")
        
    # Add a little randomness to the next scheduled run
    # to avoid predictable patterns
    jitter = random.randint(-10, 10)
    return 60 + jitter  # Minutes until next attempt

def schedule_mode():
    """Run the bot in scheduled mode."""
    print("Starting LinkedIn bot in scheduled mode.")
    print("Press Ctrl+C to exit.")
    
    # Initial run (with a small delay to let the console output settle)
    time.sleep(2)
    next_interval = run_bot_session()
    
    # Schedule next run
    import schedule
    schedule.every(next_interval).minutes.do(lambda: run_bot_session())
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check schedule every minute
    except KeyboardInterrupt:
        print("\nShutting down bot...")
        import sys
        sys.exit(0)

def single_run_mode(account_name=None):
    """Run the bot once for a specific account or next scheduled account."""
    bot = EnhancedLinkedInBot()
    
    if account_name:
        # Set up the specific account
        if not bot.setup_account(account_name):
            print(f"Failed to set up account: {account_name}")
            return False
            
        # Initialize browser and run session
        if not bot.initialize_browser():
            print("Failed to initialize browser.")
            return False
            
        # Login to LinkedIn
        if not bot.login_to_linkedin():
            print("Failed to log in to LinkedIn.")
            return False
            
        # Get account settings
        account_data = bot.account_manager.get_account(account_name)
        max_comments_per_session = account_data.get("schedule", {}).get("max_comments_per_session", 5)
        
        # Select keyword
        current_keyword = bot.keyword_tracker.select_next_keyword()
        print(f"Selected keyword: {current_keyword}")
        
        # Process posts
        comments_posted = bot.process_posts(current_keyword, max_comments_per_session)
        print(f"Comments posted: {comments_posted}")
        
        # Run secondary verification
        if comments_posted > 0:
            print("Running secondary comment verification...")
            verification_results = bot.comment_verifier.check_and_manage_comments()
            print(f"Verification results: {verification_results['comments_deleted']} comments deleted")
            
        # Clean up
        if bot.driver:
            bot.driver.quit()
    else:
        # Run with next scheduled account
        success = bot.run_scheduled_session()
        if success:
            print("Session completed successfully.")
        else:
            print("Session did not complete successfully.")
            
    return True

def main():
    """Main entry point for the LinkedIn bot."""
    import argparse
    import os
    import sys
    
    parser = argparse.ArgumentParser(description="Enhanced LinkedIn Engagement Bot")
    parser.add_argument("--schedule", action="store_true", help="Run in scheduled mode")
    parser.add_argument("--account", type=str, help="Specific account to use")
    parser.add_argument("--brave", action="store_true", help="Use Brave browser instead of Chrome")
    
    args = parser.parse_args()
    
    # Create necessary directories
    os.makedirs("logs", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    os.makedirs("accounts", exist_ok=True)
    
    if args.schedule:
        schedule_mode()
    else:
        single_run_mode(args.account)

if __name__ == "__main__":
    main()