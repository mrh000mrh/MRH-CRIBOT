# handlers/disclaimer.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import db

async def show_disclaimer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش شرایط و قوانین برای کاربران جدید"""
    
    disclaimer_text = """
📜 **شرایط و قوانین استفاده از ربات**

🔸 **سلب مسئولیت (Disclaimer):**
- کلیه سیگنال‌های ارائه شده صرفاً تحلیل تیم فنی می‌باشد
- مسئولیت سود و زیان حاصل از معاملات بر عهده خود کاربر است
- ربات هیچ گونه تضمینی برای سودآوری سیگنال‌ها نمی‌دهد

🔸 **قوانین استفاده:**
- کاربر موظف است نام کاربری (Username) تلگرام خود را تنظیم کند
- هرگونه سوء استفاده از ربات منجر به مسدودی حساب می‌شود
- فروش یا انتقال حساب به دیگران ممنوع است

🔸 **هشدار ریسک:**
- بازارهای مالی دارای ریسک بالا هستند
- تنها با سرمایه مازاد معامله کنید
- از مدیریت سرمایه صحیح استفاده نمایید

✅ با کلیک روی دکمه "موافقم"، تمامی شرایط فوق را می‌پذیرید.
"""
    
    keyboard = [
        [InlineKeyboardButton("✅ موافقم", callback_data="accept_disclaimer")],
        [InlineKeyboardButton("❌ خروج", callback_data="exit_bot")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        disclaimer_text, 
        reply_markup=reply_markup, 
        parse_mode='Markdown'
    )

async def handle_disclaimer_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت پاسخ کاربر به شرایط و قوانین"""
    query = update.callback_query
    user = query.from_user
    
    if query.data == "accept_disclaimer":
        # بررسی وجود یوزرنیم
        if not user.username:
            await query.edit_message_text(
                "❌ **خطا: نام کاربری تنظیم نشده**\n\n"
                "برای استفاده از ربات باید نام کاربری (Username) تلگرام خود را تنظیم کنید.\n\n"
                "📝 **روش تنظیم نام کاربری:**\n"
                "1. به Settings تلگرام بروید\n"
                "2. روی Edit کلیک کنید\n"
                "3. Username را تنظیم کنید\n"
                "4. سپس دوباره از ربات استارت کنید",
                parse_mode='Markdown'
            )
            return
        
        # کاربر شرایط را پذیرفته و یوزرنیم دارد
        db.accept_disclaimer(user.id)
        context.user_data['disclaimer_accepted'] = True
        
        await query.edit_message_text(
            "✅ **شرایط و قوانین پذیرفته شد**\n\n"
            "اکنون می‌توانید از امکانات ربات استفاده کنید.",
            parse_mode='Markdown'
        )
        
        # انتقال کاربر به منوی اصلی
        from handlers.start import start_handler
        await start_handler(update, context)
        
    elif query.data == "exit_bot":
        await query.edit_message_text(
            "❌ **شرایط و قوانین پذیرفته نشد**\n\n"
            "متأسفانه بدون پذیرش شرایط نمی‌توانید از ربات استفاده کنید.",
            parse_mode='Markdown'
        )
