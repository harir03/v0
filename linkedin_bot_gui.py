#!/usr/bin/env python3
import os
import sys
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import json
import time
import traceback
from datetime import datetime

# Import the bot code
# This assumes linkedin_bot_complete.py is in the same directory
try:
    from linkedin_bot_complete import EnhancedLinkedInBot, AccountManager
except ImportError:
    messagebox.showerror("Import Error", "Could not import linkedin_bot_complete.py. Make sure it's in the same directory.")
    sys.exit(1)

class LinkedInBotGUI:
    """Simple GUI for the LinkedIn Bot with enhanced error handling."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("LinkedIn Bot v1.0")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Set icon if available
        try:
            self.root.iconbitmap("icon.ico")  # Create an icon.ico file for your bot
        except:
            pass
        
        # Initialize bot components
        try:
            self.account_manager = AccountManager()
            self.bot = None
            self.running = False
            self.schedule_thread = None
        except Exception as e:
            messagebox.showerror("Initialization Error", f"Error initializing bot components: {e}")
            traceback.print_exc()
            sys.exit(1)
        
        # Create the main UI
        self.create_ui()
        
        # Load accounts
        self.load_accounts()
        
        # Add diagnostic info
        self.add_system_info()
    
    def create_ui(self):
        """Create the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook (tabs)
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Main tab
        main_tab = ttk.Frame(notebook, padding="10")
        notebook.add(main_tab, text="Main")
        
        # Logs tab
        logs_tab = ttk.Frame(notebook, padding="10")
        notebook.add(logs_tab, text="Logs")
        
        # Diagnostics tab
        diagnostics_tab = ttk.Frame(notebook, padding="10")
        notebook.add(diagnostics_tab, text="Diagnostics")
        
        # Account Management tab
        account_tab = ttk.Frame(notebook, padding="10")
        notebook.add(account_tab, text="Accounts")
        
        # Create content for Main tab
        self.create_main_tab(main_tab)
        
        # Create content for Logs tab
        self.create_logs_tab(logs_tab)
        
        # Create content for Diagnostics tab
        self.create_diagnostics_tab(diagnostics_tab)
        
        # Create content for Account tab
        self.create_account_tab(account_tab)
        
    def create_main_tab(self, parent):
        """Create the main tab UI elements."""
        # Title label
        title_label = ttk.Label(
            parent, 
            text="LinkedIn Engagement Bot", 
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # Settings frame
        settings_frame = ttk.LabelFrame(parent, text="Settings", padding="10")
        settings_frame.pack(fill=tk.X, pady=5)
        
        # Account selection
        account_frame = ttk.Frame(settings_frame)
        account_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(account_frame, text="Account:").pack(side=tk.LEFT, padx=5)
        self.account_var = tk.StringVar()
        self.account_combo = ttk.Combobox(account_frame, textvariable=self.account_var, state="readonly", width=30)
        self.account_combo.pack(side=tk.LEFT, padx=5)
        
        refresh_button = ttk.Button(account_frame, text="Refresh", command=self.load_accounts)
        refresh_button.pack(side=tk.LEFT, padx=5)
        
        # Keyword settings
        keyword_frame = ttk.Frame(settings_frame)
        keyword_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(keyword_frame, text="Keyword:").pack(side=tk.LEFT, padx=5)
        self.keyword_var = tk.StringVar(value="artificial intelligence")
        keyword_entry = ttk.Entry(keyword_frame, textvariable=self.keyword_var, width=40)
        keyword_entry.pack(side=tk.LEFT, padx=5)
        
        # Comments limit
        comments_frame = ttk.Frame(settings_frame)
        comments_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(comments_frame, text="Max Comments:").pack(side=tk.LEFT, padx=5)
        self.comments_var = tk.IntVar(value=5)
        comments_spin = ttk.Spinbox(comments_frame, from_=1, to=20, textvariable=self.comments_var, width=5)
        comments_spin.pack(side=tk.LEFT, padx=5)
        
        # Mode selection
        mode_frame = ttk.LabelFrame(settings_frame, text="Run Mode")
        mode_frame.pack(fill=tk.X, pady=10, padx=5)
        
        self.mode_var = tk.StringVar(value="single")
        single_radio = ttk.Radiobutton(
            mode_frame, text="Single Run (Use selected keyword)", variable=self.mode_var, value="single"
        )
        single_radio.pack(anchor=tk.W, padx=10, pady=5)
        
        schedule_radio = ttk.Radiobutton(
            mode_frame, text="Scheduled Mode (Use account's scheduled timing)", variable=self.mode_var, value="schedule"
        )
        schedule_radio.pack(anchor=tk.W, padx=10, pady=5)
        
        # Browser option
        browser_frame = ttk.Frame(settings_frame)
        browser_frame.pack(fill=tk.X, pady=5)
        
        self.brave_var = tk.BooleanVar(value=True)
        brave_check = ttk.Checkbutton(
            browser_frame, text="Use Brave Browser (recommended)", variable=self.brave_var
        )
        brave_check.pack(side=tk.LEFT, padx=5)
        
        # Control buttons frame
        buttons_frame = ttk.Frame(parent)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        self.start_button = ttk.Button(
            buttons_frame, text="Start Bot", command=self.start_bot, width=15
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(
            buttons_frame, text="Stop Bot", command=self.stop_bot, width=15, state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Status display frame
        status_frame = ttk.LabelFrame(parent, text="Status")
        status_frame.pack(fill=tk.X, pady=5, padx=5)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, font=("Arial", 10, "bold"))
        status_label.pack(fill=tk.X, padx=10, pady=5)
        
        # Progress section
        progress_frame = ttk.Frame(status_frame)
        progress_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.progress_var = tk.StringVar(value="Not started")
        progress_label = ttk.Label(progress_frame, textvariable=self.progress_var)
        progress_label.pack(pady=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, padx=10, pady=5)
        
        # Recent log summary
        log_summary_frame = ttk.LabelFrame(parent, text="Recent Activity")
        log_summary_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.log_summary = scrolledtext.ScrolledText(log_summary_frame, wrap=tk.WORD, height=10)
        self.log_summary.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log_summary.config(state=tk.DISABLED)
    
    def create_logs_tab(self, parent):
        """Create the logs tab UI elements."""
        # Control frame
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, pady=5)
        
        # Clear logs button
        clear_button = ttk.Button(control_frame, text="Clear Logs", command=self.clear_logs)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # Save logs button
        save_button = ttk.Button(control_frame, text="Save Logs", command=self.save_logs)
        save_button.pack(side=tk.LEFT, padx=5)
        
        # Log verbosity
        verbose_var = tk.BooleanVar(value=True)
        verbose_check = ttk.Checkbutton(
            control_frame, text="Verbose Logging", variable=verbose_var
        )
        verbose_check.pack(side=tk.RIGHT, padx=5)
        
        # Full log output
        self.log_output = scrolledtext.ScrolledText(parent, wrap=tk.WORD)
        self.log_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def create_diagnostics_tab(self, parent):
        """Create the diagnostics tab UI elements."""
        # System info
        system_frame = ttk.LabelFrame(parent, text="System Information")
        system_frame.pack(fill=tk.X, pady=5, padx=5)
        
        self.system_info_text = scrolledtext.ScrolledText(system_frame, wrap=tk.WORD, height=8)
        self.system_info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Test connections
        test_frame = ttk.LabelFrame(parent, text="Connection Tests")
        test_frame.pack(fill=tk.X, pady=5, padx=5)
        
        test_button = ttk.Button(test_frame, text="Test LinkedIn Connection", command=self.test_linkedin)
        test_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        test_ollama_button = ttk.Button(test_frame, text="Test Ollama API", command=self.test_ollama)
        test_ollama_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Account health
        health_frame = ttk.LabelFrame(parent, text="Account Health")
        health_frame.pack(fill=tk.BOTH, expand=True, pady=5, padx=5)
        
        # Account selection for health check
        health_account_frame = ttk.Frame(health_frame)
        health_account_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(health_account_frame, text="Account:").pack(side=tk.LEFT, padx=5)
        self.health_account_var = tk.StringVar()
        self.health_account_combo = ttk.Combobox(health_account_frame, textvariable=self.health_account_var, state="readonly")
        self.health_account_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        check_health_button = ttk.Button(health_account_frame, text="Check Health", command=self.check_account_health)
        check_health_button.pack(side=tk.LEFT, padx=5)
        
        # Health results
        self.health_results = scrolledtext.ScrolledText(health_frame, wrap=tk.WORD)
        self.health_results.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def create_account_tab(self, parent):
        """Create the account management tab UI elements."""
        # Account list
        account_list_frame = ttk.LabelFrame(parent, text="Available Accounts")
        account_list_frame.pack(fill=tk.BOTH, expand=True, pady=5, padx=5)
        
        # Create a treeview for accounts
        columns = ("Username", "Enabled", "Health", "Last Used", "Keywords")
        self.account_tree = ttk.Treeview(account_list_frame, columns=columns, show="headings")
        
        # Define headings
        for col in columns:
            self.account_tree.heading(col, text=col)
            self.account_tree.column(col, width=100)
            
        self.account_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Button frame
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=5)
        
        # Add/Edit account buttons
        add_button = ttk.Button(button_frame, text="Add Account", command=self.show_add_account)
        add_button.pack(side=tk.LEFT, padx=5)
        
        edit_button = ttk.Button(button_frame, text="Edit Selected", command=self.show_edit_account)
        edit_button.pack(side=tk.LEFT, padx=5)
        
        # Reload config button
        reload_button = ttk.Button(button_frame, text="Reload Config", command=self.reload_account_config)
        reload_button.pack(side=tk.LEFT, padx=5)
        
        # Open config file button
        open_config_button = ttk.Button(button_frame, text="Open Config File", command=self.open_config_file)
        open_config_button.pack(side=tk.LEFT, padx=5)
        
    def add_system_info(self):
        """Add system diagnostic information to the diagnostics tab."""
        try:
            import platform
            
            self.system_info_text.config(state=tk.NORMAL)
            self.system_info_text.delete(1.0, tk.END)
            
            # Platform info
            system_info = f"Operating System: {platform.platform()}\n"
            system_info += f"Python Version: {platform.python_version()}\n"
            
            # Check for selenium
            try:
                import selenium
                system_info += f"Selenium Version: {selenium.__version__}\n"
            except ImportError:
                system_info += "Selenium: Not installed\n"
                
            # Check for requests
            try:
                import requests
                system_info += f"Requests Version: {requests.__version__}\n"
            except ImportError:
                system_info += "Requests: Not installed\n"
                
            # Check for nltk
            try:
                import nltk
                system_info += f"NLTK Version: {nltk.__version__}\n"
            except ImportError:
                system_info += "NLTK: Not installed\n"
                
            # Check for sklearn
            try:
                import sklearn
                system_info += f"Scikit-learn Version: {sklearn.__version__}\n"
            except ImportError:
                system_info += "Scikit-learn: Not installed\n"
                
            # Check for cryptography
            try:
                import cryptography
                system_info += f"Cryptography Version: {cryptography.__version__}\n"
            except ImportError:
                system_info += "Cryptography: Not installed\n"
                
            # Check for Chrome or Brave
            import shutil
            chrome_path = shutil.which("chrome") or shutil.which("google-chrome")
            brave_path = shutil.which("brave-browser") or shutil.which("brave")
            
            if chrome_path:
                system_info += f"Chrome: Found at {chrome_path}\n"
            else:
                system_info += "Chrome: Not found in PATH\n"
                
            if brave_path:
                system_info += f"Brave: Found at {brave_path}\n"
            else:
                system_info += "Brave: Not found in PATH\n"
                
            # Add to text widget
            self.system_info_text.insert(tk.END, system_info)
            self.system_info_text.config(state=tk.DISABLED)
            
        except Exception as e:
            self.system_info_text.insert(tk.END, f"Error collecting system info: {e}")
            self.system_info_text.config(state=tk.DISABLED)
    
    def load_accounts(self):
        """Load accounts from the account manager."""
        try:
            # Get all enabled accounts
            enabled_accounts = self.account_manager.get_enabled_accounts()
            
            # Update the comboboxes
            self.account_combo['values'] = enabled_accounts
            self.health_account_combo['values'] = enabled_accounts
            
            # Select the first account if available
            if enabled_accounts and not self.account_var.get():
                self.account_var.set(enabled_accounts[0])
                
            if enabled_accounts and not self.health_account_var.get():
                self.health_account_var.set(enabled_accounts[0])
                
            # Update the account treeview
            self.update_account_tree()
                
            # Check if we need to show a message
            if not enabled_accounts:
                messagebox.showinfo("No Accounts", 
                                   "No enabled accounts found. Please add an account in the accounts_config.json file.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load accounts: {e}")
            self.log(f"Error loading accounts: {e}")
    
    def update_account_tree(self):
        """Update the account treeview with current account info."""
        try:
            # Clear existing items
            for item in self.account_tree.get_children():
                self.account_tree.delete(item)
                
            # Add all accounts to the treeview
            for account_name, account_data in self.account_manager.accounts.items():
                # Format values
                username = account_data.get("username", "")
                enabled = "Yes" if account_data.get("enabled", False) else "No"
                health = account_data.get("health_score", "N/A")
                last_used = account_data.get("last_used", "Never")
                
                # Format last used date/time
                if last_used and last_used != "Never":
                    try:
                        dt = datetime.fromisoformat(last_used)
                        last_used = dt.strftime("%Y-%m-%d %H:%M")
                    except:
                        pass
                        
                keywords = ", ".join(account_data.get("keywords", []))[:50]
                if len(keywords) > 50:
                    keywords += "..."
                    
                # Add to treeview
                self.account_tree.insert("", tk.END, values=(username, enabled, health, last_used, keywords))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update account list: {e}")
            
    def show_add_account(self):
        """Show dialog to add a new account."""
        messagebox.showinfo("Add Account", 
                           "To add a new account, please edit the accounts_config.json file directly.\n\n"
                           "Or use the 'Open Config File' button to open it.")
                           
    def show_edit_account(self):
        """Show dialog to edit an account."""
        messagebox.showinfo("Edit Account", 
                           "To edit accounts, please modify the accounts_config.json file directly.\n\n"
                           "Or use the 'Open Config File' button to open it.")
                           
    def reload_account_config(self):
        """Reload the account configuration file."""
        try:
            # Re-initialize the account manager
            self.account_manager = AccountManager()
            
            # Reload accounts
            self.load_accounts()
            
            messagebox.showinfo("Success", "Account configuration reloaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reload account configuration: {e}")
            
    def open_config_file(self):
        """Open the account configuration file in the default text editor."""
        try:
            import os
            import platform
            import subprocess
            
            config_file = self.account_manager.config_file
            
            if not os.path.exists(config_file):
                messagebox.showerror("Error", f"Configuration file not found: {config_file}")
                return
                
            # Open with default application based on OS
            if platform.system() == 'Windows':
                os.startfile(config_file)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.call(('open', config_file))
            else:  # Linux
                subprocess.call(('xdg-open', config_file))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open configuration file: {e}")
    
    def start_bot(self):
        """Start the LinkedIn bot with robust error handling."""
        # Get selected account
        account_name = self.account_var.get()
        
        if not account_name:
            messagebox.showerror("Error", "Please select an account")
            return
            
        # Check if account exists and is enabled
        account_data = self.account_manager.get_account(account_name)
        if not account_data:
            messagebox.showerror("Error", f"Account {account_name} not found")
            return
            
        if not account_data.get("enabled", False):
            messagebox.showerror("Error", f"Account {account_name} is disabled")
            return
            
        # Disable start button and enable stop button
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # Clear log summary
        self.clear_log_summary()
        
        # Start progress bar
        self.progress.start()
        
        # Set running flag
        self.running = True
        
        # Start bot in a separate thread to avoid freezing the UI
        if self.mode_var.get() == "single":
            self.status_var.set("Running single session...")
            self.progress_var.set(f"Starting session for account: {account_name}")
            threading.Thread(target=self.run_single_session, daemon=True).start()
        else:
            self.status_var.set("Running in scheduled mode...")
            self.progress_var.set("Monitoring schedule for available accounts...")
            self.schedule_thread = threading.Thread(target=self.run_scheduled_mode, daemon=True)
            self.schedule_thread.start()
    
    def stop_bot(self):
        """Stop the LinkedIn bot with proper cleanup."""
        self.status_var.set("Stopping bot...")
        self.progress_var.set("Shutting down...")
        self.running = False
        
        # If the bot is a browser instance, try to quit it
        if hasattr(self, 'bot') and self.bot and hasattr(self.bot, 'driver') and self.bot.driver:
            try:
                self.bot.driver.quit()
            except Exception as e:
                self.log(f"Error quitting browser: {e}")
                
        # Enable start button and disable stop button
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        
        # Stop progress bar
        self.progress.stop()
        
        # Update status
        self.status_var.set("Ready")
        self.progress_var.set("Bot stopped by user")
        
        self.log("Bot stopped by user")
    
    def run_single_session(self):
        """Run a single bot session with comprehensive error handling."""
        try:
            # Redirect stdout to the log
            original_stdout = sys.stdout
            sys.stdout = self
            
            # Log start
            self.log(f"Starting single session with account: {self.account_var.get()}")
            self.log(f"Keyword: {self.keyword_var.get()}")
            self.log(f"Max comments: {self.comments_var.get()}")
            
            # Initialize bot
            self.bot = EnhancedLinkedInBot()
            
            # Set up account
            account_name = self.account_var.get()
            self.progress_var.set(f"Setting up account: {account_name}")
            if not self.bot.setup_account(account_name):
                self.log(f"Failed to set up account: {account_name}")
                self.handle_session_end(False, "Failed to set up account")
                return
                
            # Initialize browser
            self.progress_var.set("Initializing browser...")
            if not self.bot.initialize_browser():
                self.log("Failed to initialize browser.")
                self.handle_session_end(False, "Failed to initialize browser")
                return
                
            # Login to LinkedIn
            self.progress_var.set("Logging in to LinkedIn...")
            if not self.bot.login_to_linkedin():
                self.log("Failed to log in to LinkedIn.")
                self.handle_session_end(False, "Failed to log in")
                return
                
            # Get account settings
            account_data = self.bot.account_manager.get_account(account_name)
            max_comments = self.comments_var.get()
            
            # Use specified keyword instead of the automatic one
            keyword = self.keyword_var.get()
            self.log(f"Using keyword: {keyword}")
            
            # Process posts
            self.progress_var.set(f"Searching for posts with keyword: {keyword}")
            comments_posted = self.bot.process_posts(keyword, max_comments)
            self.log(f"Comments posted: {comments_posted}")
            
            # Run secondary verification
            if comments_posted > 0:
                self.progress_var.set("Running secondary comment verification...")
                self.log("Running secondary comment verification...")
                verification_results = self.bot.comment_verifier.check_and_manage_comments()
                self.log(f"Verification results: {verification_results['comments_deleted']} comments deleted")
                
            # Restore stdout
            sys.stdout = original_stdout
            
            # Clean up
            self.progress_var.set("Cleaning up...")
            if self.bot.driver:
                self.bot.driver.quit()
                
            # Complete
            self.handle_session_end(True, f"Session completed - {comments_posted} comments posted")
            
        except Exception as e:
            self.handle_exception(e, "Error in bot session")
    
    def run_scheduled_mode(self):
        """Run the bot in scheduled mode with robust error handling."""
        try:
            # Redirect stdout to the log
            original_stdout = sys.stdout
            sys.stdout = self
            
            self.log("Starting scheduled mode")
            
            while self.running:
                try:
                    # Log current time
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.log(f"Checking schedule at {current_time}")
                    
                    # Initialize bot (fresh for each check to avoid stale state)
                    self.bot = EnhancedLinkedInBot()
                    
                    # Run a scheduled session
                    self.progress_var.set("Running scheduled session...")
                    success = self.bot.run_scheduled_session()
                    
                    if success:
                        self.log("Scheduled session completed successfully.")
                    else:
                        self.log("No accounts scheduled for this time or session failed.")
                    
                    # Wait before next check
                    self.progress_var.set("Waiting for next schedule check...")
                    self.log("Waiting 5 minutes before next schedule check...")
                    
                    # Wait in small increments so we can stop more responsively
                    for _ in range(5 * 60 // 5):
                        if not self.running:
                            break
                        time.sleep(5)
                        
                except Exception as e:
                    self.handle_exception(e, "Error in scheduled session")
                    time.sleep(60)  # Wait a bit after an error
                    
            # Restore stdout
            sys.stdout = original_stdout
            
        except Exception as e:
            self.handle_exception(e, "Critical error in scheduled mode")
    
    def handle_session_end(self, success, message):
        """Handle the end of a bot session."""
        # Update UI
        if success:
            self.status_var.set("Session completed")
        else:
            self.status_var.set("Session failed")
            
        self.progress_var.set(message)
        self.progress.stop()
        
        # Log end message
        self.log(message)
        
        # Reset UI state if we're still running
        if self.running:
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.running = False
    
    def handle_exception(self, exception, context):
        """Handle exceptions with detailed logging."""
        # Get exception details
        exc_type, exc_obj, exc_tb = sys.exc_info()
        filename = exc_tb.tb_frame.f_code.co_filename
        line = exc_tb.tb_lineno
        
        # Format error message
        error_msg = f"{context}: {str(exception)} in {filename} line {line}"
        
        # Log error
        self.log(f"ERROR: {error_msg}")
        self.log(traceback.format_exc())
        
        # Update UI
        self.status_var.set("Error occurred")
        self.progress_var.set(f"Error: {str(exception)}")
        
        # Show error dialog if it's a critical error
        if "Critical" in context:
            messagebox.showerror("Critical Error", error_msg)
            
        # Reset UI state if we're still running
        if self.running:
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.progress.stop()
            self.running = False
    
    def log(self, message):
        """Add a message to the log output with timestamps."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Add to main log
        try:
            self.log_output.configure(state='normal')
            self.log_output.insert(tk.END, f"[{timestamp}] {message}\n")
            self.log_output.see(tk.END)
            self.log_output.configure(state='disabled')
            
            # Also add to log summary for important messages
            if any(keyword in message for keyword in ["Error", "ERROR", "Failed", "Success", "Comment", "Posted", "Started"]):
                self.add_to_log_summary(f"[{timestamp}] {message}")
                
            # Update the UI
            self.root.update_idletasks()
        except:
            # If logging fails, just print to console
            print(f"[{timestamp}] {message}")
    
    def add_to_log_summary(self, message):
        """Add a message to the log summary on the main tab."""
        try:
            self.log_summary.configure(state='normal')
            self.log_summary.insert(tk.END, f"{message}\n")
            
            # Keep only the last 100 lines
            line_count = int(self.log_summary.index('end-1c').split('.')[0])
            if line_count > 100:
                self.log_summary.delete('1.0', '2.0')
                
            self.log_summary.see(tk.END)
            self.log_summary.configure(state='disabled')
        except:
            pass
    
    def clear_log_summary(self):
        """Clear the log summary text widget."""
        try:
            self.log_summary.configure(state='normal')
            self.log_summary.delete('1.0', tk.END)
            self.log_summary.configure(state='disabled')
        except:
            pass
    
    def clear_logs(self):
        """Clear the log output."""
        self.log_output.configure(state='normal')
        self.log_output.delete('1.0', tk.END)
        self.log_output.configure(state='disabled')
        self.log("Logs cleared.")
    
    def save_logs(self):
        """Save the log output to a file."""
        try:
            # Ask for save location
            file_path = filedialog.asksaveasfilename(
                defaultextension=".log",
                filetypes=[("Log files", "*.log"), ("Text files", "*.txt"), ("All files", "*.*")],
                initialfile=f"linkedin_bot_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            )
            
            if file_path:
                # Save logs
                with open(file_path, 'w') as file:
                    file.write(self.log_output.get('1.0', tk.END))
                    
                self.log(f"Logs saved to: {file_path}")
                messagebox.showinfo("Success", f"Logs saved to: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save logs: {e}")
    
    def test_linkedin(self):
        """Test connection to LinkedIn."""
        self.health_results.configure(state='normal')
        self.health_results.delete('1.0', tk.END)
        self.health_results.insert(tk.END, "Testing LinkedIn connection...\n")
        
        try:
            import requests
            response = requests.get("https://www.linkedin.com", timeout=10)
            status = response.status_code
            
            self.health_results.insert(tk.END, f"LinkedIn connection test: {'Success' if status == 200 else 'Failed'}\n")
            self.health_results.insert(tk.END, f"Status code: {status}\n")
            
        except Exception as e:
            self.health_results.insert(tk.END, f"LinkedIn connection test failed: {e}\n")
            
        self.health_results.configure(state='disabled')
    
    def test_ollama(self):
        """Test connection to Ollama API."""
        self.health_results.configure(state='normal')
        self.health_results.delete('1.0', tk.END)
        self.health_results.insert(tk.END, "Testing Ollama API connection...\n")
        
        try:
            import requests
            
            # Get config for Ollama URL
            bot = EnhancedLinkedInBot()
            ollama_url = bot.config.get("ollama_url", "http://localhost:11434/api/generate")
            
            self.health_results.insert(tk.END, f"Using Ollama URL: {ollama_url}\n")
            
            # Test model list endpoint first (doesn't require a specific model)
            list_url = ollama_url.replace("/generate", "/tags")
            response = requests.get(list_url, timeout=5)
            
            if response.status_code == 200:
                self.health_results.insert(tk.END, "Successfully connected to Ollama API\n")
                
                # Try listing available models
                try:
                    models = response.json().get("models", [])
                    if models:
                        self.health_results.insert(tk.END, "Available models:\n")
                        for model in models:
                            self.health_results.insert(tk.END, f"- {model.get('name')}\n")
                    else:
                        self.health_results.insert(tk.END, "No models found. Please download a model using 'ollama pull <model>'\n")
                except:
                    self.health_results.insert(tk.END, "Connected but couldn't list models\n")
            else:
                self.health_results.insert(tk.END, f"Failed to connect to Ollama API: Status {response.status_code}\n")
                
        except Exception as e:
            self.health_results.insert(tk.END, f"Ollama API connection test failed: {e}\n")
            self.health_results.insert(tk.END, "\nMake sure Ollama is installed and running. You can install it from https://ollama.ai/\n")
            
        self.health_results.configure(state='disabled')
    
    def check_account_health(self):
        """Check the health of the selected account."""
        account_name = self.health_account_var.get()
        
        if not account_name:
            messagebox.showerror("Error", "Please select an account")
            return
            
        self.health_results.configure(state='normal')
        self.health_results.delete('1.0', tk.END)
        self.health_results.insert(tk.END, f"Checking health for account: {account_name}\n\n")
        
        try:
            # Initialize health monitor
            health_monitor = AccountHealthMonitor(
                account_name=account_name,
                storage_dir=f"accounts/{account_name}/health"
            )
            
            # Get health summary
            health_summary = health_monitor.get_health_summary()
            
            # Display results
            self.health_results.insert(tk.END, f"Health Score: {health_summary['health_score']}/100\n")
            self.health_results.insert(tk.END, f"Risk Level: {health_summary['risk_level'].upper()}\n\n")
            
            self.health_results.insert(tk.END, "Today's Activity:\n")
            self.health_results.insert(tk.END, f"Searches: {health_summary['today_activity']['searches']}\n")
            self.health_results.insert(tk.END, f"Comments: {health_summary['today_activity']['comments']}\n\n")
            
            self.health_results.insert(tk.END, f"Recent Captchas: {health_summary['recent_captchas']}\n")
            self.health_results.insert(tk.END, f"Recent Warnings: {health_summary['recent_warnings']}\n\n")
            
            self.health_results.insert(tk.END, "Recommendations:\n")
            for rec in health_summary['recommendations']:
                self.health_results.insert(tk.END, f"- {rec}\n")
                
        except Exception as e:
            self.health_results.insert(tk.END, f"Error checking account health: {e}\n")
            
        self.health_results.configure(state='disabled')
    
    # Required method to make our class work as a file-like object for stdout redirection
    def write(self, message):
        self.log(message.strip())
        
    def flush(self):
        # Needed for file-like object compatibility
        pass

def main():
    """Main entry point for the LinkedIn Bot GUI."""
    # Create main window
    root = tk.Tk()
    app = LinkedInBotGUI(root)
    
    # Start the UI event loop
    root.mainloop()

if __name__ == "__main__":
    main()