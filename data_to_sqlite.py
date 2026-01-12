import pandas as pd
import sqlite3

# Baca data dari Excel
df = pd.read_excel('data.xlsx')

# Buat database SQLite
conn = sqlite3.connect('produk.db')

# Simpan ke database
df.to_sql('produk', conn, if_exists='replace', index=False)

conn.close()
print("Konversi berhasil! File produk.db telah dibuat.")