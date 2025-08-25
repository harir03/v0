import os
import time
import uuid
import json
import requests
import hashlib
import random
import schedule
import threading
import psutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
import logging
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException, WebDriverException

# --- Constants ---
LINKEDIN_URL = "https://www.linkedin.com"
SEARCH_URL_TEMPLATE = "https://www.linkedin.com/search/results/content/?keywords={query}"
OLLAMA_URL = "http://localhost:11434/api/generate"
ACCOUNTS_CONFIG_FILE = "accounts_config.json"
SCHEDULER_CONFIG_FILE = "scheduler_config.json"
LOGS_DIR = "logs"

# Create necessary directories
for directory in ["screenshots", "logs", "account_histories"]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# --- Logging Setup ---
def setup_logging():
    """Setup logging for the multi-account bot"""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Main logger
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(os.path.join(LOGS_DIR, 'main_bot.log')),
            logging.StreamHandler()
        ]
    )
    
    # Account-specific loggers will be created dynamically
    return logging.getLogger('LinkedInBot')

# --- Account Configuration Manager ---
class AccountConfigManager:
    def __init__(self):
        self.config_file = ACCOUNTS_CONFIG_FILE
        self.accounts = self.load_accounts()
    
    def load_accounts(self):
        """Load account configurations from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ Could not load accounts config: {e}")
        
        # Default configuration
        return {
            "accounts": [
                {
                    "name": "Account 1",
                    "profile_directory": "Profile 1",
                    "browser_path": "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe",
                    "user_data_dir": "~/AppData/Local/BraveSoftware/Brave-Browser/User Data",
                    "search_queries": ["AI development", "machine learning"],
                    "comments_per_session": 5,
                    "enabled": True,
                    "headless": False,
                    "proxies": {
                        "primary": None,
                        "backups": []
                    },
                    "schedule": {
                        "days": ["monday", "wednesday", "friday"],
                        "times": ["09:00", "15:00"]
                    }
                }
            ]
        }
    
    def save_accounts(self):
        """Save account configurations to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.accounts, f, indent=2)
            print(f"💾 Saved account configurations to {self.config_file}")
        except Exception as e:
            print(f"⚠️ Could not save accounts config: {e}")
    
    def add_account(self, account_config):
        """Add a new account configuration"""
        self.accounts["accounts"].append(account_config)
        self.save_accounts()
    
    def get_enabled_accounts(self):
        """Get list of enabled accounts"""
        return [acc for acc in self.accounts["accounts"] if acc.get("enabled", True)]
    
    def update_account_setting(self, account_name, key, value):
        """Update a specific setting for an account"""
        for account in self.accounts["accounts"]:
            if account["name"] == account_name:
                account[key] = value
                self.save_accounts()
                return True
        return False

# --- Enhanced Post Tracking Class (Account-Specific) ---
class PostTracker:
    def __init__(self, account_name="default"):
        self.account_name = account_name
        self.history_file = f"account_histories/comment_history_{account_name.replace(' ', '_')}.json"
        self.processed_posts = set()
        self.commented_posts = set()
        self.failed_posts = set()
        self.post_signatures = {}
        self.comment_history = self.load_comment_history()
        self.user_name = None
    
    def load_comment_history(self):
        """Load persistent comment history from account-specific file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"📚 [{self.account_name}] Loaded {len(data.get('commented_posts', []))} previously commented posts")
                    return data
        except Exception as e:
            print(f"⚠️ [{self.account_name}] Could not load comment history: {e}")
        return {"commented_posts": [], "post_urls": set(), "post_content_hashes": set()}
    
    def save_comment_history(self):
        """Save comment history to account-specific file"""
        try:
            history_to_save = {
                "commented_posts": list(self.comment_history.get("commented_posts", [])),
                "post_urls": list(self.comment_history.get("post_urls", set())),
                "post_content_hashes": list(self.comment_history.get("post_content_hashes", set()))
            }
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history_to_save, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ [{self.account_name}] Could not save comment history: {e}")
    
    def is_processed(self, post_id):
        return post_id in self.processed_posts
    
    def mark_processed(self, post_id, signature=None):
        self.processed_posts.add(post_id)
        if signature: 
            self.post_signatures[post_id] = signature
    
    def mark_commented(self, post_id, signature=None, post_url=None, content_hash=None):
        self.commented_posts.add(post_id)
        self.processed_posts.add(post_id)
        if signature: 
            self.post_signatures[post_id] = signature
        
        # Add to persistent history
        self.comment_history["commented_posts"].append({
            "post_id": post_id,
            "timestamp": time.time(),
            "signature": signature,
            "post_url": post_url,
            "content_hash": content_hash,
            "account": self.account_name
        })
        
        if post_url:
            if isinstance(self.comment_history["post_urls"], list):
                self.comment_history["post_urls"] = set(self.comment_history["post_urls"])
            self.comment_history["post_urls"].add(post_url)
        
        if content_hash:
            if isinstance(self.comment_history["post_content_hashes"], list):
                self.comment_history["post_content_hashes"] = set(self.comment_history["post_content_hashes"])
            self.comment_history["post_content_hashes"].add(content_hash)
        
        self.save_comment_history()
    
    def mark_failed(self, post_id, signature=None):
        self.failed_posts.add(post_id)
        self.processed_posts.add(post_id)
        if signature: 
            self.post_signatures[post_id] = signature
    
    def is_duplicate_signature(self, signature):
        return signature in self.post_signatures.values()
    
    def has_commented_on_content(self, content_hash):
        """Check if we've commented on similar content before"""
        post_hashes = self.comment_history.get("post_content_hashes", set())
        if isinstance(post_hashes, list):
            post_hashes = set(post_hashes)
        return content_hash in post_hashes
    
    def has_commented_on_url(self, post_url):
        """Check if we've commented on this URL before"""
        post_urls = self.comment_history.get("post_urls", set())
        if isinstance(post_urls, list):
            post_urls = set(post_urls)
        return post_url in post_urls
    
    def get_stats(self):
        return {
            "processed": len(self.processed_posts), 
            "commented": len(self.commented_posts), 
            "failed": len(self.failed_posts),
            "historical_comments": len(self.comment_history.get("commented_posts", []))
        }

