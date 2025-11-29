# app.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import StringVar, IntVar
import datetime
import mysql_module as db

db.init_database()  # đảm bảo DB + bảng đã có
def center_window(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()

    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)

    win.geometry(f'{width}x{height}+{x}+{y}')

root = tk.Tk()
root.title("Quản Lý Các Tuyến Xe Du Lịch")
root.geometry("1100x700")
center_window(root)

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# Helper: tạo table trong tab
def make_table(parent, columns, headings, height=12):
    frame = tk.Frame(parent)
    frame.pack(fill="both", expand=True)
    tv = ttk.Treeview(frame, columns=columns, show="headings", height=height)
    for col, hd in zip(columns, headings):
        tv.heading(col, text=hd)
        tv.column(col, width=140, anchor="center")
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tv.yview)
    tv.configure(yscroll=vsb.set)
    vsb.pack(side="right", fill="y")
    tv.pack(fill="both", expand=True)
    return tv

# TAB 1: TUYẾN XE
tab_tuyen = ttk.Frame(notebook)
notebook.add(tab_tuyen, text="Tuyến Xe")

frm_tuyen_form = tk.Frame(tab_tuyen)
frm_tuyen_form.pack(fill="x", pady=8)

labels = ["Mã tuyến", "Tên tuyến", "Điểm đi", "Điểm đến", "Khoảng cách (km)", "Giá vé"]
entries_tuyen = {}
for i, text in enumerate(labels):
    tk.Label(frm_tuyen_form, text=text).grid(row=i, column=0, sticky="w", padx=8, pady=4)
    e = tk.Entry(frm_tuyen_form, width=40)
    e.grid(row=i, column=1, padx=8, pady=4, sticky="w")
    entries_tuyen[text] = e

def load_tuyen():
    tv = tree_tuyen
    tv.delete(*tv.get_children())
    rows = db.get_all_tuyen()
    for r in rows:
        tv.insert("", tk.END, values=r)

def t_add():
    try:
        ma = entries_tuyen["Mã tuyến"].get().strip()
        if ma == "":
            messagebox.showwarning("Lỗi", "Mã tuyến không được để trống")
            return
        if db.search_tuyen_by_ma(ma):
            messagebox.showerror("Lỗi", "Mã tuyến đã tồn tại")
            return
        db.insert_tuyen(
            ma,
            entries_tuyen["Tên tuyến"].get(),
            entries_tuyen["Điểm đi"].get(),
            entries_tuyen["Điểm đến"].get(),
            int(entries_tuyen["Khoảng cách (km)"].get()),
            float(entries_tuyen["Giá vé"].get())
        )
        load_tuyen()
        load_comboboxes()
        messagebox.showinfo("OK", "Đã thêm tuyến")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Dữ liệu không hợp lệ:\n{e}")

def t_update():
    try:
        ma = entries_tuyen["Mã tuyến"].get().strip()
        if not db.search_tuyen_by_ma(ma):
            messagebox.showerror("Lỗi", "Mã tuyến không tồn tại")
            return
        db.update_tuyen(
            ma,
            entries_tuyen["Tên tuyến"].get(),
            entries_tuyen["Điểm đi"].get(),
            entries_tuyen["Điểm đến"].get(),
            int(entries_tuyen["Khoảng cách (km)"].get()),
            float(entries_tuyen["Giá vé"].get())
        )
        load_tuyen()
        load_comboboxes()
        messagebox.showinfo("OK", "Đã cập nhật")
    except Exception as e:
        messagebox.showerror("Lỗi", f"{e}")

def t_delete():
    ma = entries_tuyen["Mã tuyến"].get().strip()
    if ma == "":
        messagebox.showwarning("Lỗi", "Chưa nhập mã tuyến")
        return
    if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa tuyến? (các chuyến liên quan cũng sẽ bị xóa)"):
        db.delete_tuyen(ma)
        load_tuyen()
        load_comboboxes()

def t_search():
    ma = entries_tuyen["Mã tuyến"].get().strip()
    if ma == "":
        load_tuyen()
        return
    row = db.search_tuyen_by_ma(ma)
    tree_tuyen.delete(*tree_tuyen.get_children())
    if row:
        tree_tuyen.insert("", tk.END, values=row)
    else:
        messagebox.showinfo("Không tìm thấy", "Không có mã tuyến này")

