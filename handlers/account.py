# handlers/account.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import db

async def show_account_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش منوی حساب کاربری آپدیت شده"""
    
    user = update.effective_user
    user_id = user.id
    username = user.username or "تنظیم نشده"
    
    # اطلاعات از دیتابیس
    vpn_access = db.check_vpn_access(user_id)
    license_access = db.check_license_access(user_id)
    balance = 0
    balance_type = "تومان"
    subscription_status = "کاربر عادی"
    active_subscription = vpn_access or license_access
    
    keyboard = [
        [InlineKeyboardButton("💳 افزایش موجودی", callback_data="increase_balance")],
        [InlineKeyboardButton("📊 تاریخچه تراکنش‌ها", callback_data="transaction_history")],
        [InlineKeyboardButton("🎫 استفاده از کوپن", callback_data="use_coupon")],
        [InlineKeyboardButton("👥 دعوت از دوستان", callback_data="invite_friends")],
        [InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="main_menu")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = f"""
👤 **حساب کاربری**

🆔 آیدی: `{user_id}`
👤 نام کاربری: @{username}  
💰 موجودی: {balance} {balance_type}
📊 وضعیت اشتراک: {subscription_status}

🛡 **اشتراک فعال:**
{"✅ اشتراک فعال دارید" if active_subscription else "❌ هیچ اشتراک فعالی ندارید"}
"""
    
    await update.callback_query.edit_message_text(
        message, 
        reply_markup=reply_markup, 
        parse_mode='Markdown'
    )
