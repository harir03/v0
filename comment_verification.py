#!/usr/bin/env python3
"""
Comment Verification Module for LinkedIn Bot

Verifies comments after posting and manages existing comments:
1. Verifies successful comment posting
2. Checks comment quality and relevance
3. Finds and deletes duplicate or low-quality comments
"""

import re
from datetime import datetime


class CommentVerificationManager:
    """
    Verifies comments after posting and manages existing comments:
    1. Verifies successful comment posting
    2. Checks comment quality and relevance
    3. Finds and deletes duplicate or low-quality comments
    """
    
    def __init__(self, driver, selectors, duplicate_detector, logger, min_quality_score=0.6):
        """
        Initialize the comment verification manager.
        
        Args:
            driver: Selenium WebDriver instance
            selectors: LinkedInSelectors class
            duplicate_detector: EnhancedDuplicateDetector instance
            logger: Logger instance
            min_quality_score: Minimum quality score for comments (0-1)
        """
        self.driver = driver
        self.selectors = selectors
        self.duplicate_detector = duplicate_detector
        self.logger = logger
        self.min_quality_score = min_quality_score
        
    def verify_comment_posted(self, post_element, expected_text, wait_time=10):
        """
        Verify that a comment was successfully posted.
        
        Args:
            post_element: Post element where comment was posted
            expected_text: Expected comment text
            wait_time: Time to wait for comment to appear (seconds)
            
        Returns:
            tuple: (success, comment_element)
        """
        try:
            # Wait for comment to appear
            import time
            time.sleep(2)  # Initial wait
            
            # Find existing comments
            comments = self.selectors.find_elements_with_fallbacks(
                post_element, 
                self.selectors.EXISTING_COMMENTS_SELECTORS
            )
            
            # Check if our comment appears
            for comment in comments:
                comment_text_elements = self.selectors.find_elements_with_fallbacks(
                    comment, 
                    self.selectors.COMMENT_TEXT_SELECTORS
                )
                
                for text_element in comment_text_elements:
                    if expected_text.lower() in text_element.text.lower():
                        self.logger.log_event("comment_verified", {
                            "expected_text": expected_text[:50],
                            "found_text": text_element.text[:50]
                        })
                        return True, comment
                        
            return False, None
            
        except Exception as e:
            self.logger.log_error("comment_verification_error", str(e))
            return False, None
            
    def evaluate_comment_quality(self, comment_text, post_text):
        """
        Evaluate the quality and relevance of a comment in relation to the post.
        
        Args:
            comment_text (str): Comment text
            post_text (str): Post text
            
        Returns:
            dict: Quality evaluation results
        """
        quality_score = 0.0
        issues = []
        
        # Check comment length
        if len(comment_text) < 20:
            issues.append("Comment too short")
            quality_score -= 0.3
        elif len(comment_text) > 500:
            issues.append("Comment too long")
            quality_score -= 0.1
            
        # Check for generic phrases that don't add value
        generic_phrases = [
            "great post", "nice post", "thanks for sharing", "interesting",
            "well said", "i agree", "good point", "awesome", "love this"
        ]
        
        if any(phrase in comment_text.lower() for phrase in generic_phrases) and len(comment_text) < 60:
            issues.append("Comment too generic")
            quality_score -= 0.2
            
        # Check relevance to post
        relevance_score = 0.5  # Default neutral score
        if post_text:
            relevance_score = self._calculate_relevance(comment_text, post_text)
            
        # Check for promotional content
        promotional_patterns = [
            r'check out', r'visit my', r'my profile', r'follow me',
            r'check my', r'dm me', r'message me', r'https?://'
        ]
        
        if any(re.search(pattern, comment_text.lower()) for pattern in promotional_patterns):
            issues.append("Promotional content detected")
            quality_score -= 0.4
            
        # Check for question engagement
        if '?' in comment_text:
            quality_score += 0.2
            
        # Normalize final score to 0-1 range
        final_score = min(1.0, max(0.0, 0.7 + quality_score))
        
        return {
            "quality_score": final_score,
            "issues": issues,
            "meets_threshold": final_score >= self.min_quality_score,
            "relevance_score": relevance_score
        }
        
    def _calculate_relevance(self, comment_text, post_text):
        """
        Calculate relevance of comment to post.
        
        Args:
            comment_text (str): Comment text
            post_text (str): Post text
            
        Returns:
            float: Relevance score (0-1)
        """
        # Use the duplicate detector's semantic similarity to calculate relevance
        if hasattr(self.duplicate_detector, 'calculate_similarity'):
            similarity = self.duplicate_detector.calculate_similarity(comment_text, post_text)
            return similarity
        else:
            # Simple word overlap calculation
            comment_words = set(comment_text.lower().split())
            post_words = set(post_text.lower().split())
            
            if not comment_words or not post_words:
                return 0.0
                
            intersection = len(comment_words.intersection(post_words))
            union = len(comment_words.union(post_words))
            
            return intersection / union if union > 0 else 0.0
        
    def get_account_comments(self, max_comments=50):
        """
        Get recent comments made by the account by navigating to activity section.
        
        Args:
            max_comments (int): Maximum number of comments to retrieve
            
        Returns:
            list: List of comment data dictionaries
        """
        try:
            # Simplified implementation - return empty list
            # In a full implementation, this would navigate to the activity section
            self.logger.log_event("get_account_comments", {"max_comments": max_comments})
            return []
            
        except Exception as e:
            self.logger.log_error("get_account_comments_error", str(e))
            return []
            
    def delete_comment(self, comment_element):
        """
        Delete a comment.
        
        Args:
            comment_element: Comment element to delete
            
        Returns:
            bool: Whether deletion was successful
        """
        try:
            # Find options menu button
            options_button = self.selectors.find_element_with_fallbacks(
                comment_element, 
                self.selectors.COMMENT_OPTIONS_MENU_SELECTORS
            )
            
            if not options_button:
                return False
                
            # Click options menu
            options_button.click()
            
            # Wait a moment for menu to appear
            import time
            time.sleep(1)
            
            # Find delete button
            delete_button = self.selectors.find_element_with_fallbacks(
                self.driver, 
                self.selectors.COMMENT_DELETE_BUTTON_SELECTORS
            )
            
            if not delete_button:
                return False
                
            # Click delete
            delete_button.click()
            
            # Confirm deletion if confirmation dialog appears
            time.sleep(1)
            confirm_button = self.selectors.find_element_with_fallbacks(
                self.driver, 
                self.selectors.CONFIRM_DELETE_BUTTON_SELECTORS
            )
            
            if confirm_button:
                confirm_button.click()
                
            self.logger.log_event("comment_deleted", {"success": True})
            return True
            
        except Exception as e:
            self.logger.log_error("comment_deletion_error", str(e))
            return False
            
    def find_duplicate_comments(self, comments):
        """
        Find duplicate comments in a list of comments.
        
        Args:
            comments (list): List of comment dictionaries
            
        Returns:
            list: Groups of duplicate comments
        """
        duplicate_groups = []
        
        # Skip if less than 2 comments
        if len(comments) < 2:
            return duplicate_groups
            
        processed_indices = set()
        
        for i, comment1 in enumerate(comments):
            if i in processed_indices:
                continue
                
            group = [comment1]
            processed_indices.add(i)
            
            for j, comment2 in enumerate(comments[i+1:], i+1):
                if j in processed_indices:
                    continue
                    
                is_duplicate, score, method = self.duplicate_detector.is_duplicate(
                    comment1.get("text", ""), 
                    comment2.get("text", "")
                )
                
                if is_duplicate:
                    group.append(comment2)
                    processed_indices.add(j)
                    
            if len(group) > 1:
                duplicate_groups.append(group)
                
        return duplicate_groups
        
    def check_and_manage_comments(self, max_comments=50, delete_duplicates=True, delete_low_quality=True):
        """
        Check and manage account comments:
        1. Find all comments made by the account
        2. Evaluate quality and find duplicates
        3. Delete low-quality or duplicate comments if specified
        
        Args:
            max_comments (int): Maximum number of comments to check
            delete_duplicates (bool): Whether to delete duplicate comments
            delete_low_quality (bool): Whether to delete low-quality comments
            
        Returns:
            dict: Results of comment management
        """
        # Get account comments
        self.logger.log_event("comment_management_start", {"max_comments": max_comments})
        comments = self.get_account_comments(max_comments)
        
        if not comments:
            return {
                "comments_checked": 0,
                "duplicates_found": 0,
                "low_quality_found": 0,
                "comments_deleted": 0,
                "duplicate_groups": [],
                "low_quality_comments": []
            }
            
        self.logger.log_event("comments_found", {"count": len(comments)})
        
        # Evaluate quality
        low_quality_comments = []
        for comment in comments:
            evaluation = self.evaluate_comment_quality(
                comment.get("text", ""), 
                comment.get("post_text", "")
            )
            
            if not evaluation["meets_threshold"]:
                low_quality_comments.append({
                    "comment": comment,
                    "evaluation": evaluation
                })
                
        # Find duplicates
        duplicate_groups = self.find_duplicate_comments(comments)
        
        # Log findings
        self.logger.log_event("comment_analysis_complete", {
            "low_quality_count": len(low_quality_comments),
            "duplicate_groups": len(duplicate_groups)
        })
        
        # Delete comments if specified
        comments_deleted = 0
        
        if delete_low_quality and low_quality_comments:
            for item in low_quality_comments:
                if self.delete_comment(item["comment"].get("element")):
                    comments_deleted += 1
                    
        if delete_duplicates and duplicate_groups:
            for group in duplicate_groups:
                # Keep the first comment, delete the rest
                for comment in group[1:]:
                    if self.delete_comment(comment.get("element")):
                        comments_deleted += 1
                        
        return {
            "comments_checked": len(comments),
            "duplicates_found": sum(len(group) - 1 for group in duplicate_groups),
            "low_quality_found": len(low_quality_comments),
            "comments_deleted": comments_deleted,
            "duplicate_groups": duplicate_groups,
            "low_quality_comments": low_quality_comments
        }