btn_frame = tk.Frame(frm_tuyen_form)
btn_frame.grid(row=0, column=2, rowspan=6, padx=10)
tk.Button(btn_frame, text="Thêm", width=12, command=t_add).pack(pady=4)
tk.Button(btn_frame, text="Sửa", width=12, command=t_update).pack(pady=4)
tk.Button(btn_frame, text="Xóa", width=12, command=t_delete).pack(pady=4)
tk.Button(btn_frame, text="Tải lại", width=12, command=load_tuyen).pack(pady=4)
tk.Button(btn_frame, text="Tìm (theo mã)", width=12, command=t_search).pack(pady=4)

tree_tuyen = make_table(tab_tuyen,
                        columns=("ma_tuyen","ten_tuyen","diem_di","diem_den","khoang_cach","gia_ve"),
                        headings=["Mã tuyến","Tên tuyến","Điểm đi","Điểm đến","Khoảng cách(km)","Giá vé(VNĐ)"],
                        height=12)

def on_tuyen_select(event):
    sel = tree_tuyen.selection()
    if not sel: return
    vals = tree_tuyen.item(sel[0])['values']
    for i, key in enumerate(labels):
        entries_tuyen[key].delete(0, tk.END)
        entries_tuyen[key].insert(0, vals[i])

tree_tuyen.bind("<<TreeviewSelect>>", on_tuyen_select)

# TAB 2: XE 
tab_xe = ttk.Frame(notebook)
notebook.add(tab_xe, text="Xe")

frm_xe_form = tk.Frame(tab_xe)
frm_xe_form.pack(fill="x", pady=8)

labels_xe = ["Mã xe", "Biển số", "Số ghế", "Hãng xe", "Trạng thái"]
entries_xe = {}
for i, text in enumerate(labels_xe):
    tk.Label(frm_xe_form, text=text).grid(row=i, column=0, sticky="w", padx=8, pady=4)
    e = tk.Entry(frm_xe_form, width=40)
    e.grid(row=i, column=1, padx=8, pady=4, sticky="w")
    entries_xe[text] = e

def load_xe():
    tree_xe.delete(*tree_xe.get_children())
    for r in db.get_all_xe():
        tree_xe.insert("", tk.END, values=r)

def xe_add():
    try:
        db.insert_xe(
            entries_xe["Mã xe"].get().strip(),
            entries_xe["Biển số"].get(),
            int(entries_xe["Số ghế"].get()),
            entries_xe["Hãng xe"].get(),
            entries_xe["Trạng thái"].get()
        )
        load_xe()
        load_comboboxes()
        messagebox.showinfo("OK", "Đã thêm xe")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def xe_update():
    try:
        db.update_xe(
            entries_xe["Mã xe"].get().strip(),
            entries_xe["Biển số"].get(),
            int(entries_xe["Số ghế"].get()),
            entries_xe["Hãng xe"].get(),
            entries_xe["Trạng thái"].get()
        )
        load_xe()
        load_comboboxes()
        messagebox.showinfo("OK", "Đã cập nhật xe")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def xe_delete():
    ma = entries_xe["Mã xe"].get().strip()
    if messagebox.askyesno("Xác nhận","Xóa xe sẽ đặt NULL cho chuyến liên quan. Tiếp tục?"):
        db.delete_xe(ma)
        load_xe()
        load_comboboxes()

btn_frame_xe = tk.Frame(frm_xe_form)
btn_frame_xe.grid(row=0, column=2, rowspan=5, padx=10)
tk.Button(btn_frame_xe, text="Thêm", width=12, command=xe_add).pack(pady=4)
tk.Button(btn_frame_xe, text="Sửa", width=12, command=xe_update).pack(pady=4)
tk.Button(btn_frame_xe, text="Xóa", width=12, command=xe_delete).pack(pady=4)
tk.Button(btn_frame_xe, text="Tải lại", width=12, command=load_xe).pack(pady=4)

tree_xe = make_table(tab_xe,
                     columns=("ma_xe","bien_so","so_ghe","hang_xe","trang_thai"),
                     headings=["Mã xe","Biển số","Số ghế","Hãng xe","Trạng thái"],
                     height=12)

def on_xe_select(event):
    sel = tree_xe.selection()
    if not sel: return
    vals = tree_xe.item(sel[0])['values']
    for i, k in enumerate(labels_xe):
        entries_xe[k].delete(0, tk.END)
        entries_xe[k].insert(0, vals[i])

