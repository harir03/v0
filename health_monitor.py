#!/usr/bin/env python3
"""
Health Monitor Module for LinkedIn Bot

Monitors the health of a LinkedIn account by tracking activity patterns,
captchas, warnings, and other signals that may indicate risk.
"""

import os
import json
from datetime import datetime, timedelta


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
