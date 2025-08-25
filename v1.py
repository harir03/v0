import os
import time
import uuid
import json
import requests
import hashlib
import random
import schedule
import threading
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

# --- Scheduler Class ---
class LinkedInBotScheduler:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.running_accounts = {}
        self.logger = setup_logging()
        self.scheduler_running = False
        
    def setup_schedules(self):
        """Setup schedules for all enabled accounts"""
        schedule.clear()  # Clear existing schedules
        
        accounts = self.config_manager.get_enabled_accounts()
        for account in accounts:
            account_schedule = account.get("schedule", {})
            days = account_schedule.get("days", [])
            times = account_schedule.get("times", [])
            
            for day in days:
                for time_str in times:
                    # Schedule the job
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
        
        # Add random delay to avoid simultaneous starts
        delay = random.uniform(0, 300)  # 0-5 minutes
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
            automator = LinkedInAccountAutomator(account_config, account_logger)
            result = automator.run_automation()
            
            self.logger.info(f"✅ {account_name} completed - {result['comments_made']} comments made")
            
        except Exception as e:
            self.logger.error(f"❌ {account_name} failed: {e}")
        finally:
            # Remove from running accounts
            if account_name in self.running_accounts:
                del self.running_accounts[account_name]
    
    def start_scheduler(self):
        """Start the scheduler in a separate thread"""
        self.scheduler_running = True
        self.setup_schedules()
        
        def scheduler_thread():
            self.logger.info("🕐 Scheduler started - monitoring for scheduled jobs...")
            while self.scheduler_running:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
        thread = threading.Thread(target=scheduler_thread, name="Scheduler")
        thread.daemon = True
        thread.start()
        
        self.logger.info("📅 LinkedIn Bot Scheduler is now running!")
        self.logger.info("   - Use Ctrl+C to stop")
        self.logger.info("   - Check logs/ directory for detailed logs")
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        self.scheduler_running = False
        schedule.clear()
        self.logger.info("⏹️ Scheduler stopped")
    
    def run_all_accounts_now(self):
        """Run all enabled accounts immediately (for testing)"""
        accounts = self.config_manager.get_enabled_accounts()
        
        with ThreadPoolExecutor(max_workers=min(len(accounts), 3)) as executor:
            futures = []
            
            for account in accounts:
                future = executor.submit(self.run_single_account, account)
                futures.append((account["name"], future))
                
                # Stagger starts
                time.sleep(random.uniform(60, 180))  # 1-3 minutes between starts
            
            # Wait for all to complete
            for account_name, future in futures:
                try:
                    future.result(timeout=3600)  # 1 hour timeout per account
                    self.logger.info(f"✅ {account_name} completed successfully")
                except Exception as e:
                    self.logger.error(f"❌ {account_name} failed: {e}")

