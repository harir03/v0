#!/usr/bin/env python3
import os
import json
import random
import requests
from datetime import datetime, timedelta

class KeywordPerformanceTracker:
    def __init__(self, initial_keyword=None, storage_file=None, rotation_threshold=25, ollama_url=None):
        self.rotation_threshold = rotation_threshold
        self.storage_file = storage_file
        self.ollama_url = ollama_url
        self.keyword_data = {}
        self.current_keyword = initial_keyword
        
    def update_search_stats(self, keyword, results_count):
        if keyword not in self.keyword_data:
            self.keyword_data[keyword] = {"searches": 0, "search_results": 0, "comments_attempted": 0, "comments_successful": 0}
        self.keyword_data[keyword]["searches"] += 1
        self.keyword_data[keyword]["search_results"] += results_count
        
    def update_comment_stats(self, keyword, success=True, attempted=True):
        if keyword not in self.keyword_data:
            self.keyword_data[keyword] = {"searches": 0, "search_results": 0, "comments_attempted": 0, "comments_successful": 0}
        if attempted:
            self.keyword_data[keyword]["comments_attempted"] += 1
        if success:
            self.keyword_data[keyword]["comments_successful"] += 1
            
    def should_rotate_keyword(self, keyword):
        return False
        
    def select_next_keyword(self, current_keyword=None):
        return current_keyword or "AI"
