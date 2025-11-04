# handlers/coupon_system.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from datetime import datetime, timedelta

async def coupon_management_system(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """سیستم مدیریت تخفیف و کوپن"""
    
    keyboard = [
        [InlineKeyboardButton("🎫 ایجاد کوپن جدید", callback_data="admin_create_coupon")],
        [InlineKeyboardButton("📋 مشاهده کوپن‌های فعال", callback_data="admin_view_coupons")],
        [InlineKeyboardButton("✏️ ویرایش کوپن", callback_data="admin_edit_coupon")],
        [InlineKeyboardButton("🗑️ حذف کوپن", callback_data="admin_delete_coupon")],
        [InlineKeyboardButton("📊 آمار استفاده از کوپن‌ها", callback_data="admin_coupon_stats")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="super_admin_panel")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = """🎫 **سیستم مدیریت تخفیف و کوپن**

✨ **انواع کوپن قابل ایجاد:**
- درصد تخفیف (10%، 20%، ...)
- مبلغ ثابت (5000 تومان، 10000 تومان، ...)
- تخفیف روی محصول خاص
- تخفیف برای کاربران خاص

⏰ **تنظیم زمان:**
- تاریخ انقضا
- تعداد استفاده محدود
- حداقل مبلغ سفارش

لطفاً عمل مورد نظر را انتخاب کنید:"""
    
    await update.callback_query.edit_message_text(
        message, 
        reply_markup=reply_markup, 
        parse_mode='Markdown'
    )