# --- Resource Monitor ---
class ResourceMonitor:
    def __init__(self, cpu_threshold=85, memory_threshold=85):
        self.cpu_threshold = cpu_threshold
        self.memory_threshold = memory_threshold
    
    def check_system_health(self):
        """Check if system resources are available"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        
        return {
            "cpu_percent": cpu_percent,
            "memory_percent": memory_percent,
            "healthy": cpu_percent < self.cpu_threshold and memory_percent < self.memory_threshold
        }

# --- Proxy Health Checker ---
class ProxyHealthChecker:
    def __init__(self, timeout=10):
        self.timeout = timeout
    
    def check_proxy_health(self, proxy_url):
        """Check if a proxy is healthy and working"""
        if not proxy_url:
            return True  # No proxy means direct connection
        
        try:
            proxies = {'http': proxy_url, 'https': proxy_url}
            response = requests.get('https://httpbin.org/ip', 
                                  proxies=proxies, 
                                  timeout=self.timeout)
            return response.status_code == 200
        except Exception as e:
            print(f"⚠️ Proxy health check failed for {proxy_url}: {e}")
            return False
    
    def get_healthy_proxy(self, proxy_config):
        """Get a healthy proxy from the configuration"""
        primary = proxy_config.get("primary")
        backups = proxy_config.get("backups", [])
        
        # Check primary proxy first
        if self.check_proxy_health(primary):
            return primary
        
        # Check backup proxies
        for backup in backups:
            if self.check_proxy_health(backup):
                return backup
        
        return None  # No healthy proxy found

# --- Import existing functions from v0.py ---
def detect_current_user(driver):
    """Detect the current LinkedIn user"""
    try:
        # Try multiple selectors to find the user's name
        selectors = [
            "//span[contains(@class, 'nav-item__profile-member-photo')]/..//span[contains(@class, 'break-words')]",
            "//div[contains(@class, 'global-nav__me')]//span[contains(@class, 'break-words')]",
            "//button[contains(@class, 'global-nav__primary-link')]//span[contains(@class, 'break-words')]"
        ]
        
        for selector in selectors:
            try:
                user_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                user_name = user_element.text.strip()
                if user_name and len(user_name) > 2:
                    return user_name
            except:
                continue
        
        return "Unknown User"
    except Exception as e:
        print(f"⚠️ Could not detect current user: {e}")
        return "Unknown User"

# --- Ollama Comment Generator Class ---
class OllamaCommentGenerator:
    """Generates custom comments and related keywords using the Ollama local LLM service."""
    def __init__(self, model_name="llama3.2:3b", ollama_url=OLLAMA_URL):
        self.model_name = model_name
        self.ollama_url = ollama_url
        self.test_connection() # Test connection on initialization
    
    def test_connection(self):
        """Test if Ollama is running and the specified model is available."""
        try:
            # Attempt to connect to Ollama's API to list models
            response = requests.get(f"{self.ollama_url.rsplit('/', 1)[0]}/tags", timeout=5)
            if response.status_code == 200:
                print("✅ Ollama connection successful.")
                models = response.json().get("models", [])
                model_names = [m["name"] for m in models]
                if self.model_name not in model_names:
                    print(f"⚠️ Model '{self.model_name}' not found. Available models: {model_names}")
                    if model_names:
                        self.model_name = model_names[0] # Fallback to the first available model
                        print(f"🔄 Using model: {self.model_name}")
                    else:
                        raise Exception("No Ollama models found. Please pull a model (e.g., 'ollama pull llama3.2:3b').")
            else:
                raise Exception(f"Ollama not responding (Status: {response.status_code})")
        except requests.exceptions.ConnectionError:
            print(f"❌ Ollama connection failed: Connection refused. Is Ollama running at {self.ollama_url}?")
            print("Please ensure Ollama is running on localhost:11434 and the model is pulled.")
            raise
        except Exception as e:
            print(f"❌ Ollama connection failed: {e}")
            print("Please ensure Ollama is running on localhost:11434 and the model is pulled.")
            raise
    
    def generate_comment(self, post_text, author_name=None, post_type="general", retries=3):
        """Generate a custom comment based on post content"""
        cleaned_text = self.extract_actual_content(post_text)
        
        for attempt in range(retries + 1):
            prompt = f"""
