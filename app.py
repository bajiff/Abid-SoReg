from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db_config import get_db_connection
from functools import wraps

app = Flask(__name__)
app.secret_key = 'kunci_rahasia_horeg_123' # Ganti dengan random string yang kuat

# --- Decorators ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Silakan login terlebih dahulu.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':
            flash('Akses ditolak. Halaman ini khusus Admin.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# --- Routes Auth ---
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_pw = generate_password_hash(password)
        
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_pw))
            conn.commit()
            flash('Registrasi berhasil! Silakan login.', 'success')
            return redirect(url_for('login'))
        except:
            flash('Username sudah digunakan.', 'error')
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('dashboard'))
        else:
            flash('Username atau password salah.', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- Dashboard Router ---
@app.route('/dashboard')
@login_required
def dashboard():
    if session['role'] == 'admin':
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('user_dashboard'))

# --- User Area ---
@app.route('/user/dashboard')
@login_required
def user_dashboard():
    conn = get_db_connection()
    sounds = conn.execute('SELECT * FROM sound_systems WHERE status = "tersedia"').fetchall()
    
    # Ambil history booking user ini
    my_bookings = conn.execute('''
        SELECT b.*, s.nama_paket 
        FROM bookings b 
        JOIN sound_systems s ON b.sound_id = s.id 
        WHERE b.user_id = ? 
        ORDER BY b.id DESC
    ''', (session['user_id'],)).fetchall()
    
    conn.close()
    return render_template('user_dashboard.html', sounds=sounds, bookings=my_bookings)

@app.route('/book/<int:sound_id>', methods=['GET', 'POST'])
@login_required
def book_sound(sound_id):
    conn = get_db_connection()
    if request.method == 'POST':
        tanggal = request.form['tanggal_sewa']
        conn.execute('INSERT INTO bookings (user_id, sound_id, tanggal_sewa) VALUES (?, ?, ?)',
                     (session['user_id'], sound_id, tanggal))
        conn.commit()
        conn.close()
        flash('Booking berhasil dibuat! Tunggu konfirmasi admin.', 'success')
        return redirect(url_for('user_dashboard'))
    
    sound = conn.execute('SELECT * FROM sound_systems WHERE id = ?', (sound_id,)).fetchone()
    conn.close()
    return render_template('booking.html', sound=sound)

# --- Admin Area ---
@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    conn = get_db_connection()
    sounds = conn.execute('SELECT * FROM sound_systems').fetchall()
    
    # Join 3 tabel untuk info lengkap booking
    bookings = conn.execute('''
        SELECT b.id, u.username, s.nama_paket, b.tanggal_sewa, b.status_booking 
        FROM bookings b
        JOIN users u ON b.user_id = u.id
        JOIN sound_systems s ON b.sound_id = s.id
        ORDER BY b.id DESC
    ''').fetchall()
    conn.close()
    return render_template('admin_dashboard.html', sounds=sounds, bookings=bookings)

@app.route('/admin/add_sound', methods=['POST'])
@login_required
@admin_required
def add_sound():
    nama = request.form['nama_paket']
    watt = request.form['daya_watt']
    harga = request.form['harga_sewa']
    desc = request.form['deskripsi']
    
    conn = get_db_connection()
    conn.execute('INSERT INTO sound_systems (nama_paket, daya_watt, harga_sewa, deskripsi) VALUES (?, ?, ?, ?)',
                 (nama, watt, harga, desc))
    conn.commit()
    conn.close()
    flash('Paket sound berhasil ditambahkan.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_sound/<int:id>')
@login_required
@admin_required
def delete_sound(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM sound_systems WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Paket dihapus.', 'success')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)