# --- Single Account Automator ---
class LinkedInAccountAutomator:
    def __init__(self, account_config, logger):
        self.account_config = account_config
        self.account_name = account_config["name"]
        self.logger = logger
        self.driver = None
        self.tracker = PostTracker(self.account_name)
        self.comment_generator = OllamaCommentGenerator()
    
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
            
            # Add account-specific window position to avoid overlap
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
                
                if comments_made < comments_per_session:
                    delay = random.uniform(300, 600)  # 5-10 minutes between queries
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
                
                try:
                    success = self.process_single_post(post_element)
                    if success:
                        comments_made += 1
                        
                        # Random delay between comments
                        if comments_made < max_comments:
                            delay = random.uniform(30, 90)
                            self.logger.info(f"⏳ Waiting {delay:.1f}s before next comment...")
                            time.sleep(delay)
                            
                except Exception as e:
                    self.logger.error(f"Error processing post: {e}")
                    continue
            
            return comments_made
            
        except Exception as e:
            self.logger.error(f"Error processing query '{query}': {e}")
            return 0
    
    def process_single_post(self, post_element):
        """Process a single post for commenting"""
        try:
            post_data = extract_post_data(post_element, self.driver)
            if not post_data:
                return False
            
            # Check for duplicates
            if self.tracker.is_processed(post_data["id"]) or check_and_remove_duplicate_comments(self.driver, post_element, post_data["id"], self.tracker):
                self.tracker.mark_processed(post_data["id"], post_data["signature"])
                return False
            
            # Check author credibility
            is_credible, credibility_info = self.comment_generator.check_author_credibility(post_element, post_data["author"], self.driver)
            if not is_credible:
                self.logger.info(f"👤 SKIP: {credibility_info}")
                self.tracker.mark_processed(post_data["id"], post_data["signature"])
                return False
            
            # Evaluate post worthiness
            should_comment, reasoning, score = self.comment_generator.evaluate_post_worthiness(post_data["text"], post_data["author"])
            if not should_comment or score < 25:
                self.logger.info(f"📉 SKIP: AI evaluation failed (Score: {score}/50)")
                self.tracker.mark_processed(post_data["id"], post_data["signature"])
                return False
            
            # Generate and post comment
            comment = self.comment_generator.generate_comment(post_data["text"], post_data["author"])
            if not comment:
                self.tracker.mark_processed(post_data["id"], post_data["signature"])
                return False
            
            success = comment_on_post_improved(self.driver, post_data, comment, [])
            
            if success:
                content_hash = hashlib.md5(f"{post_data['author']}:{post_data['text'][:300]}".encode()).hexdigest()
                self.tracker.mark_commented(
                    post_data["id"], 
                    post_data["signature"], 
                    post_data.get("url"), 
                    content_hash
                )
                self.logger.info(f"✅ Comment posted successfully")
                return True
            else:
                self.tracker.mark_failed(post_data["id"], post_data["signature"])
                return False
                
        except Exception as e:
            self.logger.error(f"Error in process_single_post: {e}")
            return False

# --- Keep all your existing classes and functions ---
# [OllamaCommentGenerator, detect_current_user, check_and_remove_duplicate_comments, etc.]
# I'll include the essential ones here, but the full implementation would include all your existing functions

