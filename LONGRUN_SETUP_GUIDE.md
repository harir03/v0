#  LinkedIn Bot v2 - Enhanced Long Run Setup Guide

##  Overview
Enhanced LinkedIn automation bot capable of running 100+ comments per account with advanced stealth features, proxy rotation, and human behavior simulation.

##  Installation

### Step 1: Install Python Dependencies
```powershell
pip install -r requirements_longrun.txt
```

### Step 2: Install Ollama (for AI Comments)
1. Download from https://ollama.ai/download
2. Install and run: `ollama serve`
3. Pull model: `ollama pull llama3:8b`

### Step 3: Setup Chrome/Brave Browser
- Install Chrome or Brave browser
- Create separate browser profiles for each account
- Log into LinkedIn manually in each profile

##  Configuration

### 1. Basic Account Configuration
Create `longrun_bot_config.json` with your account details:
```json
{
  "accounts": [
    {
      "name": "account1",
      "username": "your-email@example.com", 
      "password": "your-password",
      "daily_comment_target": 150,
      "keywords": ["AI", "machine learning", "data science"],
      "enabled": true
    }
  ]
}
```

### 2. Proxy Configuration
Edit `proxy_config_longrun.json`:
- Add your proxy URLs with authentication
- Configure rotation strategies
- Set health check parameters

### 3. Stealth Settings
The bot includes these stealth features:
-  Human-like typing with errors and corrections
-  Random mouse movements
-  Natural scrolling patterns  
-  Proxy rotation every 15 comments
-  Session breaks every 25 comments
-  Random page browsing between comments
-  User agent rotation
-  Anti-detection measures

##  Usage

### Running Long Sessions
```python
from v1 import LongRunBot

# Configure bot
config = {
    "username": "your-email@example.com",
    "password": "your-password", 
    "account_name": "account1",
    "keywords": ["artificial intelligence", "machine learning"],
    "use_proxies": True,
    "stealth_mode": True
}

# Create and run bot
bot = LongRunBot(config)
comments_made = bot.run_long_session(target_comments=100)
print(f"Session completed: {comments_made} comments")
```

### Command Line Usage
```powershell
python v1.py --long-run --target 150 --account account1
```

##  Features

### Session Management
- **Comments per session**: 25 (configurable)
- **Session breaks**: 15-30 minutes
- **Daily limits**: 150 comments per account
- **Smart timing**: 2-5 minutes between comments

### Proxy Features
- **Multiple pools**: Residential, datacenter, mobile
- **Health monitoring**: Automatic proxy health checks
- **Intelligent rotation**: Based on performance metrics
- **Failover support**: Automatic backup proxy selection

### Human Behavior Simulation
- **Natural typing**: Variable speed with occasional errors
- **Mouse movements**: Random cursor positioning
- **Page interactions**: Feed browsing, profile viewing
- **Scroll patterns**: Human-like scrolling behavior

### Content Intelligence
- **Post quality scoring**: 50-point evaluation system
- **AI comment generation**: Contextual responses via Ollama
- **Duplicate prevention**: Never comment twice on same post
- **Author tracking**: Avoid commenting on same authors repeatedly

##  Safety Features

### Rate Limiting
- Minimum 2 minutes between comments
- Maximum 150 comments per day per account
- Automatic session breaks every 25 comments
- Daily cooldown periods

### Detection Avoidance
- Proxy rotation every 15 comments
- User agent randomization
- Canvas/WebGL fingerprint randomization
- Anti-automation script injection
- Natural behavior simulation

### Error Handling
- Automatic retry on failures
- Graceful degradation on proxy issues
- Manual intervention for CAPTCHAs
- Account health monitoring

##  Monitoring

### Real-time Stats
- Comments made per session
- Success/failure rates
- Proxy performance metrics
- Account health indicators

### Logging
- Separate logs per account
- Performance metrics tracking
- Error reporting and debugging
- Session activity summaries

##  Advanced Usage

### Multi-Account Management
```python
# Run multiple accounts simultaneously
accounts = [
    {"username": "account1@email.com", "target": 100},
    {"username": "account2@email.com", "target": 120}, 
    {"username": "account3@email.com", "target": 80}
]

for account in accounts:
    bot = LongRunBot(account)
    bot.run_long_session(target_comments=account["target"])
    time.sleep(1800)  # 30 min break between accounts
```

### Custom Scheduling
```python
import schedule

def run_account_session():
    bot = LongRunBot(config)
    bot.run_long_session(target_comments=50)

# Schedule runs
schedule.every().day.at("09:00").do(run_account_session)
schedule.every().day.at("14:00").do(run_account_session)
schedule.every().day.at("18:00").do(run_account_session)

while True:
    schedule.run_pending()
    time.sleep(60)
```

##  Troubleshooting

### Common Issues

1. **"Proxy connection failed"**
   - Check proxy credentials in config
   - Verify proxy server status
   - Test with health check URL

2. **"Login verification required"**
   - Complete verification manually
   - Use trusted IP addresses
   - Reduce automation frequency

3. **"Comment limit reached"**
   - Check daily limits in config
   - Verify timing intervals
   - Review account health status

4. **"Posts not found"**
   - Verify keywords are relevant
   - Check LinkedIn search results manually
   - Adjust post quality threshold

### Performance Optimization

1. **For faster execution**:
   - Reduce wait times (but increase risk)
   - Use datacenter proxies
   - Disable image loading

2. **For better stealth**:
   - Increase wait times
   - Use residential proxies
   - Enable all human behavior features

3. **For stability**:
   - Use fewer concurrent accounts
   - Implement longer session breaks
   - Monitor system resources

##  Support

### Best Practices
- Start with 1 account for testing
- Gradually increase targets
- Monitor logs regularly
- Keep proxies updated
- Respect LinkedIn terms of service

### Recommended Limits
- **Conservative**: 50 comments/day per account
- **Moderate**: 100 comments/day per account  
- **Aggressive**: 150 comments/day per account

Remember: Higher limits = higher detection risk
