# =============================================
# 🚀 MRH-CRIBOT - Crypto Intelligence Bot
# 👤 Developer: Mohammad Reza Hossein Khani
# 🎯 Crypto Intelligence & VPN Services
# =============================================

import os
from dataclasses import dataclass

@dataclass
class BotConfig:
    # 🔐 اطلاعات توسعه‌دهنده
    DEVELOPER = "Mohammad Reza Hossein Khani"
    BOT_NAME = "MRH-CRIBOT"
    VERSION = "1.0.0"
    
    # 🔑 تنظیمات اصلی ربات
    BOT_TOKEN = "8560782678:AAG8dqx5OToq1YPN_FmcCtTEBWptiqQ6nE0"
    ADMIN_IDS = [123456789]  # 🔧 آی‌دی عددی ادمین
    
    # 🗄️ پایگاه داده
    DATABASE_URL = "sqlite:///mrh_cribot.db"
    
    # 💰 شبکه‌های پرداخت ارزی
    CRYPTO_NETWORKS = {
        "BEP20": {
            "name": "Binance Smart Chain",
            "fee": 0.5,
            "recommended": True,
            "address": "0x8318ab253316ee2eba4642f3d447f11ebf52f2f3"
        },
        "SOL": {
            "name": "Solana", 
            "fee": 0.1,
            "recommended": True,
            "address": "EJA4kvZt2oNZLSiRHtAKwE2NNYqUcww9MLkX2HZUJURM"
        },
        "TRC20": {
            "name": "Tron Network",
            "fee": 1.0,
            "recommended": False,
            "address": "TYW8RCCELPKLThC2iKjVe96Ts7ob9CzeDF"
        }
    }
    
    # 🛡️ پلن‌های سرویس VPN
    VPN_SERVICES = {
        "basic": {
            "name": "پلن پایه - 30 روزه",
            "duration": 30,
            "price_usdt": 10,
            "features": ["سرعت استاندارد", "پشتیبانی پایه", "کانفیگ خودکار"]
        },
        "pro": {
            "name": "پلن حرفه‌ای - 90 روزه", 
            "duration": 90,
            "price_usdt": 25,
            "discount": "15%",
            "features": ["سرعت بالا", "پشتیبانی VIP", "سرورهای اختصاصی"]
        },
        "premium": {
            "name": "پلن طلایی - 180 روزه",
            "duration": 180, 
            "price_usdt": 40,
            "discount": "33%",
            "features": ["بالاترین سرعت", "پشتیبانی 24/7", "سرورهای پرسرعت"]
        }
    }
    
    # 📊 سرویس هوشمند سیگنال‌ها
    INTELLIGENCE_SERVICES = {
        "scalp": {
            "name": "سیگنال اسکالپ",
            "leverage": "5-10x",
            "risk": "HIGH",
            "description": "معاملات کوتاه مدت 5-40 دقیقه"
        },
        "swing": {
            "name": "سیگنال سوئینگ", 
            "leverage": "3-5x",
            "risk": "MEDIUM", 
            "description": "معاملات میان‌مدت 3-8 روز"
        },
        "portfolio": {
            "name": "مدیریت سبد",
            "leverage": "1x",
            "risk": "LOW",
            "description": "سرمایه‌گذاری بلندمدت و مدیریت ریسک"
        }
    }
    
    # 🔗 APIهای خارجی
    EXTERNAL_APIS = {
        "coingecko": "https://api.coingecko.com/api/v3",
        "fear_greed": "https://api.alternative.me/fng/",
        "binance": "https://api.binance.com/api/v3"
    }
    
    # 🏪 پرداخت ریالی (قابل توسعه)
    IRAN_PAYMENT = {
        "merchant_api": "your_merchant_key",
        "callback_url": "https://yourdomain.com/verify",
        "minimum_amount": 10000  # تومان
    }

# دسترسی‌های سریع
CONFIG = BotConfig()
BOT_TOKEN = CONFIG.BOT_TOKEN
ADMIN_IDS = CONFIG.ADMIN_IDS
