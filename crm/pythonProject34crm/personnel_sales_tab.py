import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import pandas as pd

# Veritabanı bağlantısı
conn = sqlite3.connect('sales.db')
cursor = conn.cursor()

class PersonnelSalesTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_personnel_sales_tab()

    def create_personnel_sales_tab(self):
        self.personnel_var = tk.StringVar()
        self.total_sales_var = tk.IntVar()
        self.total_price_var = tk.DoubleVar()
        self.total_advance_var = tk.DoubleVar()
        self.total_bonus_var = tk.DoubleVar()
        self.return_rate_var = tk.StringVar()
        self.advance_var = tk.DoubleVar()
        self.bonus_var = tk.DoubleVar()

        control_frame = ttk.Frame(self)
        control_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(control_frame, text="Personel:").pack(side='left', padx=5)
        self.personnel_menu = ttk.Combobox(control_frame, textvariable=self.personnel_var, state="readonly", width=30)
        self.personnel_menu.pack(side='left', padx=5)
        self.load_personnel_names()

        ttk.Button(control_frame, text="Yenile", command=self.load_personnel_sales).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Excel'e Aktar", command=self.export_to_excel).pack(side='left', padx=5)

        self.sales_table = ttk.Treeview(self, columns=("ID", "Ad", "Soyad", "Ürün", "Fiyat", "Tarih", "İade"), show='headings')
        self.sales_table.pack(expand=True, fill='both', padx=10, pady=10)

        for col in self.sales_table["columns"]:
            self.sales_table.heading(col, text=col.replace("_", " ").title())
            self.sales_table.column(col, anchor='center', width=100)

        summary_frame = ttk.Frame(self)
        summary_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(summary_frame, text="Toplam Satış Adedi:").grid(row=0, column=0, sticky='E')
        ttk.Entry(summary_frame, textvariable=self.total_sales_var, state='readonly').grid(row=0, column=1, padx=5, pady=5, sticky='W')

        ttk.Label(summary_frame, text="Toplam Satış Fiyatı:").grid(row=1, column=0, sticky='E')
        ttk.Entry(summary_frame, textvariable=self.total_price_var, state='readonly').grid(row=1, column=1, padx=5, pady=5, sticky='W')

        ttk.Label(summary_frame, text="Toplam Avans:").grid(row=2, column=0, sticky='E')
        ttk.Entry(summary_frame, textvariable=self.total_advance_var, state='readonly').grid(row=2, column=1, padx=5, pady=5, sticky='W')

        ttk.Label(summary_frame, text="Toplam Prim:").grid(row=3, column=0, sticky='E')
        ttk.Entry(summary_frame, textvariable=self.total_bonus_var, state='readonly').grid(row=3, column=1, padx=5, pady=5, sticky='W')

        ttk.Label(summary_frame, text="İade Oranı:").grid(row=4, column=0, sticky='E')
        ttk.Entry(summary_frame, textvariable=self.return_rate_var, state='readonly').grid(row=4, column=1, padx=5, pady=5, sticky='W')

        ttk.Label(summary_frame, text="Avans:").grid(row=5, column=0, sticky='E')
        ttk.Entry(summary_frame, textvariable=self.advance_var).grid(row=5, column=1, padx=5, pady=5, sticky='W')

        ttk.Label(summary_frame, text="Prim:").grid(row=6, column=0, sticky='E')
        ttk.Entry(summary_frame, textvariable=self.bonus_var).grid(row=6, column=1, padx=5, pady=5, sticky='W')

        ttk.Button(summary_frame, text="Kaydet", command=self.save_personnel_data).grid(row=7, column=0, columnspan=2, pady=10)

    def load_personnel_names(self):
        cursor.execute("SELECT name, surname FROM personnel")
        personnel = cursor.fetchall()
        personnel_names = [f"{name} {surname}" for name, surname in personnel]
        self.personnel_menu['values'] = personnel_names

    def load_personnel_sales(self):
        personnel_name = self.personnel_var.get()
        if not personnel_name:
            return

        cursor.execute("""
            SELECT s.id, s.name, s.surname, s.product, s.price, s.sale_date, s.returned
            FROM sales s
            LEFT JOIN personnel p ON s.salesperson = p.name || ' ' || p.surname
            WHERE s.salesperson = ?
        """, (personnel_name,))
        rows = cursor.fetchall()
        self.refresh_table(rows)
        self.update_summary(personnel_name)

    def refresh_table(self, data):
        for item in self.sales_table.get_children():
            self.sales_table.delete(item)
        for row in data:
            self.sales_table.insert('', 'end', values=row)
        self.reset_column_widths()

    def reset_column_widths(self):
        for col in self.sales_table["columns"]:
            self.sales_table.column(col, width=100)

    def update_summary(self, personnel_name):
        cursor.execute("""
            SELECT COUNT(*), SUM(price)
            FROM sales
            WHERE salesperson = ? AND returned = 'Hayır'
        """, (personnel_name,))
        total_sales, total_price = cursor.fetchone()

        self.total_sales_var.set(total_sales if total_sales else 0)
        self.total_price_var.set(total_price if total_price else 0.0)

        cursor.execute("""
            SELECT SUM(advance), SUM(bonus)
            FROM personnel_sales
            WHERE personnel_id = (SELECT id FROM personnel WHERE name || ' ' || surname = ?)
        """, (personnel_name,))
        total_advance, total_bonus = cursor.fetchone() or (0.0, 0.0)

        self.total_advance_var.set(total_advance)
        self.total_bonus_var.set(total_bonus)

        cursor.execute("""
            SELECT COUNT(*)
            FROM sales
            WHERE salesperson = ? AND returned = 'Evet'
        """, (personnel_name,))
        total_returns = cursor.fetchone()[0]

        return_rate = (total_returns / total_sales) * 100 if total_sales else 0
        self.return_rate_var.set(f"{return_rate:.2f}%")

    def save_personnel_data(self):
        try:
            personnel_name = self.personnel_var.get()
            new_advance = self.advance_var.get()
            new_bonus = self.bonus_var.get()

            cursor.execute("""
                SELECT id FROM personnel WHERE name || ' ' || surname = ?
            """, (personnel_name,))
            personnel_id = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO personnel_sales (personnel_id, advance, bonus)
                VALUES (?, ?, ?)
                ON CONFLICT(personnel_id) DO UPDATE SET advance = advance + excluded.advance, bonus = bonus + excluded.bonus
            """, (personnel_id, new_advance, new_bonus))
            conn.commit()
            messagebox.showinfo("Başarılı", "Personel verileri güncellendi!")
            self.load_personnel_sales()  # Verileri güncelle
        except Exception as e:
            messagebox.showerror("Hata", f"Veri kaydetme hatası: {e}")

    def export_to_excel(self):
        data = [self.sales_table.item(item_id, 'values') for item_id in self.sales_table.get_children()]
        df = pd.DataFrame(data, columns=[col.replace("_", " ").title() for col in self.sales_table["columns"]])
        df.to_excel("exported_personnel_sales_data.xlsx", index=False)
        messagebox.showinfo("Başarılı", "Veriler başarıyla Excel'e aktarıldı!")

if __name__ == "__main__":
    app = tk.Tk()
    app.title("Personel Satışları")
    PersonnelSalesTab(app).pack(expand=True, fill='both')
    app.mainloop()
    conn.close()