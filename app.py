import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime, timedelta
import telebot
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wtf-hostel-ultra-premium-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/hostel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- پیکربندی تلگرام ---
BOT_TOKEN = "8702709953:AAEy6xPvd-WhuhatRY7fmzMsDT7qMchXnFQ22"
ADMIN_CHAT_ID = "220668411" 
bot = telebot.TeleBot(BOT_TOKEN)

# --- مدل‌های دیتابیس (ساختار اطلاعات) ---

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    price_per_night = db.Column(db.Float, default=0.0)
    bookings = db.relationship('Booking', backref='room', lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    bed_number = db.Column(db.Integer, nullable=False)
    stay_days = db.Column(db.Integer, nullable=False)
    total_paid = db.Column(db.Float, nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_expiry_date(self):
        return self.created_at + timedelta(days=self.stay_days)

    def days_remaining(self):
        delta = self.get_expiry_date() - datetime.utcnow()
        return max(0, delta.days)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50)) # نظافت، قبض، تعمیرات
    date = db.Column(db.DateTime, default=datetime.utcnow)

# --- مدیریت لاگین ---
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- وظایف خودکار تلگرام ---
def telegram_auto_report():
    with app.app_context():
        rooms = Room.query.all()
        bookings = Booking.query.all()
        total_beds = sum([r.capacity for r in rooms])
        occupied = len(bookings)
        
        msg = f"🏨 *گزارش وضعیت WTF HOSTEL*\n"
        msg += f"────────────────\n"
        msg += f"✅ تخت‌های خالی: {total_beds - occupied}\n"
        msg += f"🚫 تخت‌های پر: {occupied}\n\n"
        
        expiring_soon = [b for b in bookings if b.days_remaining() <= 1]
        if expiring_soon:
            msg += "🚨 *هشدار تمدید یا تخلیه:*\n"
            for b in expiring_soon:
                msg += f"👤 {b.customer_name} | {b.room.name} (تخت {b.bed_number})\n"
        
        try:
            bot.send_message(ADMIN_CHAT_ID, msg, parse_mode="Markdown")
        except Exception as e:
            print(f"Telegram Error: {e}")

scheduler = BackgroundScheduler()
scheduler.add_job(func=telegram_auto_report, trigger="cron", hour=10) # هر روز ساعت ۱۰ صبح
scheduler.start()

# --- مسیرها (Routes) ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('خطا در ورود!')
    return render_template('login.html')

@app.route('/')
@login_required
def dashboard():
    rooms = Room.query.all()
    bookings = Booking.query.all()
    expenses = Expense.query.all()
    
    # محاسبات آماری
    income = sum([b.total_paid for b in bookings])
    costs = sum([e.amount for e in expenses])
    total_beds = sum([r.capacity for r in rooms])
    
    return render_template('dashboard.html', 
                           rooms=rooms, bookings=bookings, expenses=expenses,
                           full=len(bookings), empty=total_beds - len(bookings),
                           income=income, costs=costs)

@app.route('/add_booking', methods=['POST'])
@login_required
def add_booking():
    new_b = Booking(
        customer_name=request.form['name'],
        room_id=request.form['room_id'],
        bed_number=request.form['bed_num'],
        stay_days=int(request.form['days']),
        total_paid=float(request.form['price']),
        phone=request.form.get('phone')
    )
    db.session.add(new_b)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/delete_booking/<int:id>')
@login_required
def delete_booking(id):
    b = Booking.query.get(id)
    db.session.delete(b)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/add_expense', methods=['POST'])
@login_required
def add_expense():
    new_e = Expense(
        title=request.form['title'],
        amount=float(request.form['amount']),
        category=request.form.get('category')
    )
    db.session.add(new_e)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- مقداردهی اولیه ---
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        db.session.add(User(username='admin', password='123'))
        # ساخت ۴ اتاق طبق سناریوی شما
        db.session.add_all([
            Room(name="اتاق شماره ۱", capacity=3),
            Room(name="اتاق شماره ۲", capacity=3),
            Room(name="اتاق شماره ۳", capacity=6),
            Room(name="اتاق شماره ۴", capacity=9)
        ])
        db.session.commit()

if __name__ == '__main__':
    app.run()