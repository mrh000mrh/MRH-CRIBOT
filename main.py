# =============================================
# 🚀 MRH-CRIBOT - Crypto Intelligence Bot
# 👤 Developer: Mohammad Reza Hossein Khani
# 🎯 Main Bot File - Startup & Core Handlers
# =============================================

import logging
import asyncio
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import CONFIG, BOT_TOKEN

# تنظیمات پیشرفته لاگ‌گیری
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("mrh_cribot.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MRHCribot:
    def __init__(self):
        self.config = CONFIG
        self.application = None
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """دستور /start - اولین ارتباط کاربر با ربات"""
        user = update.effective_user
        
        welcome_text = f"""
👋 **سلام {user.first_name} عزیز!**

به **{self.config.BOT_NAME}** خوش آمدید 🤖

🧠 **ربات هوشمند کریپتو و VPN**
• توسعه‌دهنده: **{self.config.DEVELOPER}**
• نسخه: **{self.config.VERSION}**

🎯 **سرویس‌های هوشمند ما:**
📊 **سیگنال‌های کریپتو** - تحلیل هوشمند بازار
🛡 **سرویس VPN** - امنیت و سرعت بالا  
💰 **پرداخت چند ارزی** - ریالی و ارز دیجیتال
🤖 **پشتیبانی هوشمند** - پاسخگویی 24/7

لطفاً از منوی زیر انتخاب کنید:
        """
        
        # ایجاد کیبورد منوی اصلی
        keyboard = [
            [InlineKeyboardButton("📊 سیگنال‌های هوشمند", callback_data="intelligence_menu")],
            [InlineKeyboardButton("🛡 سرویس VPN", callback_data="vpn_menu")],
            [InlineKeyboardButton("💰 پرداخت و کیف پول", callback_data="payment_menu")],
            [InlineKeyboardButton("🤖 پشتیبانی MRH", callback_data="support_menu")],
            [InlineKeyboardButton("ℹ️ درباره ربات", callback_data="about_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
        
        logger.info(f"کاربر جدید شروع کرد: {user.id} - {user.first_name}")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """دستور /help - راهنمای کامل ربات"""
        help_text = f"""
📖 **راهنمای {self.config.BOT_NAME}**

🔸 **دستورات اصلی:**
/start - شروع ربات و منوی اصلی
/help - نمایش راهنمای کامل
/about - اطلاعات ربات و توسعه‌دهنده

🔸 **منوهای هوشمند:**
• 📊 سیگنال‌های کریپتو - تحلیل هوشمند بازار
• 🛡 سرویس VPN - اتصال امن و پرسرعت
• 💰 پرداخت - درگاه ریالی و ارزی
• 🤖 پشتیبانی - راهنمایی و حل مشکل

🔸 **ویژگی‌های منحصر بفرد:**
✅ هوش مصنوعی در تحلیل بازار
✅ سرویس VPN با کانفیگ خودکار
✅ پشتیبانی 24 ساعته
✅ رابط کاربری فارسی و ساده

🛠 **توسعه‌دهنده:** {self.config.DEVELOPER}
        """
        
        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def about_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """دستور /about - اطلاعات ربات و توسعه‌دهنده"""
        about_text = f"""
🤖 **{self.config.BOT_NAME}**

🧠 **Crypto Intelligence Bot**
ربات هوشمند تحلیل بازار کریپتو و سرویس VPN

👤 **توسعه‌دهنده:**
{self.config.DEVELOPER}

🎯 **ماموریت ربات:**
ارائه سرویس‌های هوشمند و امن در حوزه ارزهای دیجیتال

📊 **خدمات اصلی:**
• تحلیل هوشمند بازار کریپتو
• سیگنال‌های معاملاتی دقیق
• سرویس VPN پرسرعت
• پشتیبانی هوشمند

🔧 **مشخصات فنی:**
• نسخه: {self.config.VERSION}
• پایگاه داده: SQLite
• زبان: Python 3.8+
• کتابخانه: python-telegram-bot

🌐 **توسعه‌دهنده:** محمد رضا حسین خانی
        """
        
        await update.message.reply_text(about_text, parse_mode='Markdown')

    async def handle_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """مدیریت کلیک روی منوی اصلی"""
        query = update.callback_query
        await query.answer()
        
        menu_type = query.data
        user = query.from_user
        
        responses = {
            "intelligence_menu": "📊 **سیستم هوشمند سیگنال‌ها**\n\nبه زودی فعال می‌شود...\n\n🧠 تحلیل هوشمند بازار\n🎯 سیگنال‌های دقیق\n⚡ به روزرسانی لحظه‌ای",
            "vpn_menu": "🛡 **سرویس VPN اختصاصی**\n\nبه زودی فعال می‌شود...\n\n🚀 سرعت بالا\n🔒 امنیت کامل\n🌐 عبور از محدودیت",
            "payment_menu": "💰 **سیستم پرداخت هوشمند**\n\nبه زودی فعال می‌شود...\n\n💳 پرداخت ریالی\n🪙 پرداخت ارزی\n⚡ تراکنش سریع",
            "support_menu": "🤖 **پشتیبانی MRH**\n\nبه زودی فعال می‌شود...\n\n👤 پشتیبانی توسعه‌دهنده\n🔄 پاسخگویی سریع\n🔧 حل مشکلات فنی",
            "about_menu": f"ℹ️ **درباره {self.config.BOT_NAME}**\n\n🤖 ربات هوشمند کریپتو و VPN\n👤 توسعه‌دهنده: {self.config.DEVELOPER}\n🎯 نسخه: {self.config.VERSION}\n\n🔧 به زودی تمام قابلیت‌ها فعال می‌شوند!"
        }
        
        if menu_type in responses:
            # ایجاد دکمه بازگشت به منوی اصلی
            keyboard = [[InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="main_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                text=responses[menu_type],
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            
            logger.info(f"کاربر {user.id} منو را باز کرد: {menu_type}")

    async def handle_back_to_main(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """بازگشت به منوی اصلی"""
        query = update.callback_query
        await query.answer()
        
        await self.start_command(update, context)

    def setup_handlers(self):
        """تنظیم تمام هندلرهای ربات"""
        # دستورات متنی
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("about", self.about_command))
        
        # هندلرهای منو
        self.application.add_handler(CallbackQueryHandler(self.handle_main_menu, pattern="^(intelligence|vpn|payment|support|about)_menu$"))
        self.application.add_handler(CallbackQueryHandler(self.handle_back_to_main, pattern="^main_menu$"))

    def run(self):
        """راه‌اندازی اصلی ربات"""
        try:
            # ایجاد برنامه ربات
            self.application = Application.builder().token(BOT_TOKEN).build()
            
            # تنظیم هندلرها
            self.setup_handlers()
            
            # راه‌اندازی ربات
            logger.info(f"🤖 {self.config.BOT_NAME} در حال راه‌اندازی...")
            logger.info(f"👤 توسعه‌دهنده: {self.config.DEVELOPER}")
            logger.info(f"🎯 نسخه: {self.config.VERSION}")
            
            print("=" * 50)
            print(f"🚀 {self.config.BOT_NAME} - Crypto Intelligence Bot")
            print(f"👤 Developer: {self.config.DEVELOPER}")
            print(f"🎯 Version: {self.config.VERSION}")
            print("🤖 ربات با موفقیت راه‌اندازی شد!")
            print("📍 آماده دریافت دستورات از کاربران...")
            print("=" * 50)
            
            self.application.run_polling()
            
        except Exception as e:
            logger.error(f"خطا در راه‌اندازی ربات: {e}")
            print(f"❌ خطا در راه‌اندازی: {e}")

if __name__ == "__main__":
    # ایجاد نمونه ربات و اجرا
    bot = MRHCribot()
    bot.run()
