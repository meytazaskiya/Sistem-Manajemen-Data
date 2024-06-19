import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import csv

class Kontak:
    def __init__(self, nama, telepon, email):
        self.nama = nama
        self.telepon = telepon
        self.email = email

class ManajerKontak:
    def __init__(self):
        self.kontak_list = []

    def tambah_kontak(self, kontak):
        self.kontak_list.append(kontak)

    def lihat_kontak(self):
        return self.kontak_list

    def perbarui_kontak(self, nama_lama, kontak_baru):
        for idx, kontak in enumerate(self.kontak_list):
            if kontak.nama == nama_lama:
                self.kontak_list[idx] = kontak_baru
                return True
        return False

    def hapus_kontak(self, nama):
        for idx, kontak in enumerate(self.kontak_list):
            if kontak.nama == nama:
                del self.kontak_list[idx]
                return True
        return False

    def urutkan_kontak(self, kriteria):
        if kriteria == "Nama":
            self.kontak_list.sort(key=lambda kontak: kontak.nama)
        elif kriteria == "Telepon":
            self.kontak_list.sort(key=lambda kontak: kontak.telepon)

    def cari_kontak(self, nama_partial):
        hasil_pencarian = []
        for kontak in self.kontak_list:
            if nama_partial.lower() in kontak.nama.lower():
                hasil_pencarian.append(kontak)
        return hasil_pencarian

    def impor_dari_csv(self, filename):
        try:
            with open(filename, mode='r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    self.tambah_kontak(Kontak(row['nama'], row['telepon'], row['email']))
            return True
        except FileNotFoundError:
            return False

class KontakApp:
    def __init__(self, root):
        self.manager = ManajerKontak()
        self.root = root
        self.root.title("SELAMAT DATANG DI SISTEM MANAJEMEN KONTAK")
       
        # Apply a style
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#ADD8E6')
        self.style.configure('TButton', background='#ADD8E6')
        self.style.configure('TLabel', background='#ADD8E6', font=('Poppins', 10))
        self.style.configure('TEntry', font=('Poppins', 10))
        self.style.configure('TText', font=('Poppins', 10))

        # Add menu bar
        self.create_menu()      

        # Add widgets
        self.create_widgets()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

      
        search_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Search", menu=search_menu)
        search_menu.add_command(label="Cari Kontak", command=self.show_search_dialog)

    def show_search_dialog(self):
        search_dialog = tk.Toplevel(self.root)
        search_dialog.title("Cari Kontak")

        ttk.Label(search_dialog, text="Masukkan Nama:").grid(row=0, column=0, padx=10, pady=10)
        self.search_entry = ttk.Entry(search_dialog, width=30)
        self.search_entry.grid(row=0, column=1, padx=10, pady=10)

        search_button = ttk.Button(search_dialog, text="Cari", command=self.perform_search)
        search_button.grid(row=1, column=0, columnspan=2, pady=10)

    def perform_search(self):
        nama_partial = self.search_entry.get()
        hasil_pencarian = self.manager.cari_kontak(nama_partial)
        self.kontak_text.delete(1.0, tk.END)
        if hasil_pencarian:
            for kontak in hasil_pencarian:
                self.kontak_text.insert(tk.END, f"Nama\t: {kontak.nama}\nTelepon\t: {kontak.telepon}\nEmail\t: {kontak.email}\n\n")
        else:
            messagebox.showinfo("Error", "Kontak tidak ditemukan.")

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="10 10 10 10")
        frame.pack(padx=10, pady=10, fill='x', expand=True)

       
        self.nama_label = ttk.Label(frame, text="Nama\t:")
        self.nama_label.grid(row=0, column=0, sticky="e")
        self.nama_entry = ttk.Entry(frame, width=30)
        self.nama_entry.grid(row=0, column=1, pady=5)

        self.telepon_label = ttk.Label(frame, text="Telepon\t:")
        self.telepon_label.grid(row=1, column=0, sticky="e")
        self.telepon_entry = ttk.Entry(frame, width=30)
        self.telepon_entry.grid(row=1, column=1, pady=5)

        self.email_label = ttk.Label(frame, text="Email\t:")
        self.email_label.grid(row=2, column=0, sticky="e")
        self.email_entry = ttk.Entry(frame, width=30)
        self.email_entry.grid(row=2, column=1, pady=5)

       
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        self.tambah_button = ttk.Button(button_frame, text="Tambah Kontak", command=self.tambah_kontak)
        self.tambah_button.grid(row=0, column=0, padx=5, pady=5)

        self.lihat_button = ttk.Button(button_frame, text="Lihat Kontak", command=self.lihat_kontak)
        self.lihat_button.grid(row=0, column=1, padx=5, pady=5)

        self.perbarui_button = ttk.Button(button_frame, text="Perbarui Kontak", command=self.perbarui_kontak)
        self.perbarui_button.grid(row=0, column=2, padx=5, pady=5)

        self.hapus_button = ttk.Button(button_frame, text="Hapus Kontak", command=self.hapus_kontak)
        self.hapus_button.grid(row=1, column=0, padx=5, pady=5)

       
        self.kriteria_urutkan_label = ttk.Label(button_frame, text="Urutkan Berdasarkan:")
        self.kriteria_urutkan_label.grid(row=1, column=1, padx=5, pady=5)
        self.kriteria_urutkan = tk.StringVar(value="Nama")
        self.kriteria_urutkan_dropdown = ttk.OptionMenu(button_frame, self.kriteria_urutkan, "Nama", "Nama", "Telepon")
        self.kriteria_urutkan_dropdown.grid(row=1, column=2, padx=5, pady=5)

        self.urutkan_button = ttk.Button(button_frame, text="Urutkan Kontak", command=self.urutkan_kontak)
        self.urutkan_button.grid(row=1, column=3, padx=5, pady=5)

        self.impor_button = ttk.Button(button_frame, text="Impor dari CSV", command=self.impor_dari_csv)
        self.impor_button.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

        self.keluar_button = ttk.Button(button_frame, text="Keluar", command=self.root.quit)
        self.keluar_button.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

       
        self.kontak_text = tk.Text(self.root, height=15, width=50, font=('Poppins', 10))
        self.kontak_text.pack(pady=10, padx=10)

    def tambah_kontak(self):
        nama = self.nama_entry.get()
        telepon = self.telepon_entry.get()
        email = self.email_entry.get()

        if nama and telepon and email:
            self.manager.tambah_kontak(Kontak(nama, telepon, email))
            messagebox.showinfo("Sukses", "Kontak berhasil ditambahkan!")
        else:
            messagebox.showerror("Error", "Semua field harus diisi.")

        self.clear_entries()

    def lihat_kontak(self):
        kontak_list = self.manager.lihat_kontak()
        self.kontak_text.delete(1.0, tk.END)
        for kontak in kontak_list:
            self.kontak_text.insert(tk.END, f"Nama\t: {kontak.nama}\nTelepon\t: {kontak.telepon}\nEmail\t: {kontak.email}\n\n")

    def perbarui_kontak(self):
        nama_lama = self.nama_entry.get()
        nama_baru = self.nama_entry.get()
        telepon_baru = self.telepon_entry.get()
        email_baru = self.email_entry.get()

        if self.manager.perbarui_kontak(nama_lama, Kontak(nama_baru, telepon_baru, email_baru)):
            messagebox.showinfo("Sukses", "Kontak berhasil diperbarui.")
        else:
            messagebox.showerror("Error", "Kontak tidak ditemukan.")
        
        self.clear_entries()

    def hapus_kontak(self):
        nama = self.nama_entry.get()
        if self.manager.hapus_kontak(nama):
            messagebox.showinfo("Sukses", "Kontak berhasil dihapus.")
        else:
            messagebox.showerror("Error", "Kontak tidak ditemukan.")
        
        self.clear_entries()

    def urutkan_kontak(self):
        kriteria = self.kriteria_urutkan.get()
        self.manager.urutkan_kontak(kriteria)
        self.lihat_kontak()
        messagebox.showinfo("Sukses", f"Kontak berhasil diurutkan berdasarkan {kriteria}.")

    def impor_dari_csv(self):
        filename = filedialog.askopenfilename(filetypes=(("CSV Files", "*.csv"),))
        if filename:
            if self.manager.impor_dari_csv(filename):
                messagebox.showinfo("Sukses", "Kontak berhasil diimpor.")
                self.lihat_kontak()
            else:
                messagebox.showerror("Error", f"File {filename} tidak ditemukan.")
        
    def clear_entries(self):
        self.nama_entry.delete(0, tk.END)
        self.telepon_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = KontakApp(root)
    root.mainloop()
