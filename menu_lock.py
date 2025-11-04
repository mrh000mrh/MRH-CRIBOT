# menu_lock.py
"""
🔒 MENU LOCK SYSTEM - MRH CRIBOT
🚫 PROTECTION AGAINST UNAUTHORIZED CHANGES
⚡ DEVELOPER: @mrh000mrh
📅 CREATED: 2024
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class MenuLock:
    """
    سیستم قفل منو - جلوگیری از تغییرات ناخواسته توسط دستیارهای AI
    """
    
    # 🚫 منوهای قفل شده - تغییر ممنوع!
    LOCKED_MENUS = {
        'main_menu': {
            'text': "🎉 **به ربات MRH CRIBOT خوش آمدید!**\n\nلطفاً گزینه مورد نظر خود را انتخاب کنید:",
            'buttons': [
                ["🎯 ورود به کانال های VIP", "vip_channels"],
                ["🛡️ خرید کانفیگ", "buy_config"],
                ["👤 حساب کاربری", "my_account"],
                ["📞 پشتیبانی", "support"],
                ["ℹ️ راهنما", "help"]
            ]
        },
        
        'vip_channels': {
            'text': "🎯 **کانال‌های VIP**\n\nلطفاً نوع کانال مورد نظر خود را انتخاب کنید:",
            'buttons': [
                ["⚡ اسکالپ | Scalp", "channel_scalp"],
                ["📈 سوئینگ | Swing", "channel_swing"],
                ["💼 پورتفولیو | Portfolio", "channel_portfolio"],
                ["🔙 بازگشت به منوی اصلی", "main_menu"]
            ]
        },
        
        'access_methods': {
            'text': "🔒 **به ربات MRH CRIBOT خوش آمدید!**\n\n🎯 کانال انتخاب شده: **{channel_name}**\n\nبرای دسترسی به کانال های VIP، یکی از روش‌های زیر را انتخاب کنید:",
            'buttons': [
                ["🛡️ خرید کانفیگ برای دسترسی", "buy_config"],
                ["🔑 کد لایسنس", "activate_license"],
                ["📞 پشتیبانی", "support"],
                ["🔙 بازگشت به کانال‌ها", "vip_channels"],
                ["🔙 بازگشت به منوی اصلی", "main_menu"]
            ]
        },
        
        'account_menu': {
            'text': """👤 **حساب کاربری**

🆔 آیدی: `{user_id}`
👤 نام کاربری: @{username}  
💰 موجودی: {balance} {balance_type}
📊 وضعیت اشتراک: {subscription_status}

🛡 **اشتراک فعال:**
{active_status}""",
            'buttons': [
                ["💳 افزایش موجودی", "increase_balance"],
                ["📊 تاریخچه تراکنش‌ها", "transaction_history"],
                ["🎫 استفاده از کوپن", "use_coupon"],
                ["👥 دعوت از دوستان", "invite_friends"],
                ["🔙 بازگشت به منوی اصلی", "main_menu"]
            ]
        }
    }
    
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
    def create_keyboard(cls, buttons_data):
        """
        ایجاد کیبورد از دیتای قفل شده
        """
        keyboard = []
        for button_text, callback_data in buttons_data:
            keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])
        return InlineKeyboardMarkup(keyboard)
    
    @classmethod
    def verify_all_menus(cls):
        """
        بررسی سلامت تمام منوها
        """
        required_menus = ['main_menu', 'vip_channels', 'access_methods', 'account_menu']
        missing_menus = [menu for menu in required_menus if menu not in cls.LOCKED_MENUS]
        
        if missing_menus:
            print(f"❌ منوهای گمشده: {missing_menus}")
            return False
        
        print("✅ تمام منوها سالم هستند")
        return True

# بررسی سلامت منوها در زمان ایمپورت
MenuLock.verify_all_menus()
