# handlers/start.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import ADMINS, BOT_NAME
from database import db
from menu_lock import MenuLock  # 🔒 سیستم قفل
from handlers.admin_manager import is_admin

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    🚫 منوی اصلی - قفل شده
    ⚠️ تغییر متن یا دکمه‌ها ممنوع!
    🔒 استفاده از سیستم menu_lock.py الزامی است
    """
    
    user_id = update.effective_user.id
    username = update.effective_user.username
    
    # افزودن کاربر به دیتابیس
    db.add_user(user_id, username)
    
    # بررسی اینکه کاربر قبلاً شرایط را پذیرفته
    if not context.user_data.get('disclaimer_accepted'):
        from handlers.disclaimer import show_disclaimer
        await show_disclaimer(update, context)
        return
    
    # 🔒 استفاده از منوی قفل شده - تغییر این بخش ممنوع!
    menu_text, menu_buttons = MenuLock.get_locked_menu('main_menu')
    
    # ایجاد کیبورد از دیتای قفل شده - تغییر این بخش ممنوع!
    keyboard = []
    for button_text, callback_data in menu_buttons:
        keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])
    
    # افزودن دکمه مدیریت برای ادمین‌ها (این بخش قابل توسعه است)
    if is_admin(user_id):
        keyboard.append([InlineKeyboardButton("👑 مدیریت ربات", callback_data="admin_panel")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # ارسال پیام با منوی قفل شده - تغییر این بخش ممنوع!
    await update.message.reply_text(
        menu_text, 
        reply_markup=reply_markup, 
        parse_mode='Markdown'
    )

async def handle_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    مدیریت کلیک روی دکمه‌های منوی اصلی
    """
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    # هندلرهای منوی اصلی
    if data == "vip_channels":
        from handlers.vip_channels import show_vip_channels_menu
        await show_vip_channels_menu(update, context)
        
    elif data == "buy_config":
        from handlers.vip_channels import show_access_methods
        await show_access_methods(update, context, "general")
        
    elif data == "my_account":
        from handlers.account import show_account_menu
        await show_account_menu(update, context)
        
    elif data == "support":
        from handlers.smart_support import smart_support_system
        await smart_support_system(update, context)
        
    elif data == "help":
        await help_command(update, context)
        
    elif data == "admin_panel":
        from handlers.admin_manager import show_admin_panel
        await show_admin_panel(update, context)
        
    # هندلر بازگشت به منوی اصلی
    elif data == "main_menu":
        if query.message:
            await query.delete_message()
        await start_handler(update, context)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    دستور /help - راهنمای ربات
    """
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
    
    if update.message:
        await update.message.reply_text(help_text, parse_mode='Markdown')
    else:
        await update.callback_query.edit_message_text(help_text, parse_mode='Markdown')

# 🔒 تأیید سلامت ماژول
print("✅ handlers/start.py: سیستم قفل منو فعال شد")