tree_xe.bind("<<TreeviewSelect>>", on_xe_select)

# TAB 3: TÀI XẾ 
tab_tx = ttk.Frame(notebook)
notebook.add(tab_tx, text="Tài Xế")

frm_tx_form = tk.Frame(tab_tx)
frm_tx_form.pack(fill="x", pady=8)

labels_tx = ["Mã tài xế","Họ tên","SĐT","Bằng lái","Kinh nghiệm (năm)"]
entries_tx = {}
for i, text in enumerate(labels_tx):
    tk.Label(frm_tx_form, text=text).grid(row=i, column=0, sticky="w", padx=8, pady=4)
    e = tk.Entry(frm_tx_form, width=40)
    e.grid(row=i, column=1, padx=8, pady=4, sticky="w")
    entries_tx[text] = e

def load_tx():
    tree_tx.delete(*tree_tx.get_children())
    for r in db.get_all_taixe():
        tree_tx.insert("", tk.END, values=r)

def tx_add():
    try:
        db.insert_taixe(
            entries_tx["Mã tài xế"].get().strip(),
            entries_tx["Họ tên"].get(),
            entries_tx["SĐT"].get(),
            entries_tx["Bằng lái"].get(),
            int(entries_tx["Kinh nghiệm (năm)"].get())
        )
        load_tx()
        load_comboboxes()
        messagebox.showinfo("OK", "Đã thêm tài xế")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def tx_update():
    try:
        db.update_taixe(
            entries_tx["Mã tài xế"].get().strip(),
            entries_tx["Họ tên"].get(),
            entries_tx["SĐT"].get(),
            entries_tx["Bằng lái"].get(),
            int(entries_tx["Kinh nghiệm (năm)"].get())
        )
        load_tx()
        load_comboboxes()
        messagebox.showinfo("OK", "Đã cập nhật")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def tx_delete():
    ma = entries_tx["Mã tài xế"].get().strip()
    if messagebox.askyesno("Xác nhận","Xóa tài xế sẽ đặt NULL cho chuyến liên quan. Tiếp tục?"):
        db.delete_taixe(ma)
        load_tx()
        load_comboboxes()

btn_frame_tx = tk.Frame(frm_tx_form)
btn_frame_tx.grid(row=0, column=2, rowspan=5, padx=10)
tk.Button(btn_frame_tx, text="Thêm", width=12, command=tx_add).pack(pady=4)
tk.Button(btn_frame_tx, text="Sửa", width=12, command=tx_update).pack(pady=4)
tk.Button(btn_frame_tx, text="Xóa", width=12, command=tx_delete).pack(pady=4)
tk.Button(btn_frame_tx, text="Tải lại", width=12, command=load_tx).pack(pady=4)

tree_tx = make_table(tab_tx,
                     columns=("ma_tai_xe","ho_ten","so_dien_thoai","bang_lai","kinh_nghiem"),
                     headings=["Mã TX","Họ tên","SĐT","Bằng lái","Kinh nghiệm"],
                     height=12)

def on_tx_select(event):
    sel = tree_tx.selection()
    if not sel: return
    vals = tree_tx.item(sel[0])['values']
    for i, k in enumerate(labels_tx):
        entries_tx[k].delete(0, tk.END)
        entries_tx[k].insert(0, vals[i])

tree_tx.bind("<<TreeviewSelect>>", on_tx_select)

#  TAB 4: CHUYẾN XE 
tab_chuyen = ttk.Frame(notebook)
notebook.add(tab_chuyen, text="Chuyến Xe")

frm_chuyen_form = tk.Frame(tab_chuyen)
frm_chuyen_form.pack(fill="x", pady=8)

labels_ch = ["Mã chuyến", "Mã tuyến", "Tên tuyến (auto)", "Mã xe", "Biển số (auto)", "Mã tài xế", "Tên tài xế (auto)", "Khởi hành (YYYY-MM-DD HH:MM)", "Dự kiến (YYYY-MM-DD HH:MM)", "Giá vé"]
entries_ch = {}
for i, text in enumerate(labels_ch):
    tk.Label(frm_chuyen_form, text=text).grid(row=i, column=0, sticky="w", padx=8, pady=4)
    e = tk.Entry(frm_chuyen_form, width=40)
    e.grid(row=i, column=1, padx=8, pady=4, sticky="w")
    entries_ch[text] = e

