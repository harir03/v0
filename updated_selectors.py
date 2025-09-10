#!/usr/bin/env python3
"""
Updated Selectors Module for LinkedIn Bot

Updated and comprehensive LinkedIn UI selectors with fallback options
based on recent LinkedIn interface changes.
"""

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class LinkedInSelectors:
    """
    Updated and comprehensive LinkedIn UI selectors with fallback options
    based on recent LinkedIn interface changes.
    """
    
    # Comment section selectors
    COMMENT_BUTTON_SELECTORS = [
        ".feed-shared-social-action-bar__action-button[aria-label*='comment']",
        ".feed-shared-social-action-bar__action-button[aria-label*='Comment']",
        "button[data-control-name='comment']",
        ".artdeco-button[data-control-name='comment']",
        "button[aria-label*='comment' i]",  # Case insensitive
        ".comments-comment-box__block",  # Area around the comment box
        ".feed-shared-update-v2__social-actions-comment", # Newest LinkedIn selector (2025)
        "//button[contains(@class, 'social-actions-button') and contains(@aria-label, 'comment')]" # XPath fallback
    ]
    
    # Comment input field selectors
    COMMENT_INPUT_SELECTORS = [
        ".editor-content[role='textbox']",
        ".ql-editor[data-placeholder='Add a comment']",
        ".comments-comment-box__content-editor",
        ".comments-comment-texteditor__content", 
        "[contenteditable='true'][data-placeholder*='comment' i]",
        "div[role='textbox'][aria-label*='comment' i]",
        "div[contenteditable='true'][aria-label*='Add a comment']",  # Latest LinkedIn selector (2025)
        "//div[@contenteditable='true' and contains(@aria-label, 'Add a comment')]" # XPath fallback
    ]
    
    # Comment post button selectors
    COMMENT_POST_BUTTON_SELECTORS = [
        ".comments-comment-box__submit-button",
        "button.comments-comment-box__submit-button",
        "button[data-control-name='post_comment']",
        ".artdeco-button--primary[type='submit']",
        ".comments-comment-box__submit-button:not(.artdeco-button--disabled)",
        "button.social-actions-comment-submit",  # Latest LinkedIn selector (2025)
        "//button[contains(@class, 'comments-comment-box__submit-button') or contains(@class, 'social-actions-comment-submit')]" # XPath fallback
    ]
    
    # Selectors for finding existing comments
    EXISTING_COMMENTS_SELECTORS = [
        ".comments-comments-list",
        ".comments-comments-list__comment-item",
        ".comments-comment-item",
        ".feed-shared-comment",
        ".feed-shared-comment-list__comment",  # Newest LinkedIn selector (2025)
        "//div[contains(@class, 'comments-comment-item') or contains(@class, 'feed-shared-comment')]"  # XPath fallback
    ]
    
    # Selector for comment text within existing comments
    COMMENT_TEXT_SELECTORS = [
        ".comments-comment-item-content-body",
        ".comments-comment-item__main-content",
        ".feed-shared-comment__content-body",
        ".feed-shared-text",
        ".feed-shared-comment-text",  # Latest LinkedIn selector (2025)
        "//div[contains(@class, 'comments-comment-item__main-content') or contains(@class, 'feed-shared-comment-text')]" # XPath fallback
    ]
    
    # Delete comment button selectors
    COMMENT_DELETE_BUTTON_SELECTORS = [
        ".comments-comment-item__delete-button",
        ".feed-shared-comment-actions__action-button[aria-label*='Delete']",
        ".artdeco-dropdown__item[aria-label*='Delete']",
        ".feed-shared-comment-menu-item--delete",  # Latest LinkedIn selector (2025)
        "//button[contains(@aria-label, 'Delete this comment')]",
        "//li[contains(@class, 'feed-shared-comment-menu-item--delete')]",  # XPath fallback
        "//span[text()='Delete']//ancestor::button"  # Text-based XPath fallback
    ]
    
    # Comment options menu selectors (to access delete option)
    COMMENT_OPTIONS_MENU_SELECTORS = [
        ".feed-shared-comment-actions__action-button[aria-label*='More actions']",
        ".artdeco-dropdown__trigger.artdeco-dropdown__trigger--placement-bottom",
        ".feed-shared-control-menu__trigger",
        ".comment-options-trigger",  # Latest LinkedIn selector (2025)
        "//button[contains(@aria-label, 'More actions')]",
        "//button[contains(@class, 'feed-shared-control-menu__trigger')]"  # XPath fallback
    ]
    
    # Confirm delete dialog button selectors
    CONFIRM_DELETE_BUTTON_SELECTORS = [
        ".artdeco-modal__confirm-dialog-btn[data-test-dialog-primary-btn]",
        ".artdeco-modal__confirm-dialog-btn--primary",
        ".artdeco-button--primary.artdeco-button--2",
        "//button[text()='Delete']",
        "//button[contains(@class, 'artdeco-button--primary') and contains(text(), 'Delete')]"  # XPath fallback
    ]
    
    @classmethod
    def find_element_with_fallbacks(cls, driver, selector_list, by_type="css"):
        """
        Try multiple selectors until one works.
        
        Args:
            driver: WebDriver instance
            selector_list: List of selectors to try
            by_type: Type of selector ('css' or 'xpath')
            
        Returns:
            WebElement if found, None otherwise
        """
        for selector in selector_list:
            try:
                if selector.startswith("//") or by_type == "xpath":
                    return driver.find_element(By.XPATH, selector)
                else:
                    return driver.find_element(By.CSS_SELECTOR, selector)
            except NoSuchElementException:
                continue
        
        return None
        
    @classmethod
    def find_elements_with_fallbacks(cls, driver, selector_list, by_type="css"):
        """
        Try multiple selectors until one returns elements.
        
        Args:
            driver: WebDriver instance
            selector_list: List of selectors to try
            by_type: Type of selector ('css' or 'xpath')
            
        Returns:
            List of WebElements if found, empty list otherwise
        """
        for selector in selector_list:
            try:
                if selector.startswith("//") or by_type == "xpath":
                    elements = driver.find_elements(By.XPATH, selector)
                else:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    
                if elements:
                    return elements
            except:
                continue
        
        return []
