# LinkedIn Bot v1 - Multi-Account Scheduler Platform

## Overview

This is a complete upgrade from the basic v0 LinkedIn bot to a sophisticated multi-account automation platform. Instead of a single script that requires manual execution, v1 is an entire command center that can manage multiple LinkedIn accounts simultaneously with automated scheduling, resource monitoring, and self-healing capabilities.

## 🚀 Key Features

### 1. 🧠 Multi-Account Management
- **Central Configuration**: All accounts managed through `accounts_config.json`
- **Profile Isolation**: Each account uses separate browser profiles
- **Independent Settings**: Unique search queries, schedules, and settings per account
- **Easy Scaling**: Add new accounts without modifying code

### 2. 📅 Automated Scheduling  
- **Cron-like Scheduling**: Set specific days and times for each account
- **Natural Patterns**: Staggered execution to mimic human behavior
- **Background Operation**: Runs continuously without manual intervention
- **Flexible Timing**: Multiple time slots per day for each account

### 3. 🚀 Concurrent Operations
- **Parallel Execution**: Multiple accounts run simultaneously
- **Thread Management**: Safe multi-threading with proper isolation
- **Resource-Aware**: Monitors system load and adjusts accordingly
- **Staggered Starts**: Avoids simultaneous launches

### 4. 📚 Persistent Memory
- **Account-Specific History**: Separate comment history per account
- **Duplicate Prevention**: Never comments on the same post twice
- **Cross-Session Memory**: Remembers across restarts
- **Content Hashing**: Detects similar content to avoid repetition

### 5. 🛡️ Advanced Security & Reliability
- **Proxy Support**: Built-in proxy rotation and health checking
- **Headless/Visible Toggle**: Automatic fallback to visible mode on failures
- **Resource Monitoring**: CPU/RAM monitoring with throttling
- **Self-Healing**: Automatic restart of failed accounts
- **Failure Management**: Auto-disable problematic accounts

### 6. 📝 Professional Logging
- **Centralized Logging**: Main bot operations in `main_bot.log`
- **Account-Specific Logs**: Detailed logs per account
- **Timestamped Events**: Full audit trail of all activities
- **Error Tracking**: Comprehensive error reporting and debugging

### 7. 🎮 Interactive Management
- **Menu-Driven Interface**: Easy-to-use command-line interface
- **Real-Time Control**: Start, stop, and monitor operations
- **Account Management**: Add, edit, enable/disable accounts
- **System Monitoring**: View resource usage and status

## 📁 File Structure

```
v0/
├── v1.py                     # Main bot application
├── accounts_config.json      # Account configurations
├── logs/                     # Log files directory
│   ├── main_bot.log         # Main scheduler logs
│   └── account_*.log        # Individual account logs
├── account_histories/        # Comment history per account
│   └── comment_history_*.json
└── screenshots/             # Screenshot storage
```

## 🔧 Installation & Setup

### Prerequisites
```bash
pip install selenium schedule psutil requests
```

### Initial Setup
1. **Clone the repository**
2. **Run the bot**: `python3 v1.py`
3. **Configure accounts** through the menu system
4. **Set up browser profiles** for each account (manual login required)

### Browser Configuration
- Each account requires a separate browser profile
- Accounts must be logged into LinkedIn in their respective profiles
- The bot reuses existing login sessions

## ⚙️ Configuration

### Account Configuration (`accounts_config.json`)
```json
{
  "accounts": [
    {
      "name": "Account 1",
      "profile_directory": "Profile 1",
      "browser_path": "/usr/bin/google-chrome",
      "user_data_dir": "~/.config/google-chrome",
      "search_queries": ["AI development", "machine learning"],
      "comments_per_session": 5,
      "enabled": true,
      "headless": false,
      "user_agent": null,
      "window_size": null,
      "proxies": {
        "primary": "http://user:pass@proxy:port",
        "backups": ["http://user:pass@backup1:port"]
      },
      "schedule": {
        "days": ["monday", "wednesday", "friday"],
        "times": ["09:00", "15:00"]
      },
      "behavior": {
        "like_probability": 0.1,
        "scroll_probability": 0.15,
        "read_probability": 0.05
      }
    }
  ]
}
```

### Configuration Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `name` | Unique account identifier | "Marketing Account" |
| `profile_directory` | Browser profile folder | "Profile 1" |
| `browser_path` | Path to browser executable | "/usr/bin/google-chrome" |
| `user_data_dir` | Browser user data directory | "~/.config/google-chrome" |
| `search_queries` | LinkedIn search terms | ["AI", "ML"] |
| `comments_per_session` | Max comments per run | 5 |
| `enabled` | Account active status | true/false |
| `headless` | Run without UI | true/false |
| `user_agent` | Custom user agent (null = random) | null or "Mozilla/5.0..." |
| `window_size` | Browser window size (null = random) | null or "1920,1080" |
| `proxies` | Proxy configuration | See above |
| `schedule` | When to run | See above |
| `behavior` | Behavioral randomization settings | See below |

### Behavioral Configuration

| Parameter | Description | Range | Default |
|-----------|-------------|-------|---------|
| `like_probability` | Chance to like instead of comment | 0.0-1.0 | 0.1 |
| `scroll_probability` | Chance to scroll/read instead of comment | 0.0-1.0 | 0.15 |
| `read_probability` | Chance to just read instead of comment | 0.0-1.0 | 0.05 |

## 🎮 Usage

### Main Menu Options

