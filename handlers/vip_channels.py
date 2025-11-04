# handlers/vip_channels.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import VIP_CHANNEL_TYPES, BOT_NAME
from database import db
from handlers.admin_manager import is_admin

async def show_vip_channels_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش منوی کانال‌های VIP"""
    
    keyboard = [
        [InlineKeyboardButton("⚡ اسکالپ | Scalp", callback_data="channel_scalp")],
        [InlineKeyboardButton("📈 سوئینگ | Swing", callback_data="channel_swing")],
        [InlineKeyboardButton("💼 پورتفولیو | Portfolio", callback_data="channel_portfolio")],
        [InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="main_menu")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = """🎯 **کانال‌های VIP**

لطفاً نوع کانال مورد نظر خود را انتخاب کنید:"""
    
    await update.callback_query.edit_message_text(
        message, 
        reply_markup=reply_markup, 
        parse_mode='Markdown'
    )

async def handle_vip_access(update: Update, context: ContextTypes.DEFAULT_TYPE, channel_type: str):
    """مدیریت دسترسی به کانال‌های VIP"""
    user_id = update.callback_query.from_user.id
    
    # بررسی دسترسی کاربر
    has_access = db.check_vpn_access(user_id) or db.check_license_access(user_id) or is_admin(user_id)
    
    if has_access:
        # اگر کاربر دسترسی دارد، لینک کانال را نشان بده
        await show_channel_link(update, context, channel_type)
    else:
        # اگر دسترسی ندارد، روش‌های دسترسی را نشان بده
        await show_access_methods(update, context, channel_type)

async def show_channel_link(update: Update, context: ContextTypes.DEFAULT_TYPE, channel_type: str):
    """نمایش لینک کانال برای کاربران دارای دسترسی"""
    channel_info = VIP_CHANNEL_TYPES.get(channel_type, {})
    channel_name = channel_info.get("name", "کانال VIP")
    channel_description = channel_info.get("description", "")
    channel_link = channel_info.get("link", "https://t.me/example")
    
    keyboard = [
        [InlineKeyboardButton("🔗 عضویت در کانال", url=channel_link)],
        [InlineKeyboardButton("🔙 بازگشت به کانال‌ها", callback_data="vip_channels")],
        [InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="main_menu")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = f"""✅ **دسترسی تایید شد!**

🎯 کانال: **{channel_name}**
📝 {channel_description}

برای ورود به کانال روی دکمه زیر کلیک کنید:"""

    await update.callback_query.edit_message_text(
        message, 
        reply_markup=reply_markup, 
        parse_mode='Markdown'
    )

async def show_access_methods(update: Update, context: ContextTypes.DEFAULT_TYPE, channel_type: str):
    """نمایش روش‌های دسترسی بعد از انتخاب کانال"""
    channel_info = VIP_CHANNEL_TYPES.get(channel_type, {})
    channel_name = channel_info.get("name", "کانال VIP")
    
    keyboard = [
        [InlineKeyboardButton("🛡️ خرید کانفیگ برای دسترسی", callback_data="buy_config")],
        [InlineKeyboardButton("🔑 کد لایسنس", callback_data="activate_license")],
        [InlineKeyboardButton("📞 پشتیبانی", callback_data="support")],
        [InlineKeyboardButton("🔙 بازگشت به کانال‌ها", callback_data="vip_channels")],
        [InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="main_menu")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = f"""🔒 **به {BOT_NAME} خوش آمدید!**

🎯 کانال انتخاب شده: **{channel_name}**

برای دسترسی به کانال های VIP، یکی از روش‌های زیر را انتخاب کنید:"""

    await update.callback_query.edit_message_text(
        message, 
        reply_markup=reply_markup, 
        parse_mode='Markdown'
    )