# thay thế các trường ‘mã’ bằng combobox
cbb_ma_tuyen = ttk.Combobox(frm_chuyen_form, width=37)
cbb_ma_xe = ttk.Combobox(frm_chuyen_form, width=37)
cbb_ma_tai_xe = ttk.Combobox(frm_chuyen_form, width=37)
# Đặt các combobox chồng lên entry
entries_ch["Mã tuyến"].grid_forget()
entries_ch["Mã tuyến"] = cbb_ma_tuyen
cbb_ma_tuyen.grid(row=1, column=1, padx=8, pady=4, sticky="w")

entries_ch["Mã xe"].grid_forget()
entries_ch["Mã xe"] = cbb_ma_xe
cbb_ma_xe.grid(row=3, column=1, padx=8, pady=4, sticky="w")

entries_ch["Mã tài xế"].grid_forget()
entries_ch["Mã tài xế"] = cbb_ma_tai_xe
cbb_ma_tai_xe.grid(row=5, column=1, padx=8, pady=4, sticky="w")

def load_comboboxes():
    # load tuyen
    lst = db.fetch_tuyen_for_combobox()  # list of (ma, ten)
    cbb_ma_tuyen['values'] = [f"{m} | {t}" for m,t in lst]
    # load xe
    lst2 = db.fetch_xe_for_combobox()
    cbb_ma_xe['values'] = [f"{m} | {b}" for m,b in lst2]
    # load taixe
    lst3 = db.fetch_taixe_for_combobox()
    cbb_ma_tai_xe['values'] = [f"{m} | {n}" for m,n in lst3]

def kiemtra_combobox_value(val):
    # Giá trị hợp lệ là "ma" hoặc "name" only "ma"
    if not val:
        return ""
    if "|" in val:
        return val.split("|")[0].strip()
    return val.strip()

def load_chuyen():
    tree_ch.delete(*tree_ch.get_children())
    rows = db.fetch_chuyen_with_details()
    for r in rows:
        # r = (ma_chuyen, ma_tuyen, ten_tuyen, ma_xe, bien_so, ma_tai_xe, ho_ten, thoi_khoi, thoi_du, gia)
        tree_ch.insert("", tk.END, values=r)

def ch_add():
    try:
        ma_chuyen = entries_ch["Mã chuyến"].get().strip()
        if ma_chuyen == "":
            messagebox.showwarning("Lỗi","Mã chuyến không được để trống")
            return
        ma_tuyen = kiemtra_combobox_value(cbb_ma_tuyen.get())
        ma_xe = kiemtra_combobox_value(cbb_ma_xe.get())
        ma_tai_xe = kiemtra_combobox_value(cbb_ma_tai_xe.get())
        t_khoi = entries_ch["Khởi hành (YYYY-MM-DD HH:MM)"].get().strip()
        t_du = entries_ch["Dự kiến (YYYY-MM-DD HH:MM)"].get().strip()
        gia = float(entries_ch["Giá vé"].get())

        # Chuyển sang định dạng ngày h chuẩn strings (MySQL accepts 'YYYY-MM-DD HH:MM:SS')
        def to_mysql_dt(s):
            # try parse YYYY-MM-DD HH:MM
            if s == "": return None
            try:
                dt = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M")
                return dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                raise ValueError("Sai định dạng thời gian, dùng YYYY-MM-DD HH:MM")

        tkhoi = to_mysql_dt(t_khoi)
        tdu = to_mysql_dt(t_du)

        db.insert_chuyen(ma_chuyen, ma_tuyen or None, ma_xe or None, ma_tai_xe or None, tkhoi, tdu, gia)
        load_chuyen()
        messagebox.showinfo("OK","Đã thêm chuyến")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def ch_update():
    try:
        ma_chuyen = entries_ch["Mã chuyến"].get().strip()
        ma_tuyen = kiemtra_combobox_value(cbb_ma_tuyen.get())
        ma_xe = kiemtra_combobox_value(cbb_ma_xe.get())
        ma_tai_xe = kiemtra_combobox_value(cbb_ma_tai_xe.get())
        t_khoi = entries_ch["Khởi hành (YYYY-MM-DD HH:MM)"].get().strip()
        t_du = entries_ch["Dự kiến (YYYY-MM-DD HH:MM)"].get().strip()
        gia = float(entries_ch["Giá vé"].get())

        def to_mysql_dt(s):
            if s == "": return None
            try:
                dt = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M")
                return dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                raise ValueError("Sai định dạng thời gian, dùng YYYY-MM-DD HH:MM")

        tkhoi = to_mysql_dt(t_khoi)
        tdu = to_mysql_dt(t_du)

        db.update_chuyen(ma_chuyen, ma_tuyen or None, ma_xe or None, ma_tai_xe or None, tkhoi, tdu, gia)
        load_chuyen()
        messagebox.showinfo("OK","Đã cập nhật chuyến")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def ch_delete():
    ma = entries_ch["Mã chuyến"].get().strip()
    if ma == "":
        messagebox.showwarning("Lỗi", "Chưa nhập mã chuyến")
        return
    if messagebox.askyesno("Xác nhận","Bạn có chắc muốn xóa chuyến?"):
        db.delete_chuyen(ma)
        load_chuyen()

