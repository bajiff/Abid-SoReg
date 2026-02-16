from db_config import get_db_connection
from werkzeug.security import generate_password_hash

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Tabel Users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        )
    ''')

    # 2. Tabel Sound Systems
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sound_systems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_paket TEXT NOT NULL,
            daya_watt INTEGER NOT NULL,
            harga_sewa INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'tersedia',
            deskripsi TEXT
        )
    ''')

    # 3. Tabel Bookings
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            sound_id INTEGER NOT NULL,
            tanggal_sewa TEXT NOT NULL,
            status_booking TEXT DEFAULT 'pending',
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (sound_id) REFERENCES sound_systems (id)
        )
    ''')

    # --- Seeding Data Awal ---
    
    # Cek apakah admin sudah ada
    admin_exist = cursor.execute('SELECT * FROM users WHERE username = ?', ('admin',)).fetchone()
    if not admin_exist:
        # Buat Admin Default (Password: admin123)
        pw_hash = generate_password_hash('admin123')
        cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', 
                       ('admin', pw_hash, 'admin'))
        print("Admin user created.")

    # Cek data sound system
    sound_exist = cursor.execute('SELECT count(*) FROM sound_systems').fetchone()[0]
    if sound_exist == 0:
        sound_data = [
            ('Paket Karnaval Brewog', 50000, 15000000, 'tersedia', 'Paket full horeg untuk karnaval, 24 Subwoofer.'),
            ('Paket Hajatan Standard', 5000, 2500000, 'tersedia', 'Cocok untuk nikahan rumahan.'),
            ('Paket Battle Sound', 30000, 10000000, 'tersedia', 'Spesifikasi tinggi untuk adu balap sound.')
        ]
        cursor.executemany('INSERT INTO sound_systems (nama_paket, daya_watt, harga_sewa, status, deskripsi) VALUES (?, ?, ?, ?, ?)', sound_data)
        print("Dummy sound systems added.")

    conn.commit()
    conn.close()
    print("Database Abid SoReg initialized successfully!")

if __name__ == '__main__':
    init_db()