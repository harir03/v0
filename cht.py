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
OLLAMA_URL = "http://localhost:11434/api/generate"
COMMENT_HISTORY_FILE = "comment_history.json"

if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

# --- Enhanced Post Tracking Class ---
class PostTracker:
    def __init__(self):
        self.processed_posts = set()
        self.commented_posts = set()
        self.failed_posts = set()
        self.post_signatures = {}
        self.comment_history = self.load_comment_history()
        self.user_name = None  # Will be detected from LinkedIn profile
    
    def load_comment_history(self):
        """Load persistent comment history from file"""
        try:
            if os.path.exists(COMMENT_HISTORY_FILE):
                with open(COMMENT_HISTORY_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"📚 Loaded {len(data.get('commented_posts', []))} previously commented posts from history")
                    return data
        except Exception as e:
            print(f"⚠️ Could not load comment history: {e}")
        return {"commented_posts": [], "post_urls": set(), "post_content_hashes": set()}
    
    def save_comment_history(self):
        """Save comment history to file"""
        try:
            # Convert sets to lists for JSON serialization
            history_to_save = {
                "commented_posts": list(self.comment_history.get("commented_posts", [])),
                "post_urls": list(self.comment_history.get("post_urls", set())),
                "post_content_hashes": list(self.comment_history.get("post_content_hashes", set()))
            }
            with open(COMMENT_HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(history_to_save, f, indent=2, ensure_ascii=False)
            print(f"💾 Saved comment history with {len(history_to_save['commented_posts'])} entries")
        except Exception as e:
            print(f"⚠️ Could not save comment history: {e}")
    
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
            "content_hash": content_hash
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

# --- Enhanced User Detection ---
def detect_current_user(driver):
    """Detect the current LinkedIn user's name for accurate duplicate detection"""
    try:
        print("🔍 Detecting current LinkedIn user...")
        
        # Try to get user info from profile menu
        try:
            profile_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@id, 'ember') and contains(@class, 'global-nav__primary-link-me-menu')]"))
            )
            profile_button.click()
            time.sleep(2)
            
            # Get name from dropdown
            name_element = driver.find_element(By.XPATH, "//div[contains(@class, 'authentication-outlet')]//div[contains(@class, 'text-heading-large')]")
            user_name = name_element.text.strip()
            
            # Close dropdown
            driver.find_element(By.XPATH, "//body").click()
            time.sleep(1)
            
            if user_name:
                print(f"✅ Detected LinkedIn user: {user_name}")
                return user_name
                
        except Exception as e:
            print(f"⚠️ Could not detect user from profile menu: {e}")
        
        # Fallback: Try to get from navigation
        try:
            nav_name = driver.find_element(By.XPATH, "//span[contains(@class, 'global-nav__me-text')]").text
            if nav_name:
                print(f"✅ Detected LinkedIn user (fallback): {nav_name}")
                return nav_name
        except:
            pass
        
        # If all fails, try to extract from page source
        try:
            page_source = driver.page_source
            import re
            name_match = re.search(r'"firstName":"([^"]+)"', page_source)
            if name_match:
                first_name = name_match.group(1)
                last_match = re.search(r'"lastName":"([^"]+)"', page_source)
                last_name = last_match.group(1) if last_match else ""
                full_name = f"{first_name} {last_name}".strip()
                print(f"✅ Detected LinkedIn user (page source): {full_name}")
                return full_name
        except:
            pass
            
        print("⚠️ Could not detect current user name")
        return None
        
    except Exception as e:
        print(f"❌ Error detecting current user: {e}")
        return None

