# handlers/admin_manager.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import ADMINS, ADMIN_LEVELS

def is_admin(user_id: int) -> bool:
    """بررسی اینکه کاربر ادمین هست یا نه"""
    return user_id in ADMINS

def get_admin_level(user_id: int) -> str:
    """دریافت سطح دسترسی ادمین"""
    return ADMIN_LEVELS.get(user_id, "user")

async def show_admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش پنل مدیریت برای ادمین‌ها"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.callback_query.answer("❌ دسترسی denied!", show_alert=True)
        return
    
    admin_level = get_admin_level(user_id)
    
    keyboard = []
    
    # دکمه‌های مشترک برای همه ادمین‌ها
    keyboard.append([InlineKeyboardButton("👥 مدیریت کاربران", callback_data="admin_manage_users")])
    keyboard.append([InlineKeyboardButton("📊 آمار ربات", callback_data="admin_stats")])
    
    # دکمه پنل حرفه ای فقط برای سوپر ادمین
    if admin_level == "super_admin":
        keyboard.append([InlineKeyboardButton("👑 پنل مدیریت حرفه ای", callback_data="super_admin_panel")])
    
    keyboard.append([InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="main_menu")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    level_names = {
        "super_admin": "سوپر ادمین",
        "support_admin": "پشتیبان",
        "user": "کاربر"
    }
    
    message = f"""👑 **پنل مدیریت**

🆔 آیدی ادمین: `{user_id}`
📊 سطح دسترسی: {level_names[admin_level]}

لطفاً گزینه مورد نظر را انتخاب کنید:"""
    
    await update.callback_query.edit_message_text(
        message, 
        reply_markup=reply_markup, 
        parse_mode='Markdown'
    )