class OllamaCommentGenerator:
    def __init__(self, model_name="llama3.2:3b", ollama_url=OLLAMA_URL):
        self.model_name = model_name
        self.ollama_url = ollama_url
        self.test_connection()

    def test_connection(self):
        try:
            response = requests.get(f"{self.ollama_url.rsplit('/', 1)[0]}/tags", timeout=5)
            if response.status_code != 200: 
                raise Exception(f"Ollama not responding (Status: {response.status_code})")
            print("✅ Ollama connection successful.")
        except Exception as e:
            print(f"❌ Ollama connection failed: {e}")
            raise

    def generate_ai_profile_keywords(self, num_keywords=5, base_query="AI"):
        """Generates specific AI/tech topic keywords for better content discovery."""
        prompt = f"""Generate {num_keywords} specific LinkedIn search keywords related to {base_query} and technology.
Focus on actual topics, technologies, and industry trends - NOT on people or job titles.
Examples: "machine learning algorithms", "AI automation tools", "neural networks breakthrough", "ChatGPT development", "computer vision applications"
Generate {num_keywords} similar specific AI/tech topic keywords as a comma-separated list:"""
        
        fallback_keywords = [
            f"{base_query} development", f"{base_query} automation", "machine learning", 
            "neural networks", "deep learning", "computer vision", "natural language processing",
            "AI tools", "artificial intelligence trends", "tech innovation"
        ]
        
        try:
            payload = {"model": self.model_name, "prompt": prompt, "stream": False}
            response = requests.post(self.ollama_url, json=payload, timeout=30)
            if response.status_code == 200:
                keywords_str = response.json().get("response", "").strip()
                keywords = [k.strip() for k in keywords_str.split(',') if k.strip()]
                return keywords if keywords else fallback_keywords
            else:
                return fallback_keywords
        except Exception as e:
            return fallback_keywords

    def evaluate_post_worthiness(self, post_text, author_name, post_type="general"):
        """AI evaluates posts based on content quality and engagement potential."""
        cleaned_text = self.extract_actual_content(post_text)
        evaluation_prompt = f"""You are a LinkedIn engagement strategist. Analyze this post to decide if commenting would increase professional visibility and engagement.

POST CONTENT: {cleaned_text[:800]}
AUTHOR: {author_name or "Unknown"}

Evaluate on these criteria (score 1-10 each):
1. CONTENT DEPTH: Does it discuss substantial AI/tech concepts?
2. ENGAGEMENT POTENTIAL: Will this post likely get good engagement?
3. PROFESSIONAL VALUE: Will commenting here showcase expertise?
4. DISCUSSION QUALITY: Does it invite meaningful discussion?
5. AUDIENCE REACH: Does the post reach professionals?

Respond in this exact format:
DECISION: COMMENT or SKIP
REASONING: [Brief explanation]
ENGAGEMENT_SCORE: X/50"""

        try:
            payload = {"model": self.model_name, "prompt": evaluation_prompt, "stream": False, "options": {"temperature": 0.3}}
            response = requests.post(self.ollama_url, json=payload, timeout=45)
            if response.status_code == 200:
                evaluation = response.json().get("response", "").strip()
                should_comment = "COMMENT" in evaluation.upper()
                reasoning = evaluation.split("REASONING:")[1].split("ENGAGEMENT_SCORE:")[0].strip() if "REASONING:" in evaluation else "N/A"
                score = int(evaluation.split("ENGAGEMENT_SCORE:")[1].split("/")[0].strip()) if "ENGAGEMENT_SCORE:" in evaluation else 0
                return should_comment, reasoning, score
        except Exception as e:
            pass
        return False, "Evaluation Error", 0

    def check_author_credibility(self, post_element, author_name, driver):
        """Check author credibility"""
        if not author_name:
            return True, "No author filtering needed"
        
        red_flag_indicators = [
            "student at", "intern at", "looking for opportunities", 
            "seeking job", "fresh graduate", "recent graduate"
        ]
        
        try:
            post_text = post_element.text.lower()
            for flag in red_flag_indicators:
                if flag in post_text:
                    return False, f"Student/job-seeking content detected: {flag}"
            return True, "Author seems credible"
        except Exception as e:
            return True, f"Could not verify author, proceeding anyway: {e}"

    def generate_comment(self, post_text, author_name=None):
        prompt = f"Write a professional, 15-30 word insightful comment for the following AI-related post by {author_name or 'the author'}. Sound like an expert. POST: {post_text[:1000]}"
        try:
            payload = {"model": self.model_name, "prompt": prompt, "stream": False}
            response = requests.post(self.ollama_url, json=payload, timeout=45)
            if response.status_code == 200:
                comment = response.json().get("response", "").strip().strip('"')
                return comment
        except Exception as e:
            pass
        return None

    def extract_actual_content(self, post_text):
        lines = post_text.split('\n')
        content_lines = []
        skip_patterns = ['Like', 'Comment', 'Repost', 'Share', 'Send', 'ago', 'Follow']
        for line in lines:
            if not any(pattern in line for pattern in skip_patterns) and len(line.strip()) > 20:
                content_lines.append(line.strip())
        return ' '.join(content_lines)

# --- Essential utility functions (simplified versions) ---
def detect_current_user(driver):
    """Detect the current LinkedIn user's name"""
    try:
        profile_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'global-nav__primary-link-me-menu')]"))
        )
        profile_button.click()
        time.sleep(2)
        
        name_element = driver.find_element(By.XPATH, "//div[contains(@class, 'text-heading-large')]")
        user_name = name_element.text.strip()
        
        driver.find_element(By.XPATH, "//body").click()
        time.sleep(1)
        
        return user_name if user_name else None
    except:
        return None

def check_and_remove_duplicate_comments(driver, post_element, post_id, tracker):
    """Check for duplicate comments"""
    try:
        # Quick check using persistent history
        post_data = extract_post_data(post_element, driver)
        if post_data:
            content_hash = hashlib.md5(f"{post_data['author']}:{post_data['text'][:300]}".encode()).hexdigest()
            if tracker.has_commented_on_content(content_hash):
                return True
        
        # Check DOM for existing comments
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", post_element)
        time.sleep(1)
        
        user_comment_selectors = [
            ".//span[contains(., '(You)')]",
            f".//span[contains(., '{tracker.user_name}')]" if tracker.user_name else None
        ]
        
        for selector in user_comment_selectors:
            if selector is None:
                continue
            try:
                post_element.find_element(By.XPATH, selector)
                return True
            except:
                continue
        
        return False
    except:
        return False

