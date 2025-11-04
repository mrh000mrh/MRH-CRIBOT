# database.py
import sqlite3
import json
from datetime import datetime, timedelta

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('bot.db', check_same_thread=False)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # جدول کاربران
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                vpn_access BOOLEAN DEFAULT FALSE,
                vpn_expiry TIMESTAMP,
                license_key TEXT,
                is_admin BOOLEAN DEFAULT FALSE,
                balance INTEGER DEFAULT 0,
                balance_type TEXT DEFAULT 'تومان',
                subscription_status TEXT DEFAULT 'کاربر عادی',
                disclaimer_accepted BOOLEAN DEFAULT FALSE
            )
        ''')
        
        # جدول خریدهای VPN
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vpn_purchases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                plan_type TEXT,
                price INTEGER,
                purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expiry_date TIMESTAMP,
                payment_status TEXT DEFAULT 'pending'
            )
        ''')
        
        # جدول لایسنس‌ها
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS licenses (
                license_key TEXT PRIMARY KEY,
                created_by INTEGER,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                used_by INTEGER,
                used_date TIMESTAMP,
                is_used BOOLEAN DEFAULT FALSE,
                duration_days INTEGER DEFAULT 30
            )
        ''')
        
        # جدول تراکنش‌ها
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount INTEGER,
                description TEXT,
                status TEXT DEFAULT 'pending',
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                transaction_type TEXT
            )
        ''')
        
        # جدول کوپن‌ها
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS coupons (
                coupon_code TEXT PRIMARY KEY,
                discount_type TEXT,
                discount_value INTEGER,
                expiry_date TIMESTAMP,
                usage_limit INTEGER,
                used_count INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT TRUE
            )
        ''')
        
        self.conn.commit()
    
    def add_user(self, user_id, username):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO users (user_id, username) 
            VALUES (?, ?)
        ''', (user_id, username))
        self.conn.commit()
    
    def accept_disclaimer(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE users 
            SET disclaimer_accepted = TRUE 
            WHERE user_id = ?
        ''', (user_id,))
        self.conn.commit()
    
    def check_vpn_access(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT vpn_access, vpn_expiry FROM users 
            WHERE user_id = ? AND vpn_access = 1 AND (vpn_expiry IS NULL OR vpn_expiry > datetime('now'))
        ''', (user_id,))
        result = cursor.fetchone()
        return result is not None
    
    def check_license_access(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT license_key FROM users 
            WHERE user_id = ? AND license_key IS NOT NULL
        ''', (user_id,))
        result = cursor.fetchone()
        return result is not None
    
    def grant_vpn_access(self, user_id, days, plan_type):
        cursor = self.conn.cursor()
        expiry_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            UPDATE users 
            SET vpn_access = 1, vpn_expiry = ?
            WHERE user_id = ?
        ''', (expiry_date, user_id))
        
        cursor.execute('''
            INSERT INTO vpn_purchases (user_id, plan_type, expiry_date, payment_status)
            VALUES (?, ?, ?, 'completed')
        ''', (user_id, plan_type, expiry_date))
        
        self.conn.commit()
        return True
    
    def create_license(self, license_key, created_by, duration_days=30):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO licenses (license_key, created_by, duration_days)
            VALUES (?, ?, ?)
        ''', (license_key, created_by, duration_days))
        self.conn.commit()
        return True
    
    def use_license(self, license_key, user_id):
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT license_key, duration_days FROM licenses 
            WHERE license_key = ? AND is_used = 0
        ''', (license_key,))
        license_data = cursor.fetchone()
        
        if not license_data:
            return False
        
        cursor.execute('''
            UPDATE licenses 
            SET is_used = 1, used_by = ?, used_date = datetime('now')
            WHERE license_key = ?
        ''', (user_id, license_key))
        
        expiry_date = (datetime.now() + timedelta(days=license_data[1])).strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
            UPDATE users 
            SET vpn_access = 1, vpn_expiry = ?, license_key = ?
            WHERE user_id = ?
        ''', (expiry_date, license_key, user_id))
        
        self.conn.commit()
        return True

    def get_user_stats(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users')
        total_users = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM users WHERE vpn_access = 1')
        active_users = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM vpn_purchases WHERE payment_status = "completed"')
        total_sales = cursor.fetchone()[0]
        
        cursor.execute('SELECT SUM(price) FROM vpn_purchases WHERE payment_status = "completed"')
        total_income = cursor.fetchone()[0] or 0
        
        return {
            'total_users': total_users,
            'active_users': active_users,
            'total_sales': total_sales,
            'total_income': total_income
        }

# ایجاد نمونه از دیتابیس
db = Database()