# --- Enhanced Duplicate Detection ---
def check_and_remove_duplicate_comments(driver, post_element, post_id, tracker):
    """Comprehensive duplicate check using multiple methods"""
    try:
        print(f"🔍 Performing comprehensive duplicate check for post {post_id}...")
        
        # Method 1: Check persistent history first (fastest)
        post_data = extract_post_data(post_element, driver)
        if post_data:
            content_hash = hashlib.md5(f"{post_data['author']}:{post_data['text'][:300]}".encode()).hexdigest()
            if tracker.has_commented_on_content(content_hash):
                print(f"  ❌ DUPLICATE FOUND: Content hash matches previous comment")
                return True
        
        # Method 2: Check post URL if available
        try:
            post_link = post_element.find_element(By.XPATH, ".//a[contains(@href, '/posts/')]")
            post_url = post_link.get_attribute('href')
            if post_url and tracker.has_commented_on_url(post_url):
                print(f"  ❌ DUPLICATE FOUND: URL matches previous comment")
                return True
        except:
            pass
        
        # Method 3: Live DOM check - look for existing comments
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", post_element)
        time.sleep(2)
        
        # Try to expand comments if they're collapsed
        try:
            see_more_comments = post_element.find_element(By.XPATH, ".//button[contains(@aria-label, 'Show more comments') or contains(text(), 'Show') or contains(@class, 'comments-comments-list__show-more-button')]")
            driver.execute_script("arguments[0].click();", see_more_comments)
            time.sleep(3)
            print("  🔄 Expanded comments section")
        except:
            pass
        
        # Check for our comments using multiple selectors
        user_comment_selectors = [
            ".//span[contains(@class, 'comments-post-meta__name-text') and (contains(., '(You)') or contains(., 'you'))]",
            ".//span[contains(@class, 'hoverable-link-text') and contains(@class, 'comments-post-meta__name-text')]",
            f".//span[contains(@class, 'comments-post-meta__name-text') and contains(., '{tracker.user_name}')]" if tracker.user_name else None
        ]
        
        for selector in user_comment_selectors:
            if selector is None:
                continue
            try:
                user_comment = post_element.find_element(By.XPATH, selector)
                print(f"  ❌ DUPLICATE FOUND: Found existing comment in DOM")
                return True
            except NoSuchElementException:
                continue
        
        # Method 4: Check comment authors more broadly
        try:
            comment_authors = post_element.find_elements(By.XPATH, ".//span[contains(@class, 'comments-post-meta__name-text')]")
            for author in comment_authors:
                author_text = author.text.strip()
                if tracker.user_name and tracker.user_name.lower() in author_text.lower():
                    print(f"  ❌ DUPLICATE FOUND: Found comment by user '{author_text}'")
                    return True
                if "(You)" in author_text or "you commented" in author_text.lower():
                    print(f"  ❌ DUPLICATE FOUND: Found 'You' indicator in comments")
                    return True
        except Exception as e:
            print(f"  ⚠️ Error checking comment authors: {e}")
        
        print(f"  ✅ No duplicate found - safe to comment")
        return False
        
    except Exception as e:
        print(f"  ⚠️ Error during comprehensive duplicate check: {e}")
        return False

