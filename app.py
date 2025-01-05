from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from otp import codeotp, sendotp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rahasia'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/TAMK/backup/TINYPROJECT/database.db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Mengatur halaman login default

# Model database untuk pengguna
class Pengguna(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    otp = db.Column(db.String(6), nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return Pengguna.query.get(int(user_id))

# Halaman utama
@app.route('/')
def index():
    return render_template('index.html')

# Halaman register
from otp import codeotp, sendotp
from flask import flash

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']
        password = request.form['password']

        # Validasi input
        if not nama or not email or not password:
            flash('Semua field harus diisi.', 'danger')
            return redirect(url_for('register'))

        if Pengguna.query.filter_by(email=email).first():
            flash('Email sudah terdaftar.', 'danger')
            return redirect(url_for('register'))

        # Menyimpan pengguna baru ke database
        pengguna_baru = Pengguna(nama=nama, email=email, password=password)
        db.session.add(pengguna_baru)
        db.session.commit()

        # Menghasilkan dan mengirim OTP
        otp_code = codeotp()
        pengguna_baru.otp = otp_code  # Simpan OTP di database
        db.session.commit()

        try:
            sendotp(email, otp_code)  # Kirim OTP ke email pengguna
            flash('Registrasi berhasil! OTP telah dikirim ke email Anda.', 'success')
        except Exception as e:
            flash(f'Gagal mengirim OTP: {e}', 'danger')

        session['email'] = email
        return redirect(url_for('login'))
    return render_template('register.html')


# Halaman login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        pengguna = Pengguna.query.filter_by(email=email).first()

        if pengguna and pengguna.password == password:
            login_user(pengguna)
            session['email'] = email  # Simpan email ke session
            flash('Login berhasil.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email atau password salah.', 'danger')
    return render_template('login.html')

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()  # Hapus session
    flash('Logout berhasil.', 'success')
    return redirect(url_for('index'))

# Halaman dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Mengirim OTP
@app.route('/kirim-otp', methods=['POST'])
def kirim_otp():
    email = session.get('email')  # Ambil email dari session
    if not email:
        flash('Silakan login untuk mengirim OTP.', 'danger')
        return redirect(url_for('login'))

    pengguna = Pengguna.query.filter_by(email=email).first()
    if pengguna:
        otp = codeotp()  # Menghasilkan OTP
        pengguna.otp = otp
        db.session.commit()

        sendotp(otp)  # Kirim OTP ke email
        flash('OTP telah dikirim ke email Anda.', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Pengguna tidak ditemukan.', 'danger')
        return redirect(url_for('index'))

# Verifikasi OTP
@app.route('/verifikasi-otp', methods=['GET', 'POST'])
@login_required
def verifikasi_otp():
    if request.method == 'POST':
        email = session.get('email')
        otp = request.form['otp']
        pengguna = Pengguna.query.filter_by(email=email).first()

        if pengguna and pengguna.otp == otp:
            pengguna.otp = None  # Reset OTP setelah verifikasi
            db.session.commit()
            flash('Verifikasi OTP berhasil!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('OTP salah atau tidak valid.', 'danger')
            return redirect(url_for('verifikasi_otp'))
    return render_template('verifikasi_otp.html')

if __name__ == '__main__':
    with app.app_context():  # Memastikan konteks aplikasi aktif
        db.create_all()      # Membuat tabel di database
    app.run(debug=True)
