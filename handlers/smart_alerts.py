# handlers/smart_alerts.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def smart_notification_alerts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """سیستم نوتیفیکیشن هوشمند"""
    
    keyboard = [
        [InlineKeyboardButton("🔔 تنظیم اعلان فروش", callback_data="admin_set_sale_alert")],
        [InlineKeyboardButton("📈 اعلان آمار خاص", callback_data="admin_set_stats_alert")],
        [InlineKeyboardButton("👤 اعلان کاربر جدید", callback_data="admin_set_user_alert")],
        [InlineKeyboardButton("🛍️ اعلان محصول جدید", callback_data="admin_set_product_alert")],
        [InlineKeyboardButton("📋 مدیریت اعلان‌ها", callback_data="admin_manage_alerts")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="super_admin_panel")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = """🔔 **سیستم نوتیفیکیشن هوشمند**

📱 **انواع اعلان‌های قابل تنظیم:**
- 🔔 **فروش جدید** - اطلاع‌رسانی هر فروش
- 📈 **آمار خاص** - رسیدن به عدد مشخص
- 👤 **کاربر جدید** - ثبت‌نام کاربر VIP
- 🛍️ **محصول جدید** - اضافه شدن محصول

⚡ **کانال‌های ارسال:**
- پیام در ربات
- اعلان در گروه/کانال
- ایمیل (در صورت تنظیم)

لطفاً نوع اعلان را انتخاب کنید:"""
    
    await update.callback_query.edit_message_text(
        message, 
        reply_markup=reply_markup, 
        parse_mode='Markdown'
    )