# --- Ollama Class (from v0.2) ---
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
            payload = {"model": self.model_name, "prompt": prompt, "stream": False, "options": {"temperature": 0.8, "top_p": 0.9, "max_tokens": 100}}
            response = requests.post(self.ollama_url, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                keywords_str = result.get("response", "").strip()
                keywords = [k.strip() for k in keywords_str.split(',') if k.strip()]
                print(f"🎯 Generated high-profile AI keywords: {keywords}")
                return keywords
            else:
                print(f"❌ Ollama API error generating AI profile keywords: {response.status_code}")
                return fallback_keywords
        except Exception as e:
            print(f"❌ Error generating AI profile keywords: {e}")
            return fallback_keywords

    def evaluate_post_worthiness(self, post_text, author_name, post_type="general"):
        """AI evaluates posts based on content quality and engagement potential, not just author status."""
        cleaned_text = self.extract_actual_content(post_text)
        
        evaluation_prompt = f"""You are a LinkedIn engagement strategist. Analyze this post to decide if commenting would increase professional visibility and engagement.

POST CONTENT: {cleaned_text[:800]}
AUTHOR: {author_name or "Unknown"}

Evaluate on these criteria (score 1-10 each):
1. CONTENT DEPTH: Does it discuss substantial AI/tech concepts, not just basic tutorials?
2. ENGAGEMENT POTENTIAL: Will this post likely get good engagement (likes, comments, shares)?
3. PROFESSIONAL VALUE: Will commenting here showcase my AI/tech expertise?
4. DISCUSSION QUALITY: Does it invite meaningful technical or business discussion?
5. AUDIENCE REACH: Does the post seem to reach professionals (not just students posting achievements)?

AVOID commenting on:
- Student project showcases or academic achievements
- Basic tutorials or "how-to" posts
- Job announcements or hiring posts
- Personal milestones (graduations, certifications)
- Generic motivational content
- Posts with very few engagements

PRIORITIZE commenting on:
- Technical deep-dives and analysis
- Industry trends and insights
- AI/tech business strategy discussions
- Innovative product announcements
- Thought-provoking questions about tech future
- Posts that already have good engagement (20+ reactions)

Respond in this exact format:
DECISION: COMMENT or SKIP
REASONING: [Brief explanation focusing on content and engagement potential]
ENGAGEMENT_SCORE: X/50"""

        try:
            payload = {
                "model": self.model_name,
                "prompt": evaluation_prompt,
                "stream": False,
                "options": {"temperature": 0.3, "top_p": 0.8, "max_tokens": 200}
            }
            
            response = requests.post(self.ollama_url, json=payload, timeout=45)
            
            if response.status_code == 200:
                result = response.json()
                evaluation = result.get("response", "").strip()
                
                print(f"\n🧠 AI EVALUATION:")
                print(f"    Author: {author_name or 'Unknown'}")
                print(f"    Post Preview: {cleaned_text[:100]}...")
                print(f"    AI Response: {evaluation}")
                
                should_comment = "COMMENT" in evaluation.upper() and "SKIP" not in evaluation.upper()
                
                reasoning = "No reasoning provided"
                if "REASONING:" in evaluation:
                    reasoning_part = evaluation.split("REASONING:")[1].split("ENGAGEMENT_SCORE:")[0].strip()
                    reasoning = reasoning_part if reasoning_part else "No reasoning provided"
                
                score = 0
                if "ENGAGEMENT_SCORE:" in evaluation:
                    try:
                        score_part = evaluation.split("ENGAGEMENT_SCORE:")[1].split("/")[0].strip()
                        score = int(score_part)
                    except:
                        score = 0
                
                decision_emoji = "✅" if should_comment else "⏭️"
                print(f"    {decision_emoji} DECISION: {'COMMENT' if should_comment else 'SKIP'}")
                print(f"    📝 REASONING: {reasoning}")
                print(f"    📊 SCORE: {score}/50")
                
                return should_comment, reasoning, score
                
            else:
                print(f"❌ Ollama API error during evaluation: {response.status_code}")
                return False, "API Error", 0
                
        except Exception as e:
            print(f"❌ Error during post evaluation: {e}")
            return False, f"Evaluation Error: {e}", 0

    def check_author_credibility(self, post_element, author_name, driver):
        """Light check to avoid obvious student/spam accounts without being overly restrictive."""
        if not author_name:
            return True, "No author filtering needed"
        
        try:
            post_text = post_element.text.lower()
            
            red_flag_patterns = [
                "student at", "intern at", "looking for opportunities", 
                "seeking job", "fresh graduate", "recent graduate",
                "just graduated", "completed my", "got my degree",
                "passed my exam", "cleared my", "got placed at",
                "offer from", "joining as intern", "starting my journey",
                "got selected", "interview experience", "#placement",
                "campus placement", "college project", "university project",
                "semester project", "final year project", "thesis project"
            ]
            
            red_flags_found = [pattern for pattern in red_flag_patterns if pattern in post_text]
            
            if red_flags_found:
                return False, f"Student/job-seeking content detected: {red_flags_found[0]}"
            
            spam_patterns = [
                "dm me", "dm for", "check dm", "inbox me",
                "whatsapp me", "call me at", "contact me at",
                "buy now", "limited offer", "discount", "sale",
                "click link", "visit my", "check my website"
            ]
            
            spam_found = [pattern for pattern in spam_patterns if pattern in post_text]
            
            if spam_found:
                return False, f"Promotional/spam content detected: {spam_found[0]}"
            
            return True, "Author appears credible"
            
        except Exception as e:
            print(f"     ⚠️ Error checking author credibility: {e}")
            return True, f"Could not verify author, proceeding anyway: {e}"

    def generate_comment(self, post_text, author_name=None):
        prompt = f"Write an insightful, expert-toned comment (15-30 words) on the following AI-related post by {author_name or 'the author'}. Add value. Sound like a knowledgeable colleague. POST: \"{post_text[:1200]}\""
        try:
            payload = {"model": self.model_name, "prompt": prompt, "stream": False}
            response = requests.post(self.ollama_url, json=payload, timeout=45)
            if response.status_code == 200:
                comment = response.json().get("response", "").strip().strip('"')
                print(f"  🤖 Generated comment: {comment}")
                return comment
        except Exception as e:
            print(f"  ❌ Comment generation failed: {e}")
        return None
        
    def extract_actual_content(self, post_text):
        lines = post_text.split('\n')
        content_lines = []
        skip_patterns = ['Like', 'Comment', 'Repost', 'Share', 'Send', 'ago', 'Follow']
        for line in lines:
            if not any(pattern in line for pattern in skip_patterns) and len(line.strip()) > 20:
                content_lines.append(line.strip())
        return ' '.join(content_lines)

# --- Selenium Driver & v0 Functions ---
def create_driver():
    brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
    user_data_dir = os.path.expanduser("~") + "/AppData/Local/BraveSoftware/Brave-Browser/User Data"
    profile_dir = "Default"
    options = Options()
    options.binary_location = brave_path
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument(f"--profile-directory={profile_dir}")
    options.add_experimental_option("detach", True)
    options.add_argument("--disable-blink-features=AutomationControlled")
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    print("✅ Brave browser driver created.")
    return driver

def apply_post_filter(driver):
    try:
        filter_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Posts']")))
        driver.execute_script("arguments[0].click();", filter_button)
        print("✅ Posts filter applied.")
        time.sleep(3)
    except:
        print("⚠️ Could not apply 'Posts' filter.")

def get_robust_post_id(post_element, driver):
    try:
        data_urn = post_element.get_attribute("data-urn")
        if data_urn: 
            return data_urn
        return f"element-{hashlib.md5(post_element.get_attribute('outerHTML')[:500].encode()).hexdigest()[:10]}"
    except: 
        return f"fallback-{uuid.uuid4().hex[:10]}"

def find_posts_improved(driver):
    post_selectors = ["//div[contains(@class, 'feed-shared-update-v2')]", "//div[contains(@class, 'update-components-post')]"]
    all_posts = []
    for selector in post_selectors:
        try:
            posts = driver.find_elements(By.XPATH, selector)
            all_posts.extend(posts)
        except: 
            continue
    return list({id(post): post for post in all_posts}.values())

def extract_post_data(post_element, driver):
    try:
        post_text = post_element.text
        author_name = "Unknown"
        try:
            author_name = post_element.find_element(By.XPATH, ".//span[contains(@class, 'feed-shared-actor__name')]//span[@aria-hidden='true']").text
        except: 
            pass
        post_id = get_robust_post_id(post_element, driver)
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

def wait_for_comment_box_improved(driver):
    selectors = ['//div[@role="textbox" and @contenteditable="true"]', '//div[contains(@aria-placeholder, "Add a comment…")]']
    for selector in selectors:
        try: 
            return WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, selector)))
        except: 
            continue
    return None

