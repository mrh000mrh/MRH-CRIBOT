# handlers/callback.py
from telegram import Update
from telegram.ext import ContextTypes

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت کلیک روی تمام دکمه‌ها"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    # هندلرهای منوی اصلی
    if data == "vip_channels":
        from handlers.vip_channels import show_vip_channels_menu
        await show_vip_channels_menu(update, context)
        
    elif data == "buy_config":
        from handlers.vip_channels import show_vip_access_methods
        await show_vip_access_methods(update, context, "general")
        
    elif data == "my_account":
        from handlers.account import show_account_menu
        await show_account_menu(update, context)
        
    elif data == "support":
        from handlers.smart_support import smart_support_system
        await smart_support_system(update, context)
        
    elif data == "help":
        from handlers.start import start_handler
        await start_handler(update, context)
        
    elif data == "admin_panel":
        from handlers.admin_manager import show_admin_panel
        await show_admin_panel(update, context)
        
    # هندلرهای کانال‌های VIP
    elif data.startswith("vip_"):
        channel_type = data.replace("vip_", "")
        from handlers.vip_channels import show_vip_access_methods
        await show_vip_access_methods(update, context, channel_type)
        
    elif data.startswith("channel_"):
        channel_type = data.replace("channel_", "")
        from handlers.vip_channels import handle_vip_access
        await handle_vip_access(update, context, channel_type)
        
    # هندلرهای مدیریت
    elif data == "super_admin_panel":
        from handlers.super_admin import super_admin_panel
        await super_admin_panel(update, context)
        
    elif data == "smart_support":
        from handlers.smart_support import smart_support_system
        await smart_support_system(update, context)
        
    elif data == "coupon_management":
        from handlers.coupon_system import coupon_management_system
        await coupon_management_system(update, context)
        
    elif data == "smart_notification":
        from handlers.notification_system import smart_notification_system
        await smart_notification_system(update, context)
        
    elif data == "smart_alerts":
        from handlers.smart_alerts import smart_notification_alerts
        await smart_notification_alerts(update, context)
        
    elif data == "advanced_stats":
        from handlers.advanced_stats import advanced_statistics_charts
        await advanced_statistics_charts(update, context)
        
    # هندلر بازگشت به منوی اصلی
    elif data == "main_menu":
        from handlers.start import start_handler
        if query.message:
            await query.delete_message()
        await start_handler(update, context)
        
    else:
        await query.edit_message_text(
            "⚠️ این قابلیت به زودی اضافه خواهد شد!",
            parse_mode='Markdown'
        )
