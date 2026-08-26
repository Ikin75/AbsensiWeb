from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Biar frontend boleh akses dari browser

DB_FILE = 'absensi.db'

# ========== INISIALISASI DATABASE ==========
def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        # Tabel karyawan (sesuai ID kamu)
        c.execute('''CREATE TABLE IF NOT EXISTS karyawan (
            id_karyawan TEXT PRIMARY KEY,
            nama TEXT,
            no_wa TEXT
        )''')
        # Tabel absensi
        c.execute('''CREATE TABLE IF NOT EXISTS absensi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_karyawan TEXT,
            nama TEXT,
            jenis TEXT,
            lat REAL,
            lng REAL,
            lokasi TEXT,
            created_at TIMESTAMP
        )''')
        # Contoh data karyawan (sesuaikan dengan data excel kamu ya)
        c.execute("INSERT OR IGNORE INTO karyawan VALUES ('MK001', 'dr. Hasniah Harun, MKK', '628123456789')")
        c.execute("INSERT OR IGNORE INTO karyawan VALUES ('MK008', 'Faqih', '628987654321')")
        # ... tambahin yang lain
        conn.commit()
        conn.close()
        print("✅ Database siap!")

init_db()

# ========== API ENDPOINT ==========
@app.route('/api/karyawan', methods=['GET'])
def get_karyawan():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id_karyawan, nama, no_wa FROM karyawan")
    rows = c.fetchall()
    conn.close()
    return jsonify([{"id_karyawan": r[0], "nama": r[1], "no_wa": r[2]} for r in rows])

@app.route('/api/absensi', methods=['GET'])
def get_absensi():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id_karyawan, nama, jenis, lat, lng, lokasi, created_at FROM absensi ORDER BY created_at ASC")
    rows = c.fetchall()
    conn.close()
    return jsonify([{
        "id_karyawan": r[0], "nama": r[1], "jenis": r[2],
        "lat": r[3], "lng": r[4], "lokasi": r[5], "created_at": r[6]
    } for r in rows])

@app.route('/api/absensi', methods=['POST'])
def post_absensi():
    data = request.json
    id_karyawan = data.get('id_karyawan')
    nama = data.get('nama')
    jenis = data.get('jenis')
    lat = data.get('lat')
    lng = data.get('lng')
    lokasi = data.get('lokasi')
    now = datetime.now().isoformat()  # ISO format untuk SQLite

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO absensi (id_karyawan, nama, jenis, lat, lng, lokasi, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (id_karyawan, nama, jenis, lat, lng, lokasi, now))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "created_at": now})

if __name__ == '__main__':
    app.run(debug=True, port=5000)