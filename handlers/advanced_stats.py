# handlers/advanced_stats.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def advanced_statistics_charts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمودارهای آماری پیشرفته"""
    
    keyboard = [
        [InlineKeyboardButton("📊 نمودار فروش روزانه", callback_data="admin_daily_sales_chart")],
        [InlineKeyboardButton("📈 نمودار رشد کاربران", callback_data="admin_user_growth_chart")],
        [InlineKeyboardButton("💰 نمودار درآمد", callback_data="admin_income_chart")],
        [InlineKeyboardButton("🛍️ نمودار محصولات پرفروش", callback_data="admin_top_products_chart")],
        [InlineKeyboardButton("👥 نمودار کاربران فعال", callback_data="admin_active_users_chart")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="super_admin_panel")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = """📈 **نمودارهای آماری پیشرفته**

📊 **انواع نمودارهای قابل نمایش:**
- 📊 **فروش روزانه** - روند فروش در زمان
- 📈 **رشد کاربران** - نمودار ثبت‌نام‌ها
- 💰 **درآمد** - نمودار سود و زیان
- 🛍️ **محصولات پرفروش** - مقایسه محصولات
- 👥 **کاربران فعال** - فعالیت کاربران

📅 **بازه‌های زمانی:**
- روزانه
- هفتگی  
- ماهانه
- سالانه

لطفاً نوع نمودار مورد نظر را انتخاب کنید:"""
    
    await update.callback_query.edit_message_text(
        message, 
        reply_markup=reply_markup, 
        parse_mode='Markdown'
    )
