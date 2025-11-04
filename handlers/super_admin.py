# handlers/super_admin.py
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import ADMINS, ADMIN_LEVELS, VIP_CHANNEL_TYPES, VPN_CONFIGS
from database import db

async def super_admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پنل مدیریت حرفه ای سوپر ادمین"""
    user_id = update.effective_user.id
    
    if user_id not in ADMINS or ADMIN_LEVELS.get(user_id) != "super_admin":
        await update.callback_query.answer("❌ دسترسی denied!", show_alert=True)
        return
    
    keyboard = [
        [InlineKeyboardButton("📝 مدیریت منوها", callback_data="admin_manage_menus")],
        [InlineKeyboardButton("🛍️ مدیریت محصولات (VPN)", callback_data="admin_manage_products")],
        [InlineKeyboardButton("📡 مدیریت کانال‌ها", callback_data="admin_manage_channels")],
        [InlineKeyboardButton("👥 مدیریت کاربران", callback_data="admin_manage_users")],
        [InlineKeyboardButton("📋 سیستم پشتیبانی هوشمند", callback_data="smart_support")],
        [InlineKeyboardButton("🎫 سیستم تخفیف و کوپن", callback_data="coupon_management")],
        [InlineKeyboardButton("📢 اطلاع‌رسانی هوشمند", callback_data="smart_notification")],
        [InlineKeyboardButton("🔔 نوتیفیکیشن هوشمند", callback_data="smart_alerts")],
        [InlineKeyboardButton("📈 نمودارهای آماری", callback_data="advanced_stats")],
        [InlineKeyboardButton("⚙️ تنظیمات ربات", callback_data="admin_bot_settings")],
        [InlineKeyboardButton("🔐 مدیریت ادمین‌ها", callback_data="admin_manage_admins")],
        [InlineKeyboardButton("🔙 بازگشت به پنل مدیریت", callback_data="admin_panel")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = """👑 **پنل مدیریت حرفه ای**

🔧 **امکانات در دسترس:**

• 📝 **مدیریت منوها** - ویرایش تمام متن‌ها و دکمه‌ها
• 🛍️ **مدیریت محصولات** - افزودن/حذف/ویرایش پلن‌های VPN
• 📡 **مدیریت کانال‌ها** - افزودن/حذف کانال‌های سیگنال
• 👥 **مدیریت کاربران** - مشاهده و مدیریت کاربران
• 📋 **پشتیبانی هوشمند** - سیستم FAQ و پشتیبانی AI
• 🎫 **تخفیف و کوپن** - مدیریت کدهای تخفیف
• 📢 **اطلاع‌رسانی** - ارسال پیام به کاربران
• 🔔 **نوتیفیکیشن** - اعلان‌های هوشمند
• 📈 **نمودارهای آماری** - گزارشات پیشرفته
• ⚙️ **تنظیمات ربات** - تغییر تنظیمات اصلی
• 🔐 **مدیریت ادمین‌ها** - افزودن/حذف ادمین

