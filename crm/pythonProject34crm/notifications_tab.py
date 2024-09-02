import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta
import pandas as pd

class NotificationsTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_notifications_tab()

    def create_notifications_tab(self):
        self.time_frame_var = tk.StringVar(value="1 Gün Kalan")

        control_frame = ttk.Frame(self)
        control_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(control_frame, text="Zaman Aralığı:").pack(side='left', padx=5)
        time_frame_options = ttk.Combobox(control_frame, textvariable=self.time_frame_var, values=["1 Gün Kalan", "2 Gün Kalan", "3 Gün Kalan", "4 Gün Kalan", "5 Gün Kalan", "6 Gün Kalan", "7 Gün Kalan"], state="readonly", width=20)
        time_frame_options.pack(side='left', padx=5)

        ttk.Button(control_frame, text="Yenile", command=self.load_notifications).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Excel'e Aktar", command=self.export_to_excel).pack(side='left', padx=5)

        self.notifications_table = ttk.Treeview(self, columns=("ID", "Ad", "Soyad", "Telefon", "Taksit No", "Taksit Sayısı", "Taksit Tarihi", "Kalan Gün", "Aylık Ödeme"), show='headings')
        self.notifications_table.pack(expand=True, fill='both', padx=10, pady=10)

        for col in self.notifications_table["columns"]:
            self.notifications_table.heading(col, text=col.replace("_", " ").title())
            self.notifications_table.column(col, anchor='center', width=100)

        self.load_notifications()

    def parse_date(self, date_str):
        formats = ["%d.%m.%Y", "%Y-%m-%d"]
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt).date()
            except (ValueError, TypeError):
                pass
        raise ValueError(f"Tarih formatı yanlış: {date_str}")

    def load_notifications(self):
        self.notifications_table.delete(*self.notifications_table.get_children())
        time_frame = self.time_frame_var.get()

        today = datetime.today().date()
        days_before = int(time_frame.split()[0])

        conn = sqlite3.connect('sales.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM sales WHERE installment_count > 0 AND returned = 'Hayır'")
        rows = cursor.fetchall()
        for row in rows:
            try:
                sale_date = self.parse_date(row[9])
                installment_count = int(row[13])
                price = float(row[10])
                received_amount = float(row[11])
                remaining_amount = price - received_amount
                monthly_payment = float(row[14]) if row[14] else remaining_amount / installment_count

                for i in range(installment_count):
                    payment_date = sale_date + timedelta(days=(i + 1) * 30)
                    days_remaining = (payment_date - today).days
                    if days_remaining <= days_before and days_remaining >= 0:
                        self.notifications_table.insert('', 'end', values=(
                            row[0], row[1], row[2], row[6], i + 1, installment_count, payment_date.strftime("%d.%m.%Y"), days_remaining, round(monthly_payment, 2)
                        ))
            except ValueError as e:
                print(f"Error parsing date: {e}")
        conn.close()

    def export_to_excel(self):
        try:
            data = [self.notifications_table.item(item_id, 'values') for item_id in self.notifications_table.get_children()]
            df = pd.DataFrame(data, columns=[col.replace("_", " ").title() for col in self.notifications_table["columns"]])
            df.to_excel("notifications.xlsx", index=False)
            messagebox.showinfo("Başarılı", "Veriler başarıyla Excel'e aktarıldı!")
        except Exception as e:
            messagebox.showerror("Hata", f"Veri dışa aktarma hatası: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NotificationsTab(root)
    app.pack(expand=True, fill='both')
    root.mainloop()