def close_comment_box_or_modal(driver):
    try:
        close_button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Dismiss')]")))
        close_button.click()
    except: 
        pass

# --- New/Upgraded Functions for v0.4 ---
def scroll_feed(driver, scroll_times=15, target_posts=10):
    """Enhanced scrolling to find more high-quality posts with better loading detection."""
    print(f"🔄 Enhanced scrolling to find high-quality posts (max {scroll_times} scrolls)...")
    initial_posts_count = len(find_posts_improved(driver))
    print(f"📊 Initial posts found: {initial_posts_count}")
    last_height = driver.execute_script("return document.body.scrollHeight")
    posts_found = initial_posts_count
    for i in range(scroll_times):
        driver.execute_script("window.scrollBy(0, window.innerHeight * 0.8);")
        time.sleep(3)
        new_posts_count = len(find_posts_improved(driver))
        new_height = driver.execute_script("return document.body.scrollHeight")
        print(f"⬇️ Scroll {i+1}/{scroll_times} - Posts: {new_posts_count} (+ {new_posts_count - posts_found}) - Height: {new_height}")
        if new_posts_count >= target_posts:
            print(f"🎯 Target reached: Found {new_posts_count} posts (target: {target_posts})")
            break
        if new_height == last_height and new_posts_count == posts_found:
            print("📄 No more content detected, waiting longer...")
            time.sleep(3)
            final_posts_count = len(find_posts_improved(driver))
            final_height = driver.execute_script("return document.body.scrollHeight")
            if final_posts_count == posts_found and final_height == last_height:
                print("📄 Confirmed: No more content loading (reached end of feed)")
                break
        last_height = new_height
        posts_found = new_posts_count
        time.sleep(random.uniform(0.5, 1.5))
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)