def apply_post_filter(driver):
    """Apply Posts filter to search results"""
    try:
        filter_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Posts']"))
        )
        driver.execute_script("arguments[0].click();", filter_button)
        time.sleep(3)
    except:
        pass

def scroll_feed(driver, scroll_times=10, target_posts=15):
    """Scroll feed to load more posts"""
    for i in range(scroll_times):
        driver.execute_script("window.scrollBy(0, window.innerHeight * 0.8);")
        time.sleep(2)
        posts_count = len(find_posts_improved(driver))
        if posts_count >= target_posts:
            break
    driver.execute_script("window.scrollTo(0, 0);")

def find_posts_improved(driver):
    """Find post elements on the page"""
    post_selectors = [
        "//div[contains(@class, 'feed-shared-update-v2')]",
        "//div[contains(@class, 'update-components-post')]"
    ]
    all_posts = []
    for selector in post_selectors:
        try:
            posts = driver.find_elements(By.XPATH, selector)
            all_posts.extend(posts)
        except:
            continue
    return list({id(post): post for post in all_posts}.values())

def extract_post_data(post_element, driver):
    """Extract data from post element"""
    try:
        post_text = post_element.text
        author_name = "Unknown"
        try:
            author_name = post_element.find_element(
                By.XPATH, ".//span[contains(@class, 'feed-shared-actor__name')]//span[@aria-hidden='true']"
            ).text
        except:
            pass
        
        post_id = f"element-{hashlib.md5(post_element.get_attribute('outerHTML')[:500].encode()).hexdigest()[:10]}"
        signature = hashlib.md5(f"{author_name}:{post_text[:200]}".encode()).hexdigest()
        
        post_url = None
        try:
            post_link = post_element.find_element(By.XPATH, ".//a[contains(@href, '/posts/')]")
            post_url = post_link.get_attribute('href')
        except:
            pass
            
        return {
            "id": post_id,
            "text": post_text,
            "author": author_name,
            "element": post_element,
            "signature": signature,
            "url": post_url
        }
    except:
        return None

def comment_on_post_improved(driver, post_data, comment_text, saved_screenshots):
    """Post a comment on a LinkedIn post"""
    try:
        post_element = post_data["element"]
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", post_element)
        time.sleep(2)
        
        # Click comment button
        comment_btn = post_element.find_element(By.XPATH, ".//button[contains(@aria-label, 'Comment')]")
        driver.execute_script("arguments[0].click();", comment_btn)
        time.sleep(3)

        # Find comment box
        comment_box = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="textbox" and @contenteditable="true"]'))
        )

        # Type comment
        ActionChains(driver).move_to_element(comment_box).click().send_keys(comment_text).perform()
        time.sleep(2)

        # Submit comment
        submit_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'comments-comment-box__submit-button')]")
        driver.execute_script("arguments[0].click();", submit_btn)
        time.sleep(3)
        
        return True
    except Exception as e:
        print(f"Comment failed: {e}")
        return False

