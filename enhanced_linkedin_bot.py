#!/usr/bin/env python3
import os
import time
import random
import json
import logging
import hashlib
from datetime import datetime, timedelta
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, 
    StaleElementReferenceException, WebDriverException
)

from post_evaluator import PostEvaluator
from keyword_intelligence import KeywordPerformanceTracker
from comment_history import CommentHistory
from account_interests import AccountInterests
from health_monitor import AccountHealthMonitor
from human_behavior_simulator import HumanBehaviorSimulator
from enhanced_logger import EnhancedLogger
from account_manager import AccountManager
from updated_selectors import LinkedInSelectors
from enhanced_duplicate_detection import EnhancedDuplicateDetector
from comment_verification import CommentVerificationManager

class EnhancedLinkedInBot:
    """
    Enhanced LinkedIn bot with advanced features:
    - Multi-account support
    - Post quality scoring
    - Keyword intelligence
    - Human behavior mimicking
    - Comment history tracking
    - Account health monitoring
    - Enhanced duplicate detection
    - Secondary comment verification
    """
    
    def __init__(self, config_file="bot_config.json"):
        """
        Initialize the enhanced LinkedIn bot.
        
        Args:
            config_file (str): Path to configuration file
        """
        # Load configuration
        self.config = self._load_config(config_file)
        
        # Initialize account manager
        self.account_manager = AccountManager(
            config_file=self.config.get("accounts_config", "accounts_config.json"),
            encryption_key=self.config.get("master_key", None)
        )
        
        # Initialize components
        self.active_account = None
        self.driver = None
        self.keyword_tracker = None
        self.comment_history = None
        self.post_evaluator = None
        self.account_interests = None
        self.health_monitor = None
        self.behavior_simulator = None
        self.logger = None
        
        # Initialize LinkedIn-specific components
        self.linkedin_selectors = LinkedInSelectors()
        self.duplicate_detector = EnhancedDuplicateDetector(similarity_threshold=0.75)
        self.comment_verifier = None  # Will be initialized when driver is available
        
        # Create base directories
        os.makedirs("logs", exist_ok=True)
        os.makedirs("data", exist_ok=True)
        os.makedirs("accounts", exist_ok=True)
        
    def _load_config(self, config_file):
        """Load bot configuration from file."""
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Error loading config file: {config_file}")
                
        # Default configuration
        return {
            "accounts_config": "accounts_config.json",
            "default_comment_model": "llama3.2:3b",
            "ollama_url": "http://localhost:11434/api/generate",
            "min_post_score": 25,
            "default_keywords": ["artificial intelligence", "machine learning"],
            "session_cooldown_minutes": 120,
            "duplicate_similarity_threshold": 0.75,
            "comment_quality_threshold": 0.6
        }
        
    def setup_account(self, account_name):
        """
        Set up the bot for a specific account.
        
        Args:
            account_name (str): Name of the account to set up
            
        Returns:
            bool: Whether setup was successful
        """
        # Check if account exists
        account_data = self.account_manager.get_account(account_name)
        if not account_data:
            print(f"Account {account_name} not found.")
            return False
            
        # Check if account is enabled
        if not account_data.get("enabled", False):
            print(f"Account {account_name} is disabled.")
            return False
            
        # Check account health
        self.active_account = account_name
        self.health_monitor = AccountHealthMonitor(
            account_name=account_name,
            storage_dir=f"accounts/{account_name}/health"
        )
        
        health_summary = self.health_monitor.get_health_summary()
        if health_summary["health_score"] < 30:
            print(f"Account {account_name} health score too low ({health_summary['health_score']}). Skipping.")
            return False
            
        # Set up directories
        account_dirs = self.account_manager.get_account_directories(account_name)
        
        # Set up logger
        self.logger = EnhancedLogger(
            account_name=account_name,
            base_dir=account_dirs["logs"],
            encryption_key=self.config.get("master_key", None)
        )
        
        self.logger.logger.info(f"Setting up bot for account: {account_name}")
        
        # Set up keyword tracker
        keywords = account_data.get("keywords", self.config.get("default_keywords", ["artificial intelligence"]))
        initial_keyword = keywords[0] if keywords else "artificial intelligence"
        
        self.keyword_tracker = KeywordPerformanceTracker(
            initial_keyword=initial_keyword,
            storage_file=os.path.join(account_dirs["data"], "keyword_performance.json"),
            rotation_threshold=25,  # Changed from 50 to 25 successful comments
            ollama_url=self.config.get("ollama_url")
        )
        
        # Set up comment history
        self.comment_history = CommentHistory(
            account_name=account_name,
            encryption_key=self.config.get("master_key", None),
            storage_dir=os.path.join(account_dirs["data"], "comment_history"),
            retention_days=90
        )
        
        # Set up account interests
        self.account_interests = AccountInterests(
            account_name=account_name,
            storage_dir=account_dirs["data"]
        )
        
        # Set up post evaluator
        self.post_evaluator = PostEvaluator(
            target_keywords=keywords,
            min_score_threshold=self.config.get("min_post_score", 25),
            account_interests=self.account_interests
        )
        
        # Set up human behavior simulator
        self.behavior_simulator = HumanBehaviorSimulator()
        
        return True
        
    def initialize_browser(self, headless=False):
        """Initialize browser with proper profile and fingerprinting."""
        if self.active_account is None:
            self.logger.logger.error("No active account selected. Cannot initialize browser.")
            return False
            
        try:
            account_data = self.account_manager.get_account(self.active_account)
            account_dirs = self.account_manager.get_account_directories(self.active_account)
            
            # Browser profile directory
            profile_dir = os.path.join(account_dirs["profile"], "selenium")
            os.makedirs(profile_dir, exist_ok=True)
            
            # Set up browser options
            options = webdriver.ChromeOptions()
            options.add_argument(f"user-data-dir={profile_dir}")
            
            # Set up proxy if configured
            if "proxy" in account_data and account_data["proxy"].get("host"):
                proxy = account_data["proxy"]
                proxy_url = f"{proxy['host']}:{proxy['port']}"
                
                # Add proxy authentication if needed
                if "credentials" in proxy:
                    options.add_argument(f"--proxy-server={proxy_url}")
                    # Note: For authenticated proxies, you would need a proxy extension
                    # or browser automation to handle the authentication dialog
                else:
                    options.add_argument(f"--proxy-server={proxy_url}")
                    
            # Set headless mode if needed
            if headless:
                options.add_argument("--headless")
                options.add_argument("--window-size=1920,1080")
                
            # Add human-like fingerprinting
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            options.add_argument(f"user-agent={user_agent}")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)
            
            # Initialize browser
            self.driver = webdriver.Chrome(options=options)
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
                """
            })
            
            # Set window size to a common resolution
            self.driver.set_window_size(1920, 1080)
            
            # Set behavior simulator driver
            self.behavior_simulator.set_driver(self.driver)
            
            # Initialize comment verifier
            self.comment_verifier = CommentVerificationManager(
                self.driver,
                self.linkedin_selectors,
                self.duplicate_detector,
                self.logger,
                min_quality_score=self.config.get("comment_quality_threshold", 0.6)
            )
            
            self.logger.logger.info("Browser initialized successfully")
            return True
        except Exception as e:
            if hasattr(self, 'logger') and self.logger:
                self.logger.logger.error(f"Error initializing browser: {e}")
            else:
                print(f"Error initializing browser: {e}")
            return False
            
    def login_to_linkedin(self):
        """Log in to LinkedIn with the active account."""
        if not self.driver or not self.active_account:
            self.logger.logger.error("Browser or active account not initialized")
            return False
            
        try:
            account_data = self.account_manager.get_account(self.active_account)
            
            # Go to LinkedIn login page
            self.driver.get("https://www.linkedin.com/login")
            
            # Wait for the page to load
            self.behavior_simulator.adaptive_delay(2, 5)
            
            # Check if we're already logged in
            if "feed" in self.driver.current_url:
                self.logger.logger.info("Already logged in to LinkedIn")
                return True
                
            # Enter username
            username_field = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "username"))
            )
            self.behavior_simulator.type_like_human(username_field, account_data["username"])
            
            # Enter password
            password_field = self.driver.find_element(By.ID, "password")
            self.behavior_simulator.type_like_human(password_field, account_data["password"], typing_style="careful")
            
            # Click sign in
            sign_in_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            sign_in_button.click()
            
            # Wait for login to complete
            self.behavior_simulator.adaptive_delay(3, 7)
            
            # Check for captcha or verification
            page_source = self.driver.page_source.lower()
            if "captcha" in page_source or "verify" in page_source or "security check" in page_source:
                self.logger.logger.warning("Captcha or verification detected during login")
                
                # Take a screenshot
                screenshot_path = os.path.join(
                    self.account_manager.get_account_directories(self.active_account)["screenshots"],
                    f"captcha_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                )
                self.driver.save_screenshot(screenshot_path)
                
                # Record captcha event
                self.health_monitor.record_captcha_event(self.driver.current_url)
                
                # Notify about captcha
                print("CAPTCHA detected! Please complete it manually.")
                print("Bot will wait for 2 minutes...")
                
                # Wait for manual intervention
                time.sleep(120)
                
                # Check if we're logged in after manual intervention
                if "feed" in self.driver.current_url:
                    self.health_monitor.record_captcha_event(
                        self.driver.current_url, 
                        resolved=True, 
                        resolution_time=120
                    )
                    return True
                else:
                    return False
                    
            # Check if login successful
            if "feed" in self.driver.current_url or "checkpoint" in self.driver.current_url:
                self.logger.logger.info("Successfully logged in to LinkedIn")
                return True
            else:
                self.logger.logger.error("Failed to log in to LinkedIn")
                return False
                
        except Exception as e:
            self.logger.logger.error(f"Error logging in to LinkedIn: {e}")
            return False
            
    def search_for_posts(self, keyword):
        """
        Search for LinkedIn posts with the given keyword.
        
        Args:
            keyword (str): Search keyword
            
        Returns:
            list: List of post elements found
        """
        if not self.driver:
            return []
            
        try:
            # Record search activity
            self.health_monitor.record_activity("searches")
            
            # Navigate to LinkedIn feed
            self.driver.get("https://www.linkedin.com/feed/")
            self.behavior_simulator.adaptive_delay(2, 5)
            
            # Click on search box
            search_box = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[contains(@class, 'search-global-typeahead__input')]"))
            )
            search_box.click()
            self.behavior_simulator.adaptive_delay(0.5, 1.5)
            
            # Clear and type search query
            search_box.clear()
            self.behavior_simulator.type_like_human(search_box, keyword)
            self.behavior_simulator.adaptive_delay(0.5, 1.5)
            
            # Press Enter to search
            search_box.send_keys(Keys.RETURN)
            
            # Wait for search results
            self.behavior_simulator.adaptive_delay(2, 5)
            
            # Click on "Posts" tab to show only posts
            try:
                posts_tab = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Posts']"))
                )
                posts_tab.click()
                self.behavior_simulator.adaptive_delay(2, 5)
            except:
                self.logger.logger.warning("Could not find 'Posts' tab, continuing with current results")
                
            # Find all post elements
            posts = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'feed-shared-update-v2')]")
            
            # If no posts found with the primary selector, try fallback selectors
            if not posts:
                posts = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'feed-shared-update')]")
                
            if not posts:
                posts = self.driver.find_elements(By.XPATH, "//div[contains(@data-urn, 'activity')]")
                
            # Update keyword stats
            self.keyword_tracker.update_search_stats(keyword, len(posts))
            
            # Log search results
            self.logger.logger.info(f"Found {len(posts)} posts for keyword: {keyword}")
            
            # Simulate a delay between searching and processing
            self.behavior_simulator.adaptive_delay(1, 3)
            
            return posts
        except Exception as e:
            self.logger.logger.error(f"Error searching for posts: {e}")
            return []
            
    def extract_post_data(self, post_element):
        """
        Extract data from a post element.
        
        Args:
            post_element: Selenium element representing a LinkedIn post
            
        Returns:
            dict: Post data including text, author, etc.
        """
        try:
            # Create a unique ID for the post
            post_id = post_element.get_attribute("data-urn") or str(hash(post_element.text))
            
            # Extract author name
            try:
                author = post_element.find_element(By.XPATH, ".//span[contains(@class, 'feed-shared-actor__name')]").text
            except:
                try:
                    # Fallback to alternative author selectors
                    author_element = post_element.find_element(By.XPATH, 
                        ".//a[contains(@class, 'app-aware-link') and contains(@class, 'feed-shared')]//span"
                    )
                    author = author_element.text
                except:
                    author = "Unknown Author"
                    
            # Extract post text
            try:
                text_element = post_element.find_element(By.XPATH, ".//div[contains(@class, 'feed-shared-update-v2__description')]")
                post_text = text_element.text
            except:
                try:
                    # Fallback to alternative text selectors
                    text_element = post_element.find_element(By.XPATH, ".//div[contains(@class, 'feed-shared-text')]")
                    post_text = text_element.text
                except:
                    try:
                        # One more fallback
                        text_element = post_element.find_element(By.XPATH, ".//*[contains(@class, 'update-components-text')]")
                        post_text = text_element.text
                    except:
                        post_text = ""
                        
            # Create a signature for duplicate detection
            signature = hashlib.md5(f"{author}:{post_text[:100]}".encode()).hexdigest()
            
            # Create post data
            post_data = {
                "id": post_id,
                "author": author,
                "text": post_text,
                "element": post_element,
                "signature": signature,
                "timestamp": datetime.now().isoformat()
            }
            
            # Record viewing this post
            self.health_monitor.record_activity("posts")
            
            return post_data
        except Exception as e:
            self.logger.logger.error(f"Error extracting post data: {e}")
            traceback.print_exc()  # Print stack trace for debugging
            return None
            
    def generate_comment(self, post_data):
        """
        Generate a comment for a post.
        
        Args:
            post_data (dict): Post data
            
        Returns:
            str: Generated comment
        """
        # This would call your existing comment generation function
        # Assuming a function like generate_comment_ollama exists
        return self.generate_comment_ollama(post_data["text"])
        
    def generate_comment_ollama(self, post_text):
        """
        Generate a comment using Ollama API.
        Placeholder implementation - replace with actual implementation.
        
        Args:
            post_text (str): Post text to comment on
            
        Returns:
            str: Generated comment
        """
        # Placeholder - replace with actual implementation
        return f"This is a thoughtful comment about the post that mentions key points and adds value to the discussion."
            
    def is_duplicate_comment(self, comment_text):
        """
        Enhanced duplicate comment detection using our improved detector.
        
        Args:
            comment_text (str): Comment text to check
            
        Returns:
            bool: Whether the comment is a duplicate
        """
        # Get recent comments from history
        recent_comments = []
        for comment_data in list(self.comment_history.comments.values())[-30:]:
            recent_comments.append(comment_data.get("comment_text", ""))
            
        # Check if any of the recent comments are similar to this one
        for existing_comment in recent_comments:
            is_duplicate, score, method = self.duplicate_detector.is_duplicate(
                comment_text, existing_comment
            )
            
            if is_duplicate:
                self.logger.logger.warning(
                    f"Duplicate comment detected. Similarity score: {score:.2f}, method: {method}"
                )
                return True
                
        return False
            
    def post_comment(self, post_data, comment_text):
        """
        Enhanced method to post a comment on a LinkedIn post with advanced verification.
        
        Args:
            post_data (dict): Post data
            comment_text (str): Comment text to post
            
        Returns:
            bool: Whether comment was posted successfully
        """
        if not post_data or not comment_text:
            return False
            
        try:
            post_element = post_data["element"]
            
            # Scroll to the post
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", post_element)
            self.behavior_simulator.adaptive_delay(1, 3)
            
            # Find comment button using our enhanced selectors
            comment_button = self.linkedin_selectors.find_element_with_fallbacks(
                post_element, self.linkedin_selectors.COMMENT_BUTTON_SELECTORS
            )
            
            if not comment_button:
                self.logger.logger.error("Could not find comment button")
                return False
                
            comment_button.click()
            self.behavior_simulator.adaptive_delay(1, 3)
            
            # Find comment input using our enhanced selectors
            comment_input = self.linkedin_selectors.find_element_with_fallbacks(
                post_element, self.linkedin_selectors.COMMENT_INPUT_SELECTORS
            )
            
            if not comment_input:
                # Try finding in the entire driver context in case the comment box is in a different container
                comment_input = self.linkedin_selectors.find_element_with_fallbacks(
                    self.driver, self.linkedin_selectors.COMMENT_INPUT_SELECTORS
                )
                
            if not comment_input:
                self.logger.logger.error("Could not find comment input field")
                return False
                
            comment_input.click()
            self.behavior_simulator.adaptive_delay(0.5, 1.5)
            
            # Type comment
            self.behavior_simulator.type_like_human(comment_input, comment_text, typing_style="normal")
            self.behavior_simulator.adaptive_delay(1, 3)
            
            # Find submit button using our enhanced selectors
            post_button = self.linkedin_selectors.find_element_with_fallbacks(
                post_element, self.linkedin_selectors.COMMENT_POST_BUTTON_SELECTORS
            )
            
            if not post_button:
                # Try finding in the entire driver context
                post_button = self.linkedin_selectors.find_element_with_fallbacks(
                    self.driver, self.linkedin_selectors.COMMENT_POST_BUTTON_SELECTORS
                )
                
            if not post_button:
                self.logger.logger.error("Could not find post comment button")
                return False
                
            # Check if post button is enabled
            if not post_button.is_enabled():
                self.logger.logger.error("Post button is disabled")
                return False
                
            post_button.click()
            
            # Wait for comment to post
            self.behavior_simulator.adaptive_delay(2, 5)
            
            # Take a screenshot
            screenshot_path = os.path.join(
                self.account_manager.get_account_directories(self.active_account)["screenshots"],
                f"comment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            )
            self.driver.save_screenshot(screenshot_path)
            
            # Verify that the comment was actually posted
            comment_verified, comment_element = self.comment_verifier.verify_comment_posted(
                post_element, comment_text
            )
            
            if not comment_verified:
                self.logger.logger.warning("Failed to verify comment was posted")
                return False
                
            # Record the comment
            self.comment_history.record_comment(post_data, comment_text)
            
            # Record interaction with account interests
            self.account_interests.record_interaction(post_data)
            
            # Record comment activity
            self.health_monitor.record_activity("comments")
            
            # Log the comment
            self.logger.log_comment(post_data, comment_text, True)
            
            # Update keyword stats
            current_keyword = self.keyword_tracker.select_next_keyword()
            self.keyword_tracker.update_comment_stats(current_keyword, success=True)
            
            return True
        except Exception as e:
            self.logger.log_error("comment_error", str(e), {"post_id": post_data.get("id")})
            traceback.print_exc()  # Print stack trace for debugging
            return False
            
    def refresh_browser(self):
        """Refresh the browser to maintain session stability."""
        if self.driver:
            try:
                # Save current URL
                current_url = self.driver.current_url
                
                # Refresh the page
                self.driver.refresh()
                
                # Wait for page to load
                self.behavior_simulator.adaptive_delay(2, 5)
                
                self.logger.logger.info("Browser refreshed successfully")
                return True
            except Exception as e:
                self.logger.logger.error(f"Error refreshing browser: {e}")
                return False
        return False
        
    def process_posts(self, keyword, max_comments=5):
        """
        Process LinkedIn posts for a given keyword.
        
        Args:
            keyword (str): Search keyword
            max_comments (int): Maximum number of comments to post
            
        Returns:
            int: Number of comments posted
        """
        if not self.driver:
            return 0
            
        # Check account health first
        health_limits = self.health_monitor.check_daily_limits()
        if health_limits["limits_reached"]:
            self.logger.logger.warning(f"Daily limits reached: {health_limits['recommendations']}")
            return 0
            
        # Search for posts with the keyword
        posts = self.search_for_posts(keyword)
        posts_found = len(posts)
        
        if not posts:
            self.logger.logger.warning(f"No posts found for keyword: {keyword}")
            return 0
            
        # Simulate browsing behavior
        self.behavior_simulator.simulate_browsing_behavior((15, 40))
        
        # Process posts
        comments_posted = 0
        processed_posts = 0
        
        for post in posts:
            # Extract post data
            post_data = self.extract_post_data(post)
            if not post_data:
                continue
                
            processed_posts += 1
            
            # Check if we've already commented on this post
            if self.comment_history.has_commented(post_data["id"]):
                self.logger.logger.info(f"Already commented on post: {post_data['id']}")
                continue
                
            # Check if this is a duplicate post
            if self.comment_history.is_duplicate_post(post_data["signature"]):
                self.logger.logger.info(f"Duplicate post detected: {post_data['signature']}")
                continue
                
            # Evaluate post quality
            evaluation = self.post_evaluator.evaluate_post(post_data)
            self.logger.log_event("post_evaluation", {
                "post_id": post_data["id"],
                "score": evaluation["total_score"],
                "pass_threshold": evaluation["pass_threshold"]
            })
            
            # Skip if post doesn't meet quality threshold
            if not evaluation["pass_threshold"]:
                self.logger.logger.info(f"Post quality too low: {evaluation['total_score']}/50")
                continue
                
            # Simulate reading the post content
            if post_data["text"]:
                self.behavior_simulator.simulate_reading(len(post_data["text"]))
                
            # Generate comment
            comment_text = self.generate_comment(post_data)
            
            # Check if comment is a duplicate
            if self.is_duplicate_comment(comment_text):
                self.logger.logger.info("Generated comment too similar to recent comments, skipping")
                continue
                
            # Post comment
            success = self.post_comment(post_data, comment_text)
            if success:
                comments_posted += 1
                self.logger.logger.info(f"Comment posted successfully ({comments_posted}/{max_comments})")
                
                # Refresh browser after comment to increase stability
                self.refresh_browser()
                
                # Add some delay between comments
                comment_delay = random.uniform(10, 25)
                self.behavior_simulator.adaptive_delay(comment_delay, comment_delay + 10)
                
                # Check if we've reached the maximum comments
                if comments_posted >= max_comments:
                    break
            else:
                self.logger.logger.warning("Failed to post comment")
                
            # Check if we need to rotate keywords after 25 successful comments
            if self.keyword_tracker.should_rotate_keyword(keyword):
                self.logger.logger.info(f"Rotating keyword after {self.keyword_tracker.rotation_threshold} comments")
                break
                
        # Update keyword tracker stats
        self.keyword_tracker.update_search_stats(keyword, posts_found)
        
        return comments_posted
        
    def run_session(self):
        """Enhanced run_session with secondary comment verification."""
        # Select next account
        account_name = self.account_manager.select_next_account()
        if not account_name:
            print("No available accounts to use.")
            return False
            
        # Check if account is scheduled now
        if not self.account_manager.is_account_scheduled_now(account_name):
            print(f"Account {account_name} is not scheduled to run now.")
            return False
            
        # Set up account
        if not self.setup_account(account_name):
            print(f"Failed to set up account: {account_name}")
            return False
            
        try:
            # Initialize browser
            if not self.initialize_browser():
                return False
                
            # Login to LinkedIn
            if not self.login_to_linkedin():
                return False
                
            # Get account settings
            account_data = self.account_manager.get_account(account_name)
            max_comments_per_session = account_data.get("schedule", {}).get("max_comments_per_session", 5)
            
            # Select keyword
            current_keyword = self.keyword_tracker.select_next_keyword()
            self.logger.logger.info(f"Selected keyword: {current_keyword}")
            
            # Process posts with the keyword
            comments_posted = self.process_posts(current_keyword, max_comments_per_session)
            
            # Check if we need to rotate to a new keyword
            if self.keyword_tracker.should_rotate_keyword(current_keyword):
                new_keyword = self.keyword_tracker.select_next_keyword(current_keyword)
                self.logger.logger.info(f"Rotated to new keyword: {new_keyword}")
                
            # SECONDARY VERIFICATION: Check and manage comments after the session
            if comments_posted > 0:
                self.logger.logger.info("Running secondary comment verification...")
                verification_results = self.comment_verifier.check_and_manage_comments(
                    max_comments=max_comments_per_session * 2,  # Check twice as many comments as we posted
                    delete_duplicates=True,
                    delete_low_quality=True
                )
                
                self.logger.logger.info(
                    f"Comment verification results: {verification_results['comments_checked']} checked, "
                    f"{verification_results['duplicates_found']} duplicates, "
                    f"{verification_results['low_quality_found']} low quality, "
                    f"{verification_results['comments_deleted']} deleted"
                )
                
            # Log session stats
            self.logger.logger.info(f"Session completed - Comments posted: {comments_posted}")
            
            # Update account health
            health_summary = self.health_monitor.get_health_summary()
            self.account_manager.update_account_health(account_name, health_summary["health_score"])
            
            # End session logging
            if self.logger:
                self.logger.log_session_end()
                
            return True
        except Exception as e:
            if self.logger:
                self.logger.log_error("session_error", str(e))
            traceback.print_exc()  # Print stack trace for debugging
            return False
        finally:
            # Clean up
            if self.driver:
                self.driver.quit()
                
    def run_scheduled_session(self):
        """Run a session if scheduled, with proper timing."""
        # Get accounts scheduled for now
        scheduled_accounts = self.account_manager.get_scheduled_accounts()
        
        if not scheduled_accounts:
            print("No accounts scheduled to run now.")
            return False
            
        # Select one of the scheduled accounts (randomly to add variability)
        account_name = random.choice(scheduled_accounts)
        
        # Check cooldown
        if self.account_manager.check_cooldown(account_name):
            print(f"Account {account_name} is still in cooldown period.")
            return False
            
        # Run session with selected account
        print(f"Running scheduled session for account: {account_name}")
        return self.run_session()