def manage_keywords(keywords_list, current_index, comments_on_keyword, consecutive_empty_searches, comment_generator, initial_query):
    """Handles keyword rotation and generation logic."""
    MAX_EMPTY_SEARCHES = 2
    if consecutive_empty_searches >= MAX_EMPTY_SEARCHES:
        print(f"🔄 Generating new keywords due to poor results...")
        new_keywords = comment_generator.generate_ai_profile_keywords(3, initial_query)
        if new_keywords:
            keywords_list.extend(new_keywords)
            print(f"✅ Added new keywords: {new_keywords}")
        current_index += 1
        comments_on_keyword = 0
        consecutive_empty_searches = 0
    return keywords_list, current_index, comments_on_keyword, consecutive_empty_searches

def scan_and_collect_posts(driver, search_url, max_posts=15):
    """Handles navigation, filtering, scrolling, and post collection."""
    try:
        print(f"\n📡 SCANNING AND COLLECTING POSTS: {search_url}")
        driver.get(search_url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'search-results-container')]")))
        apply_post_filter(driver)
        scroll_feed(driver, target_posts=max_posts)
        return find_posts_improved(driver)
    except Exception as e:
        print(f"❌ Error during post scanning: {e}")
        return []

def evaluate_and_process_post(driver, post_element, comment_generator, tracker, comment_number, saved_screenshots, current_search_url=None):
    """Handles single post evaluation and commenting pipeline with refresh support"""
    try:
        post_data = extract_post_data(post_element, driver)
        if not post_data: 
            return False, False, True, False
        
        print(f"\n📋 EVALUATING POST #{comment_number}")
        print(f"    Post ID: {post_data['id']}")
        print(f"    Author: {post_data['author']}")

        if tracker.is_processed(post_data["id"]) or check_and_remove_duplicate_comments(driver, post_element, post_data["id"], tracker):
            tracker.mark_processed(post_data["id"], post_data["signature"])
            return False, False, True, False

        is_credible, credibility_info = comment_generator.check_author_credibility(post_element, post_data["author"], driver)
        if not is_credible:
            print(f"    👤 SKIP: {credibility_info}")
            tracker.mark_processed(post_data["id"], post_data["signature"])
            return False, False, True, False
            
        should_comment, reasoning, score = comment_generator.evaluate_post_worthiness(post_data["text"], post_data["author"])
        if not should_comment or score < 25:
            print(f"    📉 SKIP: AI evaluation failed (Score: {score}/50) - {reasoning}")
            tracker.mark_processed(post_data["id"], post_data["signature"])
            return False, False, True, False
            
        print(f"\n🎯 TARGET IDENTIFIED - PROCEEDING TO COMMENT")
        
        comment = comment_generator.generate_comment(post_data["text"], post_data["author"])
        if not comment:
            print(f"    ❌ Failed to generate comment")
            tracker.mark_processed(post_data["id"], post_data["signature"])
            return False, False, True, False
            
        print(f"    💬 Generated comment: {comment}")
        
        if check_and_remove_duplicate_comments(driver, post_element, post_data["id"], tracker):
            print(f"    ❌ DUPLICATE DETECTED: Aborting comment (found during final check)")
            tracker.mark_processed(post_data["id"], post_data["signature"])
            return False, False, True, False
        
        success = comment_on_post_improved(driver, post_data, comment, saved_screenshots)
        
        if success:
            content_hash = hashlib.md5(f"{post_data['author']}:{post_data['text'][:300]}".encode()).hexdigest()
            tracker.mark_commented(
                post_data["id"], 
                post_data["signature"], 
                post_data.get("url"), 
                content_hash
            )
            print(f"    ✅ SUCCESS: Comment posted and logged")
            return True, True, True, True
        else:
            tracker.mark_failed(post_data["id"], post_data["signature"])
            print(f"    ❌ FAILED: Could not post comment")
            return False, False, True, True
            
    except StaleElementReferenceException:
        print("    ⚠️ Stale element during evaluation. Signalling for refresh.")
        return False, False, False, False
    except Exception as e:
        print(f"    ❌ Unhandled error during post evaluation: {e}")
        return False, False, True, False

