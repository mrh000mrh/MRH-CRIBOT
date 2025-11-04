# 🤖 AI ASSISTANT GUIDE - MRH CRIBOT
# 🔒 PROTECTED BUT EXTENDABLE PROJECT

## 🎯 **NEW: CONTROLLED EXTENSION SYSTEM**

### **🚫 WHAT AI CANNOT DO:**
- ❌ Modify LOCKED_MENUS directly
- ❌ Change existing menu texts
- ❌ Remove existing buttons
- ❌ Alter callback patterns

### **✅ WHAT AI CAN DO (With Permission):**
- ✅ Add NEW features to EXTENDABLE_SECTIONS
- ✅ Create NEW sub-menus (not main menus)
- ✅ Add NEW buttons to extendable areas
- ✅ Suggest improvements (developer must approve)

## 🔧 **HOW TO ADD NEW FEATURES:**

### **Method 1: Using AI Extension System**
```python
from menu_lock import MenuLock

# درخواست اضافه کردن ویژگی جدید
success = MenuLock.ai_add_feature(
    section_name='account_features',
    new_button_text='🔄 ویژگی جدید',
    new_callback_data='new_feature',
    ai_notes='اضافه کردن قابلیت جدید به حساب کاربری'
)
