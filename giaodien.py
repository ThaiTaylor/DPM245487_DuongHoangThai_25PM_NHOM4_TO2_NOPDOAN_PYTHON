import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="quanly_tuyenxe"
    )


# Thêm tuyến xe
def Them():
    con = connect()
    cursor = con.cursor()

    sql = "INSERT INTO tuyen_xe (diem_di, diem_den, khoang_cach, gia_ve, ghi_chu) VALUES (%s,%s,%s,%s,%s)"
    val = (e_diemdi.get(), e_diemden.get(), e_kc.get(), e_giave.get(), e_ghichu.get())

    cursor.execute(sql, val)
    con.commit()
    con.close()

    CapNhat()
    messagebox.showinfo("Thông báo", "Thêm thành công!")

# Load dữ liệu lên bảng
def CapNhat():
    for row in tree.get_children():
        tree.delete(row)

    con = connect()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tuyen_xe")
    rows = cursor.fetchall()
    con.close()

    for row in rows:
        tree.insert("", tk.END, values=row)

# Xóa tuyến xe
def Xoa():
    selected = tree.focus()
    if selected == "":
        messagebox.showwarning("Cảnh báo", "Chọn tuyến để xóa!")
        return

    id = tree.item(selected)["values"][0]

    con = connect()
    cursor = con.cursor()
    cursor.execute("DELETE FROM tuyen_xe WHERE id=%s", (id,))
    con.commit()
    con.close()

    CapNhat()
    messagebox.showinfo("Thông báo", "Xóa thành công!")

# Giao diện Tkinter
root = tk.Tk()
root.title("Quản lý tuyến xe du lịch")

# --- Form nhập ---
tk.Label(root, text="Điểm đi").grid(row=0, column=0)
e_diemdi = tk.Entry(root); e_diemdi.grid(row=0, column=1)

tk.Label(root, text="Điểm đến").grid(row=1, column=0)
e_diemden = tk.Entry(root); e_diemden.grid(row=1, column=1)

tk.Label(root, text="Khoảng cách").grid(row=2, column=0)
e_kc = tk.Entry(root); e_kc.grid(row=2, column=1)

tk.Label(root, text="Giá vé").grid(row=3, column=0)
e_giave = tk.Entry(root); e_giave.grid(row=3, column=1)

tk.Label(root, text="Ghi chú").grid(row=4, column=0)
e_ghichu = tk.Entry(root); e_ghichu.grid(row=4, column=1)

tk.Button(root, text="Thêm", command=Them).grid(row=5, column=0)
tk.Button(root, text="Xóa", command=Xoa).grid(row=5, column=1)
tk.Button(root, text="Tải lại", command=CapNhat).grid(row=5, column=2)

# --- Bảng dữ liệu ---
tree = ttk.Treeview(root, columns=("ID","Điểm đi","Điểm đến","Khoảng cách","Giá vé","Ghi chú"), show="headings")
for col in ("ID","Điểm đi","Điểm đến","Khoảng cách","Giá vé","Ghi chú"):
    tree.heading(col, text=col)

tree.grid(row=6, column=0, columnspan=3)

CapNhat()
root.mainloop()