def process_posts_improved(driver, max_comments, comment_generator, initial_search_query):
    """Orchestrates the entire process with automatic page refresh after each comment"""
    tracker = PostTracker()
    
    tracker.user_name = detect_current_user(driver)
    
    comments_made = 0
    saved_screenshots = []
    
    keywords_list, current_keyword_index, comments_on_current_keyword, consecutive_empty_searches = comment_generator.generate_ai_profile_keywords(5, initial_search_query), 0, 0, 0

    print(f"\n🚀 STARTING LINKEDIN COMMENT AUTOMATION")
    print(f"   Target comments: {max_comments}")
    print(f"   Current user: {tracker.user_name or 'Not detected'}")
    print(f"   Historical comments: {len(tracker.comment_history.get('commented_posts', []))}")
    
    while comments_made < max_comments:
        keywords_list, current_keyword_index, comments_on_current_keyword, consecutive_empty_searches = manage_keywords(
            keywords_list, current_keyword_index, comments_on_current_keyword, consecutive_empty_searches,
            comment_generator, initial_search_query
        )
        
        if current_keyword_index >= len(keywords_list):
            print("❌ Exhausted all keywords. Halting.")
            break
            
        current_keyword = keywords_list[current_keyword_index]
        search_url = SEARCH_URL_TEMPLATE.format(query=requests.utils.quote(current_keyword))
        
        print(f"\n🔍 SEARCHING WITH KEYWORD: '{current_keyword}'")
        print(f"   Comments made with this keyword: {comments_on_current_keyword}")
        
        posts = scan_and_collect_posts(driver, search_url)
        if not posts:
            print(f"   📭 No posts found for keyword: '{current_keyword}'")
            consecutive_empty_searches += 1
            continue
        else:
            consecutive_empty_searches = 0
            print(f"   📊 Found {len(posts)} posts to evaluate")

        post_processed_in_batch = 0
        for post_element in posts:
            if comments_made >= max_comments: 
                break
            
            post_processed_in_batch += 1
            success, commented, should_continue, page_refreshed = evaluate_and_process_post(
                driver, post_element, comment_generator, tracker, 
                comments_made + 1, saved_screenshots, search_url
            )
            
            if commented:
                comments_made += 1
                comments_on_current_keyword += 1
                print(f"\n🎉 PROGRESS UPDATE:")
                print(f"   Comments made: {comments_made}/{max_comments}")
                
                if comments_made < max_comments:
                    delay = random.uniform(30, 60)
                    print(f"   ⏳ Waiting {delay:.1f} seconds before next comment...")
                    time.sleep(delay)
                    
                print(f"   🔄 Getting fresh posts after successful comment...")
                break
                
            if not should_continue or page_refreshed:
                if page_refreshed:
                    print("🔄 Page was refreshed, getting fresh posts...")
                else:
                    print("🔄 Refreshing page due to stale element...")
                break
        
        if comments_made >= max_comments: 
            break
    
    return comments_made, tracker, saved_screenshots
    
