# =============================================
# 🚀 MRH-CRIBOT - Run Script
# 👤 Developer: Mohammad Reza Hossein Khani
# 🏃 Easy Startup Script
# =============================================

import os
import sys
import logging
from pathlib import Path

# اضافه کردن مسیر پروژه به PATH
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def setup_logging():
    """تنظیمات پیشرفته لاگ‌گیری"""
    log_dir = project_root / "logs"
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "mrh_cribot.log", encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def check_environment():
    """بررسی محیط اجرا"""
    try:
        # بررسی وجود فایل‌های ضروری
        essential_files = [
            "config.py",
            "main.py", 
            "database/models.py",
            "requirements.txt"
        ]
        
        for file in essential_files:
            if not (project_root / file).exists():
                print(f"❌ فایل ضروری یافت نشد: {file}")
                return False
        
        # بررسی ایمپورت ماژول‌ها
        try:
            from config import BOT_TOKEN, CONFIG
            from database.models import init_db
        except ImportError as e:
            print(f"❌ خطا در ایمپورت ماژول‌ها: {e}")
            return False
        
        print("✅ بررسی محیط اجرا موفق بود")
        return True
        
    except Exception as e:
        print(f"❌ خطا در بررسی محیط: {e}")
        return False

def show_welcome():
    """نمایش پیام خوشآمدگویی"""
    welcome_text = """
🤖 ============================================ 🤖
🚀           MRH-CRIBOT                    
👤      Developer: Mohammad Reza Hossein Khani    
🎯          Version: 1.0.0                
💫      Crypto Intelligence Bot                  
🤖 ============================================ 🤖

🎯 سرویس‌های هوشمند:
• 📊 سیگنال‌های کریپتو
• 🛡 سرویس VPN 
• 💰 پرداخت چند ارزی
• 🤖 پشتیبانی هوشمند

🔧 در حال راه‌اندازی...
    """
    print(welcome_text)

def main():
    """تابع اصلی اجرای ربات"""
    try:
        # نمایش بنر
        show_welcome()
        
        # تنظیم لاگ‌گیری
        setup_logging()
        logger = logging.getLogger(__name__)
        
        # بررسی محیط
        if not check_environment():
            print("\n❌ لطفاً ابتدا setup.py را اجرا کنید:")
            print("   python setup.py")
            sys.exit(1)
        
        # راه‌اندازی دیتابیس
        try:
            from database.models import init_db
            init_db()
            logger.info("✅ پایگاه داده راه‌اندازی شد")
        except Exception as e:
            logger.error(f"❌ خطا در راه‌اندازی دیتابیس: {e}")
            print("⚠️  ادامه بدون دیتابیس...")
        
        # بررسی توکن ربات
        from config import BOT_TOKEN
        if BOT_TOKEN == "8560782678:AAG8dqx5OToq1YPN_FmcCtTEBWptiqQ6nE0":
            print("\n⚠️  هشدار: از توکن پیش‌فرض استفاده می‌کنید")
            print("💡 برای امنیت بیشتر، توکن ربات خود را در config.py قرار دهید")
        
        # اجرای ربات اصلی
        print("\n🚀 در حال اجرای ربات اصلی...")
        print("⏳ لطفاً منتظر بمانید...\n")
        
        from main import MRHCribot
        bot = MRHCribot()
        bot.run()
        
    except KeyboardInterrupt:
        print("\n\n🛑 ربات توسط کاربر متوقف شد")
        print("👋 خدانگهدار!")
    except Exception as e:
        print(f"\n❌ خطای غیرمنتظره: {e}")
        print("🔧 لطفاً خطا را بررسی کنید")
        logging.error(f"خطای غیرمنتظره: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
