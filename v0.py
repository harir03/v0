import os
import time
import uuid
import json
import requests
import hashlib
import random
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
OLLAMA_URL = "http://localhost:11434/api/generate"  # Default Ollama endpoint

# Ensure screenshots directory exists
if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

# --- Post Tracking Class ---
class PostTracker:
    """Track processed posts to avoid duplicates and manage state."""
    def __init__(self):
        self.processed_posts = set()  # Stores IDs of all posts attempted
        self.commented_posts = set()  # Stores IDs of successfully commented posts
        self.failed_posts = set()     # Stores IDs of posts where commenting failed
        self.post_signatures = {}     # Stores post signatures (hash of content + author) for robust duplicate detection
    
    def is_processed(self, post_id):
        """Check if a post has already been processed (attempted)."""
        return post_id in self.processed_posts
    
    def is_commented(self, post_id):
        """Check if a post has already been successfully commented on."""
        return post_id in self.commented_posts
    
    def mark_processed(self, post_id, signature=None):
        """Mark a post as processed, optionally storing its signature."""
        self.processed_posts.add(post_id)
        if signature:
            self.post_signatures[post_id] = signature
    
    def mark_commented(self, post_id, signature=None):
        """Mark a post as successfully commented, also marking it as processed."""
        self.commented_posts.add(post_id)
        self.processed_posts.add(post_id) # A commented post is also a processed one
        if signature:
            self.post_signatures[post_id] = signature
    
    def mark_failed(self, post_id, signature=None):
        """Mark a post as failed, also marking it as processed."""
        self.failed_posts.add(post_id)
        self.processed_posts.add(post_id) # A failed post is also a processed one
        if signature:
            self.post_signatures[post_id] = signature
    
    def is_duplicate_signature(self, signature):
        """Check if we've seen this post signature before, indicating a duplicate."""
        return signature in self.post_signatures.values()
    
    def get_stats(self):
        """Return current statistics on processed posts."""
        return {
            "processed": len(self.processed_posts),
            "commented": len(self.commented_posts),
            "failed": len(self.failed_posts)
        }

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
        """
        Generates a custom, professional LinkedIn comment based on the post content.
        Includes a retry mechanism if the generated comment fails validation.
        
        Args:
            post_text (str): The full text content of the LinkedIn post.
            author_name (str, optional): The name of the post's author. Defaults to None.
            post_type (str, optional): The type of post (e.g., "general", "technical"). Not currently used.
            retries (int): Number of times to retry comment generation if validation fails.
        
        Returns:
            str: A generated comment if successful, None otherwise.
        """
        # Clean the post text to get actual content, removing LinkedIn UI elements
        cleaned_text = self.extract_actual_content(post_text)
        
        for attempt in range(retries + 1): # +1 for the initial attempt
            prompt = f"""
You are writing a professional and insightful LinkedIn comment. Be authentic, engaging, and add value to the conversation.

POST CONTENT:
{cleaned_text[:1000]} # Limit input to avoid exceeding context window

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
                print(f"🔄 Retrying comment generation (Attempt {attempt}/{retries})...")
                prompt += f"\n\nPrevious comment failed validation. Please ensure the comment is strictly between 10 and 30 words."

            try:
                payload = {
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False, # We want the full response at once
                    "options": {
                        "temperature": 0.8, # Higher temperature for more creativity
                        "top_p": 0.9,       # Control diversity
                        "max_tokens": 25,  # Adjusted for 10-30 words (approx 1.5 tokens per word, aiming for max 30 words)
                        "stop": ["\n\n", "Comment:", "Response:", "Reply:"] # Stop generation at these phrases
                    }
                }
                
                response = requests.post(self.ollama_url, json=payload, timeout=45) # Increased timeout
                
                if response.status_code == 200:
                    result = response.json()
                    comment = result.get("response", "").strip()
                    
                    # Clean up the generated comment
                    comment = self.clean_comment(comment)
                    
                    print(f"🤖 Generated comment: {comment}")
                    
                    if self.is_valid_comment(comment):
                        return comment
                    else:
                        print(f"⚠️ Generated comment failed validation: '{comment}'")
                        # Will retry if 'attempt' is less than 'retries'
                else:
                    print(f"❌ Ollama API error: {response.status_code} - {response.text}")
                    return None # Exit if API error
                    
            except requests.exceptions.Timeout:
                print("❌ Error generating comment: Ollama request timed out.")
                # Will retry if 'attempt' is less than 'retries'
            except requests.exceptions.RequestException as e:
                print(f"❌ Error generating comment (network/request issue): {e}")
                return None # Exit if network/request error
            except Exception as e:
                print(f"❌ Unexpected error generating comment: {e}")
                return None # Exit for other unexpected errors
        
        print(f"❌ Failed to generate a valid comment after {retries+1} attempts.")
        return None # Return None if all retries fail
    
    def generate_related_keywords(self, current_keyword, num_keywords=3):
        """
        Generates a list of related keywords using Ollama.
        """
        prompt = f"""
