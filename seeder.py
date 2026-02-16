import sqlite3
from werkzeug.security import generate_password_hash
from db_config import get_db_connection
from datetime import datetime, timedelta

def seed_database():
    print("🔄 Memulai proses seeding database...")
    
    conn = get_db_connection()
    cursor = conn.cursor()

    # --- 1. RESET DATABASE (DROP & RECREATE) ---
    # Kita hapus tabel lama biar bersih dan tidak duplikat
    print("🗑️  Menghapus tabel lama...")
    cursor.execute("DROP TABLE IF EXISTS bookings")
    cursor.execute("DROP TABLE IF EXISTS sound_systems")
    cursor.execute("DROP TABLE IF EXISTS users")

    # Buat ulang tabel (Sama seperti setup_db.py tapi disatukan disini)
    print("🏗️  Membuat struktur tabel baru...")
    
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        )
    ''')

    cursor.execute('''
        CREATE TABLE sound_systems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_paket TEXT NOT NULL,
            daya_watt INTEGER NOT NULL,
            harga_sewa INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'tersedia',
            deskripsi TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            sound_id INTEGER NOT NULL,
            tanggal_sewa TEXT NOT NULL,
            status_booking TEXT DEFAULT 'pending',
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (sound_id) REFERENCES sound_systems (id)
        )
    ''')

    # --- 2. SEED USERS ---
    print("👤 Menambahkan data user...")
    
    users = [
        ('admin', 'admin123', 'admin'),       # Super Admin
        ('meki', 'meki123', 'admin'),       # Super Admin
        ('jeki', 'jeki123', 'admin'),       # Super Admin
        ('bobob', 'bobob123', 'admin'),       # Super Admin
        ('mas_amba', 'amba123', 'user'),      # User Biasa 1
        ('mas_rusdi', 'rusdi123', 'user'),    # User Biasa 2
        ('juragan_lele', 'lele123', 'user')   # User Biasa 3
    ]

    for username, password, role in users:
        hashed_pw = generate_password_hash(password)
        cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', 
                       (username, hashed_pw, role))

    # --- 3. SEED SOUND SYSTEMS (HOREG EDITION) ---
    print("🔊 Menambahkan paket sound horeg...")

    sounds = [
        ('Brewog Audio - Paket Karnaval', 80000, 25000000, 'tersedia', 
         'Spesifikasi Dewa: 24 Subwoofer Double, Genset 150kVA, Lighting Full Set. Siap meruntuhkan genteng tetangga.'),
        
        ('Riswanda Audio - Paket Hajatan Sultan', 40000, 12000000, 'tersedia', 
         'Spesialis Clarity & Jedug. Cocok untuk resepsi mewah. Bonus Operator berpengalaman.'),
        
        ('Aeromax Production - Battle Spec', 60000, 18000000, 'disewa', 
         'Setingan balap sound. SPL tinggi, bass nendang di dada. Hati-hati kaca pecah.'),
        
        ('HRJ Audio - Paket Hemat', 10000, 3500000, 'tersedia', 
         'Cukup untuk acara syukuran sunatan atau 17 Agustusan tingkat RT. Suara bersih.'),
         
        ('Faskho Sengox - Full Rig', 55000, 16500000, 'tersedia', 
         'Legendary sound system. Bass gler, mid lantang. Include truk transport.')
    ]

    cursor.executemany('''
        INSERT INTO sound_systems (nama_paket, daya_watt, harga_sewa, status, deskripsi) 
        VALUES (?, ?, ?, ?, ?)
    ''', sounds)

    # --- 4. SEED BOOKINGS (DUMMY DATA) ---
    print("📅 Menambahkan riwayat booking dummy...")

    # Ambil ID user dan sound dulu biar valid
    # (Asumsi ID urut karena baru direset: Admin=1, Amba=2, Rusdi=3, Lele=4)
    # (Sound: Brewog=1, Riswanda=2, Aeromax=3, HRJ=4, Faskho=5)

    today = datetime.now()
    besok = today + timedelta(days=1)
    minggu_depan = today + timedelta(days=7)

    bookings = [
        # User Mas Amba booking Brewog (Pending)
        (2, 1, minggu_depan.strftime('%Y-%m-%d'), 'pending'),
        
        # User Mas Rusdi booking Aeromax (Approved/Disewa)
        (3, 3, today.strftime('%Y-%m-%d'), 'approved'),
        
        # Juragan Lele booking HRJ (Selesai/History)
        (4, 4, '2023-12-01', 'finished')
    ]

    cursor.executemany('''
        INSERT INTO bookings (user_id, sound_id, tanggal_sewa, status_booking) 
        VALUES (?, ?, ?, ?)
    ''', bookings)

    conn.commit()
    conn.close()
    print("✅ SEEDING SELESAI! Database 'abid_soreg.db' siap digunakan.")
    print("🔑 Login Admin: username='admin', password='admin123'")

if __name__ == '__main__':
    seed_database()