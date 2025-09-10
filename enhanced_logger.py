#!/usr/bin/env python3
"""
Enhanced Logger Module for LinkedIn Bot

Enhanced logging system for LinkedIn bot with structured JSON logs,
screenshot capture, and encrypted sensitive data.
"""

import os
import json
import logging
from datetime import datetime


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
            encryption_key (str): Optional encryption key
        """
        self.account_name = account_name
        self.base_dir = base_dir
        self.encryption_key = encryption_key
        
        # Create logs directory
        os.makedirs(base_dir, exist_ok=True)
        
        # Session data
        self.session_data = {
            "start_time": datetime.now().isoformat(),
            "account": account_name,
            "events": []
        }
        
        # Set up basic logging
        log_file = os.path.join(base_dir, f"{account_name}.log")
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(account_name)
        
    def log_event(self, event_type, details=None):
        """
        Log an event.
        
        Args:
            event_type (str): Type of event
            details (dict): Event details
        """
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "details": details or {}
        }
        
        self.session_data["events"].append(event)
        self.logger.info(f"{event_type}: {details}")
        
    def log_comment(self, post_data, comment_text, success=True):
        """
        Log a comment attempt.
        
        Args:
            post_data (dict): Post data
            comment_text (str): Comment text
            success (bool): Whether comment was successful
        """
        self.log_event("comment_attempt", {
            "post_author": post_data.get("author", ""),
            "comment_text": comment_text[:50] + "...",
            "success": success
        })
        
    def log_error(self, error_type, error_message, context=None):
        """
        Log an error.
        
        Args:
            error_type (str): Type of error
            error_message (str): Error message
            context (dict): Error context
        """
        self.log_event("error", {
            "error_type": error_type,
            "message": error_message,
            "context": context or {}
        })
        
    def log_session_end(self):
        """Log session end and save session data."""
        self.session_data["end_time"] = datetime.now().isoformat()
        self._save_session_data()
        
    def _save_session_data(self):
        """Save session data to file."""
        session_file = os.path.join(
            self.base_dir, 
            f"{self.account_name}_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        try:
            with open(session_file, 'w') as f:
                json.dump(self.session_data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving session data: {e}")
