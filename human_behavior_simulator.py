#!/usr/bin/env python3
"""
Human Behavior Simulator Module for LinkedIn Bot

Simulates human-like behavior for browsing, typing, and interaction
to avoid detection as an automated script.
"""

import time
import random
from datetime import datetime


class HumanBehaviorSimulator:
    """
    Simulates human-like behavior for browsing, typing, and interaction
    to avoid detection as an automated script.
    """
    
    def __init__(self):
        """Initialize the human behavior simulator."""
        self.driver = None
        
    def set_driver(self, driver):
        """
        Set the webdriver for the simulator.
        
        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
        
    def adaptive_delay(self, min_seconds, max_seconds=None):
        """
        Wait for a random amount of time.
        
        Args:
            min_seconds (float): Minimum seconds to wait
            max_seconds (float): Maximum seconds to wait
        """
        if max_seconds is None:
            max_seconds = min_seconds * 1.5
            
        # Add some randomness
        delay = random.uniform(min_seconds, max_seconds)
        
        # Adjust based on time of day (people are slower late at night)
        hour = datetime.now().hour
        if hour < 6 or hour > 22:  # Late night/early morning
            delay *= 1.2
        elif 12 <= hour <= 14:  # Lunch time
            delay *= 1.1
            
        time.sleep(delay)
        
    def simulate_reading(self, text_length):
        """
        Simulate reading time for a given text length.
        
        Args:
            text_length (int): Length of text
        """
        # Average reading speed (characters per second)
        # Slow: 10 chars/sec, Medium: 20 chars/sec, Fast: 30 chars/sec
        reading_speed = random.uniform(10, 30)
        
        # Calculate reading time
        read_time = text_length / reading_speed
        
        # Add some variability
        read_time *= random.uniform(0.8, 1.2)
        
        # Cap reading time (people skim long content)
        max_read_time = 20  # Maximum 20 seconds
        read_time = min(read_time, max_read_time)
        
        # Wait
        time.sleep(read_time)
        
    def type_like_human(self, element, text, typing_style="normal"):
        """
        Type text like a human with natural delays between characters.
        
        Args:
            element: Element to type into
            text (str): Text to type
            typing_style (str): Style of typing ('normal', 'fast', 'careful')
        """
        if not element or not text:
            return
            
        # Base typing speed (characters per second)
        if typing_style == "fast":
            base_speed = random.uniform(8, 12)  # Fast typing
        elif typing_style == "careful":
            base_speed = random.uniform(3, 6)   # Careful typing
        else:
            base_speed = random.uniform(5, 8)   # Normal typing
            
        # Clear field first
        element.clear()
        
        for char in text:
            # Calculate delay for this character
            if char in ['.', ',', ';', ':', '!', '?']:
                # Longer pause after punctuation
                delay = random.uniform(0.3, 0.7)
            elif char == ' ':
                # Medium pause for spaces
                delay = random.uniform(0.1, 0.3)
            else:
                # Normal typing delay
                delay = 1 / base_speed * random.uniform(0.8, 1.2)
                
            # Type the character
            element.send_keys(char)
            
            # Wait
            time.sleep(delay)
            
        # Sometimes people pause after typing
        if random.random() < 0.3:
            time.sleep(random.uniform(0.5, 1.5))
            
    def simulate_browsing_behavior(self, scroll_range=(100, 500)):
        """
        Simulate natural browsing behavior with scrolling and pauses.
        
        Args:
            scroll_range (tuple): Range of pixels to scroll
        """
        if not self.driver:
            return
            
        # Number of scroll actions to perform
        scroll_count = random.randint(2, 5)
        
        for _ in range(scroll_count):
            # Random scroll amount
            scroll_amount = random.randint(scroll_range[0], scroll_range[1])
            
            # Scroll down smoothly
            self.scroll_smoothly(scroll_amount)
            
            # Pause to simulate reading content
            self.adaptive_delay(1.5, 4)
            
        # Sometimes scroll back up
        if random.random() < 0.3:
            self.scroll_smoothly(-random.randint(100, 300))
            self.adaptive_delay(1, 2)
            
    def scroll_smoothly(self, distance):
        """
        Scroll the page smoothly like a human.
        
        Args:
            distance (int): Distance to scroll in pixels
        """
        if not self.driver:
            return
            
        # Number of steps for smooth scrolling
        steps = 10
        step_distance = distance // steps
        
        for i in range(steps):
            # Gradually increase and then decrease speed for more natural motion
            if i < steps // 2:
                # Accelerate
                step_time = 0.01 + (0.02 * i)
            else:
                # Decelerate
                step_time = 0.01 + (0.02 * (steps - i))
                
            self.driver.execute_script(f"window.scrollBy(0, {step_distance});")
            time.sleep(step_time)
            
        # Small adjustment at the end
        adjustment = distance - (step_distance * steps)
        if adjustment != 0:
            self.driver.execute_script(f"window.scrollBy(0, {adjustment});")
