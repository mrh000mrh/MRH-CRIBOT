# menu_lock.py
"""
🔒 MENU LOCK SYSTEM - MRH CRIBOT
🚫 PROTECTION AGAINST UNAUTHORIZED AI CHANGES
✅ ALLOW CONTROLLED DEVELOPER MODIFICATIONS
⚡ DEVELOPER: @mrh000mrh
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import inspect

class MenuLock:
    """
    سیستم قفل منو - فقط توسعه‌دهنده اصلی می‌تواند تغییرات اساسی ایجاد کند
    """
    
    # 🚫 منوهای قفل شده - تغییر توسط AI ممنوع!
    LOCKED_MENUS = {
        'main_menu': {
            'text': "🎉 **به ربات MRH CRIBOT خوش آمدید!**\n\nلطفاً گزینه مورد نظر خود را انتخاب کنید:",
            'buttons': [
                ["🎯 ورود به کانال های VIP", "vip_channels"],
                ["🛡️ خرید کانفیگ", "buy_config"],
                ["👤 حساب کاربری", "my_account"],
                ["📞 پشتیبانی", "support"],
                ["ℹ️ راهنما", "help"]
            ],
            'developer_notes': "برای تغییر این منو، مستقیماً در LOCKED_MENUS ویرایش کنید"
        },
        # ... دیگر منوها مثل قبل
    }
    
    # ✅ منوهای قابل توسعه توسط AI (با اجازه)
    EXTENDABLE_SECTIONS = {
        'admin_panel_extra': {
            'description': "بخش‌های اضافی پنل مدیریت",
            'allowed_changes': ["اضافه کردن دکمه جدید", "ویرایش متن توضیحات"]
        },
        'account_features': {
            'description': "ویژگی‌های جدید حساب کاربری", 
            'allowed_changes': ["اضافه کردن دکمه جدید", "ایجاد زیرمنوی جدید"]
        }
    }

    @classmethod
    def developer_modify_menu(cls, menu_name, new_text=None, new_buttons=None, developer_key="MRH_DEVELOPER"):
        """
        🔓 فقط برای توسعه‌دهنده اصلی - تغییر منوها
        """
        if developer_key != "MRH_DEVELOPER_KEY_2024":
            raise PermissionError("❌ فقط توسعه‌دهنده اصلی می‌تواند منوها را تغییر دهد!")
        
        if menu_name not in cls.LOCKED_MENUS:
            raise ValueError(f"منوی '{menu_name}' وجود ندارد!")
        
        if new_text:
            cls.LOCKED_MENUS[menu_name]['text'] = new_text
            print(f"✅ متن منوی {menu_name} آپدیت شد")
        
        if new_buttons:
            cls.LOCKED_MENUS[menu_name]['buttons'] = new_buttons
            print(f"✅ دکمه‌های منوی {menu_name} آپدیت شد")
        
        return True

    @classmethod
    def ai_add_feature(cls, section_name, new_button_text, new_callback_data, ai_notes=""):
        """
        🤖 اجازه محدود برای AI - فقط اضافه کردن ویژگی جدید
        """
        if section_name not in cls.EXTENDABLE_SECTIONS:
            raise PermissionError(f"AI نمی‌تواند در بخش {section_name} تغییر ایجاد کند!")
        
        # فقط می‌تواند به منوهای قابل توسعه اضافه کند
        if section_name == 'admin_panel_extra':
            # اضافه کردن به پنل مدیریت
            return cls._add_to_admin_panel(new_button_text, new_callback_data, ai_notes)
        
        elif section_name == 'account_features':
            # اضافه کردن به حساب کاربری  
            return cls._add_to_account_features(new_button_text, new_callback_data, ai_notes)
        
        return False

    @classmethod
    def _add_to_admin_panel(cls, button_text, callback_data, notes):
        """اضافه کردن دکمه جدید به پنل مدیریت"""
        print(f"🤖 AI درخواست اضافه کردن: {button_text} -> {callback_data}")
        print(f"📝 یادداشت AI: {notes}")
        return True

    @classmethod
    def get_locked_menu(cls, menu_name, **kwargs):
        """
        دریافت منوی قفل شده
        """
        if menu_name not in cls.LOCKED_MENUS:
            raise ValueError(f"❌ منوی '{menu_name}' در سیستم قفل تعریف نشده!")
        
        menu = cls.LOCKED_MENUS[menu_name]
        text = menu['text']
        
        # جایگزینی متغیرها در متن
        for key, value in kwargs.items():
            text = text.replace(f"{{{key}}}", str(value))
        
        return text, menu['buttons']

    @classmethod
    def create_keyboard(cls, buttons_data, extra_buttons=None):
        """
        ایجاد کیبورد با امکان اضافه کردن دکمه‌های جدید
        """
        keyboard = []
        for button_text, callback_data in buttons_data:
            keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])
        
        # اضافه کردن دکمه‌های جدید (توسط توسعه‌دهنده)
        if extra_buttons:
            for button_text, callback_data in extra_buttons:
                keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])
        
        return InlineKeyboardMarkup(keyboard)

# 🔓 تابع کمکی برای توسعه‌دهنده
def developer_override(menu_name, changes):
    """
    🔧 فقط برای توسعه‌دهنده اصلی - باز کردن قفل منو
    """
    print(f"🔓 توسعه‌دهنده در حال تغییر منوی: {menu_name}")
    print(f"📋 تغییرات: {changes}")
    return MenuLock.developer_modify_menu(menu_name, **changes)
