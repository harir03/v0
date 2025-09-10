#!/usr/bin/env python3
"""
Comment History Module for LinkedIn Bot

Tracks comment history for a LinkedIn account, preventing duplicate
comments and maintaining a searchable comment database.
"""

import os
import json
import hashlib
import base64
from datetime import datetime, timedelta

# Check for cryptography availability
try:
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("Cryptography package not available. Encryption features will be disabled.")


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
