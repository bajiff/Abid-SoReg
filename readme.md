![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Framework-Flask-green?style=for-the-badge&logo=flask)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey?style=for-the-badge&logo=sqlite)
![TailwindCSS](https://img.shields.io/badge/Frontend-TailwindCSS-38B2AC?style=for-the-badge&logo=tailwind-css)

**Abid SoReg** adalah aplikasi berbasis web yang dibangun untuk memanajemen penyewaan *Sound System Horeg* (Sound system skala besar untuk karnaval, hajatan, atau *battle sound*). Aplikasi ini mendigitalisasi proses booking yang biasanya manual menjadi terpusat, transparan, dan efisien.

---

## 🚀 Fitur Utama

### 🔐 Autentikasi & Keamanan
- **Secure Login:** Menggunakan *hashing password* (PBKDF2) untuk keamanan data pengguna.
- **Role-Based:** Pemisahan dashboard antara **Admin** dan **User**.
- **Session Management:** Proteksi halaman menggunakan session login.

### 👤 User (Pelanggan)
- **Katalog Sound:** Melihat daftar paket sound lengkap dengan spesifikasi (Watt) dan harga.
- **Booking Online:** Memilih tanggal sewa dan melihat estimasi biaya.
- **Status Monitoring:** Memantau status booking (Pending ⏳, Disetujui ✅, Ditolak ❌).

### 🛠 Admin (Pengelola)
- **Dashboard Statistik:** Ringkasan unit tersedia dan booking masuk.
- **Manajemen Inventaris (CRUD):** Tambah, Edit, Hapus data paket sound system.
- **Approval System:** Menyetujui atau menolak pesanan masuk dengan satu klik.
- **Manajemen Status Alat:** Mengubah status unit (Tersedia/Disewa/Maintenance).

---

## 📂 Struktur Project

```text
/Abid-SoReg
│
├── app.py              # Main Logic (Flask Routes & Controllers)
├── db_config.py        # Konfigurasi koneksi Database SQLite
├── setup_db.py         # Script inisialisasi tabel (Basic)
├── seeder.py           # Script Reset & Seeding Data Dummy (Advanced)
│
└── templates/          # Folder Frontend (HTML + Tailwind via CDN)
    ├── base.html       # Layout utama (Navbar & Flash Messages)
    ├── login.html
    ├── register.html
    ├── admin_dashboard.html
    ├── user_dashboard.html
    ├── booking.html
    └── edit_sound.html
```


### 💻 Cara Menjalankan di LocalhostIkuti langkah berikut untuk menjalankan aplikasi di komputer Anda:

1. Clone Repository 
``` text
git clone https://github.com/username-anda/abid-soreg.git
cd abid-soreg
```
2. Buat Virtual Environment (Disarankan menggunakan Python 3.12)
# Windows
``` bash
python -m venv venv
venv\Scripts\activate
```

# Mac/Linux
```bash

python3.12 -m venv venv
source venv/bin/activate
```
Install Dependencies
```bash
pip install flask werkzeug
```
Setup Database Jalankan script seeder.py untuk membuat database dan mengisi data awal otomatis.

``` bash
python seeder.py
```

```bash 
Output: ✅ SEEDING SELESAI!
Database 'abid_soreg.db' siap digunakan.
```

Jalankan Aplikasi python app.py
```bash
Buka browser dan akses: http://127.0.0.1:5000
```


🗄️ Skema Database

a. Tabel users
Menyimpan data otentikasi pengguna.

```text
Kolom,Tipe Data,Keterangan
id,INTEGER,"Primary Key, Auto Increment"
username,TEXT,"Unique, Not Null"
password,TEXT,Hashed Password (Security)
role,TEXT,"Enum ('admin', 'user')"
```

b. Tabel sound_systems
Menyimpan inventaris paket sound system.
```text
Kolom,Tipe Data,Keterangan
id,INTEGER,"Primary Key, Auto Increment"
nama_paket,TEXT,Nama perangkat/paket
daya_watt,INTEGER,Spesifikasi daya
harga_sewa,INTEGER,Harga per hari
status,TEXT,Status ketersediaan
deskripsi,TEXT,Detail spesifikasi
```

c. Tabel bookings
Tabel transaksi yang menghubungkan User dan Sound System.
```text
Kolom,Tipe Data,Keterangan
id,INTEGER,"Primary Key, Auto Increment"
user_id,INTEGER,Foreign Key -> users(id)
sound_id,INTEGER,Foreign Key -> sound_systems(id)
tanggal_sewa,TEXT,Format ISO YYYY-MM-DD
status_booking,TEXT,"Default 'pending', 'approved', 'rejected'"

```

🔑 Akun Demo (Default Seeder)
Gunakan akun berikut untuk pengujian aplikasi setelah menjalankan seeder.py
```text
Role,Username,Password
Admin,admin,admin123
User,mas_rusdi,rusdi123
User,mas_amba,amba123
```


🌐 Deployment
Aplikasi ini dirancang WSGI-friendly dan telah berhasil diuji deployment pada PythonAnywhere.

Teknologi:
- Backend: Python 3.12 + Flask
- Database: SQLite (Native)
- Frontend: HTML5 + Tailwind CSS
- Hosting: PythonAnywhere


👨‍💻 Developer
Baji Ajalah Pemula Coding

<i>Tugas Akhir Basis Data Lanjut</i>