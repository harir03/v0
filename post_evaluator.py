#!/usr/bin/env python3
"""
Post Evaluator Module for LinkedIn Bot

This module contains the PostEvaluator class that evaluates LinkedIn posts
for engagement value on a 50-point scale.
"""

import re
from datetime import datetime


class PostEvaluator:
    """
    Evaluates LinkedIn posts for engagement value on a 50-point scale.
    Considers content quality, author credibility, topic relevance, and engagement potential.
    """
    
    def __init__(self, target_keywords=None, min_score_threshold=25, account_interests=None):
        """
        Initialize the post evaluator with target keywords and thresholds.
        
        Args:
            target_keywords (list): List of target keywords
            min_score_threshold (int): Minimum score to pass evaluation
            account_interests: AccountInterests instance for personalization
        """
        self.target_keywords = target_keywords or []
        self.min_score_threshold = min_score_threshold
        self.account_interests = account_interests
        
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
                "scores": {"content_quality": 0, "author_credibility": 0, "topic_relevance": 0, "engagement_potential": 0},
                "notes": ["Post too short"]
            }
        
        # 1. Evaluate content quality (20 points max)
        content_score, content_notes = self._evaluate_content_quality(post_text)
        
        # 2. Evaluate author credibility (10 points max)
        author_score, author_notes = self._evaluate_author_credibility(author)
        
        # 3. Evaluate topic relevance to target keywords (10 points max)
        relevance_score, relevance_notes = self._evaluate_topic_relevance(post_text)
        
        # 4. Evaluate engagement potential (10 points max)
        engagement_score, engagement_notes = self._evaluate_engagement_potential(post_text, post_data)
        
        # Calculate total score (50 points max)
        total_score = content_score + author_score + relevance_score + engagement_score
        
        # Check if post passes minimum threshold
        passes_threshold = total_score >= self.min_score_threshold
        
        # Combine all notes
        all_notes = content_notes + author_notes + relevance_notes + engagement_notes
        
        return {
            "total_score": total_score,
            "pass_threshold": passes_threshold,
            "scores": {
                "content_quality": content_score,
                "author_credibility": author_score,
                "topic_relevance": relevance_score,
                "engagement_potential": engagement_score
            },
            "notes": all_notes
        }
        
    def _evaluate_content_quality(self, post_text):
        """Evaluate content quality of the post (20 points max)."""
        score = 0
        notes = []
        
        # Check content length (0-5 points)
        if len(post_text) < 50:
            score += 1
            notes.append("Very short content")
        elif len(post_text) < 100:
            score += 2
            notes.append("Short content")
        elif len(post_text) < 200:
            score += 3
            notes.append("Medium content")
        elif len(post_text) < 400:
            score += 4
            notes.append("Good content length")
        else:
            score += 5
            notes.append("Comprehensive content")
            
        # Check for questions (0-3 points)
        question_count = post_text.count("?")
        if question_count > 0:
            score += min(question_count, 3)
            notes.append(f"Contains {question_count} question(s)")
                
        # Check for lists, numbers, and structured content (0-4 points)
        if re.search(r'\d+\.', post_text) or re.search(r'•', post_text) or re.search(r'-\s', post_text):
            score += 4
            notes.append("Contains structured content")
            
        # Check for hashtags (0-2 points)
        hashtag_count = len(re.findall(r'#\w+', post_text))
        if 1 <= hashtag_count <= 3:
            score += 2
            notes.append(f"Good hashtag usage ({hashtag_count})")
        elif hashtag_count > 3:
            notes.append("Too many hashtags")
            
        # Check for specific content markers (0-6 points)
        content_markers = 0
        
        # Case studies, examples, or stories
        if re.search(r'case stud|example|for instance|story|experience', post_text, re.IGNORECASE):
            content_markers += 2
            notes.append("Contains examples/stories")
            
        # Data, research, or statistics
        if re.search(r'research|stud(y|ies)|data|statistics|according to|\d+%|\d+\s*percent', post_text, re.IGNORECASE):
            content_markers += 2
            notes.append("Contains data/research")
            
        # Tips, advice, or how-to content
        if re.search(r'tip|advice|how to|guide|step|strategy', post_text, re.IGNORECASE):
            content_markers += 2
            notes.append("Contains tips/advice")
            
        score += min(content_markers, 6)
        
        # Cap at 20 points
        return min(score, 20), notes
        
    def _evaluate_author_credibility(self, author_name):
        """Evaluate author credibility (10 points max)."""
        score = 5  # Default middle score
        notes = ["Author credibility: default"]
        
        # Check if we've interacted with this author before (using account interests)
        if self.account_interests and hasattr(self.account_interests, 'is_author_of_interest'):
            if self.account_interests.is_author_of_interest(author_name):
                score += 3
                notes.append("Author of interest")
            
        return min(score, 10), notes
        
    def _evaluate_topic_relevance(self, post_text):
        """Evaluate relevance to target keywords (10 points max)."""
        score = 0
        notes = []
        
        # If no target keywords, give middle score
        if not self.target_keywords:
            return 5, ["No target keywords defined"]
            
        # Check for keyword matches
        matches = 0
        matched_keywords = []
        
        for keyword in self.target_keywords:
            if keyword.lower() in post_text.lower():
                matches += 1
                matched_keywords.append(keyword)
                
        # Score based on keyword matches
        if matches > 0:
            score = min(matches * 3, 10)
            notes.append(f"Matched keywords: {', '.join(matched_keywords)}")
        else:
            notes.append("No keyword matches")
                
        return min(score, 10), notes
        
    def _evaluate_engagement_potential(self, post_text, post_data):
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
            score += min(cta_matches, 3)
            notes.append("Contains call to action")
            
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
            notes.append("Contains discussion triggers")
            
        # Check for trending topics (0-2 points)
        trending_topics_2025 = [
            'AI', 'artificial intelligence', 'ChatGPT', 'machine learning',
            'remote work', 'layoffs', 'recession', 'climate change',
            'sustainability', 'blockchain', 'crypto', 'leadership',
            'mental health', 'burnout', 'work-life balance',
            'career change', 'upskilling', 'generative AI', 'automation',
            'digital transformation', 'cybersecurity', 'data science'
        ]
        
        trending_matches = sum(1 for topic in trending_topics_2025 if topic.lower() in post_text.lower())
        if trending_matches > 0:
            score += min(trending_matches, 2)
            notes.append("Contains trending topics")
            
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
