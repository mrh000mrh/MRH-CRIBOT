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

from config import BOT_TOKEN, BOT_NAME, ADMINS
from database import db

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
        self.application = None
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """دستور /start - اولین ارتباط کاربر با ربات"""
        user = update.effective_user
        user_id = user.id
        username = user.username
        
        # افزودن کاربر به دیتابیس
        db.add_user(user_id, username)
        
        # بررسی اینکه کاربر قبلاً شرایط را پذیرفته
        if not context.user_data.get('disclaimer_accepted'):
            from handlers.disclaimer import show_disclaimer
            await show_disclaimer(update, context)
            return
        
        welcome_text = f"""
🎉 **به {BOT_NAME} خوش آمدید!**

لطفاً گزینه مورد نظر خود را انتخاب کنید:
        """
        
        # ایجاد کیبورد منوی اصلی
        keyboard = [
            [InlineKeyboardButton("🎯 ورود به کانال های VIP", callback_data="vip_channels")],
            [InlineKeyboardButton("🛡️ خرید کانفیگ", callback_data="buy_config")],
            [InlineKeyboardButton("👤 حساب کاربری", callback_data="my_account")],
            [InlineKeyboardButton("📞 پشتیبانی", callback_data="support")],
            [InlineKeyboardButton("ℹ️ راهنما", callback_data="help")]
        ]
        
        # افزودن دکمه مدیریت برای ادمین‌ها
        if user_id in ADMINS:
            keyboard.append([InlineKeyboardButton("👑 مدیریت ربات", callback_data="admin_panel")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
        
        logger.info(f"کاربر جدید شروع کرد: {user.id} - {user.first_name}")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """دستور /help - راهنمای کامل ربات"""
        help_text = f"""
📖 **راهنمای {BOT_NAME}**

🔸 **دستورات اصلی:**
/start - شروع ربات و منوی اصلی
/help - نمایش راهنمای کامل

🔸 **منوهای اصلی:**
• 🎯 کانال‌های VIP - دسترسی به سیگنال‌ها
• 🛡️ خرید کانفیگ - سرویس VPN اختصاصی
• 👤 حساب کاربری - مدیریت حساب
• 📞 پشتیبانی - راهنمایی و حل مشکل

🔸 **ویژگی‌های منحصر بفرد:**
✅ سیستم دسترسی سه‌گانه (خرید VPN، لایسنس، ادمین)
✅ پنل مدیریت پیشرفته
✅ پشتیبانی هوشمند
✅ رابط کاربری فارسی و ساده

🎯 **سیستم دسترسی به سیگنال‌ها:**
1. خرید کانفیگ VPN
2. کد لایسنس
3. دسترسی مستقیم ادمین
        """
        
        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def handle_callback_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """مدیریت کلیک روی تمام دکمه‌ها"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        user_id = query.from_user.id
        
        logger.info(f"کال‌بک دریافت شد: {data} از کاربر {user_id}")
        
        # هندلرهای منوی اصلی
        if data == "vip_channels":
            from handlers.vip_channels import show_vip_channels_menu
            await show_vip_channels_menu(update, context)
            
        elif data == "buy_config":
            from handlers.vip_channels import show_vip_access_methods
            await show_vip_access_methods(update, context, "general")
            
        elif data == "my_account":
            from handlers.account import show_account_menu
            await show_account_menu(update, context)
            
        elif data == "support":
            from handlers.smart_support import smart_support_system
            await smart_support_system(update, context)
            
        elif data == "help":
            await self.help_command(update, context)
            
        elif data == "admin_panel":
            from handlers.admin_manager import show_admin_panel
            await show_admin_panel(update, context)
            
        # هندلرهای کانال‌های VIP
        elif data.startswith("vip_"):
            channel_type = data.replace("vip_", "")
            from handlers.vip_channels import show_vip_access_methods
            await show_vip_access_methods(update, context, channel_type)
            
        elif data.startswith("channel_"):
            channel_type = data.replace("channel_", "")
            from handlers.vip_channels import handle_vip_access
            await handle_vip_access(update, context, channel_type)
            
        # هندلرهای مدیریت
        elif data == "super_admin_panel":
            from handlers.super_admin import super_admin_panel
            await super_admin_panel(update, context)
            
        elif data == "smart_support":
            from handlers.smart_support import smart_support_system
            await smart_support_system(update, context)
            
        elif data == "coupon_management":
            from handlers.coupon_system import coupon_management_system
            await coupon_management_system(update, context)
            
        elif data == "smart_notification":
            from handlers.notification_system import smart_notification_system
            await smart_notification_system(update, context)
            
        elif data == "smart_alerts":
            from handlers.smart_alerts import smart_notification_alerts
            await smart_notification_alerts(update, context)
            
        elif data == "advanced_stats":
            from handlers.advanced_stats import advanced_statistics_charts
            await advanced_statistics_charts(update, context)
            
        # هندلر بازگشت به منوی اصلی
        elif data == "main_menu":
            if query.message:
                await query.delete_message()
            await self.start_command(update, context)
            
        else:
            # برای کال‌بک‌های تعریف نشده
            await query.edit_message_text(
                "⚠️ این قابلیت به زودی اضافه خواهد شد!",
                parse_mode='Markdown'
            )

    def setup_handlers(self):
        """تنظیم تمام هندلرهای ربات"""
        # دستورات متنی
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        
        # هندلر اصلی کال‌بک‌ها
        self.application.add_handler(CallbackQueryHandler(self.handle_callback_query))
        
        # هندلر شرایط و قوانین
        from handlers.disclaimer import handle_disclaimer_callback
        self.application.add_handler(CallbackQueryHandler(handle_disclaimer_callback, pattern="^(accept_disclaimer|exit_bot)$"))

    def run(self):
        """راه‌اندازی اصلی ربات"""
        try:
            # ایجاد برنامه ربات
            self.application = Application.builder().token(BOT_TOKEN).build()
            
            # تنظیم هندلرها
            self.setup_handlers()
            
            # راه‌اندازی ربات
            logger.info(f"🤖 {BOT_NAME} در حال راه‌اندازی...")
            
            print("=" * 50)
            print(f"🚀 {BOT_NAME} - Crypto Intelligence Bot")
            print("🎯 سیستم مدیریت پیشرفته فعال شد")
            print("📊 پنل سوپر ادمین آماده است")
            print("🛡️ سیستم دسترسی سه‌گانه فعال است")
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