لطفاً گزینه مورد نظر را انتخاب کنید:"""
    
    await update.callback_query.edit_message_text(
        message, 
        reply_markup=reply_markup, 
        parse_mode='Markdown'
    )

async def manage_menus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت منوها و متن‌ها"""
    keyboard = [
        [InlineKeyboardButton("✏️ ویرایش متن استارت", callback_data="admin_edit_start_text")],
        [InlineKeyboardButton("🔄 ویرایش منوی اصلی", callback_data="admin_edit_main_menu")],
        [InlineKeyboardButton("📋 ویرایش شرایط و قوانین", callback_data="admin_edit_disclaimer")],
        [InlineKeyboardButton("🎯 ویرایش منوی VIP", callback_data="admin_edit_vip_menu")],
        [InlineKeyboardButton("👤 ویرایش منوی حساب کاربری", callback_data="admin_edit_account_menu")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="super_admin_panel")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.callback_query.edit_message_text(
        "📝 **مدیریت منوها و متن‌ها**\n\nلطفاً بخش مورد نظر برای ویرایش را انتخاب کنید:",
        reply_markup=reply_markup
    )

async def manage_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت محصولات (پلن‌های VPN)"""
    
    keyboard = []
    
    # نمایش پلن‌های موجود
    for plan_id, plan_info in VPN_CONFIGS.items():
        keyboard.append([
            InlineKeyboardButton(
                f"✏️ {plan_info['name']}", 
                callback_data=f"admin_edit_plan_{plan_id}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton("➕ افزودن پلن جدید", callback_data="admin_add_new_plan")])
    keyboard.append([InlineKeyboardButton("🗑️ حذف پلن", callback_data="admin_delete_plan")])
    keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data="super_admin_panel")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = """🛍️ **مدیریت محصولات (VPN)**

📦 **پلن‌های موجود:**
"""
    
    for plan_id, plan_info in VPN_CONFIGS.items():
        message += f"• {plan_info['name']} - {plan_info['price']:,} تومان - {plan_info['duration']} روز\n"
    
    await update.callback_query.edit_message_text(
        message, 
        reply_markup=reply_markup, 
        parse_mode='Markdown'
    )

async def manage_channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت کانال‌های سیگنال"""
    
    keyboard = []
    
    for channel_id, channel_info in VIP_CHANNEL_TYPES.items():
        keyboard.append([
            InlineKeyboardButton(
                f"✏️ {channel_info['name']}", 
                callback_data=f"admin_edit_channel_{channel_id}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton("➕ افزودن کانال جدید", callback_data="admin_add_channel")])
    keyboard.append([InlineKeyboardButton("🗑️ حذف کانال", callback_data="admin_delete_channel")])
    keyboard.append([InlineKeyboardButton("🔙 بازگشت", callback_data="super_admin_panel")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = """📡 **مدیریت کانال‌های سیگنال**

🎯 **کانال‌های موجود:**
"""
    
    for channel_id, channel_info in VIP_CHANNEL_TYPES.items():
        message += f"• {channel_info['name']} - {channel_info['description']}\n"
    
    await update.callback_query.edit_message_text(
        message, 
        reply_markup=reply_markup, 
        parse_mode='Markdown'
    )

async def manage_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت پیشرفته کاربران"""
    keyboard = [
        [InlineKeyboardButton("📊 مشاهده تمام کاربران", callback_data="admin_view_all_users")],
        [InlineKeyboardButton("🔍 جستجوی کاربر", callback_data="admin_search_user")],
        [InlineKeyboardButton("✅ فعال‌سازی دسترسی", callback_data="admin_activate_access")],
        [InlineKeyboardButton("❌ مسدود کردن کاربر", callback_data="admin_ban_user")],
        [InlineKeyboardButton("💰 مدیریت موجودی کاربران", callback_data="admin_manage_balance")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="super_admin_panel")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.callback_query.edit_message_text(
        "👥 **مدیریت پیشرفته کاربران**\n\nلطفاً عمل مورد نظر را انتخاب کنید:",
        reply_markup=reply_markup
    )

async def bot_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تنظیمات ربات"""
    keyboard = [
        [InlineKeyboardButton("🏪 فعال/غیرفعال کردن ربات", callback_data="admin_toggle_bot")],
        [InlineKeyboardButton("💬 تنظیم متن پیام‌ها", callback_data="admin_set_messages")],
        [InlineKeyboardButton("🎫 تنظیم سیستم کوپن", callback_data="admin_coupon_settings")],
        [InlineKeyboardButton("👥 تنظیم سیستم دعوت", callback_data="admin_referral_settings")],
        [InlineKeyboardButton("🔧 تنظیمات پرداخت", callback_data="admin_payment_settings")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="super_admin_panel")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.callback_query.edit_message_text(
        "⚙️ **تنظیمات ربات**\n\nلطفاً بخش مورد نظر را انتخاب کنید:",
        reply_markup=reply_markup
    )

async def stats_and_reports(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """آمار و گزارشات پیشرفته"""
    stats = db.get_user_stats()
    
    keyboard = [
        [InlineKeyboardButton("📈 آمار مالی", callback_data="admin_financial_stats")],
        [InlineKeyboardButton("👥 آمار کاربران", callback_data="admin_user_stats")],
        [InlineKeyboardButton("🛍️ آمار فروش", callback_data="admin_sales_stats")],
        [InlineKeyboardButton("📋 گزارش روزانه", callback_data="admin_daily_report")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="super_admin_panel")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = f"""📊 **آمار و گزارشات**

📈 **آمار کلی ربات:**
• 👥 کل کاربران: {stats['total_users']} نفر
• 🔥 کاربران فعال: {stats['active_users']} نفر
• 🛍️ تعداد فروش: {stats['total_sales']} عدد
• 💰 درآمد کل: {stats['total_income']:,} تومان

لطفاً نوع گزارش مورد نظر را انتخاب کنید:"""
    
    await update.callback_query.edit_message_text(
        message, 
        reply_markup=reply_markup, 
        parse_mode='Markdown'
    )

async def manage_admins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت ادمین‌ها"""
    
    keyboard = [
        [InlineKeyboardButton("➕ افزودن ادمین جدید", callback_data="admin_add_admin")],
        [InlineKeyboardButton("🗑️ حذف ادمین", callback_data="admin_remove_admin")],
        [InlineKeyboardButton("📊 تغییر سطح دسترسی", callback_data="admin_change_level")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="super_admin_panel")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = "🔐 **مدیریت ادمین‌ها**\n\n**ادمین‌های فعلی:**\n"
    
    for admin_id in ADMINS:
        level = ADMIN_LEVELS.get(admin_id, "user")
        level_name = "سوپر ادمین" if level == "super_admin" else "پشتیبان"
        message += f"• آیدی: `{admin_id}` - سطح: {level_name}\n"
    
    await update.callback_query.edit_message_text(
        message, 
        reply_markup=reply_markup, 
        parse_mode='Markdown'
    )
