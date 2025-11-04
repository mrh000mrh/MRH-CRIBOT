# handlers/account.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import db
from menu_lock import MenuLock  # 🔒 سیستم قفل

async def show_account_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    🚫 منوی حساب کاربری - قفل شده
    """
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
    active_status = "✅ اشتراک فعال دارید" if active_subscription else "❌ هیچ اشتراک فعالی ندارید"
    
    # 🔒 استفاده از منوی قفل شده
    menu_text, menu_buttons = MenuLock.get_locked_menu(
        'account_menu',
        user_id=user_id,
        username=username,
        balance=balance,
        balance_type=balance_type,
        subscription_status=subscription_status,
        active_status=active_status
    )
    
    keyboard = []
    for button_text, callback_data in menu_buttons:
        keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.callback_query.edit_message_text(
        menu_text, 
        reply_markup=reply_markup, 
        parse_mode='Markdown'
    )