# --- Configuration Setup Functions ---
def setup_initial_config():
    """Setup initial configuration files if they don't exist"""
    config_manager = AccountConfigManager()
    
    if not os.path.exists(ACCOUNTS_CONFIG_FILE):
        print("🔧 Setting up initial account configuration...")
        
        # Interactive setup
        accounts = []
        num_accounts = int(input("How many LinkedIn accounts do you want to configure? (1-5): ") or "1")
        
        for i in range(min(num_accounts, 5)):
            print(f"\n--- Account {i+1} Configuration ---")
            account_name = input(f"Account name (e.g., 'Work Account', 'Personal Account'): ") or f"Account {i+1}"
            
            # Browser configuration
            browser_path = input("Browser path (Enter for default Brave): ") or "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
            user_data_dir = input("User data directory (Enter for default): ") or "~/AppData/Local/BraveSoftware/Brave-Browser/User Data"
            profile_dir = input(f"Profile directory (e.g., 'Profile {i+1}'): ") or f"Profile {i+1}"
            
            # Search queries
            queries_input = input("Search queries (comma-separated, e.g., 'AI development, machine learning'): ")
            search_queries = [q.strip() for q in queries_input.split(",")] if queries_input else ["AI development"]
            
            # Comments per session
            comments_per_session = int(input("Comments per session (default 5): ") or "5")
            
            # Schedule
            print("Schedule configuration:")
            days_input = input("Days (comma-separated, e.g., 'monday,wednesday,friday'): ") or "monday,wednesday,friday"
            days = [day.strip().lower() for day in days_input.split(",")]
            
            times_input = input("Times (comma-separated, 24h format, e.g., '09:00,15:00'): ") or "09:00,15:00"
            times = [time.strip() for time in times_input.split(",")]
            
            account_config = {
                "name": account_name,
                "profile_directory": profile_dir,
                "browser_path": browser_path,
                "user_data_dir": user_data_dir,
                "search_queries": search_queries,
                "comments_per_session": comments_per_session,
                "enabled": True,
                "schedule": {
                    "days": days,
                    "times": times
                }
            }
            
            accounts.append(account_config)
        
        config_manager.accounts = {"accounts": accounts}
        config_manager.save_accounts()
        print("✅ Configuration saved!")
    
    return config_manager

# --- Main Control Functions ---
def run_scheduler_mode():
    """Run the bot in scheduled mode"""
    print("🕐 Starting LinkedIn Bot Scheduler...")
    
    config_manager = setup_initial_config()
    scheduler = LinkedInBotScheduler(config_manager)
    
    # Display schedule
    accounts = config_manager.get_enabled_accounts()
    print(f"\n📅 SCHEDULED ACCOUNTS ({len(accounts)}):")
    print("-" * 50)
    
    for account in accounts:
        schedule_info = account.get("schedule", {})
        days = ", ".join(schedule_info.get("days", []))
        times = ", ".join(schedule_info.get("times", []))
        print(f"📱 {account['name']}")
        print(f"   Days: {days}")
        print(f"   Times: {times}")
        print(f"   Queries: {', '.join(account.get('search_queries', []))}")
        print(f"   Comments per session: {account.get('comments_per_session', 5)}")
        print()
    
    try:
        scheduler.start_scheduler()
        
        # Keep running until interrupted
        while True:
            time.sleep(3600)  # Sleep for 1 hour
            
    except KeyboardInterrupt:
        print("\n⏹️ Scheduler stopped by user")
        scheduler.stop_scheduler()

def run_immediate_mode():
    """Run all accounts immediately (for testing)"""
    print("🚀 Running all accounts immediately...")
    
    config_manager = setup_initial_config()
    scheduler = LinkedInBotScheduler(config_manager)
    
    scheduler.run_all_accounts_now()

def run_single_account_mode():
    """Run a single account interactively"""
    print("👤 Single Account Mode")
    
    config_manager = setup_initial_config()
    accounts = config_manager.get_enabled_accounts()
    
    if not accounts:
        print("❌ No accounts configured!")
        return
    
    print("\nAvailable accounts:")
    for i, account in enumerate(accounts):
        print(f"{i+1}. {account['name']}")
    
    try:
        choice = int(input("Select account (number): ")) - 1
        if 0 <= choice < len(accounts):
            selected_account = accounts[choice]
            
            # Override comments per session
            max_comments = int(input("Number of comments to make (default from config): ") or selected_account.get('comments_per_session', 5))
            selected_account['comments_per_session'] = max_comments
            
            automator = LinkedInAccountAutomator(selected_account, logging.getLogger('SingleMode'))
            result = automator.run_automation()
            
            print(f"\n✅ Automation completed!")
            print(f"Comments made: {result.get('comments_made', 0)}")
            
        else:
            print("❌ Invalid selection")
            
    except ValueError:
        print("❌ Invalid input")

