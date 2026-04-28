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
    stay_days = db.Column(db.Integer)
    phone = db.Column(db.String(20))
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # فیلدهای اضافه شده طبق درخواست شما
    total_amount = db.Column(db.Float, default=0.0)  # مبلغ کل
    amount_paid = db.Column(db.Float, default=0.0)   # مبلغ پرداخت شده

    def end_date(self):
        return self.start_date + timedelta(days=self.stay_days)

    def debt_amount(self):
        """محاسبه بدهکاری"""
        debt = self.total_amount - self.amount_paid
        return debt if debt > 0 else 0

    def days_left(self):
        remaining = (self.end_date() - datetime.utcnow()).days
        return max(0, remaining)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100))
    category = db.Column(db.String(50))
    cost = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.utcnow)


# --- Login ---
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# --- Telegram Report ---
def send_daily_report():
    if not bot:
        return

    with app.app_context():
        rooms = Room.query.all()
        bookings = Booking.query.all()

        total_beds = sum(r.capacity for r in rooms)
        occupied = len(bookings)

        msg = "🏨 گزارش روزانه هاستل\n\n"
        msg += f"📊 اشغال: {occupied}/{total_beds}\n"
        msg += f"📈 نرخ اشغال: {(occupied/total_beds)*100:.1f}%\n\n"

        expiring = [b for b in bookings if b.days_left() <= 1]
        if expiring:
            msg += "🚨 در حال اتمام:\n"
            for b in expiring:
                msg += f"- {b.customer_name} ({b.room.name})\n"

        try:
            bot.send_message(ADMIN_CHAT_ID, msg)
        except:
            pass


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
        flash("❌ اطلاعات اشتباه است")
    return render_template('login.html')

@app.route('/')
@login_required
def dashboard():
    rooms = Room.query.all()
    bookings = Booking.query.all()
    expenses = Expense.query.all()

    total_income = sum(b.amount_paid for b in bookings)
    total_expenses = sum(e.cost for e in expenses)
    profit = total_income - total_expenses

    total_capacity = sum(r.capacity for r in rooms)
    occupancy = len(bookings)

    return render_template(
        'dashboard.html',
        rooms=rooms,
        bookings=bookings,
        income=total_income,
        costs=total_expenses,
        profit=profit,
        occupancy=occupancy,
        capacity=total_capacity,
        rate=(occupancy/total_capacity*100) if total_capacity else 0
    )


@app.route('/add_customer', methods=['POST'])
@login_required
def add_customer():
    room = Room.query.get(request.form['room_id'])
    current = Booking.query.filter_by(room_id=room.id).count()

    if current >= room.capacity:
        flash("❌ ظرفیت اتاق پر است")
        return redirect(url_for('dashboard'))

    # دریافت مقادیر جدید از فرم
    booking = Booking(
        customer_name=request.form['name'],
        room_id=room.id,
        bed_number=request.form['bed_num'],
        stay_days=int(request.form['days']),
        total_amount=float(request.form['total_price']), # مبلغ کل
        amount_paid=float(request.form['paid_price']),   # مبلغ پرداخت شده
        phone=request.form.get('phone', '')
    )

    db.session.add(booking)
    db.session.commit()
    return redirect(url_for('dashboard'))


@app.route('/checkout/<int:id>')
@login_required
def checkout(id):
    booking = Booking.query.get_or_404(id)
    db.session.delete(booking)
    db.session.commit()
    flash("✔ تخلیه انجام شد")
    return redirect(url_for('dashboard'))


@app.route('/add_expense', methods=['POST'])
@login_required
def add_expense():
    db.session.add(Expense(
        item_name=request.form['item'],
        category=request.form.get('category', 'سایر'),
        cost=float(request.form['cost'])
    ))
    db.session.commit()
    return redirect(url_for('dashboard'))


@app.route('/api/stats')
@login_required
def api_stats():
    bookings = Booking.query.all()
    expenses = Expense.query.all()
    return jsonify({
        "income": sum(b.amount_paid for b in bookings),
        "expenses": sum(e.cost for e in expenses),
        "bookings": len(bookings)
    })


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# --- Init DB ---
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            password=generate_password_hash('123')
        )
        db.session.add(admin)
        db.session.add_all([
            Room(name="اتاق ۱", capacity=3, room_type="VIP"),
            Room(name="اتاق ۲", capacity=3, room_type="استاندارد"),
            Room(name="اتاق ۳", capacity=6, room_type="عمومی"),
            Room(name="اتاق ۴", capacity=9, room_type="اقتصادی")
        ])
        db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
