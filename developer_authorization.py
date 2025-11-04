# developer_authorization.py
"""
🔐 DEVELOPER AUTHORIZATION SYSTEM - MRH CRIBOT
🎯 PASSWORD PROTECTED MENU MODIFICATION
⚡ DEVELOPER: @mrh000mrh
"""

import time
from menu_lock import MenuLock

class DeveloperAuthorization:
    """
    سیستم احراز هویت توسعه‌دهنده برای تغییر منوهای قفل شده
    """
    
    # 🔐 تنظیمات امنیتی
    DEVELOPER_PASSWORD = "mrh"  # رمز شما
    UNLOCK_DURATION = 300  # 5 دقیقه زمان برای تغییر
    unlocked_menus = {}  # منوهای باز شده موقت
    
    @classmethod
    def verify_developer_password(cls, password_attempt):
        """
        بررسی رمز توسعه‌دهنده
        """
        return password_attempt.strip().lower() == cls.DEVELOPER_PASSWORD
    
    @classmethod
    def unlock_menu_for_editing(cls, menu_name, password):
        """
        🔓 باز کردن قفل منو با رمز توسعه‌دهنده
        """
        # بررسی رمز
        if not cls.verify_developer_password(password):
            return False, "❌ رمز اشتباه است!"
        
        # بررسی وجود منو
        if menu_name not in MenuLock.LOCKED_MENUS:
            return False, f"❌ منوی '{menu_name}' وجود ندارد!"
        
        # باز کردن قفل منو
        cls.unlocked_menus[menu_name] = {
            'unlocked_at': time.time(),
            'expires_at': time.time() + cls.UNLOCK_DURATION,
            'original_data': MenuLock.LOCKED_MENUS[menu_name].copy()
        }
        
        print(f"🔓 منوی '{menu_name}' با موفقیت باز شد")
        print(f"⏰ زمان باقیمانده: {cls.UNLOCK_DURATION//60} دقیقه")
        
        return True, f"✅ منوی '{menu_name}' باز شد. شما اکنون می‌توانید تغییرات را اعمال کنید."
    
    @classmethod
    def is_menu_unlocked(cls, menu_name):
        """
        بررسی اینکه منو باز است و زمان آن نگذشته
        """
        if menu_name not in cls.unlocked_menus:
            return False
        
        menu_data = cls.unlocked_menus[menu_name]
        if time.time() > menu_data['expires_at']:
            # زمان تمام شده - قفل خودکار
            del cls.unlocked_menus[menu_name]
            print(f"⏰ زمان ویرایش منوی '{menu_name}' به پایان رسید")
            return False
        
        return True
    
    @classmethod
    def apply_menu_changes(cls, menu_name, new_text=None, new_buttons=None, final_confirmation=False):
        """
        🔧 اعمال تغییرات روی منوی باز شده
        """
        if not cls.is_menu_unlocked(menu_name):
            return False, "منو قفل است یا زمان آن گذشته است!"
        
        if not final_confirmation:
            return True, "تغییرات پیش‌نمایش شد. برای اعمال نهایی تایید کنید."
        
        # اعمال تغییرات نهایی
        changes = {}
        if new_text:
            changes['new_text'] = new_text
        if new_buttons:
            changes['new_buttons'] = new_buttons
        
        # اعمال تغییرات در منوی قفل شده
        success = MenuLock.developer_modify_menu(menu_name, **changes)
        
        if success:
            # قفل کردن مجدد منو
            del cls.unlocked_menus[menu_name]
            return True, f"✅ تغییرات منوی '{menu_name}' با موفقیت اعمال و قفل شد."
        else:
            return False, "❌ خطا در اعمال تغییرات!"
    
    @classmethod
    def cancel_changes(cls, menu_name):
        """
        ❌ لغو تغییرات و قفل مجدد
        """
        if menu_name in cls.unlocked_menus:
            del cls.unlocked_menus[menu_name]
            return True, f"🔒 تغییرات لغو شد و منوی '{menu_name}' قفل شد."
        return False, "منو از قبل قفل است!"
    
    @classmethod
    def get_unlocked_menus_status(cls):
        """
        🔍 دریافت وضعیت منوهای باز
        """
        status = []
        for menu_name, data in cls.unlocked_menus.items():
            remaining_time = data['expires_at'] - time.time()
            status.append({
                'menu': menu_name,
                'remaining_seconds': int(remaining_time),
                'remaining_minutes': int(remaining_time // 60)
            })
        return status

# 🔧 دستورات سریع برای توسعه‌دهنده
def dev_unlock(menu_name, password):
    """باز کردن قفل منو"""
    return DeveloperAuthorization.unlock_menu_for_editing(menu_name, password)

def dev_confirm(menu_name):
    """تایید نهایی تغییرات"""
    return DeveloperAuthorization.apply_menu_changes(menu_name, final_confirmation=True)

def dev_cancel(menu_name):
    """لغو تغییرات"""
    return DeveloperAuthorization.cancel_changes(menu_name)

def dev_status():
    """مشاهده وضعیت منوهای باز"""
    return DeveloperAuthorization.get_unlocked_menus_status()