Generate {num_keywords} highly relevant and professional LinkedIn search keywords related to "{current_keyword}".
Provide them as a comma-separated list, without any introductory or concluding sentences.
Examples:
If current_keyword is "AI development", output: Machine Learning, Deep Learning, Artificial Intelligence Ethics
If current_keyword is "cloud computing", output: AWS Cloud, Azure Services, Google Cloud Platform
Keywords:
"""
        try:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 50 # Enough for a few keywords
                }
            }
            response = requests.post(self.ollama_url, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                keywords_str = result.get("response", "").strip()
                keywords = [k.strip() for k in keywords_str.split(',') if k.strip()]
                print(f"🤖 Generated new keywords: {keywords}")
                return keywords
            else:
                print(f"❌ Ollama API error generating keywords: {response.status_code} - {response.text}")
                return []
        except requests.exceptions.RequestException as e:
            print(f"❌ Error generating keywords (network/request issue): {e}")
            return []
        except Exception as e:
            print(f"❌ Unexpected error generating keywords: {e}")
            return []

    def extract_actual_content(self, post_text):
        """
        Extracts the core content of a LinkedIn post by filtering out common UI elements
        and metadata often scraped along with the actual text.
        """
        lines = post_text.split('\n')
        content_lines = []
        
        # Patterns to identify and skip LinkedIn UI elements or metadata
        # Expanded and refined based on recent logs
        skip_patterns = [
            '• 1st', '• 2nd', '• 3rd', 'Feed post', 'Like', 'Comment', 'Repost', 'Share', 'Send',
            'views', 'reactions', 'comments', 'Follow', 'Connect', 'Message',
            'ago', 'min', 'hour', 'day', 'week', 'month', 'year',
            'promoted', 'Ad', 'Show all reactions', 'See all comments',
            'See translation', 'Translate', 'Liked by', 'commented on this',
            'reactions', 'shares', 'comments', 'views', 'Followers', 'Connections',
            'View all', 'Show more', 'Show less', '…more', '…see more',
            'React', 'Add a comment', 'Write a comment', 'Post', 'Reply',
            # Specific profile/metadata lines that appear in post_text:
            'Software Engineering Leader, Cloud Operatio',
            'Flutter, AI/ML, 7k+ on SO, Blog (malwinder.com)',
            'Building Production AI Systems: Compute',
            'Small entrepreneur in hospitality. #SustainableTouris',
            '𝕯𝖊𝖒𝖆𝖓𝖉 𝕿𝖍𝖊 𝖎𝖒𝖕𝖔𝖘𝖘𝖎𝖇𝖑𝖊',
            'CA Finalist',
            'ISO 27001:2022 LA | CISM | CEH v11 | Operations S',
            'Arvind Kumar Shahi',
            'Who writes it better -', '💻AI (Artificial Intelligence) or Me? ✍️', 'Swipe to see the results and dive in',
            'Activate to view larger image',
            'Subscribe', 'Subscribe to {:entityName}', 'Come mai uso l’#Ai? / Why do I use Ai?',
            # Video player related text
            'Play', 'Loaded:', 'Remaining time', '1x', 'Playback speed', 'Turn closed captions off', 'Unmute', 'Turn fullscreen', 'Turn fullscreen on',
            # Job post related text
            'Job Title:', 'Job by', 'View job', '#hiring', 'GCP Trainer'
        ]
        
        # Convert skip patterns to lowercase for case-insensitive matching
        skip_patterns_lower = [p.lower() for p in skip_patterns]

        # Heuristic to find the start of actual content
        # Look for the first line that seems like actual content (not metadata or short UI text)
        content_start_index = 0
        for i, line in enumerate(lines):
            stripped_line = line.strip()
            # A line is considered potential content if it's long enough and doesn't match a skip pattern
            if len(stripped_line) > 20 and not any(sp in stripped_line.lower() for sp in skip_patterns_lower):
                content_start_index = i
                break
        
        # Collect content lines from the determined start index
        for i in range(content_start_index, len(lines)):
            line = lines[i].strip()
            # Only add lines that are not too short and do not contain skip patterns
            if line and len(line) > 15 and not any(pattern in line.lower() for pattern in skip_patterns_lower):
                content_lines.append(line)
        
        content = ' '.join(content_lines)
        
        # If filtering removed too much, return the original text as a fallback
        # This prevents cases where the filter might be too aggressive on short, but valid, posts
        if len(content) < 50 and len(post_text) > 50:
            print(f"⚠️ Filtered content too short ({len(content)} chars), falling back to original post text.")
            return post_text
                
        return content
    
    def clean_comment(self, comment):
        """Cleans and formats the generated comment for posting on LinkedIn."""
        # Remove leading/trailing quotes if the model added them
        comment = comment.strip('"\'').strip()
        
        # Remove any explicit prefixes the model might have added (e.g., "Comment:")
        prefixes_to_remove = [
            "Comment:", "Response:", "Reply:", "LinkedIn comment:",
            "Professional comment:", "Comment text:", "Here's a comment:"
        ]
        
        for prefix in prefixes_to_remove:
            if comment.lower().startswith(prefix.lower()):
                comment = comment[len(prefix):].strip()
        
        # Ensure the first letter is capitalized
        if comment:
            comment = comment[0].upper() + comment[1:] if len(comment) > 1 else comment.upper()
        
        # Remove multiple spaces and normalize whitespace
        comment = " ".join(comment.split())
        
        return comment
    
    def is_valid_comment(self, comment):
        """
        Validates if the generated comment meets basic quality and length criteria
        for a professional LinkedIn comment.
        """
        words = comment.split()
        
        # Check minimum and maximum word count (updated to 10-30 words)
        if not comment or len(words) < 10 or len(words) > 30: 
            print(f"Validation failed: Comment has {len(words)} words (expected 10-30).")
            return False
        
        # Check for overly generic responses (more robustly)
        generic_phrases = [
            "great post!", "thanks for sharing!", "nice article!", "good point!",
            "totally agree!", "so true!", "well said!", "awesome!", "cool!", "nice!",
            "amazing!", "this is insightful!", "very interesting!"
        ]
        
        comment_lower = comment.lower().strip()
        # Reject if the comment is very short AND exactly matches a generic phrase
        if len(words) <= 5 and comment_lower in [phrase.lower() for phrase in generic_phrases]:
            print(f"Validation failed: Comment is too generic and short: '{comment}'.")
            return False
        
        return True

# --- Selenium Driver Setup ---
def create_driver():
    """
    Creates and configures a Selenium WebDriver for Brave browser.
    It uses a pre-existing user profile to maintain login sessions.
    Includes anti-detection measures.
    """
    brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
    # Adjust user_data_dir for cross-platform compatibility if needed, but AppData is Windows-specific
    user_data_dir = os.path.expanduser("~") + "/AppData/Local/BraveSoftware/Brave-Browser/User Data"
    profile_dir = "Default" # Typically "Default" for the main profile

    options = Options()
    options.binary_location = brave_path
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument(f"--profile-directory={profile_dir}")
    options.add_experimental_option("detach", True) # Keep browser open after script finishes
    
    # Add anti-detection measures
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Suppress console logging from Brave browser
    options.add_argument("--log-level=3") 
    options.add_argument("--disable-logging")

    service = Service() # Assumes chromedriver.exe is in PATH or specified
    driver = webdriver.Chrome(service=service, options=options)
    
    # Execute JavaScript to further hide WebDriver signature
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.maximize_window()
    print("✅ Brave browser driver created and configured.")
    return driver

# --- LinkedIn Interaction Functions ---
def apply_post_filter(driver):
    """
    Attempts to apply the "Posts" filter on the LinkedIn search results page.
    Uses multiple robust selectors and waits.
    """
    print("🔄 Attempting to apply 'Posts' filter... (This might be skipped if already applied)")
    filter_selectors = [
        # Common LinkedIn filter button patterns
        "//button[contains(@aria-label, 'Filter by: Posts')]",
        "//button[contains(@aria-label, 'Posts filter')]",
        "//button[contains(@class, 'search-filter-button') and contains(span/text(), 'Posts')]",
        "//button[contains(@class, 'search-reusables__filter-pill-button') and contains(span/text(), 'Posts')]",
        "//button[contains(@class, 'artdeco-pill') and contains(span/text(), 'Posts')]",
        "//button[contains(text(), 'Posts') and contains(@class, 'search-facet-button')]",
        "//div[contains(@class, 'search-s-facet')]//button[contains(text(), 'Posts')]" # Older selector
    ]
    
    for selector in filter_selectors:
        try:
            # Check if the filter is already active (e.g., has 'selected' or 'active' class)
            # This prevents unnecessary clicks and potential issues
            filter_button = WebDriverWait(driver, 3).until( # Shorter wait for existence
                EC.presence_of_element_located((By.XPATH, selector))
            )
            if "selected" in filter_button.get_attribute("class") or "active" in filter_button.get_attribute("class"):
                print(f"   - Posts filter appears to be already active with selector '{selector}'. Skipping click.")
                return True # Filter is already applied
            
            # If not active, try to click
            filter_button = WebDriverWait(driver, 5).until( # Longer wait for clickability
                EC.element_to_be_clickable((By.XPATH, selector))
            )
            # Use JavaScript click as it's often more reliable for hidden/covered elements
            driver.execute_script("arguments[0].click();", filter_button)
            print("✅ Posts filter applied successfully.")
            time.sleep(3) # Give time for the filter to apply and content to reload
            return True
        except TimeoutException:
            # print(f"   - Selector '{selector}' timed out or not clickable.")
            continue
        except Exception as e:
            print(f"   - Error clicking filter with selector '{selector}': {e}")
            continue
            
    print("⚠️ Could not find or click 'Posts' filter button. Continuing without filter.")
    return False

def scroll_feed(driver, scroll_times=10, delay_per_scroll=3):
    """
    Scrolls the LinkedIn feed to load more content.
    
    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        scroll_times (int): Number of times to scroll down.
        delay_per_scroll (int): Seconds to wait after each scroll.
    """
    print(f"🔄 Scrolling to load more posts ({scroll_times} times)...")
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    for i in range(scroll_times):
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay_per_scroll) # Wait for new content to load
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("📄 No more content loading (reached end of feed or no new content).")
            break # No new content loaded, stop scrolling
        
        last_height = new_height
        print(f"⬇️ Scrolled {i+1}/{scroll_times} - Page height: {new_height}")
    
    # Scroll back up slightly to ensure elements are in view for interaction
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.3);")
    time.sleep(1)

def create_post_signature(post_text, author_name):
    """
    Creates a unique hash signature for a post based on its cleaned content and author.
    This helps in detecting duplicates even if post IDs change or are unreliable.
    """
    # Clean the post text for signature generation
    cleaned_text = post_text.replace('\n', ' ').strip()
    # Use the first 200 characters of the cleaned text to form the signature
    signature_text = f"{author_name}:{cleaned_text[:200]}"
    return hashlib.md5(signature_text.encode('utf-8')).hexdigest()

def get_robust_post_id(post_element, driver):
    """
    Attempts to extract a unique ID for a post using multiple robust methods,
    prioritizing LinkedIn's internal URNs or data attributes.
    """
    try:
        # Method 1: Try data-urn attribute (most reliable LinkedIn identifier)
        data_urn = post_element.get_attribute("data-urn")
        if data_urn and data_urn.strip():
            return data_urn.strip()
            
        # Method 2: Try to find activity ID in nested elements (older LinkedIn structure)
        activity_selectors = [
            ".//div[contains(@class, 'feed-shared-update-v2')]",
            ".//article[contains(@class, 'feed-shared-update-v2')]",
            ".//div[@data-id]" # Generic data-id
        ]
        
        for selector in activity_selectors:
            try:
                element = post_element.find_element(By.XPATH, selector)
                for attr in ['data-id', 'data-urn', 'id']:
                    value = element.get_attribute(attr)
                    if value and value.strip():
                        return value.strip()
            except NoSuchElementException:
                continue # Element not found with this selector
            except StaleElementReferenceException:
                raise # Re-raise if element becomes stale, handled upstream
            except Exception as e:
                print(f"   - Error in get_robust_post_id (Method 2, selector {selector}): {e}")
                continue
                
        # Method 3: Try to find post URL and extract ID from it
        try:
            post_link = post_element.find_element(By.XPATH, ".//a[contains(@href, '/feed/update/')]")
            href = post_link.get_attribute("href")
            if href:
                # Extract activity ID from URL (e.g., "...activity-7123456789...")
                if "activity-" in href:
                    activity_id = href.split("activity-")[1].split("/")[0].split("?")[0]
                    return f"activity-{activity_id}"
        except NoSuchElementException:
            pass # No post link found
        except StaleElementReferenceException:
            raise
        except Exception as e:
            print(f"   - Error in get_robust_post_id (Method 3): {e}")
            
        # Method 4: Create a semi-unique ID from element's location and a text hash
        # This is a last resort and less reliable for true uniqueness across sessions
        try:
            location = post_element.location
            text_preview = post_element.text[:100].replace('\n', ' ').strip()
            combined = f"{location['x']}-{location['y']}-{hash(text_preview)}"
            return f"location-{hashlib.md5(combined.encode()).hexdigest()[:10]}"
        except StaleElementReferenceException:
            raise
        except Exception as e:
            print(f"   - Error in get_robust_post_id (Method 4): {e}")
            
        # Method 5: Fallback to a hash of the element's outer HTML (least reliable)
        element_html = post_element.get_attribute("outerHTML")[:500] # Use a portion to avoid excessively long hashes
        return f"element-{hashlib.md5(element_html.encode()).hexdigest()[:10]}"
            
    except StaleElementReferenceException:
        raise # Let the calling function handle stale elements
    except Exception as e:
        print(f"⚠️ Error getting robust post ID: {e}")
        return f"fallback-{uuid.uuid4().hex[:10]}" # Generate a truly random fallback ID

def find_posts_improved(driver):
    """
    Finds all potential LinkedIn post elements on the current page using multiple,
    robust XPath selectors. Filters out duplicates based on element identity.
    """
    post_selectors = [
        # Most common LinkedIn post container classes (current and recent past)
        "//div[contains(@class, 'feed-shared-update-v2')]",
        "//article[contains(@class, 'feed-shared-update-v2')]",
        "//div[contains(@class, 'update-components-post')]",
        "//div[contains(@class, 'feed-shared-update') and @data-urn]", # Posts with URN
        
        # Broader or older selectors as fallbacks
        "//div[contains(@class, 'feed-update')]",
        "//div[contains(@class, 'scaffold-finite-scroll__content')]//div[contains(@class, 'oc-feed-updates-container')]",
        "//div[contains(@class, 'scaffold-finite-scroll__content')]//div[contains(@class, 'ember-view') and @data-urn]"
    ]
    
    all_posts = []
    
    for selector in post_selectors:
        try:
            posts = driver.find_elements(By.XPATH, selector)
            if posts:
                print(f"✅ Found {len(posts)} potential posts using selector: '{selector}'")
                all_posts.extend(posts)
        except Exception as e:
            print(f"⚠️ Error with selector '{selector}': {e}")
            continue
            
    # Remove duplicates based on element's internal ID (memory address)
    unique_posts = []
    seen = set()
    for post in all_posts:
        try:
            element_id = id(post) # Unique identifier for the WebElement object
            if element_id not in seen:
                seen.add(element_id)
                unique_posts.append(post)
        except StaleElementReferenceException:
            # If an element becomes stale during this check, skip it
            continue
        except Exception as e:
            print(f"⚠️ Error processing post for uniqueness: {e}")
            continue
            
    print(f"📊 Total unique posts found on page: {len(unique_posts)}")
    return unique_posts

def extract_post_data(post_element, driver):
    """
    Extracts comprehensive data (ID, text, author, element reference, signature)
    from a given LinkedIn post element.
    """
    try:
        # Expand "see more" if present to get full post text
        try:
            read_more_selectors = [
                ".//span[text()='…see more']/..", # Common "see more" text
                ".//button[contains(text(), '…see more')]",
                ".//button[contains(@aria-label, 'Expand post content')]",
                ".//button[contains(@class, 'feed-shared-text__see-more-link')]"
            ]
            for selector in read_more_selectors:
                try:
                    read_more = post_element.find_element(By.XPATH, selector)
                    if read_more.is_displayed() and read_more.is_enabled():
                        driver.execute_script("arguments[0].click();", read_more)
                        time.sleep(1) # Short pause for content to expand
                        break
                except NoSuchElementException:
                    continue
                except StaleElementReferenceException:
                    raise # Re-raise to be handled by the caller
                except Exception as e:
                    print(f"   - Error expanding 'see more' with selector '{selector}': {e}")
                    continue
        except StaleElementReferenceException:
            raise
        except Exception as e:
            print(f"   - General error during 'see more' expansion: {e}")
            pass # Continue even if "see more" fails
            
        # Extract post text (get full text after potential expansion)
        post_text = post_element.text
        
        # Try to extract author name more reliably
        author_name = None
        author_selectors = [
            ".//a[contains(@href, '/in/')]//span[@aria-hidden='true']", # Primary: link to profile, then name
            ".//span[contains(@class, 'feed-shared-actor__name')]/span[@aria-hidden='true']",
            ".//span[contains(@class, 'update-components-actor__name')]/span[@aria-hidden='true']",
            ".//a[contains(@class, 'feed-shared-actor__name')]/span[@aria-hidden='true']",
            ".//span[contains(@class, 'actor-name')]", # Broader
            ".//h3//span[@aria-hidden='true']" # Sometimes author is in h3
        ]
        
        for selector in author_selectors:
            try:
                author_element = post_element.find_element(By.XPATH, selector)
                author_name = author_element.text.strip()
                if author_name and len(author_name) > 2: # Ensure it's a meaningful name
                    break
            except NoSuchElementException:
                continue
            except StaleElementReferenceException:
                raise
            except Exception as e:
                print(f"   - Error extracting author with selector '{selector}': {e}")
                continue
        
        # Get robust post ID
        post_id = get_robust_post_id(post_element, driver)
        
        # Create signature for duplicate detection
        signature = create_post_signature(post_text, author_name or "Unknown")
        
        print(f"📊 Extracted post data - ID: {post_id}, Author: {author_name or 'N/A'}, Signature: {signature[:8]}...")
        
        return {
            "id": post_id,
            "text": post_text,
            "author": author_name,
            "element": post_element, # Keep reference to the element for later interaction
            "signature": signature
        }
    except StaleElementReferenceException:
        raise # Let the calling function handle stale elements
    except Exception as e:
        print(f"❌ Error extracting post data: {e}")
        return None

def find_comment_button_enhanced(driver, post_element):
    """
    Enhanced comment button finder with LinkedIn's latest DOM structure.
    It attempts to find the comment button within a given post element.
    """
    # Ensure the post element is in view before trying to find its children
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", post_element)
    time.sleep(1) # Short pause after scrolling
    
    # Updated and comprehensive selectors for LinkedIn's comment button
    comment_selectors = [
        # Most common and stable selectors (from original code)
        './/button[contains(@aria-label, "Comment on") and contains(@class, "react-button")]',
        './/button[contains(@aria-label, "Comment") and contains(@class, "social-actions-button")]',
        './/button[contains(@data-control-name, "comment_single_feed")]', # Specific data attribute
        './/button[contains(@class, "feed-shared-social-action-bar__action-button") and .//span[text()="Comment"]]',
        
        # Other common patterns (from original code)
        './/button[contains(@aria-label, "Add a comment")]',
        './/button[contains(text(), "Comment") and contains(@class, "artdeco-button")]',
        './/div[contains(@class, "social-actions")]//button[contains(@aria-label, "Comment")]',
        './/div[contains(@class, "feed-shared-social-actions")]//button[contains(@aria-label, "Comment")]',
        
        # Fallback selectors (less specific but might catch edge cases from original code)
        './/button[contains(text(), "Comment")]', # Just text "Comment"
        './/span[contains(text(), "Comment")]/ancestor::button', # Find span with text, then its button ancestor
        './/button[contains(@class, "comments-button")]'
    ]
    
    for i, selector in enumerate(comment_selectors):
        try:
            # Find all elements matching the selector within the post_element
            elements = post_element.find_elements(By.XPATH, selector)
            for element in elements:
                try:
                    # Check if the element is visible and enabled
                    if element.is_displayed() and element.is_enabled():
                        # Further verify by checking aria-label or text content
                        aria_label = element.get_attribute("aria-label") or ""
                        button_text = element.text.lower()
                        
                        if "comment" in aria_label.lower() or "comment" in button_text:
                            print(f"✅ Found comment button using selector #{i+1}: '{selector}'")
                            return element
                except StaleElementReferenceException:
                    print(f"   - Element became stale during check for selector '{selector}'.")
                    continue # Try next element or selector
                except Exception as e:
                    print(f"   - Error checking element for selector '{selector}': {e}")
                    continue
        except NoSuchElementException:
            continue # No elements found with this selector, try next
        except StaleElementReferenceException:
            raise # Re-raise if post_element itself becomes stale
        except Exception as e:
            print(f"   - General error with selector '{selector}': {e}")
            continue
            
    print("❌ No comment button found for this post with any selector.")
    return None

def wait_for_comment_box_improved(driver, max_retries=8, delay_between_retries=1):
    """
    Waits for the editable comment input box to appear after clicking the comment button.
    Uses multiple robust selectors and retries.
    """
    comment_box_selectors = [
        # Primary selectors for contenteditable div (most common for LinkedIn)
        '//div[@role="textbox" and @contenteditable="true" and contains(@class, "ql-editor")]',
        '//div[@role="textbox" and @contenteditable="true" and contains(@class, "comments-comment-box__text-editor")]',
        '//div[@contenteditable="true" and contains(@class, "comment-text-editor")]',
        
        # Secondary selectors
        '//div[contains(@class, "comments-comment-box")]//div[@contenteditable="true"]',
        '//div[contains(@class, "share-comment-box")]//div[@contenteditable="true"]',
        
        # Fallback selectors (less specific)
        '//textarea[contains(@class, "comment-input")]', # If they ever use textarea
        '//div[@contenteditable="true" and @aria-label="Text editor for creating content"]',
        '//div[contains(@class, "comment-form__text-editor")]//div[@contenteditable="true"]' # Newer observation
    ]
    
    for i in range(max_retries):
        for j, selector in enumerate(comment_box_selectors):
            try:
                # Use a short explicit wait for presence
                element = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                
                # Verify the element is actually visible and editable
                if element.is_displayed() and element.get_attribute("contenteditable") == "true":
                    print(f"✅ Found comment box using selector #{j+1}: '{selector}'")
                    # Scroll the comment box into view for better interaction
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                    time.sleep(0.5)
                    return element
                    
            except TimeoutException:
                continue # Selector timed out, try next
            except NoSuchElementException:
                continue # Element not found, try next
            except StaleElementReferenceException:
                print(f"   - Comment box element became stale for selector '{selector}'. Retrying.")
                continue
            except Exception as e:
                print(f"   - Error finding comment box with selector '{selector}': {e}")
                continue
        
        print(f"⏳ Waiting for comment box… retry {i+1}/{max_retries}")
        time.sleep(delay_between_retries) # Wait before the next set of retries
        
    print("❌ Could not find comment box after multiple attempts.")
    return None

def verify_comment_posted_and_screenshot(driver, post_id, saved_screenshots_list):
    """
    Waits for the comment to be processed, takes a screenshot for verification,
    and records the screenshot's path. Returns True assuming success.
    """
    print("Verification: Waiting for comment to appear on the page (5 seconds)...")
    time.sleep(5)  # Wait for UI to update after posting

    try:
        screenshot_folder = "screenshots"
        # Ensure the directory exists (it's also checked at script start, but this is a safeguard)
        if not os.path.exists(screenshot_folder):
            os.makedirs(screenshot_folder)

        # Create a unique filename for the screenshot
        fname = os.path.join(screenshot_folder, f'comment_posted_{post_id.replace(":", "-")}_{uuid.uuid4().hex[:6]}.png')
        
        # Take the screenshot
        if driver.save_screenshot(fname):
            abs_path = os.path.abspath(fname)
            saved_screenshots_list.append(abs_path)
            print(f"📸 Screenshot of posted comment saved: {abs_path}")
        else:
            # This case is rare but good to handle
            print("❌ Failed to save screenshot. The driver command executed but returned false.")

    except WebDriverException as se:
        print(f"❌ Error taking screenshot after submission: {se}")
    except Exception as e:
        print(f"❌ Unexpected error taking screenshot after submission: {e}")

    print("Continuing to wait for backend processing (5 more seconds)...")
    time.sleep(5)  # Additional delay for safety
    print("✅ Comment presumed posted after full delay.")
    return True  # Assume success after delay

def close_comment_box_or_modal(driver):
    """
    Attempts to close any open comment boxes or modals that might be present.
    This is a defensive measure to ensure a clean state before processing a new post.
    """
    print("Attempting to close any open comment boxes or modals...")
    close_selectors = [
        "//button[contains(@aria-label, 'Discard') and contains(@class, 'artdeco-button--tertiary')]", # Discard button for comment draft
        "//button[contains(@aria-label, 'Close') and contains(@class, 'artdeco-modal__dismiss')]", # Generic modal close button
        "//button[contains(@data-control-name, 'cancel_comment')]", # Cancel button for comment
        "//div[@role='dialog']//button[contains(@aria-label, 'Close')]", # Close button within a dialog
        "//button[contains(@class, 'comments-comment-box__cancel-button')]" # Another common cancel button
    ]
    
    closed_something = False
    for selector in close_selectors:
        try:
            # Use a short wait to see if the element is present and clickable
            close_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, selector))
            )
            if close_button.is_displayed():
                print(f"   - Found and clicking close button with selector: '{selector}'")
                driver.execute_script("arguments[0].click();", close_button)
                time.sleep(1) # Give time for modal to close
                # After clicking discard, confirm discard if a prompt appears
                try:
                    confirm_discard_btn = WebDriverWait(driver, 1).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Discard')]"))
                    )
                    if confirm_discard_btn.is_displayed():
                        print("   - Confirming discard of comment draft.")
                        driver.execute_script("arguments[0].click();", confirm_discard_btn)
                        time.sleep(1)
                except TimeoutException:
                    pass # No discard confirmation needed
                except Exception as e:
                    print(f"   - Error confirming discard: {e}")
                closed_something = True
                # If we successfully closed one, break and assume state is cleaner
                break 
        except TimeoutException:
            continue # Element not found, try next selector
        except StaleElementReferenceException:
            print(f"   - Stale element encountered while trying to close modal with selector '{selector}'.")
            continue
        except Exception as e:
            print(f"   - Error closing modal with selector '{selector}': {e}")
            continue
    
    if not closed_something:
        print("No open comment boxes or modals found to close.")
    return closed_something

def comment_on_post_improved(driver, post_data, comment_text, comment_number, saved_screenshots_list):
    """
    Handles the entire process of commenting on a specific LinkedIn post:
    scrolling, clicking comment button, typing, submitting, and verifying with a screenshot.
    """
    try:
        post_element = post_data["element"]
        post_id = post_data["id"]
        
        print(f"\n--- Attempting to comment on Post #{comment_number} (ID: {post_id}) ---")
        
        # Scroll to the post to ensure it's in the viewport
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", post_element)
        time.sleep(2) # Give time for scroll to complete
        
        # Find comment button using the enhanced method
        comment_btn = find_comment_button_enhanced(driver, post_element)
        if not comment_btn:
            raise Exception("Comment button not found for this post.")

        # Click the comment button
        try:
            # Prefer JavaScript click for robustness
            driver.execute_script("arguments[0].click();", comment_btn)
            print(f"🗨️ Clicked comment button on post #{comment_number}.")
        except Exception as e:
            # Fallback to ActionChains click if JS click fails
            print(f"⚠️ JS click failed ({e}). Trying ActionChains click.")
            ActionChains(driver).move_to_element(comment_btn).click().perform()
            print(f"🗨️ Clicked comment button (fallback) on post #{comment_number}.")
        
        time.sleep(3) # Wait for the comment box to appear/load
        
        # Wait for and locate the editable comment box
        editable_comment_box = wait_for_comment_box_improved(driver)
        if not editable_comment_box:
            raise Exception("Editable comment box not found after clicking comment button.")

        # Clear any pre-existing text in the comment box (sometimes LinkedIn pre-fills)
        try:
            editable_comment_box.clear()
        except Exception as e:
            print(f"   - Warning: Could not clear comment box (might be empty): {e}")
            pass # Continue even if clear fails
        
        # Click the comment box to ensure it's focused before typing
        ActionChains(driver).move_to_element(editable_comment_box).click().perform()
        time.sleep(1)
        
        # Type the comment character by character to mimic human typing
        for char in comment_text:
            editable_comment_box.send_keys(char)
            time.sleep(random.uniform(0.02, 0.1)) # Small, random delay per character
            
        time.sleep(2) # Pause after typing
        
        # Find and click the submit button
        submit_selectors = [
            '//button[contains(@class, "comments-comment-box__submit-button")]',
            '//button[contains(@class, "comment-submit-button")]',
            '//button[contains(@class, "share-comment-box__submit-button")]',
            '//button[contains(@data-control-name, "comment.submit")]',
            '//button[contains(text(), "Post") and not(contains(@aria-label, "like"))]', # Ensure it's the "Post" button for comments
            '//button[contains(@aria-label, "Post comment")]',
            '//button[contains(@class, "artdeco-button--primary") and contains(text(), "Post")]'
        ]
        
        post_btn = None
        for selector in submit_selectors:
            try:
                post_btn = WebDriverWait(driver, 5).until( # Increased wait for submit button
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                if post_btn.is_displayed() and post_btn.is_enabled():
                    # Check if the button is currently disabled (e.g., if comment is too short)
                    if post_btn.get_attribute("disabled"):
                        print(f"   - Submit button found but is disabled for selector '{selector}'. Skipping.")
                        post_btn = None # Mark as not found if disabled
                        continue
                    break
            except TimeoutException:
                continue
            except StaleElementReferenceException:
                print(f"   - Submit button element became stale for selector '{selector}'. Retrying.")
                continue
            except Exception as e:
                print(f"   - Error finding submit button with selector '{selector}': {e}")
                continue
        
        if not post_btn:
            raise Exception("Submit button not found or not clickable.")
        
        # Click the submit button
        driver.execute_script("arguments[0].click();", post_btn)
        print(f"📨 Submitted comment on post #{comment_number}: '{comment_text[:50]}...'")

        # Verify the comment was posted and take a screenshot
        comment_posted = verify_comment_posted_and_screenshot(driver, post_id, saved_screenshots_list)
        
        if comment_posted:
            print("✅ Comment process deemed successful (after delay).")
            return True
        else:
            # This branch is less likely to be hit now
            print("⚠️ Comment verification failed unexpectedly.")
            return False

    except StaleElementReferenceException:
        print(f"❗ Stale element encountered while commenting on post #{comment_number}. This post might be gone or reloaded.")
        return False
    except Exception as e:
        print(f"❗ Failed commenting on post #{comment_number} (ID: {post_data.get('id', 'N/A')}): {e}")
        return False

def process_posts_improved(driver, max_comments, comment_generator, initial_search_query):
    """
    Main loop to find, filter, generate comments for, and comment on LinkedIn posts.
    Includes robust duplicate handling, error recovery, and progress tracking.
    """
    tracker = PostTracker()
    comments_made = 0
    saved_screenshots = []  # List to store paths of saved screenshots
    
    # Initialize keywords
    keywords_list = [initial_search_query]
    current_keyword_index = 0

    while comments_made < max_comments:
        if not keywords_list:
            print("❌ No keywords available to search. Exiting.")
            break

        current_keyword = keywords_list[current_keyword_index]
        current_search_url = SEARCH_URL_TEMPLATE.format(query=requests.utils.quote(current_keyword))

        print(f"\n--- Current Progress: {comments_made}/{max_comments} comments made ---")
        print(f"🌐 Navigating to search URL for keyword: '{current_keyword}'")
        driver.get(current_search_url)
        # Perform a hard refresh to ensure a clean state
        driver.refresh() 
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'search-results-container')]"))
        )
        apply_post_filter(driver)
        time.sleep(5) # Give page time to load after filter

        # IMPORTANT: Close any potentially open comment boxes/modals before processing new posts
        close_comment_box_or_modal(driver)

        # Scroll to load more posts if needed, before fetching posts
        scroll_feed(driver, 5) 
        
        posts = find_posts_improved(driver)
        
        if not posts:
            print("⚠️ No posts found for current keyword. Trying to generate new keywords or moving to next.")
            # If no posts found, try generating new keywords
            new_keywords = comment_generator.generate_related_keywords(current_keyword)
            if new_keywords:
                keywords_list.extend(new_keywords)
                print(f"Added new keywords: {new_keywords}")
            
            current_keyword_index += 1
            if current_keyword_index >= len(keywords_list):
                print("❌ Exhausted all available keywords and could not generate more. Exiting.")
                break # Exit if no more keywords
            continue # Continue to next iteration with a new keyword

        num_processed_in_this_iteration = 0
        for post_element in posts:
            if comments_made >= max_comments:
                print("🎯 Reached maximum comments target. Stopping.")
                break 
            
            try:
                post_data = extract_post_data(post_element, driver)
                if not post_data or not post_data["id"]:
                    print("⚠️ Could not extract valid data for a post. Skipping.")
                    continue
                
                # Check for duplicate by ID
                if tracker.is_processed(post_data["id"]):
                    print(f"⏭️ Skipping already processed post (ID match): {post_data['id']}")
                    continue
                
                # Check for duplicate by signature (more robust)
                if tracker.is_duplicate_signature(post_data["signature"]):
                    print(f"⏭️ Skipping duplicate post (signature match): {post_data['signature'][:8]}...")
                    tracker.mark_processed(post_data["id"], post_data["signature"])
                    continue
                
                # Skip very short posts (likely ads, images without text, or UI elements)
                if len(post_data["text"].strip()) < 50:
                    print(f"⏭️ Skipping very short post (length {len(post_data['text'].strip())}): '{post_data['text'][:30]}...'")
                    tracker.mark_processed(post_data["id"], post_data["signature"])
                    continue
                
                # If we reach here, it's a new, potentially processable post
                num_processed_in_this_iteration += 1
                
                print(f"\n📝 Processing new post for comment ({comments_made + 1}/{max_comments})")
                print(f"Post ID: {post_data['id']}")
                print(f"Author: {post_data['author'] or 'Unknown'}")
                print(f"Preview: {post_data['text'][:100]}...")
                print(f"Signature: {post_data['signature'][:8]}...")
                
                # Generate custom comment using Ollama
                comment = comment_generator.generate_comment(
                    post_data["text"], 
                    post_data["author"]
                )
                
                if comment:
                    # Attempt to comment on the post, passing the screenshot list
                    success = comment_on_post_improved(driver, post_data, comment, comments_made + 1, saved_screenshots)
                    
                    if success:
                        tracker.mark_commented(post_data["id"], post_data["signature"])
                        comments_made += 1
                        print(f"✅ Successfully processed comment for post ({comments_made}/{max_comments})")
                        
                        # After successful comment, advance to the next keyword
                        current_keyword_index += 1
                        if current_keyword_index >= len(keywords_list):
                            print("🔄 Exhausted current keyword list. Generating new keywords...")
                            new_keywords = comment_generator.generate_related_keywords(current_keyword)
                            if new_keywords:
                                keywords_list.extend(new_keywords)
                                current_keyword_index = len(keywords_list) - len(new_keywords) # Start from newly added keywords
                            else:
                                print("❌ Could not generate new keywords. Exiting.")
                                break # Exit if no more keywords can be generated
                        
                        # Introduce a random delay after a successful comment
                        delay = random.randint(10, 25) # Increased delay range for safety
                        print(f"⏱️ Waiting {delay} seconds before processing next post/keyword...")
                        time.sleep(delay)
                        
                        # Refresh page after successful comment and before moving to next keyword
                        print("🔄 Refreshing page after successful comment...")
                        driver.refresh()
                        WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'search-results-container')]"))
                        )
                        apply_post_filter(driver) # Re-apply filter after refreshing
                        time.sleep(5)
                        close_comment_box_or_modal(driver) # Ensure any lingering modals are closed
                        break # Break from inner loop to re-fetch posts on the new page
                    else:
                        tracker.mark_failed(post_data["id"], post_data["signature"])
                        print(f"❌ Failed to comment on post (ID: {post_data['id']}). Advancing to next keyword.")
                        
                        # Force advancement to next keyword if commenting failed
                        current_keyword_index += 1
                        if current_keyword_index >= len(keywords_list):
                            print("🔄 Exhausted current keyword list. Generating new keywords...")
                            new_keywords = comment_generator.generate_related_keywords(current_keyword)
                            if new_keywords:
                                keywords_list.extend(new_keywords)
                                current_keyword_index = len(keywords_list) - len(new_keywords)
                            else:
                                print("❌ Could not generate new keywords. Exiting.")
                                break
                        
                        # Refresh page after failed comment attempt
                        print("🔄 Refreshing page after failed comment attempt...")
                        driver.refresh()
                        WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'search-results-container')]"))
                        )
                        apply_post_filter(driver) # Re-apply filter after refreshing
                        time.sleep(5)
                        close_comment_box_or_modal(driver) # Ensure any lingering modals are closed
                        break # Break from inner loop to re-fetch posts on the new page
                else:
                    print(f"❌ Could not generate a valid comment for post (ID: {post_data['id']}). Advancing to next keyword.")
                    tracker.mark_failed(post_data["id"], post_data["signature"])
                    
                    # Force advancement to next keyword if comment generation failed
                    current_keyword_index += 1
                    if current_keyword_index >= len(keywords_list):
                        print("🔄 Exhausted current keyword list. Generating new keywords...")
                        new_keywords = comment_generator.generate_related_keywords(current_keyword)
                        if new_keywords:
                            keywords_list.extend(new_keywords)
                            current_keyword_index = len(keywords_list) - len(new_keywords)
                        else:
                            print("❌ Could not generate new keywords. Exiting.")
                            break
                    
                    # Refresh page after failed comment generation
                    print("🔄 Refreshing page after failed comment generation...")
                    driver.refresh()
                    WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'search-results-container')]"))
                    )
                    apply_post_filter(driver) # Re-apply filter after refreshing
                    time.sleep(5)
                    close_comment_box_or_modal(driver) # Ensure any lingering modals are closed
                    break # Break from inner loop to re-fetch posts on the new page
            
            except StaleElementReferenceException:
                print("⚠️ Element became stale. Re-fetching posts for the next iteration.")
                # Refresh page after stale element exception
                print("🔄 Refreshing page after stale element exception...")
                driver.refresh()
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'search-results-container')]"))
                )
                apply_post_filter(driver) # Re-apply filter after refreshing
                time.sleep(5)
                close_comment_box_or_modal(driver) # Ensure any lingering modals are closed
                break # Break from inner loop to re-fetch posts on the new page
            except Exception as e:
                print(f"❌ Unhandled error processing post (ID: {post_data.get('id', 'N/A')}): {e}. Advancing to next keyword.")
                if post_data and post_data.get("id"):
                    tracker.mark_failed(post_data["id"], post_data.get("signature"))
                
                # Force advancement to next keyword if unhandled error occurred
                current_keyword_index += 1
                if current_keyword_index >= len(keywords_list):
                    print("🔄 Exhausted current keyword list. Generating new keywords...")
                    new_keywords = comment_generator.generate_related_keywords(current_keyword)
                    if new_keywords:
                        keywords_list.extend(new_keywords)
                        current_keyword_index = len(keywords_list) - len(new_keywords)
                    else:
                        print("❌ Could not generate new keywords. Exiting.")
                        break
                        
                # Refresh page after unhandled error
                print("🔄 Refreshing page after unhandled error...")
                driver.refresh()
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'search-results-container')]"))
                )
                apply_post_filter(driver) # Re-apply filter after refreshing
                time.sleep(5)
                close_comment_box_or_modal(driver) # Ensure any lingering modals are closed
                break # Break from inner loop to re-fetch posts on the new page
        
        if num_processed_in_this_iteration == 0 and comments_made < max_comments:
            print("🔄 No new, processable posts found in this iteration from the current view. Moving to next keyword or generating new ones.")
            current_keyword_index += 1
            if current_keyword_index >= len(keywords_list):
                print("🔄 Exhausted current keyword list. Generating new keywords...")
                new_keywords = comment_generator.generate_related_keywords(current_keyword)
                if new_keywords:
                    keywords_list.extend(new_keywords)
                    current_keyword_index = len(keywords_list) - len(new_keywords) # Start from newly added keywords
                else:
                    print("❌ Could not generate new keywords. Exiting.")
                    break # Exit if no more keywords can be generated

        # Print overall progress after each major iteration
        stats = tracker.get_stats()
        print(f"\n📊 Overall Progress: {stats['commented']} commented, {stats['failed']} failed, {stats['processed']} total processed.")
        
    print("\n--- Automation Finished ---")
    print(f"Total comments made: {comments_made}")
    print(f"Final Stats: {tracker.get_stats()}")
    return comments_made, tracker, saved_screenshots

# --- Main Execution ---
def main():
    """Main function to run the LinkedIn automation script."""
    search_query = input("Enter the LinkedIn search query (e.g., 'AI development', 'cloud computing'): ")
    max_comments_str = input("Enter the maximum number of comments to make (e.g., 5): ")
    
    try:
        max_comments = int(max_comments_str)
        if max_comments <= 0:
            raise ValueError("Maximum comments must be a positive integer.")
    except ValueError as e:
        print(f"Invalid input for maximum comments: {e}. Exiting.")
        return

    driver = None
    try:
        # 1. Create WebDriver
        driver = create_driver()
        
        # 2. Process posts (this function now returns the list of screenshot paths)
        comments_made, tracker, saved_screenshots = process_posts_improved(driver, max_comments, OllamaCommentGenerator(), search_query)
        
        print(f"\nScript completed. Total comments made: {comments_made}")
        print(f"Final Tracker Stats: {tracker.get_stats()}")
        
        # 3. Print the final screenshot summary
        if saved_screenshots:
            print("\n--- Screenshot Summary ---")
            print(f"Successfully saved {len(saved_screenshots)} screenshot(s):")
            for path in saved_screenshots:
                print(f"  - Name: {os.path.basename(path)}")
                print(f"    Location: {path}")
            print("--------------------------")
        else:
            print("\n--- Screenshot Summary ---")
            print("No screenshots were saved during this session.")
            print("--------------------------")

    except Exception as e:
        print(f"An unexpected error occurred in the main execution block: {e}")
    finally:
        if driver:
            print("Closing browser...")
            # driver.quit() # Comment out to keep browser open based on `detach` option
            print("Browser session finished. You may close the browser manually.")

if __name__ == "__main__":
    main()