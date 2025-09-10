#!/usr/bin/env python3
"""
LinkedIn Bot v2 - Quick Setup Script
Helps configure the bot for long runs
"""

import json
import os

def create_sample_config():
    """Create sample configuration files."""
    
    # Sample bot configuration
    bot_config = {
        "long_run_config": {
            "max_comments_per_account": 150,
            "session_management": {
                "comments_per_session": 25,
                "session_break_duration": [900, 1800],
                "daily_session_limit": 6
            },
            "stealth_timing": {
                "min_comment_interval": [120, 300],
                "typing_speed": {"min_chars_per_second": 2, "max_chars_per_second": 8}
            }
        },
        "accounts": [
            {
                "name": "account1",
                "username": "your-email@example.com",
                "password": "your-password",
                "proxy_pool": "premium_residential",
                "daily_comment_target": 150,
                "keywords": [
                    "artificial intelligence",
                    "machine learning", 
                    "data science",
                    "python programming",
                    "software engineering"
                ],
                "enabled": True
            }
        ],
        "ollama_config": {
            "enabled": True,
            "api_url": "http://localhost:11434/api/generate",
            "model": "llama3:8b"
        }
    }
    
    # Sample proxy configuration
    proxy_config = {
        "proxy_pools": {
            "premium_residential": {
                "name": "Premium Residential Proxies",
                "rotation_method": "health_based",
                "proxies": [
                    {
                        "url": "http://username:password@proxy1.provider.com:8080",
                        "location": "US-East",
                        "type": "residential",
                        "enabled": True
                    },
                    {
                        "url": "http://username:password@proxy2.provider.com:8080", 
                        "location": "US-West",
                        "type": "residential",
                        "enabled": True
                    }
                ]
            }
        },
        "proxy_settings": {
            "global_enabled": True,
            "health_check_url": "https://httpbin.org/ip",
            "rotation_strategy": "health_based",
            "fallback_to_direct": True
        }
    }
    
    # Write configuration files
    with open("longrun_bot_config.json", "w") as f:
        json.dump(bot_config, f, indent=2)
    
    with open("proxy_config_longrun.json", "w") as f:
        json.dump(proxy_config, f, indent=2)
        
    print(" Sample configuration files created:")
    print("   - longrun_bot_config.json")
    print("   - proxy_config_longrun.json")

def main():
    """Main setup function."""
    print(" LinkedIn Bot v2 - Quick Setup")
    print("=" * 50)
    
    # Create sample configs
    create_sample_config()
    
    print("\n Next Steps:")
    print("1. Edit longrun_bot_config.json with your account details")
    print("2. Configure proxy_config_longrun.json with your proxies")
    print("3. Install dependencies: pip install -r requirements_longrun.txt")
    print("4. Setup Ollama: ollama serve && ollama pull llama3:8b")
    print("5. Run: python run_longrun.py --target 100")
    
    print("\n Usage Examples:")
    print("   Test run:           python run_longrun.py --test")
    print("   Specific account:   python run_longrun.py --account account1 --target 50")
    print("   All accounts:       python run_longrun.py --target 150")
    
    print("\n Important Notes:")
    print("   - Start with small targets (10-20 comments) for testing")
    print("   - Configure proxies for better stealth")
    print("   - Monitor logs for any issues")
    print("   - Respect LinkedIn's terms of service")

if __name__ == "__main__":
    main()
