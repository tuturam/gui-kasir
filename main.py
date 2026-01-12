import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

class SistemKasir:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Sistem Kasir Sederhana - Python Tkinter")
        # self.root.geometry("600x500")

        # --- 1. DATA PRODUK (Baca dari Excel) ---
        # Format: {'PLU': {'nama': 'Nama Produk', 'harga': Harga}}
        self.data_produk = self.load_produk_dari_excel()
        
        # Variabel untuk menyimpan total belanja
        self.total_belanja = 0

        # --- 2. GUI LAYOUT ---
        
        # Judul
        label_judul = tk.Label(root, text="KASIR RESTORAN KITA", font=("Arial", 16, "bold"))
        label_judul.pack(pady=10)

        # Frame Input
        frame_input = tk.Frame(root)
        frame_input.pack(pady=5)

        # Dropdown Pilih Produk
        tk.Label(frame_input, text="Pilih Produk:").grid(row=0, column=0, padx=5)
        # Format tampilan: "Plu - Nama Barang"
        produk_display = [f"{plu} - {info['nama']}" for plu, info in self.data_produk.items()]
        self.combo_produk = ttk.Combobox(frame_input, values=produk_display, width=30, validate="focus")
        self.combo_produk.grid(row=0, column=1, padx=5)
        self.combo_produk.current(0) # Pilih item pertama secara default

        # Input Jumlah
        tk.Label(frame_input, text="Jumlah:").grid(row=0, column=2, padx=5)
        self.entry_jumlah = tk.Entry(frame_input, width=5)
        self.entry_jumlah.grid(row=0, column=3, padx=5)
        self.entry_jumlah.insert(0, "1") # Default jumlah 1

        # Tombol Tambah
        btn_tambah = tk.Button(frame_input, text="Tambah", command=self.tambah_barang, bg="#4CAF50", fg="white")
        btn_tambah.grid(row=0, column=4, padx=10)

        # Tabel Keranjang Belanja (Treeview)
        # Columns: Nama, Harga Satuan, Jumlah, Subtotal
        self.tree = ttk.Treeview(root, columns=("Nama", "Harga", "Jumlah", "Subtotal"), show='headings', height=10)
        self.tree.heading("Nama", text="Nama Produk")
        self.tree.heading("Harga", text="Harga")
        self.tree.heading("Jumlah", text="Qty")
        self.tree.heading("Subtotal", text="Subtotal")
        
        self.tree.column("Nama", width=200)
        self.tree.column("Harga", width=100)
        self.tree.column("Jumlah", width=50)
        self.tree.column("Subtotal", width=100)
        self.tree.pack(pady=10)

        # Frame Pembayaran
        frame_bawah = tk.Frame(root)
        frame_bawah.pack(fill='x', padx=20)

        # Label Total
        self.label_total = tk.Label(frame_bawah, text="Total: Rp 0", font=("Arial", 14, "bold"))
        self.label_total.pack(anchor='e')

        # Input Uang Bayar
        frame_bayar = tk.Frame(root)
        frame_bayar.pack(pady=10)
        
        tk.Label(frame_bayar, text="Uang Bayar:").grid(row=0, column=0, padx=5)
        self.entry_bayar = tk.Entry(frame_bayar)
        self.entry_bayar.grid(row=0, column=1, padx=5)

        btn_bayar = tk.Button(frame_bayar, text="Proses Bayar", command=self.proses_bayar, bg="#2196F3", fg="white")
        btn_bayar.grid(row=0, column=2, padx=10)

        btn_reset = tk.Button(frame_bayar, text="Reset", command=self.reset_transaksi, bg="#f44336", fg="white")
        btn_reset.grid(row=0, column=3, padx=10)

    # --- 3. LOGIKA PROGRAM ---

    def load_produk_dari_excel(self):
        """Membaca data produk dari file Excel"""
        try:
            df = pd.read_excel('data.xlsx')
            # Kolom: 'Plu', 'Nama Barang', 'Harga'
            produk_dict = {}
            for _, row in df.iterrows():
                plu = str(row['Plu'])
                produk_dict[plu] = {
                    'nama': row['Nama Barang'],
                    'harga': row['Harga']
                }
            return produk_dict
        except (Exception, FileNotFoundError) as e:
            messagebox.showerror("Error", f"Gagal membaca file Excel: {str(e)}\nMenggunakan data default.")
            # Data default jika ada error
            return {
                "001": {"nama": "Nasi Goreng", "harga": 15000},
                "002": {"nama": "Mie Ayam", "harga": 12000},
                "003": {"nama": "Es Teh Manis", "harga": 5000},
                "004": {"nama": "Kopi Hitam", "harga": 8000},
                "005": {"nama": "Air Mineral", "harga": 4000}
            }

    def tambah_barang(self):
        # Ambil pilihan user (format: "PLU - Nama Barang")
        produk_terpilih = self.combo_produk.get()
        
        # Extract PLU dari string (ambil bagian sebelum " - ")
        plu = produk_terpilih.split(" - ")[0]

        if plu not in self.data_produk:
            messagebox.showerror("Error", "Produk tidak ditemukan! \nPencarian hanya berdasarkan PLU (Product Lookup Unit).")
            return
        
        try:
            jumlah = int(self.entry_jumlah.get())
            if jumlah <= 0:
                messagebox.showwarning("Peringatan", "Jumlah harus lebih dari 0")
                return
        except ValueError:
            messagebox.showerror("Error", "Jumlah harus berupa angka")
            return

        # Ambil data produk berdasarkan PLU
        nama = self.data_produk[plu]['nama']
        harga = self.data_produk[plu]['harga']
        subtotal = harga * jumlah

        # Masukkan ke tabel (Treeview) / hanya update jika sudah ada
        if self.tree.get_children():
            for item in self.tree.get_children():
                item_data = self.tree.item(item)['values']
                if item_data[0] == nama:
                    # Update jumlah dan subtotal
                    new_jumlah = item_data[2] + jumlah
                    new_subtotal = item_data[1] * new_jumlah
                    self.tree.item(item, values=(nama, harga, new_jumlah, new_subtotal))
                    break
        else:
            # Jika produk belum ada di tabel, tambahkan baru
            self.tree.insert("", "end", values=(nama, harga, jumlah, subtotal))

        # Update Total Belanja
        self.total_belanja += subtotal
        self.label_total.config(text=f"Total: Rp {self.total_belanja:,}")

    def proses_bayar(self):
        try:
            uang_bayar = int(self.entry_bayar.get())
            if uang_bayar < self.total_belanja:
                messagebox.showwarning("Kurang Bayar", "Uang yang dibayarkan kurang!")
            else:
                kembalian = uang_bayar - self.total_belanja
                messagebox.showinfo("Sukses", f"Transaksi Berhasil!\nKembalian: Rp {kembalian:,}")
                self.reset_transaksi()
        except ValueError:
            messagebox.showerror("Error", "Masukkan nominal uang yang valid")

    def reset_transaksi(self):
        # Hapus semua item di tabel
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Reset variabel
        self.total_belanja = 0
        self.label_total.config(text="Total: Rp 0")
        self.entry_bayar.delete(0, 'end')
        self.entry_jumlah.delete(0, 'end')
        self.entry_jumlah.insert(0, "1")

# Menjalankan Program
if __name__ == "__main__":
    root = tk.Tk()
    app = SistemKasir(root)
    root.mainloop()