You are writing a professional and insightful LinkedIn comment. Be authentic, engaging, and add value to the conversation.

POST CONTENT:
{cleaned_text[:1000]}

AUTHOR: {author_name or "The author"}

Write a thoughtful comment that:
- Is 10-30 words long.
- Clearly shows you read and understood the post.
- Asks a relevant, open-ended question OR shares a brief, constructive insight.
- Sounds natural, conversational, and professional.
- Avoids generic phrases like "Great post!", "Thanks for sharing!", or "Good job!".
- Does not include emojis unless specifically relevant and professional.

Comment:
"""
            if attempt > 0:
                prompt += f"\n\nPrevious comment failed validation. Please ensure the comment is strictly between 10 and 30 words."

            try:
                payload = {
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.8,
                        "top_p": 0.9,
                        "max_tokens": 25,
                        "stop": ["\n\n", "Comment:", "Response:", "Reply:"]
                    }
                }
                
                response = requests.post(self.ollama_url, json=payload, timeout=45)
                
                if response.status_code == 200:
                    result = response.json()
                    comment = result.get("response", "").strip()
                    comment = self.clean_comment(comment)
                    
                    if self.is_valid_comment(comment):
                        return comment
                    else:
                        print(f"⚠️ Generated comment failed validation: '{comment}'")
                else:
                    print(f"❌ Ollama API error: {response.status_code} - {response.text}")
                    return None
                    
            except requests.exceptions.Timeout:
                print("❌ Error generating comment: Ollama request timed out.")
            except Exception as e:
                print(f"❌ Unexpected error generating comment: {e}")
                return None
        
        print(f"❌ Failed to generate a valid comment after {retries+1} attempts.")
        return None
    
    def extract_actual_content(self, post_text):
        """Extract core content from LinkedIn post text"""
        lines = post_text.split('\n')
        content_lines = []
        
        skip_patterns = [
            '• 1st', '• 2nd', '• 3rd', 'Feed post', 'Like', 'Comment', 'Repost', 'Share', 'Send',
            'views', 'reactions', 'comments', 'Follow', 'Connect', 'Message',
            'ago', 'min', 'hour', 'day', 'week', 'month', 'year',
            'promoted', 'Ad', 'Show all reactions', 'See all comments'
        ]
        
        for line in lines:
            line = line.strip()
            if len(line) > 10 and not any(pattern.lower() in line.lower() for pattern in skip_patterns):
                content_lines.append(line)
        
        return ' '.join(content_lines)
    
    def clean_comment(self, comment):
        """Clean up generated comment"""
        comment = comment.strip('"').strip("'").strip()
        if comment.startswith("Comment:"):
            comment = comment[8:].strip()
        return comment
    
    def is_valid_comment(self, comment):
        """Validate if comment meets requirements"""
        if not comment or len(comment.strip()) < 10:
            return False
        
        words = comment.split()
        if len(words) < 10 or len(words) > 30:
            return False
        
        generic_phrases = [
            "great post", "thanks for sharing", "good job", "nice work", "well said",
            "totally agree", "so true", "exactly", "love this", "awesome"
        ]
        
        comment_lower = comment.lower()
        if len(words) <= 5 and comment_lower in [phrase.lower() for phrase in generic_phrases]:
            return False
        
        return True

# --- Core LinkedIn Functions (adapted from v0.py) ---
def create_post_signature(post_text, author_name):
    """Create a unique signature for a post based on content and author"""
    combined = f"{post_text.strip()}-{author_name.strip()}"
    return hashlib.md5(combined.encode('utf-8')).hexdigest()

def get_robust_post_id(post_element, driver):
    """Generate a robust post ID"""
    try:
        element_html = post_element.get_attribute('outerHTML')[:200]
        return f"element-{hashlib.md5(element_html.encode()).hexdigest()[:10]}"
    except StaleElementReferenceException:
        raise
    except Exception as e:
        print(f"⚠️ Error getting robust post ID: {e}")
        return f"fallback-{uuid.uuid4().hex[:10]}"

def apply_post_filter(driver):
    """Apply post filter to show only posts"""
    try:
        filter_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Posts')]"))
        )
        driver.execute_script("arguments[0].click();", filter_button)
        time.sleep(3)
    except:
        print("⚠️ Could not apply post filter")

def scroll_feed(driver, target_posts=20, delay_per_scroll=3):
    """Scroll the feed to load more posts"""
    for i in range(max(target_posts // 3, 5)):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay_per_scroll)

def find_posts_improved(driver):
    """Find all post elements on the page"""
    post_selectors = [
        "//div[contains(@class, 'feed-shared-update-v2')]",
        "//div[contains(@class, 'update-components-text')]//ancestor::div[contains(@class, 'feed-shared-update-v2')]",
        "//article[contains(@class, 'relative')]"
    ]
    
    for selector in post_selectors:
        try:
            posts = driver.find_elements(By.XPATH, selector)
            if posts:
                print(f"📋 Found {len(posts)} posts using selector: {selector}")
                return posts
        except Exception as e:
            print(f"⚠️ Error with selector {selector}: {e}")
    
    return []

def extract_post_data(post_element, driver):
    """Extract data from a post element"""
    try:
        # Extract post text
        text_selectors = [
            ".//div[contains(@class, 'feed-shared-text')]//span[@dir='ltr']",
            ".//div[contains(@class, 'update-components-text')]//span[@dir='ltr']",
            ".//div[contains(@class, 'feed-shared-text')]"
        ]
        
        post_text = ""
        for selector in text_selectors:
            try:
                text_elements = post_element.find_elements(By.XPATH, selector)
                if text_elements:
                    post_text = ' '.join([elem.text.strip() for elem in text_elements if elem.text.strip()])
                    break
            except:
                continue
        
        # Extract author name
        author_selectors = [
            ".//a[contains(@class, 'feed-shared-actor__name')]/span[@aria-hidden='true']",
            ".//span[contains(@class, 'actor-name')]",
            ".//h3//span[@aria-hidden='true']"
        ]
        
        author_name = ""
        for selector in author_selectors:
            try:
                author_element = post_element.find_element(By.XPATH, selector)
                author_name = author_element.text.strip()
                if author_name and len(author_name) > 2:
                    break
            except:
                continue
        
        post_id = get_robust_post_id(post_element, driver)
        signature = create_post_signature(post_text, author_name or "Unknown")
        
        return {
            "id": post_id,
            "text": post_text,
            "author": author_name,
            "signature": signature,
            "element": post_element
        }
        
    except Exception as e:
        print(f"⚠️ Error extracting post data: {e}")
        return None

# --- Scheduler Class ---
class LinkedInBotScheduler:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.running_accounts = {}
        self.logger = setup_logging()
        self.scheduler_running = False
        self.resource_monitor = ResourceMonitor()
        self.proxy_checker = ProxyHealthChecker()
        self.agent_heartbeats = {}
        self.failure_counts = {}
        
    def setup_schedules(self):
        """Setup schedules for all enabled accounts"""
        schedule.clear()
        
        accounts = self.config_manager.get_enabled_accounts()
        for account in accounts:
            account_schedule = account.get("schedule", {})
            days = account_schedule.get("days", [])
            times = account_schedule.get("times", [])
            
            for day in days:
                for time_str in times:
                    getattr(schedule.every(), day.lower()).at(time_str).do(
                        self.run_account_job, account
                    )
                    self.logger.info(f"📅 Scheduled {account['name']} for {day} at {time_str}")
    
    def run_account_job(self, account_config):
        """Run a single account automation job"""
        account_name = account_config["name"]
        
        # Check if account is already running
        if account_name in self.running_accounts:
            self.logger.warning(f"⚠️ {account_name} is already running, skipping...")
            return
        
        # Check system health before starting
        health = self.resource_monitor.check_system_health()
        if not health["healthy"]:
            self.logger.warning(f"⚠️ System resources low (CPU: {health['cpu_percent']}%, RAM: {health['memory_percent']}%), delaying {account_name}")
            return
        
        # Add random delay to avoid simultaneous starts
        delay = random.uniform(0, 300)
        self.logger.info(f"⏳ {account_name} starting in {delay:.1f} seconds...")
        time.sleep(delay)
        
        # Start account in separate thread
        thread = threading.Thread(
            target=self.run_single_account,
            args=(account_config,),
            name=f"Account_{account_name.replace(' ', '_')}"
        )
        thread.daemon = True
        self.running_accounts[account_name] = thread
        thread.start()
    
    def run_single_account(self, account_config):
        """Run automation for a single account"""
        account_name = account_config["name"]
        
        try:
            self.logger.info(f"🚀 Starting automation for {account_name}")
            
            # Create account-specific logger
            account_logger = logging.getLogger(f'Account_{account_name.replace(" ", "_")}')
            account_handler = logging.FileHandler(f'logs/account_{account_name.replace(" ", "_")}.log')
            account_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            account_logger.addHandler(account_handler)
            account_logger.setLevel(logging.INFO)
            
            # Run the automation
            automator = LinkedInAccountAutomator(account_config, account_logger, self)
            result = automator.run_automation()
            
            self.logger.info(f"✅ {account_name} completed - {result['comments_made']} comments made")
            
            # Reset failure count on success
            self.failure_counts[account_name] = 0
            
        except Exception as e:
            self.logger.error(f"❌ {account_name} failed: {e}")
            
            # Increment failure count
            self.failure_counts[account_name] = self.failure_counts.get(account_name, 0) + 1
            
            # Auto-disable account after 3 failures
            if self.failure_counts[account_name] >= 3:
                self.logger.error(f"🚫 Disabling {account_name} after 3 consecutive failures")
                self.config_manager.update_account_setting(account_name, "enabled", False)
                
        finally:
            # Remove from running accounts
            if account_name in self.running_accounts:
                del self.running_accounts[account_name]
            if account_name in self.agent_heartbeats:
                del self.agent_heartbeats[account_name]
    
    def start_scheduler(self):
        """Start the scheduler in a separate thread"""
        self.scheduler_running = True
        self.setup_schedules()
        
        def scheduler_thread():
            self.logger.info("🕐 Scheduler started - monitoring for scheduled jobs...")
            while self.scheduler_running:
                # Check system health before running pending jobs
                health = self.resource_monitor.check_system_health()
                if health["healthy"]:
                    schedule.run_pending()
                else:
                    self.logger.warning(f"⚠️ System resources low, waiting... (CPU: {health['cpu_percent']}%, RAM: {health['memory_percent']}%)")
                    time.sleep(60)
                    continue
                
                # Check for unresponsive agents
                self.check_agent_health()
                
                time.sleep(60)
                
        thread = threading.Thread(target=scheduler_thread, name="Scheduler")
        thread.daemon = True
        thread.start()
        
        self.logger.info("📅 LinkedIn Bot Scheduler is now running!")
        self.logger.info("   - Use Ctrl+C to stop")
        self.logger.info("   - Check logs/ directory for detailed logs")
    
    def check_agent_health(self):
        """Check for unresponsive agents and restart them"""
        current_time = time.time()
        for account_name, last_heartbeat in list(self.agent_heartbeats.items()):
            if current_time - last_heartbeat > 600:  # 10 minutes timeout
                self.logger.warning(f"💔 {account_name} appears unresponsive, attempting restart...")
                
                # Force terminate the unresponsive thread
                if account_name in self.running_accounts:
                    # We can't force kill threads in Python, but we can mark it for removal
                    del self.running_accounts[account_name]
                
                # Wait before restart
                time.sleep(300)  # 5 minute cooldown
                
                # Find account config and restart
                accounts = self.config_manager.get_enabled_accounts()
                for account in accounts:
                    if account["name"] == account_name:
                        self.run_account_job(account)
                        break
    
    def update_heartbeat(self, account_name):
        """Update heartbeat for an account"""
        self.agent_heartbeats[account_name] = time.time()
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        self.scheduler_running = False
        schedule.clear()
        self.logger.info("⏹️ Scheduler stopped")
    
    def run_all_accounts_now(self):
        """Run all enabled accounts immediately"""
        accounts = self.config_manager.get_enabled_accounts()
        
        with ThreadPoolExecutor(max_workers=min(len(accounts), 3)) as executor:
            futures = []
            
            for account in accounts:
                future = executor.submit(self.run_single_account, account)
                futures.append((account["name"], future))
                
                # Stagger starts
                time.sleep(random.uniform(60, 180))
            
            # Wait for all to complete
            for account_name, future in futures:
                try:
                    future.result(timeout=3600)
                    self.logger.info(f"✅ {account_name} completed successfully")
                except Exception as e:
                    self.logger.error(f"❌ {account_name} failed: {e}")

# --- Single Account Automator ---
class LinkedInAccountAutomator:
    def __init__(self, account_config, logger, scheduler=None):
        self.account_config = account_config
        self.account_name = account_config["name"]
        self.logger = logger
        self.scheduler = scheduler
        self.driver = None
        self.tracker = PostTracker(self.account_name)
        self.comment_generator = OllamaCommentGenerator()
        self.proxy_checker = ProxyHealthChecker()
    
    def create_account_driver(self):
        """Create driver for specific account"""
        try:
            options = Options()
            
            # Account-specific browser configuration
            browser_path = self.account_config.get("browser_path", "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe")
            user_data_dir = os.path.expanduser(self.account_config.get("user_data_dir", "~/AppData/Local/BraveSoftware/Brave-Browser/User Data"))
            profile_dir = self.account_config.get("profile_directory", "Default")
            
            options.binary_location = browser_path
            options.add_argument(f"--user-data-dir={user_data_dir}")
            options.add_argument(f"--profile-directory={profile_dir}")
            options.add_experimental_option("detach", True)
            options.add_argument("--disable-blink-features=AutomationControlled")
            
            # Headless mode support
            if self.account_config.get("headless", False):
                options.add_argument("--headless")
                self.logger.info(f"🔇 Running {self.account_name} in headless mode")
            
            # Proxy configuration
            proxy_config = self.account_config.get("proxies", {})
            healthy_proxy = self.proxy_checker.get_healthy_proxy(proxy_config)
            if healthy_proxy:
                options.add_argument(f'--proxy-server={healthy_proxy}')
                self.logger.info(f"🌐 Using proxy for {self.account_name}: {healthy_proxy}")
            elif proxy_config.get("primary") or proxy_config.get("backups"):
                self.logger.warning(f"⚠️ No healthy proxy found for {self.account_name}, using direct connection")
            
            # Account-specific window position to avoid overlap
            account_index = hash(self.account_name) % 4
            window_x = account_index * 200
            window_y = account_index * 100
            options.add_argument(f"--window-position={window_x},{window_y}")
            
            service = Service()
            driver = webdriver.Chrome(service=service, options=options)
            driver.maximize_window()
            
            self.logger.info(f"✅ Created browser instance for {self.account_name}")
            return driver
            
        except Exception as e:
            self.logger.error(f"❌ Failed to create driver for {self.account_name}: {e}")
            # Switch to visible mode if headless fails
            if self.account_config.get("headless", False):
                self.logger.info(f"🔄 Switching {self.account_name} to visible mode after failure")
                self.account_config["headless"] = False
                if hasattr(self, 'scheduler') and self.scheduler:
                    self.scheduler.config_manager.update_account_setting(self.account_name, "headless", False)
            raise
    
    def run_automation(self):
        """Run the full automation process for this account"""
        try:
            self.driver = self.create_account_driver()
            
            # Navigate to LinkedIn
            self.logger.info(f"📱 Navigating to LinkedIn...")
            self.driver.get(LINKEDIN_URL)
            time.sleep(5)
            
            # Check login status
            if not self.check_login_status():
                self.logger.error(f"❌ Account not logged in - automation aborted")
                return {"success": False, "comments_made": 0, "error": "Not logged in"}
            
            # Detect user
            self.tracker.user_name = detect_current_user(self.driver)
            self.logger.info(f"👤 Detected user: {self.tracker.user_name or 'Unknown'}")
            
            # Run commenting process
            comments_made = 0
            search_queries = self.account_config.get("search_queries", ["AI development"])
            comments_per_session = self.account_config.get("comments_per_session", 5)
            
            for query in search_queries:
                if comments_made >= comments_per_session:
                    break
                
                self.logger.info(f"🔍 Processing query: '{query}'")
                session_comments = self.process_query(query, comments_per_session - comments_made)
                comments_made += session_comments
                
                # Update heartbeat
                if self.scheduler:
                    self.scheduler.update_heartbeat(self.account_name)
                
                if comments_made < comments_per_session:
                    delay = random.uniform(300, 600)
                    self.logger.info(f"⏳ Waiting {delay/60:.1f} minutes before next query...")
                    time.sleep(delay)
            
            self.logger.info(f"✅ Automation completed - {comments_made} comments made")
            
            return {
                "success": True,
                "comments_made": comments_made,
                "stats": self.tracker.get_stats()
            }
            
        except Exception as e:
            self.logger.error(f"❌ Automation failed: {e}")
            return {"success": False, "comments_made": 0, "error": str(e)}
            
        finally:
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
    
    def check_login_status(self):
        """Check if account is logged in"""
        try:
            WebDriverWait(self.driver, 30).until(
                EC.any_of(
                    EC.presence_of_element_located((By.XPATH, "//nav[contains(@class, 'global-nav')]")),
                    EC.presence_of_element_located((By.XPATH, "//input[@id='username']"))
                )
            )
            
            if self.driver.find_elements(By.XPATH, "//input[@id='username']"):
                return False
            else:
                return True
                
        except TimeoutException:
            return False
    
    def process_query(self, query, max_comments):
        """Process a single search query"""
        try:
            search_url = SEARCH_URL_TEMPLATE.format(query=requests.utils.quote(query))
            self.driver.get(search_url)
            
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'search-results-container')]"))
            )
            
            # Apply filters and scroll
            apply_post_filter(self.driver)
            scroll_feed(self.driver, target_posts=max_comments * 3)
            
            # Find and process posts
            posts = find_posts_improved(self.driver)
            comments_made = 0
            
            for post_element in posts:
                if comments_made >= max_comments:
                    break
                
                # Update heartbeat during processing
                if self.scheduler:
                    self.scheduler.update_heartbeat(self.account_name)
                
                try:
                    success = self.process_single_post(post_element)
                    if success:
                        comments_made += 1
                        
                        # Random delay between comments
                        delay = random.uniform(60, 180)
                        self.logger.info(f"⏳ Waiting {delay:.1f} seconds before next comment...")
                        time.sleep(delay)
                        
                except Exception as e:
                    self.logger.error(f"⚠️ Error processing post: {e}")
                    continue
            
            return comments_made
            
        except Exception as e:
            self.logger.error(f"❌ Error processing query '{query}': {e}")
            return 0
    
    def process_single_post(self, post_element):
        """Process a single post for commenting"""
        try:
            post_data = extract_post_data(post_element, self.driver)
            if not post_data or not post_data["id"]:
                return False
            
            # Check for duplicates
            if self.tracker.is_processed(post_data["id"]):
                return False
            
            if self.tracker.is_duplicate_signature(post_data["signature"]):
                self.tracker.mark_processed(post_data["id"], post_data["signature"])
                return False
            
            # Skip very short posts
            if len(post_data["text"].strip()) < 50:
                self.tracker.mark_processed(post_data["id"], post_data["signature"])
                return False
            
            # Generate comment
            comment_text = self.comment_generator.generate_comment(
                post_data["text"], 
                post_data["author"]
            )
            
            if not comment_text:
                self.tracker.mark_failed(post_data["id"], post_data["signature"])
                return False
            
            # Find comment button and post comment
            success = self.comment_on_post(post_data, comment_text)
            
            if success:
                self.tracker.mark_commented(
                    post_data["id"], 
                    post_data["signature"],
                    post_url=self.driver.current_url,
                    content_hash=hashlib.md5(post_data["text"].encode()).hexdigest()
                )
                self.logger.info(f"✅ Successfully commented: '{comment_text[:50]}...'")
                return True
            else:
                self.tracker.mark_failed(post_data["id"], post_data["signature"])
                return False
                
        except Exception as e:
            self.logger.error(f"⚠️ Error in process_single_post: {e}")
            return False
    
    def comment_on_post(self, post_data, comment_text):
        """Comment on a specific post"""
        try:
            # Find comment button
            comment_selectors = [
                ".//button[contains(@aria-label, 'Comment') and contains(@aria-label, 'on')]",
                ".//button[contains(@class, 'comment')]",
                ".//span[text()='Comment']//ancestor::button"
            ]
            
            comment_button = None
            for selector in comment_selectors:
                try:
                    comment_button = post_data["element"].find_element(By.XPATH, selector)
                    if comment_button.is_displayed():
                        break
                except:
                    continue
            
            if not comment_button:
                return False
            
            # Click comment button
            self.driver.execute_script("arguments[0].click();", comment_button)
            time.sleep(2)
            
            # Find comment box
            comment_box_selectors = [
                "//div[@role='textbox' and @aria-label='Add a comment…']",
                "//div[contains(@class, 'ql-editor')]",
                "//div[@contenteditable='true']"
            ]
            
            comment_box = None
            for selector in comment_box_selectors:
                try:
                    comment_box = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    break
                except:
                    continue
            
            if not comment_box:
                return False
            
            # Type comment
            comment_box.click()
            time.sleep(1)
            comment_box.send_keys(comment_text)
            time.sleep(2)
            
            # Find and click post button
            post_button_selectors = [
                '//button[contains(text(), "Post") and not(contains(@aria-label, "like"))]',
                '//button[contains(@aria-label, "Post comment")]',
                '//button[contains(@class, "artdeco-button--primary") and contains(text(), "Post")]'
            ]
            
            post_button = None
            for selector in post_button_selectors:
                try:
                    post_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    if not post_button.get_attribute("disabled"):
                        break
                except:
                    continue
            
            if not post_button:
                return False
            
            # Click post button
            self.driver.execute_script("arguments[0].click();", post_button)
            time.sleep(3)
            
            return True
            
        except Exception as e:
            self.logger.error(f"⚠️ Error commenting on post: {e}")
            return False

# --- Main Menu System ---
def main_menu():
    """Interactive main menu for bot control"""
    config_manager = AccountConfigManager()
    scheduler = LinkedInBotScheduler(config_manager)
    
    while True:
        print("\n" + "="*50)
        print("🤖 LinkedIn Bot v1 - Multi-Account Scheduler")
        print("="*50)
        print("1. 🕐 Start Scheduler Mode (Automated)")
        print("2. 🚀 Run All Accounts Now (Testing)")
        print("3. 👤 Run Single Account")
        print("4. ⚙️  Manage Accounts")
        print("5. 📊 View System Status")
        print("6. 📝 View Logs")
        print("7. ❌ Exit")
        print("="*50)
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == "1":
            run_scheduler_mode(scheduler)
        elif choice == "2":
            run_all_accounts_mode(scheduler)
        elif choice == "3":
            run_single_account_mode(config_manager)
        elif choice == "4":
            manage_accounts_mode(config_manager)
        elif choice == "5":
            view_system_status(scheduler)
        elif choice == "6":
            view_logs()
        elif choice == "7":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

def run_scheduler_mode(scheduler):
    """Run the bot in scheduler mode"""
    try:
        scheduler.start_scheduler()
        print("📅 Scheduler is running! Press Ctrl+C to stop...")
        while scheduler.scheduler_running:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping scheduler...")
        scheduler.stop_scheduler()

def run_all_accounts_mode(scheduler):
    """Run all accounts immediately"""
    accounts = scheduler.config_manager.get_enabled_accounts()
    if not accounts:
        print("❌ No enabled accounts found.")
        return
    
    print(f"🚀 Running {len(accounts)} enabled accounts...")
    scheduler.run_all_accounts_now()

def run_single_account_mode(config_manager):
    """Run a single account"""
    accounts = config_manager.get_enabled_accounts()
    if not accounts:
        print("❌ No enabled accounts found.")
        return
    
    print("\nAvailable accounts:")
    for i, account in enumerate(accounts, 1):
        print(f"{i}. {account['name']}")
    
    try:
        choice = int(input(f"Select account (1-{len(accounts)}): ")) - 1
        if 0 <= choice < len(accounts):
            account = accounts[choice]
            logger = logging.getLogger(f'SingleRun_{account["name"]}')
            automator = LinkedInAccountAutomator(account, logger)
            result = automator.run_automation()
            print(f"✅ Completed: {result}")
        else:
            print("❌ Invalid selection.")
    except ValueError:
        print("❌ Invalid input.")

def manage_accounts_mode(config_manager):
    """Manage account configurations"""
    while True:
        print("\n" + "="*30)
        print("⚙️  Account Management")
        print("="*30)
        print("1. 📋 List Accounts")
        print("2. ➕ Add Account")
        print("3. ✏️  Edit Account")
        print("4. 🔄 Enable/Disable Account")
        print("5. 🔙 Back to Main Menu")
        print("="*30)
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1":
            list_accounts(config_manager)
        elif choice == "2":
            add_account(config_manager)
        elif choice == "3":
            edit_account(config_manager)
        elif choice == "4":
            toggle_account(config_manager)
        elif choice == "5":
            break
        else:
            print("❌ Invalid choice.")

def list_accounts(config_manager):
    """List all accounts"""
    accounts = config_manager.accounts["accounts"]
    if not accounts:
        print("❌ No accounts configured.")
        return
    
    print("\n📋 Configured Accounts:")
    for i, account in enumerate(accounts, 1):
        status = "✅ Enabled" if account.get("enabled", True) else "❌ Disabled"
        print(f"{i}. {account['name']} - {status}")
        print(f"   Queries: {', '.join(account.get('search_queries', []))}")
        print(f"   Comments per session: {account.get('comments_per_session', 5)}")

def add_account(config_manager):
    """Add a new account"""
    print("\n➕ Add New Account")
    name = input("Account name: ").strip()
    if not name:
        print("❌ Account name cannot be empty.")
        return
    
    # Basic account template
    new_account = {
        "name": name,
        "profile_directory": input("Profile directory (e.g., 'Profile 1'): ").strip() or "Default",
        "browser_path": input("Browser path (press Enter for default): ").strip() or "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe",
        "user_data_dir": input("User data directory (press Enter for default): ").strip() or "~/AppData/Local/BraveSoftware/Brave-Browser/User Data",
        "search_queries": input("Search queries (comma-separated): ").split(","),
        "comments_per_session": int(input("Comments per session (default 5): ") or "5"),
        "enabled": True,
        "headless": False,
        "proxies": {"primary": None, "backups": []},
        "schedule": {
            "days": input("Schedule days (comma-separated, e.g., monday,wednesday,friday): ").split(","),
            "times": input("Schedule times (comma-separated, e.g., 09:00,15:00): ").split(",")
        }
    }
    
    config_manager.add_account(new_account)
    print(f"✅ Added account: {name}")

def edit_account(config_manager):
    """Edit an existing account"""
    # Simplified edit function - in practice, you'd want more comprehensive editing
    print("✏️  Edit Account - Feature not fully implemented in this demo")

def toggle_account(config_manager):
    """Enable/disable an account"""
    accounts = config_manager.accounts["accounts"]
    if not accounts:
        print("❌ No accounts configured.")
        return
    
    print("\nSelect account to toggle:")
    for i, account in enumerate(accounts, 1):
        status = "Enabled" if account.get("enabled", True) else "Disabled"
        print(f"{i}. {account['name']} - {status}")
    
    try:
        choice = int(input(f"Select account (1-{len(accounts)}): ")) - 1
        if 0 <= choice < len(accounts):
            account = accounts[choice]
            current_status = account.get("enabled", True)
            account["enabled"] = not current_status
            config_manager.save_accounts()
            new_status = "Enabled" if account["enabled"] else "Disabled"
            print(f"✅ {account['name']} is now {new_status}")
        else:
            print("❌ Invalid selection.")
    except ValueError:
        print("❌ Invalid input.")

def view_system_status(scheduler):
    """View current system status"""
    resource_monitor = ResourceMonitor()
    health = resource_monitor.check_system_health()
    
    print("\n📊 System Status:")
    print(f"CPU Usage: {health['cpu_percent']:.1f}%")
    print(f"Memory Usage: {health['memory_percent']:.1f}%")
    print(f"System Health: {'✅ Healthy' if health['healthy'] else '⚠️ Under Load'}")
    print(f"Running Accounts: {len(scheduler.running_accounts)}")
    
    if scheduler.running_accounts:
        print("Active accounts:")
        for account_name in scheduler.running_accounts.keys():
            print(f"  - {account_name}")

def view_logs():
    """View recent log files"""
    print("\n📝 Recent Log Files:")
    if os.path.exists(LOGS_DIR):
        log_files = [f for f in os.listdir(LOGS_DIR) if f.endswith('.log')]
        for log_file in sorted(log_files):
            file_path = os.path.join(LOGS_DIR, log_file)
            size = os.path.getsize(file_path)
            print(f"  {log_file} ({size} bytes)")
    else:
        print("❌ No log directory found.")

# --- Main Execution ---
if __name__ == "__main__":
    try:
        # Ensure all directories exist
        for directory in ["screenshots", "logs", "account_histories"]:
            if not os.path.exists(directory):
                os.makedirs(directory)
        
        # Start the main menu
        main_menu()
        
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()