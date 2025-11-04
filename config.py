# config.py
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # جایگزین کن با توکن رباتت
BOT_NAME = "MRH CRIBOT"

# لیست ادمین‌ها (آیدی عددی)
ADMINS = [
    123456789,  # آیدی شما - این رو عوض کن
]

# سطوح دسترسی ادمین‌ها
ADMIN_LEVELS = {
    123456789: "super_admin",  # دسترسی کامل
}

# تنظیمات کانفیگ‌ها
VPN_CONFIGS = {
    "basic": {"price": 50000, "duration": 30, "name": "پلن پایه"},
    "premium": {"price": 100000, "duration": 90, "name": "پلن پریمیوم"},
    "vip": {"price": 200000, "duration": 180, "name": "پلن VIP"}
}

# انواع کانال‌های VIP
VIP_CHANNEL_TYPES = {
    "scalp": {
        "name": "اسکالپ | Scalp",
        "description": "سیگنال‌های کوتاه مدت و سریع",
        "link": "https://t.me/scalp_channel"
    },
    "swing": {
        "name": "سوئینگ | Swing", 
        "description": "سیگنال‌های میان مدت",
        "link": "https://t.me/swing_channel"
    },
    "portfolio": {
        "name": "پورتفولیو | Portfolio",
        "description": "سیگنال‌های بلند مدت و سبدگردانی",
        "link": "https://t.me/portfolio_channel"
    }
}
