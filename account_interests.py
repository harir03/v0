#!/usr/bin/env python3
"""
Account Interests Module for LinkedIn Bot

Tracks and manages the interests of a LinkedIn account
to personalize engagement with relevant content.
"""

import os
import json
import re
from datetime import datetime


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