def main():
    search_query = input("Enter a fallback LinkedIn search query (e.g., 'AI development'): ").strip()
    if not search_query:
        search_query = "AI development"
        print(f"Using default query: {search_query}")
        
    max_comments_str = input("Enter the maximum number of comments to make (e.g., 5): ").strip()
    
    try:
        max_comments = int(max_comments_str) if max_comments_str else 5
        if max_comments <= 0: 
            raise ValueError()
        print(f"Target: {max_comments} comments")
    except ValueError:
        print("Invalid input. Using default: 5 comments")
        max_comments = 5

    driver = None
    try:
        print("\n🚀 INITIALIZING LINKEDIN AUTOMATION BOT")
        driver = create_driver()
        
        print("📱 Navigating to LinkedIn...")
        driver.get(LINKEDIN_URL)
        time.sleep(5)
        
        try:
            WebDriverWait(driver, 30).until(
                EC.any_of(
                    EC.presence_of_element_located((By.XPATH, "//nav[contains(@class, 'global-nav')]")),
                    EC.presence_of_element_located((By.XPATH, "//input[@id='username']"))
                )
            )
            
            if driver.find_elements(By.XPATH, "//input[@id='username']"):
                print("🔐 Please log in to LinkedIn in the browser window...")
                print("   Waiting for login completion...")
                WebDriverWait(driver, 120).until(
                    EC.presence_of_element_located((By.XPATH, "//nav[contains(@class, 'global-nav')]"))
                )
                print("✅ Login detected!")
            else:
                print("✅ Already logged in!")
                
        except TimeoutException:
            print("❌ Login timeout. Please ensure you're logged into LinkedIn.")
            return
        
        comment_generator = OllamaCommentGenerator()
        
        print(f"\n🎯 STARTING COMMENT AUTOMATION")
        print(f"   Query: '{search_query}'")
        print(f"   Target: {max_comments} comments")
        
        comments_made, tracker, saved_screenshots = process_posts_improved(
            driver, max_comments, comment_generator, search_query
        )
        
        stats = tracker.get_stats()
        print(f"\n" + "="*50)
        print(f"🏁 AUTOMATION COMPLETED")
        print(f"="*50)
        print(f"✅ Comments successfully made: {comments_made}")
        print(f"📊 Posts processed: {stats['processed']}")
        print(f"❌ Failed attempts: {stats['failed']}")
        print(f"📚 Historical comments: {stats['historical_comments']}")
        print(f"🎯 Success rate: {(comments_made / max(stats['processed'], 1) * 100):.1f}%")
        
        if saved_screenshots:
            print(f"\n📸 SCREENSHOT SUMMARY ({len(saved_screenshots)} files)")
            print("-" * 50)
            for path in saved_screenshots:
                print(f"   📁 {os.path.basename(path)}")
                print(f"     {path}")
            print("-" * 50)
        else:
            print("\n📸 No screenshots were saved during this session.")
            
        print(f"\n💾 Comment history saved to: {os.path.abspath(COMMENT_HISTORY_FILE)}")
        print(f"🔄 Next run will skip previously commented posts automatically.")

    except KeyboardInterrupt:
        print("\n⏹️ Automation stopped by user.")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if driver:
            print(f"\n🌐 Browser session finished. You may close the browser manually.")

if __name__ == "__main__":
    main()