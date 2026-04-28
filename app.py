import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from datetime import datetime, timedelta
import telebot
from apscheduler.schedulers.background import BackgroundScheduler
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "change-this-secret")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/hostel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- تلگرام ---
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID", "")
bot = telebot.TeleBot(BOT_TOKEN) if BOT_TOKEN else None

# --- مدل‌ها ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(20), default="admin")

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    capacity = db.Column(db.Integer)
    room_type = db.Column(db.String(20), default="استاندارد")
    bookings = db.relationship('Booking', backref='room', lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    bed_number = db.Column(db.Integer)
    phone = db.Column(db.String(20))
    
    # فیلدهای جدید برای کنترل تاریخ و مبالغ
    stay_type = db.Column(db.String(20)) # "daily" یا "monthly"
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date_val = db.Column(db.DateTime)
    
    total_amount = db.Column(db.Float, default=0.0) # مبلغ کل (محاسبه شده)
    amount_paid = db.Column(db.Float, default=0.0)  # پرداختی فعلی

    def get_end_date(self):
        return self.end_date_val

    def debt_amount(self):
        """محاسبه بدهی"""
        debt = self.total_amount - self.amount_paid
        return max(0.0, debt)

    def days_left(self):
        if not self.end_date_val: return 0
        remaining = (self.end_date_val - datetime.utcnow()).days
        return max(0, remaining)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100))
    category = db.Column(db.String(50))
    cost = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.utcnow)

# --- مدیریت ورود ---
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- گزارش تلگرام ---
def send_daily_report():
    if not bot: return
    with app.app_context():
        bookings = Booking.query.all()
        total_debt = sum(b.debt_amount() for b in bookings)
        msg = f"🏨 گزارش هاستل\n💰 کل طلب از مشتریان: {total_debt:,.0f}"
        try: bot.send_message(ADMIN_CHAT_ID, msg)
        except: pass

scheduler = BackgroundScheduler()
scheduler.add_job(send_daily_report, 'cron', hour=9)
scheduler.start()

# --- Routes ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash("❌ خطا در ورود")
    return render_template('login.html')

@app.route('/')
@login_required
def dashboard():
    rooms = Room.query.all()
    bookings = Booking.query.all()
    expenses = Expense.query.all()
    
    total_income = sum(b.amount_paid for b in bookings)
    total_costs = sum(e.cost for e in expenses)
    
    return render_template(
        'dashboard.html',
        rooms=rooms,
        bookings=bookings,
        income=total_income,
        costs=total_costs,
        profit=total_income - total_costs,
        occupancy=len(bookings),
        capacity=sum(r.capacity for r in rooms)
    )

@app.route('/add_customer', methods=['POST'])
@login_required
def add_customer():
    room = Room.query.get(request.form['room_id'])
    
    stay_type = request.form.get('stay_type') # روزانه یا ماهانه
    unit_price = float(request.form['unit_price']) # قیمت هر روز یا هر ماه
    units = int(request.form['units']) # تعداد روز یا تعداد ماه
    paid = float(request.form['paid']) # مبلغی که الان پرداخت کرد
    
    start = datetime.utcnow()
    # محاسبه تاریخ خروج و مبلغ کل بر اساس نوع انتخاب شده
    if stay_type == 'daily':
        end = start + timedelta(days=units)
        total = unit_price * units
    else: # ماهانه (فرض هر ماه ۳۰ روز)
        end = start + timedelta(days=units * 30)
        total = unit_price * units

    new_booking = Booking(
        customer_name=request.form['name'],
        room_id=room.id,
        bed_number=request.form['bed_num'],
        phone=request.form.get('phone', ''),
        stay_type=stay_type,
        start_date=start,
        end_date_val=end,
        total_amount=total,
        amount_paid=paid
    )

    db.session.add(new_booking)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/checkout/<int:id>')
@login_required
def checkout(id):
    booking = Booking.query.get_or_404(id)
    db.session.delete(booking)
    db.session.commit()
    flash("✔ تخلیه شد")
    return redirect(url_for('dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- Init ---
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        db.session.add(User(username='admin', password=generate_password_hash('123')))
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