def show_status():
    """Show current status and statistics"""
    print("📊 LinkedIn Bot Status")
    print("-" * 40)
    
    config_manager = AccountConfigManager()
    accounts = config_manager.get_enabled_accounts()
    
    for account in accounts:
        account_name = account['name']
        tracker = PostTracker(account_name)
        stats = tracker.get_stats()
        
        print(f"\n📱 {account_name}")
        print(f"   Historical comments: {stats['historical_comments']}")
        print(f"   Profile: {account.get('profile_directory', 'Unknown')}")
        print(f"   Queries: {', '.join(account.get('search_queries', []))}")
        print(f"   Schedule: {', '.join(account.get('schedule', {}).get('days', []))} at {', '.join(account.get('schedule', {}).get('times', []))}")

def manage_accounts():
    """Account management interface"""
    config_manager = AccountConfigManager()
    
    while True:
        print("\n🔧 Account Management")
        print("1. List accounts")
        print("2. Add account")
        print("3. Enable/disable account")
        print("4. Edit account")
        print("5. Back to main menu")
        
        choice = input("Select option: ").strip()
        
        if choice == "1":
            accounts = config_manager.accounts["accounts"]
            if not accounts:
                print("No accounts configured")
                continue
                
            print("\n📱 Configured Accounts:")
            for i, account in enumerate(accounts):
                status = "✅" if account.get("enabled", True) else "❌"
                print(f"{i+1}. {status} {account['name']} ({account.get('profile_directory', 'Unknown')})")
        
        elif choice == "2":
            print("\n➕ Add New Account")
            # Account setup similar to setup_initial_config
            account_name = input("Account name: ")
            profile_dir = input("Profile directory: ")
            queries_input = input("Search queries (comma-separated): ")
            search_queries = [q.strip() for q in queries_input.split(",")] if queries_input else ["AI development"]
            
            new_account = {
                "name": account_name,
                "profile_directory": profile_dir,
                "browser_path": "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe",
                "user_data_dir": "~/AppData/Local/BraveSoftware/Brave-Browser/User Data",
                "search_queries": search_queries,
                "comments_per_session": 5,
                "enabled": True,
                "schedule": {
                    "days": ["monday", "wednesday", "friday"],
                    "times": ["09:00", "15:00"]
                }
            }
            
            config_manager.add_account(new_account)
            print("✅ Account added!")
        
        elif choice == "3":
            accounts = config_manager.accounts["accounts"]
            if not accounts:
                print("No accounts to modify")
                continue
                
            for i, account in enumerate(accounts):
                status = "enabled" if account.get("enabled", True) else "disabled"
                print(f"{i+1}. {account['name']} ({status})")
            
            try:
                selection = int(input("Select account to toggle: ")) - 1
                if 0 <= selection < len(accounts):
                    accounts[selection]["enabled"] = not accounts[selection].get("enabled", True)
                    config_manager.save_accounts()
                    new_status = "enabled" if accounts[selection]["enabled"] else "disabled"
                    print(f"✅ Account {accounts[selection]['name']} is now {new_status}")
                else:
                    print("Invalid selection")
            except ValueError:
                print("Invalid input")
        
        elif choice == "4":
            print("🔧 Edit account - Feature coming soon!")
        
        elif choice == "5":
            break
        
        else:
            print("Invalid option")

# --- Main Menu ---
def main_menu():
    """Main application menu"""
    print("🤖 LinkedIn Multi-Account Comment Bot")
    print("="*50)
    
    while True:
        print("\n📋 Main Menu:")
        print("1. 🕐 Start Scheduler (Auto-run on schedule)")
        print("2. 🚀 Run All Accounts Now (Immediate)")
        print("3. 👤 Run Single Account")
        print("4. 📊 Show Status")
        print("5. 🔧 Manage Accounts")
        print("6. ❌ Exit")
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == "1":
            run_scheduler_mode()
        elif choice == "2":
            run_immediate_mode()
        elif choice == "3":
            run_single_account_mode()
        elif choice == "4":
            show_status()
        elif choice == "5":
            manage_accounts()
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option. Please select 1-6.")

if __name__ == "__main__":
    try:
        # Ensure all dependencies
        print("🔍 Checking dependencies...")
        
        # Check if schedule is installed
        try:
            import schedule
        except ImportError:
            print("❌ Missing dependency: schedule")
            print("📦 Install with: pip install schedule")
            exit(1)
        
        print("✅ All dependencies found!")
        main_menu()
        
    except KeyboardInterrupt:
        print("\n👋 Application terminated by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()