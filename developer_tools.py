# developer_tools.py
"""
🔧 DEVELOPER TOOLS - MRH CRIBOT
🔓 TOOLS FOR CONTROLLED MENU MODIFICATIONS
⚡ ONLY FOR @mrh000mrh
"""

from menu_lock import MenuLock

class DeveloperTools:
    """
    ابزارهای مخصوص توسعه‌دهنده برای مدیریت منوها
    """
    
    @staticmethod
    def show_current_menus():
        """نمایش منوهای فعلی"""
        print("📋 منوهای فعلی:")
        for menu_name, menu_data in MenuLock.LOCKED_MENUS.items():
            print(f"\n🎯 {menu_name}:")
            print(f"📝 متن: {menu_data['text'][:50]}...")
            print(f"🔘 دکمه‌ها: {len(menu_data['buttons'])} عدد")
    
    @staticmethod
    def modify_main_menu(new_buttons=None, new_text=None):
        """
        تغییر منوی اصلی (فقط توسعه‌دهنده)
        """
        changes = {}
        if new_text:
            changes['new_text'] = new_text
        if new_buttons:
            changes['new_buttons'] = new_buttons
        
        return MenuLock.developer_modify_menu('main_menu', **changes)
    
    @staticmethod
    def add_new_menu(menu_name, menu_text, menu_buttons):
        """
        اضافه کردن منوی جدید
        """
        if menu_name in MenuLock.LOCKED_MENUS:
            print(f"⚠️ منوی {menu_name} از قبل وجود دارد!")
            return False
        
        MenuLock.LOCKED_MENUS[menu_name] = {
            'text': menu_text,
            'buttons': menu_buttons,
            'developer_notes': "اضافه شده توسط توسعه‌دهنده"
        }
        print(f"✅ منوی جدید {menu_name} اضافه شد")
        return True
    
    @staticmethod
    def remove_menu(menu_name):
        """
        حذف منوی موجود
        """
        if menu_name not in MenuLock.LOCKED_MENUS:
            print(f"❌ منوی {menu_name} وجود ندارد!")
            return False
        
        if menu_name in ['main_menu', 'vip_channels']:
            print(f"🚫 حذف منوی {menu_name} مجاز نیست!")
            return False
        
        del MenuLock.LOCKED_MENUS[menu_name]
        print(f"✅ منوی {menu_name} حذف شد")
        return True

# 🔓 دستورات سریع برای توسعه‌دهنده
def dev_add_button(menu_name, button_text, callback_data):
    """اضافه کردن دکمه جدید به منو"""
    current_buttons = MenuLock.LOCKED_MENUS[menu_name]['buttons']
    current_buttons.append([button_text, callback_data])
    print(f"✅ دکمه {button_text} به {menu_name} اضافه شد")

def dev_remove_button(menu_name, button_text):
    """حذف دکمه از منو"""
    current_buttons = MenuLock.LOCKED_MENUS[menu_name]['buttons']
    MenuLock.LOCKED_MENUS[menu_name]['buttons'] = [
        btn for btn in current_buttons if btn[0] != button_text
    ]
    print(f"✅ دکمه {button_text} از {menu_name} حذف شد")
