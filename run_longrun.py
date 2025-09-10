#!/usr/bin/env python3
"""
LinkedIn Bot v2 - Long Run Launcher
Easy launcher for extended commenting sessions
"""

import json
import time
import random
import argparse
from datetime import datetime
from v1 import LongRunBot

def load_config(config_file="longrun_bot_config.json"):
    """Load long run configuration."""
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f" Config file not found: {config_file}")
        return None

def run_single_account(account_config, target_comments=100):
    """Run long session for a single account."""
    print(f"\n Starting long run for {account_config['name']}")
    print(f" Target: {target_comments} comments")
    
    # Configure bot
    bot_config = {
        "username": account_config["username"],
        "password": account_config["password"],
        "account_name": account_config["name"],
        "keywords": account_config.get("keywords", ["AI"]),
        "use_proxies": True,
        "stealth_mode": True,
        "proxy_pool": account_config.get("proxy_pool", "premium_residential")
    }
    
    # Create and run bot
    bot = LongRunBot(bot_config)
    
    try:
        comments_made = bot.run_long_session(target_comments=target_comments)
        print(f" Session completed for {account_config['name']}: {comments_made} comments")
        return comments_made
    except Exception as e:
        print(f" Error in session for {account_config['name']}: {e}")
        return 0

def run_multi_account(config, target_comments=100):
    """Run long sessions for multiple accounts."""
    accounts = config.get("accounts", [])
    enabled_accounts = [acc for acc in accounts if acc.get("enabled", True)]
    
    print(f" Running {len(enabled_accounts)} accounts with {target_comments} comments each")
    
    total_comments = 0
    
    for i, account in enumerate(enabled_accounts):
        print(f"\n Account {i+1}/{len(enabled_accounts)}: {account['name']}")
        
        # Run account session
        account_target = account.get("daily_comment_target", target_comments)
        comments = run_single_account(account, account_target)
        total_comments += comments
        
        # Break between accounts (except last one)
        if i < len(enabled_accounts) - 1:
            break_time = random.randint(1800, 3600)  # 30-60 minutes
            print(f" Break between accounts: {break_time // 60} minutes")
            time.sleep(break_time)
    
    print(f"\n All accounts completed. Total comments: {total_comments}")
    return total_comments

def main():
    """Main launcher function."""
    parser = argparse.ArgumentParser(description="LinkedIn Bot v2 Long Run Launcher")
    parser.add_argument("--config", default="longrun_bot_config.json", help="Config file path")
    parser.add_argument("--target", type=int, default=100, help="Target comments per account")
    parser.add_argument("--account", help="Run specific account only")
    parser.add_argument("--test", action="store_true", help="Run in test mode (5 comments)")
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    if not config:
        return
    
    # Test mode
    if args.test:
        print(" Running in test mode (5 comments)")
        args.target = 5
    
    print("=" * 60)
    print(" LinkedIn Bot v2 - Long Run Session")
    print(f" Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Run specific account or all accounts
    if args.account:
        # Find specific account
        account = None
        for acc in config.get("accounts", []):
            if acc["name"] == args.account:
                account = acc
                break
        
        if account:
            run_single_account(account, args.target)
        else:
            print(f" Account '{args.account}' not found in config")
    else:
        # Run all enabled accounts
        run_multi_account(config, args.target)
    
    print("\n" + "=" * 60)
    print(f" Session completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

if __name__ == "__main__":
    main()
