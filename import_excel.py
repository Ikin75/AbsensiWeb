import pandas as pd
import sqlite3
from datetime import datetime

# 1. Baca file Excel
file_path = 'riwayat_absensi_2026-08-19.xlsx'
df = pd.read_excel(file_path)
df.columns = ['tanggal', 'id_karyawan', 'nama', 'jenis', 'lokasi']

# 2. Konversi tanggal DD-MM-YYYY ke format ISO YYYY-MM-DD HH:MM:SS
df['created_at'] = pd.to_datetime(df['tanggal'], format='%d-%m-%Y %H:%M:%S')

# 3. Siapkan kolom lat dan lng (Excel gak ada, kita isi 0)
df['lat'] = 0.0
df['lng'] = 0.0

# 4. Ambil kolom yang sesuai dengan tabel backend
df_final = df[['id_karyawan', 'nama', 'jenis', 'lat', 'lng', 'lokasi', 'created_at']]

# 5. Koneksi ke database yang sama
conn = sqlite3.connect('absensi.db')
cursor = conn.cursor()

# Pastikan tabel absensi ada (kalau belum)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS absensi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_karyawan TEXT,
        nama TEXT,
        jenis TEXT,
        lat REAL,
        lng REAL,
        lokasi TEXT,
        created_at TIMESTAMP
    )
''')

# 6. Masukkan data (if_exists='append' karena tabel udah ada)
df_final.to_sql('absensi', conn, if_exists='append', index=False)

# 7. Tutup
conn.close()
print(f"✅ Berhasil import {len(df_final)} baris data dari Excel ke absensi.db")