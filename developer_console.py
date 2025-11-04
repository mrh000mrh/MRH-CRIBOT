# developer_console.py
"""
🎮 DEVELOPER CONSOLE - MRH CRIBOT
🔐 PASSWORD PROTECTED MENU EDITING
⚡ FOR @mrh000mrh ONLY
"""

from developer_authorization import DeveloperAuthorization
from menu_lock import MenuLock

class DeveloperConsole:
    """
    کنسول توسعه‌دهنده برای مدیریت منوها با رمز
    """
    
    @staticmethod
    def process_developer_command(command):
        """
        پردازش دستورات توسعه‌دهنده
        """
        command = command.strip().lower()
        
        # تشخیص دستور باز کردن منو
        if "من میخواهم منوی" in command and "کلمه رمز" in command:
            return DeveloperConsole._handle_unlock_command(command)
        
        # تشخیص دستور تایید نهایی
        elif "تایید نهایی" in command or "تایید میکنم" in command:
            return DeveloperConsole._handle_confirmation_command(command)
        
        # تشخیص دستور لغو
        elif "لغو" in command or "cancel" in command:
            return DeveloperConsole._handle_cancel_command(command)
        
        # وضعیت
        elif "وضعیت" in command or "status" in command:
            return DeveloperConsole._handle_status_command()
        
        else:
            return "❌ دستور نامعتبر. فرمت صحیح:\n" + \
                   "«من میخواهم منوی [نام منو] را تغییر دهم کلمه رمز: mrh»"
    
    @staticmethod
    def _handle_unlock_command(command):
        """پردازش دستور باز کردن منو"""
        try:
            # استخراج نام منو و رمز از دستور
            parts = command.split("منوی")[1].split("را تغییر دهم کلمه رمز:")
            menu_name = parts[0].strip()
            password = parts[1].strip()
            
            # باز کردن منو
            success, message = DeveloperAuthorization.unlock_menu_for_editing(menu_name, password)
            
            if success:
                # نمایش اطلاعات منوی باز شده
                menu_data = MenuLock.LOCKED_MENUS.get(menu_name, {})
                current_text = menu_data.get('text', '')[:100] + "..." if len(menu_data.get('text', '')) > 100 else menu_data.get('text', '')
                current_buttons = menu_data.get('buttons', [])
                
                response = f"{message}\n\n"
                response += f"📋 **منوی فعلی:**\n"
                response += f"📝 متن: {current_text}\n"
                response += f"🔘 دکمه‌ها: {len(current_buttons)} عدد\n\n"
                response += "💡 **دستورات موجود:**\n"
                response += "• «تایید نهایی» - اعمال تغییرات و قفل\n"
                response += "• «لغو تغییرات» - بازگردانی و قفل\n"
                response += "• «وضعیت» - نمایش منوهای باز\n"
                
                return response
            else:
                return message
                
        except Exception as e:
            return f"❌ خطا در پردازش دستور: {e}"
    
    @staticmethod
    def _handle_confirmation_command(command):
        """پردازش دستور تایید نهایی"""
        unlocked_menus = DeveloperAuthorization.get_unlocked_menus_status()
        
        if not unlocked_menus:
            return "❌ هیچ منوی بازی برای تایید وجود ندارد!"
        
        response = "✅ **تایید نهایی تغییرات:**\n\n"
        
        for menu_status in unlocked_menus:
            menu_name = menu_status['menu']
            success, message = DeveloperAuthorization.apply_menu_changes(
                menu_name, 
                final_confirmation=True
            )
            response += f"🎯 {menu_name}: {message}\n"
        
        return response
    
    @staticmethod
    def _handle_cancel_command(command):
        """پردازش دستور لغو"""
        unlocked_menus = DeveloperAuthorization.get_unlocked_menus_status()
        
        if not unlocked_menus:
            return "❌ هیچ منوی بازی برای لغو وجود ندارد!"
        
        response = "❌ **لغو تغییرات:**\n\n"
        
        for menu_status in unlocked_menus:
            menu_name = menu_status['menu']
            success, message = DeveloperAuthorization.cancel_changes(menu_name)
            response += f"🎯 {menu_name}: {message}\n"
        
        return response
    
    @staticmethod
    def _handle_status_command():
        """پردازش دستور وضعیت"""
        unlocked_menus = DeveloperAuthorization.get_unlocked_menus_status()
        
        if not unlocked_menus:
            return "🔒 همه منوها قفل هستند"
        
        response = "🔓 **منوهای باز شده:**\n\n"
        
        for menu_status in unlocked_menus:
            response += f"🎯 {menu_status['menu']}\n"
            response += f"⏰ زمان باقیمانده: {menu_status['remaining_minutes']} دقیقه\n"
            response += f"📊 وضعیت: آماده برای ویرایش\n\n"
        
        response += "💡 برای تایید: «تایید نهایی»\n"
        response += "💡 برای لغو: «لغو تغییرات»"
        
        return response

# 🎯 تابع اصلی برای استفاده در ربات
def handle_developer_input(user_input, user_id):
    """
    مدیریت ورودی توسعه‌دهنده در ربات
    """
    # بررسی اینکه کاربر توسعه‌دهنده است (بر اساس آیدی)
    from config import ADMINS
    if user_id not in ADMINS:
        return "❌ دسترسی denied!"
    
    return DeveloperConsole.process_developer_command(user_input)
