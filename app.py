from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from twilio.rest import Client
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rahasia'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/syafiq efendi/Desktop/TINY PROJECT/database.db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)

# Konfigurasi Twilio
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
client = Client(account_sid, auth_token)

class Pengguna(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    otp = db.Column(db.String(6), nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return Pengguna.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']
        password = request.form['password']
        pengguna_baru = Pengguna(nama=nama, email=email, password=password)
        db.session.add(pengguna_baru)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        pengguna = Pengguna.query.filter_by(email=email).first()
        if pengguna and pengguna.password == password:
            login_user(pengguna)
            return redirect(url_for('dashboard'))
        else:
            return 'Email atau password salah'
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/kirim-otp', methods=['POST'])
def kirim_otp():
    email = request.form['email']
    pengguna = Pengguna.query.filter_by(email=email).first()
    if pengguna:
        otp = str(random.randint(100000, 999999))
        pengguna.otp = otp
        db.session.commit()
        message = client.messages.create(
            body=f'Kode OTP Anda: {otp}',
            from_='your_twilio_number',
            to=pengguna.email
        )
        return 'OTP dikirim'
    else:
        return 'Email tidak ditemukan'

@app.route('/verifikasi-otp', methods=['POST'])
def verifikasi_otp():
    email = request.form['email']
    otp = request.form['otp']
    pengguna = Pengguna.query.filter_by(email=email).first()
    if pengguna and pengguna.otp == otp:
        return 'OTP benar'
    else:
        return 'OTP salah'

if __name__ == '__main__':
    with app.app_context():  # Memastikan konteks aplikasi aktif
        db.create_all()      # Membuat tabel di database
    app.run(debug=True)

