# =============================================
# 🚀 MRH-CRIBOT - Setup Script
# 👤 Developer: Mohammad Reza Hossein Khani
# ⚡ Quick Setup & Installation
# =============================================

import os
import sys
import subprocess
import logging
from pathlib import Path

# تنظیمات لاگ‌گیری
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MRHCribotSetup:
    def __init__(self):
        self.project_name = "MRH-CRIBOT"
        self.developer = "Mohammad Reza Hossein Khani"
        self.version = "1.0.0"
        
    def print_banner(self):
        """نمایش بنر زیبای ربات"""
        banner = f"""
🤖 ============================================ 🤖
🚀           {self.project_name}                   
👤      Developer: {self.developer}    
🎯          Version: {self.version}                
💫    Crypto Intelligence Bot                  
🤖 ============================================ 🤖

🔧 در حال راه‌اندازی ربات...
        """
        print(banner)
    
    def check_python_version(self):
        """بررسی نسخه پایتون"""
        try:
            version = sys.version_info
            if version.major < 3 or (version.major == 3 and version.minor < 8):
                logger.error("❌ پایتون نسخه 3.8 یا بالاتر نیاز است")
                return False
            
            logger.info(f"✅ نسخه پایتون: {version.major}.{version.minor}.{version.micro}")
            return True
            
        except Exception as e:
            logger.error(f"خطا در بررسی نسخه پایتون: {e}")
            return False
    
    def install_requirements(self):
        """نصب کتابخانه‌های مورد نیاز"""
        try:
            logger.info("📦 در حال نصب کتابخانه‌های مورد نیاز...")
            
            # نصب از requirements.txt
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("✅ کتابخانه‌ها با موفقیت نصب شدند")
                return True
            else:
                logger.error(f"❌ خطا در نصب کتابخانه‌ها: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"خطا در نصب کتابخانه‌ها: {e}")
            return False
    
    def setup_database(self):
        """راه‌اندازی پایگاه داده"""
        try:
            logger.info("🗄️ در حال راه‌اندازی پایگاه داده...")
            
            # ایمپورت مدل‌ها و ایجاد جداول
            from database.models import init_db
            
            init_db()
            logger.info("✅ پایگاه داده با موفقیت راه‌اندازی شد")
            return True
            
        except ImportError as e:
            logger.error(f"❌ خطا در ایمپورت مدل‌های دیتابیس: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ خطا در راه‌اندازی دیتابیس: {e}")
            return False
    
    def create_directories(self):
        """ایجاد دایرکتوری‌های مورد نیاز"""
        try:
            directories = [
                "backups",
                "logs", 
                "configs",
                "temp"
            ]
            
            for directory in directories:
                Path(directory).mkdir(exist_ok=True)
                logger.info(f"📁 دایرکتوری {directory} ایجاد شد")
            
            return True
            
        except Exception as e:
            logger.error(f"خطا در ایجاد دایرکتوری‌ها: {e}")
            return False
    
    def check_config(self):
        """بررسی تنظیمات ربات"""
        try:
            from config import BOT_TOKEN, CONFIG
            
            if BOT_TOKEN and BOT_TOKEN != "8560782678:AAG8dqx5OToq1YPN_FmcCtTEBWptiqQ6nE0":
                logger.info("✅ توکن ربات تنظیم شده است")
                return True
            else:
                logger.warning("⚠️  لطفاً توکن ربات را در فایل config.py تنظیم کنید")
                return False
                
        except ImportError:
            logger.error("❌ فایل config.py یافت نشد")
            return False
        except Exception as e:
            logger.error(f"خطا در بررسی تنظیمات: {e}")
            return False
    
    def run_setup(self):
        """اجرای کامل مراحل راه‌اندازی"""
        self.print_banner()
        
        steps = [
            ("بررسی نسخه پایتون", self.check_python_version),
            ("ایجاد دایرکتوری‌ها", self.create_directories),
            ("بررسی تنظیمات", self.check_config),
            ("نصب کتابخانه‌ها", self.install_requirements),
            ("راه‌اندازی دیتابیس", self.setup_database),
        ]
        
        success_count = 0
        total_steps = len(steps)
        
        for step_name, step_function in steps:
            logger.info(f"🔧 در حال اجرای: {step_name}...")
            
            if step_function():
                logger.info(f"✅ {step_name} - موفق")
                success_count += 1
            else:
                logger.error(f"❌ {step_name} - ناموفق")
        
        # نمایش نتیجه نهایی
        print("\n" + "="*50)
        if success_count == total_steps:
            print("🎉 راه‌اندازی با موفقیت کامل شد!")
            print("🤖 برای اجرای ربات دستور زیر را وارد کنید:")
            print("   python main.py")
            print("\n📖 برای اطلاعات بیشتر README.md را مطالعه کنید")
        else:
            print(f"⚠️  راه‌اندازی با {success_count} از {total_steps} مرحله موفق بود")
            print("🔧 لطفاً خطاهای بالا را بررسی کنید")
        print("="*50)

def main():
    """تابع اصلی اجرای راه‌اندازی"""
    try:
        setup = MRHCribotSetup()
        setup.run_setup()
        
    except KeyboardInterrupt:
        print("\n❌ راه‌اندازی توسط کاربر متوقف شد")
    except Exception as e:
        print(f"❌ خطای غیرمنتظره: {e}")

if __name__ == "__main__":
    main()