btn_frame_ch = tk.Frame(frm_chuyen_form)
btn_frame_ch.grid(row=0, column=2, rowspan=10, padx=10)
tk.Button(btn_frame_ch, text="Thêm", width=14, command=ch_add).pack(pady=4)
tk.Button(btn_frame_ch, text="Sửa", width=14, command=ch_update).pack(pady=4)
tk.Button(btn_frame_ch, text="Xóa", width=14, command=ch_delete).pack(pady=4)
tk.Button(btn_frame_ch, text="Tải lại", width=14, command=load_chuyen).pack(pady=4)
tk.Button(btn_frame_ch, text="Tải lại combobox", width=14, command=load_comboboxes).pack(pady=4)

tree_ch = make_table(tab_chuyen,
                     columns=("ma_chuyen","ma_tuyen","ten_tuyen","ma_xe","bien_so","ma_tai_xe","ho_ten","thoi_khoi","thoi_du","gia"),
                     headings=["Mã chuyến","Mã tuyến","Tên tuyến","Mã xe","Biển số","Mã tài xế","Tên tài xế","Khởi hành","Dự kiến","Giá vé(VNĐ)"],
                     height=12)

def on_ch_select(event):
    sel = tree_ch.selection()
    if not sel: return
    vals = tree_ch.item(sel[0])['values']
    # cập nhật hoặc điền dữ liệu
    entries_ch["Mã chuyến"].delete(0, tk.END); entries_ch["Mã chuyến"].insert(0, vals[0])
    # đặt giá trị hiển thị trong ComboBox theo định dạng "<ma> | <name>"
    if vals[1]:
        cbb_ma_tuyen.set(f"{vals[1]} | {vals[2] if vals[2] else ''}")
    else:
        cbb_ma_tuyen.set("")
    if vals[3]:
        cbb_ma_xe.set(f"{vals[3]} | {vals[4] if vals[4] else ''}")
    else:
        cbb_ma_xe.set("")
    if vals[5]:
        cbb_ma_tai_xe.set(f"{vals[5]} | {vals[6] if vals[6] else ''}")
    else:
        cbb_ma_tai_xe.set("")
    # times
    if vals[7]:
        entries_ch["Khởi hành (YYYY-MM-DD HH:MM)"].delete(0, tk.END)
        dt = vals[7]
        try:
            entries_ch["Khởi hành (YYYY-MM-DD HH:MM)"].insert(0, dt.strftime("%Y-%m-%d %H:%M"))
        except:
            entries_ch["Khởi hành (YYYY-MM-DD HH:MM)"].insert(0, str(dt)[:16])
    else:
        entries_ch["Khởi hành (YYYY-MM-DD HH:MM)"].delete(0, tk.END)
    if vals[8]:
        entries_ch["Dự kiến (YYYY-MM-DD HH:MM)"].delete(0, tk.END)
        dt2 = vals[8]
        try:
            entries_ch["Dự kiến (YYYY-MM-DD HH:MM)"].insert(0, dt2.strftime("%Y-%m-%d %H:%M"))
        except:
            entries_ch["Dự kiến (YYYY-MM-DD HH:MM)"].insert(0, str(dt2)[:16])
    else:
        entries_ch["Dự kiến (YYYY-MM-DD HH:MM)"].delete(0, tk.END)
    entries_ch["Giá vé"].delete(0, tk.END)
    entries_ch["Giá vé"].insert(0, vals[9] if vals[9] is not None else "")

tree_ch.bind("<<TreeviewSelect>>", on_ch_select)

# Init load 
load_tuyen()
load_xe()
load_tx()
load_comboboxes()
load_chuyen()

root.mainloop()
