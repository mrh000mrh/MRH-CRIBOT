# handlers/smart_support.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def smart_support_system(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """سیستم پشتیبانی هوشمند با هوش مصنوعی و سوالات متداول"""
    
    keyboard = [
        [InlineKeyboardButton("🤖 پشتیبانی هوشمند", callback_data="ai_support")],
        [InlineKeyboardButton("❓ سوالات متداول", callback_data="faq_support")],
        [InlineKeyboardButton("👨‍💼 پشتیبانی انسانی", callback_data="human_support")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="super_admin_panel")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = """📋 **سیستم پشتیبانی هوشمند**

🤖 **پشتیبانی هوشمند (AI):**
- پاسخگویی خودکار به سوالات کاربران
- یادگیری از سوالات پرتکرار
- پاسخ‌دهی 24 ساعته

❓ **سوالات متداول (FAQ):**
- مدیریت سوالات و پاسخ‌ها
- دسته‌بندی موضوعات
- جستجوی هوشمند

👨‍💼 **پشتیبانی انسانی:**
- ارسال تیکت به ادمین
- پاسخگویی توسط پشتیبان

لطفاً نوع پشتیبانی را انتخاب کنید:"""
    
    await update.callback_query.edit_message_text(
        message, 
        reply_markup=reply_markup, 
        parse_mode='Markdown'
    )

async def manage_faq_system(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت سوالات متداول"""
    keyboard = [
        [InlineKeyboardButton("➕ افزودن سوال جدید", callback_data="admin_add_faq")],
        [InlineKeyboardButton("✏️ ویرایش سوالات", callback_data="admin_edit_faq")],
        [InlineKeyboardButton("🗑️ حذف سوال", callback_data="admin_delete_faq")],
        [InlineKeyboardButton("📁 مدیریت دسته‌بندی‌ها", callback_data="admin_manage_faq_categories")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="smart_support")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.callback_query.edit_message_text(
        "❓ **مدیریت سوالات متداول (FAQ)**\n\nلطفاً عمل مورد نظر را انتخاب کنید:",
        reply_markup=reply_markup
    )
