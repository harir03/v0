#!/usr/bin/env python3
"""
Account Manager Module for LinkedIn Bot

Manages multiple LinkedIn accounts with scheduling, rotation, and health tracking.
"""

import os
import json
from datetime import datetime, timedelta


class AccountManager:
    """
    Manages multiple LinkedIn accounts with scheduling, rotation, and health tracking.
    """
    
    def __init__(self, config_file="accounts_config.json", encryption_key=None):
        """
        Initialize the account manager.
        
        Args:
            config_file (str): Path to accounts configuration file
            encryption_key (str): Optional encryption key
        """
        self.config_file = config_file
        self.encryption_key = encryption_key
        self.accounts = self._load_accounts()
        
    def _load_accounts(self):
        """
        Load account configurations from file.
        
        Returns:
            dict: Account configurations
        """
        if not os.path.exists(self.config_file):
            return {}
            
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
            
    def _save_accounts(self, accounts):
        """
        Save account configurations to file.
        
        Args:
            accounts (dict): Account configurations
        """
        try:
            with open(self.config_file, 'w') as f:
                json.dump(accounts, f, indent=2)
        except Exception as e:
            print(f"Error saving accounts: {e}")
            
    def _create_account_directories(self, account_name):
        """
        Create necessary directories for an account.
        
        Args:
            account_name (str): Name of the account
        """
        base_dir = f"accounts/{account_name}"
        directories = [
            base_dir,
            f"{base_dir}/logs",
            f"{base_dir}/data",
            f"{base_dir}/health_data",
            f"{base_dir}/comment_history"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            
    def add_account(self, account_name, username, password, **kwargs):
        """
        Add a new account.
        
        Args:
            account_name (str): Name of the account
            username (str): LinkedIn username
            password (str): LinkedIn password
            **kwargs: Additional account settings
        """
        account_config = {
            "username": username,
            "password": password,
            "enabled": True,
            "last_used": None,
            "health_score": 100,
            "created": datetime.now().isoformat(),
            **kwargs
        }
        
        self.accounts[account_name] = account_config
        self._save_accounts(self.accounts)
        self._create_account_directories(account_name)
        
    def get_account(self, account_name):
        """
        Get account configuration.
        
        Args:
            account_name (str): Name of the account
            
        Returns:
            dict: Account configuration
        """
        return self.accounts.get(account_name)
        
    def get_enabled_accounts(self):
        """
        Get all enabled accounts.
        
        Returns:
            list: List of enabled account names
        """
        return [name for name, config in self.accounts.items() if config.get("enabled", True)]
        
    def get_account_directories(self, account_name):
        """
        Get directory paths for an account.
        
        Args:
            account_name (str): Name of the account
            
        Returns:
            dict: Directory paths
        """
        base_dir = f"accounts/{account_name}"
        return {
            "base": base_dir,
            "logs": f"{base_dir}/logs",
            "data": f"{base_dir}/data",
            "health_data": f"{base_dir}/health_data",
            "comment_history": f"{base_dir}/comment_history"
        }
        
    def is_account_scheduled_now(self, account_name):
        """
        Check if account is scheduled to run now.
        
        Args:
            account_name (str): Name of the account
            
        Returns:
            bool: Whether account is scheduled
        """
        # Simple implementation - return True for now
        return True
        
    def get_scheduled_accounts(self):
        """
        Get accounts scheduled to run now.
        
        Returns:
            list: List of scheduled account names
        """
        return [name for name in self.get_enabled_accounts() 
                if self.is_account_scheduled_now(name)]
        
    def select_next_account(self):
        """
        Select the next account to use.
        
        Returns:
            str: Account name or None
        """
        enabled_accounts = self.get_enabled_accounts()
        if not enabled_accounts:
            return None
            
        # Simple selection - return first enabled account
        return enabled_accounts[0]
        
    def check_cooldown(self, account_name):
        """
        Check if account is in cooldown period.
        
        Args:
            account_name (str): Name of the account
            
        Returns:
            bool: Whether account is in cooldown
        """
        account = self.get_account(account_name)
        if not account:
            return True
            
        last_used = account.get("last_used")
        if not last_used:
            return False
            
        try:
            last_used_time = datetime.fromisoformat(last_used)
            cooldown_hours = account.get("cooldown_hours", 8)
            return datetime.now() < last_used_time + timedelta(hours=cooldown_hours)
        except (ValueError, TypeError):
            return False
            
    def update_account_last_used(self, account_name):
        """
        Update the last used timestamp for an account.
        
        Args:
            account_name (str): Name of the account
        """
        if account_name in self.accounts:
            self.accounts[account_name]["last_used"] = datetime.now().isoformat()
            self._save_accounts(self.accounts)
            
    def update_account_health(self, account_name, health_score):
        """
        Update the health score for an account.
        
        Args:
            account_name (str): Name of the account
            health_score (int): Health score (0-100)
        """
        if account_name in self.accounts:
            self.accounts[account_name]["health_score"] = health_score
            self._save_accounts(self.accounts)
            
    def disable_account(self, account_name):
        """
        Disable an account.
        
        Args:
            account_name (str): Name of the account
        """
        if account_name in self.accounts:
            self.accounts[account_name]["enabled"] = False
            self._save_accounts(self.accounts)
