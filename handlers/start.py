# handlers/start.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import ADMINS, BOT_NAME
from database import db

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username
    
    # افزودن کاربر به دیتابیس
    db.add_user(user_id, username)
    
    # بررسی اینکه کاربر قبلاً شرایط را پذیرفته
    if not context.user_data.get('disclaimer_accepted'):
        from handlers.disclaimer import show_disclaimer
        await show_disclaimer(update, context)
        return
    
    keyboard = []
    
    # منوی کاربر عادی
    keyboard.append([InlineKeyboardButton("🎯 ورود به کانال های VIP", callback_data="vip_channels")])
    keyboard.append([InlineKeyboardButton("🛡️ خرید کانفیگ", callback_data="buy_config")])
    keyboard.append([InlineKeyboardButton("👤 حساب کاربری", callback_data="my_account")])
    keyboard.append([InlineKeyboardButton("📞 پشتیبانی", callback_data="support")])
    keyboard.append([InlineKeyboardButton("ℹ️ راهنما", callback_data="help")])
    
    # افزودن دکمه مدیریت برای ادمین‌ها
    from handlers.admin_manager import is_admin
    if is_admin(user_id):
        keyboard.append([InlineKeyboardButton("👑 مدیریت ربات", callback_data="admin_panel")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = f"""🎉 **به {BOT_NAME} خوش آمدید!**

لطفاً گزینه مورد نظر خود را انتخاب کنید:"""
    
    await update.message.reply_text(
        message, 
        reply_markup=reply_markup, 
        parse_mode='Markdown'
    )