1. **🕐 Start Scheduler Mode**: Automated scheduling mode
2. **🚀 Run All Accounts Now**: Immediate execution for testing
3. **👤 Run Single Account**: Test individual accounts
4. **⚙️ Manage Accounts**: Add/edit/enable accounts
5. **📊 View System Status**: Monitor resources and activity
6. **📝 View Logs**: Access log files
7. **❌ Exit**: Stop the application

### Running Modes

#### Scheduler Mode (Recommended)
```bash
python3 v1.py
# Choose option 1
```
- Runs continuously in background
- Executes accounts according to their schedules
- Monitors system health and resources
- Automatically recovers from failures

#### Manual Testing Mode
```bash
python3 v1.py  
# Choose option 2 or 3
```
- Run all accounts immediately
- Test individual accounts
- Debug configuration issues

## 🛡️ Advanced Features

### Resource Management
- **CPU Monitoring**: Pauses execution when CPU > 85%
- **Memory Monitoring**: Pauses execution when RAM > 85%
- **Adaptive Throttling**: Automatically adjusts based on system load

### Proxy Management
- **Enhanced Health Checking**: Tests both connectivity and LinkedIn accessibility
- **LinkedIn-Specific Validation**: Verifies proxies can reach LinkedIn endpoints
- **Automatic Rotation**: Switches to backup proxies on failure
- **Direct Fallback**: Uses direct connection if all proxies fail

### Anti-Detection & Security
- **Browser Fingerprinting**: Randomized user agents and window sizes
- **Human-like Timing**: 1-15 minute random jitter on all scheduled times
- **Behavioral Randomization**: Mix of commenting, liking, scrolling, and reading
- **IP Diversity**: Proxy rotation prevents single IP footprint detection
- **Adaptive Patterns**: Variable timing and actions mimic human behavior

### Self-Healing Protocol
- **Heartbeat Monitoring**: Detects unresponsive accounts
- **Automatic Restart**: Restarts frozen accounts after timeout
- **Failure Tracking**: Disables accounts after 3 consecutive failures
- **Mode Switching**: Switches to visible mode after headless failures

### Security Measures
- **Advanced Anti-Detection**: Multiple layers of automation hiding
- **Randomized Browser Fingerprints**: Unique user agents and window sizes per account
- **Human-like Behavioral Patterns**: Variable actions beyond just commenting
- **Intelligent Timing Jitter**: 1-15 minute randomization on all schedules
- **Profile Isolation**: Complete separation between accounts
- **Session Persistence**: Reuses existing login sessions
- **Proxy Validation**: LinkedIn-specific connectivity testing

## 📊 Monitoring & Debugging

### Log Files
- **main_bot.log**: Scheduler events, system status, job launches
- **account_[name].log**: Detailed activity per account
- **Error levels**: INFO, WARNING, ERROR for different event types

### System Status
- Real-time CPU and memory usage
- List of currently running accounts
- Heartbeat status for active operations
- Resource health indicators

### Performance Metrics
- Comments made per account
- Success/failure rates  
- Processing speed and efficiency
- Resource utilization over time

## 🔒 Security & Compliance

### Rate Limiting
- Configurable comments per session
- Random delays between actions
- Respect for LinkedIn's usage policies
- Human-like interaction patterns

### Data Protection
- Local storage only (no cloud uploads)
- Encrypted comment history
- Secure proxy authentication
- Privacy-focused design

### LinkedIn Compliance
- Respectful automation practices
- No spam or inappropriate content
- Professional comment generation
- Account-specific personalization

## 🆚 v0 vs v1 Comparison

| Feature | v0 (Basic Bot) | v1 (Platform) |
|---------|----------------|---------------|
| Accounts | Single | Multiple |
| Execution | Manual | Scheduled |
| Memory | Session-only | Persistent |
| Monitoring | None | Advanced |
| Recovery | Manual | Automatic |
| Interface | Command-line | Menu-driven |
| Logging | Basic | Professional |
| Scalability | Limited | Enterprise |

## 🚨 Important Notes

### Prerequisites
- Ollama must be running with a compatible model
- Browser profiles must be set up with LinkedIn logins
- Sufficient system resources for concurrent operations

### Limitations
- Requires manual browser profile setup
- LinkedIn rate limits still apply
- System resource dependent
- Platform-specific browser paths

### Best Practices
- Start with single account testing
- Monitor logs regularly for issues
- Keep comment counts reasonable
- Update configurations as needed
- Regular system resource monitoring

## 🛠️ Troubleshooting

### Common Issues

1. **"Account not logged in"**
   - Ensure LinkedIn is logged in for the browser profile
   - Check profile directory paths
   - Verify browser executable location

2. **"Ollama connection failed"**
   - Start Ollama service: `ollama serve`
   - Pull required model: `ollama pull llama3.2:3b`
   - Check Ollama is running on port 11434

3. **"System resources low"**
   - Close unnecessary applications
   - Reduce concurrent account limits
   - Monitor with system status option

4. **"Proxy health check failed"**
   - Verify proxy credentials and connectivity
   - Check backup proxy configurations
   - Consider direct connection fallback

## 📈 Future Enhancements

Potential improvements for future versions:
- Web-based dashboard interface
- Database integration for analytics
- Advanced AI comment personalization
- Integration with CRM systems
- Mobile app for monitoring
- Cloud deployment options

---

**Note**: This bot is designed for professional networking and should be used responsibly in accordance with LinkedIn's Terms of Service. Always ensure your automation practices comply with platform guidelines and respect other users' experience.