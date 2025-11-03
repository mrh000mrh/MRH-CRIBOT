# =============================================
# 🚀 MRH-CRIBOT - Database Models
# 👤 Developer: Mohammad Reza Hossein Khani
# 🗄️ Complete Database Structure
# =============================================

from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Float, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime, timedelta
from config import CONFIG

Base = declarative_base()

class User(Base):
    """مدل کاربران - اطلاعات اصلی کاربران"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False, index=True)
    username = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    language = Column(String(10), default='fa')
    phone_number = Column(String(20))
    
    # وضعیت حساب
    balance = Column(Float, default=0.0)
    total_deposits = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    is_banned = Column(Boolean, default=False)
    
    # تنظیمات ربات
    agreed_terms = Column(Boolean, default=False)
    notification_enabled = Column(Boolean, default=True)
    
    # سرویس‌های فعال
    vpn_active = Column(Boolean, default=False)
    signals_active = Column(Boolean, default=False)
    subscription_end = Column(DateTime)
    
    # اطلاعات زمانی
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    last_activity = Column(DateTime, default=datetime.now)
    
    # روابط
    payments = relationship("Payment", back_populates="user")
    vpn_subscriptions = relationship("VPNSubscription", back_populates="user")
    crypto_signals = relationship("UserSignal", back_populates="user")
    referrals = relationship("Referral", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

class Payment(Base):
    """مدل پرداخت‌ها - تراکنش‌های مالی"""
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    
    # اطلاعات پرداخت
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default='IRT')
    payment_method = Column(String(50))
    network = Column(String(20))
    
    # وضعیت پرداخت
    status = Column(String(20), default='pending')
    description = Column(String(200))
    invoice_id = Column(String(100), unique=True)
    
    # اطلاعات تراکنش
    tx_hash = Column(String(200))
    wallet_address = Column(String(200))
    
    # زمان‌ها
    created_at = Column(DateTime, default=datetime.now)
    completed_at = Column(DateTime)
    
    # رابطه
    user = relationship("User", back_populates="payments")
    
    def __repr__(self):
        return f"<Payment(id={self.id}, amount={self.amount}, status='{self.status}')>"

class VPNSubscription(Base):
    """مدل اشتراک‌های VPN"""
    __tablename__ = 'vpn_subscriptions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    
    # اطلاعات پلن
    plan_type = Column(String(20))
    plan_name = Column(String(100))
    duration_days = Column(Integer)
    
    # اطلاعات پرداخت
    amount_paid = Column(Float)
    payment_id = Column(Integer, ForeignKey('payments.id'))
    
    # وضعیت اشتراک
    is_active = Column(Boolean, default=True)
    start_date = Column(DateTime, default=datetime.now)
    expiry_date = Column(DateTime)
    
    # اطلاعات فنی
    config_file_url = Column(String(500))
    server_details = Column(JSON)
    
    # رابطه
    user = relationship("User", back_populates="vpn_subscriptions")
    
    def __repr__(self):
        return f"<VPNSubscription(id={self.id}, plan='{self.plan_type}', active={self.is_active})>"

class CryptoSignal(Base):
    """مدل سیگنال‌های کریپتو"""
    __tablename__ = 'crypto_signals'
    
    id = Column(Integer, primary_key=True)
    
    # اطلاعات سیگنال
    pair = Column(String(20), nullable=False)
    signal_type = Column(String(20))
    direction = Column(String(10))
    
    # قیمت‌ها
    current_price = Column(Float)
    entry_range_min = Column(Float)
    entry_range_max = Column(Float)
    targets = Column(JSON)
    stop_loss = Column(Float)
    
    # تنظیمات معامله
    leverage = Column(String(20))
    risk_level = Column(String(20))
    position_size = Column(String(20))
    
    # تحلیل تکنیکال
    technical_analysis = Column(Text)
    confidence_level = Column(Integer)
    
    # وضعیت سیگنال
    status = Column(String(20), default='active')
    priority = Column(String(20), default='normal')
    
    # زمان‌ها
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    expiry_time = Column(DateTime)
    
    def __repr__(self):
        return f"<CryptoSignal(id={self.id}, pair='{self.pair}', type='{self.signal_type}')>"

class UserSignal(Base):
    """مدل ارتباط کاربران با سیگنال‌ها"""
    __tablename__ = 'user_signals'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    signal_id = Column(Integer, ForeignKey('crypto_signals.id'), nullable=False)
    
    # وضعیت سیگنال برای کاربر
    status = Column(String(20), default='active')
    entry_price = Column(Float)
    exit_price = Column(Float)
    pnl_percentage = Column(Float)
    
    # زمان‌ها
    received_at = Column(DateTime, default=datetime.now)
    executed_at = Column(DateTime)
    closed_at = Column(DateTime)
    
    # رابطه
    user = relationship("User", back_populates="crypto_signals")
    signal = relationship("CryptoSignal")
    
    def __repr__(self):
        return f"<UserSignal(user_id={self.user_id}, signal_id={self.signal_id})>"

class Referral(Base):
    """مدل سیستم زیرمجموعه‌گیری"""
    __tablename__ = 'referrals'
    
    id = Column(Integer, primary_key=True)
    referrer_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    referred_user_id = Column(Integer, unique=True, nullable=False)
    
    # اطلاعات کمیسیون
    commission_rate = Column(Float, default=0.1)
    commission_amount = Column(Float, default=0.0)
    total_earnings = Column(Float, default=0.0)
    
    # وضعیت
    status = Column(String(20), default='active')
    level = Column(Integer, default=1)
    
    # زمان
    created_at = Column(DateTime, default=datetime.now)
    
    # رابطه
    user = relationship("User", back_populates="referrals")
    
    def __repr__(self):
        return f"<Referral(referrer={self.referrer_id}, referred={self.referred_user_id})>"

class BotSettings(Base):
    """مدل تنظیمات ربات"""
    __tablename__ = 'bot_settings'
    
    id = Column(Integer, primary_key=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text)
    value_type = Column(String(20), default='string')
    description = Column(String(200))
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f"<BotSettings(key='{self.key}', value='{self.value}')>"

# ایجاد انجین و session
engine = create_engine(CONFIG.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """ایجاد جداول دیتابیس"""
    Base.metadata.create_all(bind=engine)
    print("✅ پایگاه داده MRH-CRIBOT راه‌اندازی شد")

def get_db():
    """دریافت session دیتابیس"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_or_create_user(db, user_id, username=None, first_name=None, last_name=None):
    """دریافت یا ایجاد کاربر جدید"""
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        user = User(
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"✅ کاربر جدید ایجاد شد: {user_id} - {username}")
    return user
