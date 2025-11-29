# mysql_module.py
import mysql.connector
from mysql.connector import Error

# CẤU HÌNH MYSQL  
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASS = "123456"        
MYSQL_DB   = "quanly_tuyenxe"


def connect_server():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASS
    )

def connect_db():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASS,
        database=MYSQL_DB
    )

def init_database():
    # Tạo database + bảng 
    conn = connect_server()
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DB}")
    conn.commit()
    conn.close()

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tuyen_xe (
            ma_tuyen VARCHAR(20) PRIMARY KEY,
            ten_tuyen VARCHAR(255) NOT NULL,
            diem_di VARCHAR(255) NOT NULL,
            diem_den VARCHAR(255) NOT NULL,
            khoang_cach INT NOT NULL,
            gia_ve DECIMAL(15,2) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS xe (
            ma_xe VARCHAR(20) PRIMARY KEY,
            bien_so VARCHAR(20) NOT NULL,
            so_ghe INT NOT NULL,
            hang_xe VARCHAR(100),
            trang_thai VARCHAR(50)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tai_xe (
            ma_tai_xe VARCHAR(20) PRIMARY KEY,
            ho_ten VARCHAR(255) NOT NULL,
            so_dien_thoai VARCHAR(20),
            bang_lai VARCHAR(20),
            kinh_nghiem INT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chuyen_xe (
            ma_chuyen VARCHAR(20) PRIMARY KEY,
            ma_tuyen VARCHAR(20),
            ma_xe VARCHAR(20),
            ma_tai_xe VARCHAR(20),
            thoi_gian_khoi_hanh DATETIME,
            thoi_gian_du_kien DATETIME,
            gia_ve DECIMAL(15,2),
            FOREIGN KEY (ma_tuyen) REFERENCES tuyen_xe(ma_tuyen) ON DELETE CASCADE,
            FOREIGN KEY (ma_xe) REFERENCES xe(ma_xe) ON DELETE SET NULL,
            FOREIGN KEY (ma_tai_xe) REFERENCES tai_xe(ma_tai_xe) ON DELETE SET NULL
        )
    """)

    conn.commit()
    conn.close()


# TUYEN_XE CRUD
def get_all_tuyen():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tuyen_xe")
    rows = cur.fetchall()
    conn.close()
    return rows

def insert_tuyen(ma_tuyen, ten, di, den, kc, gia):
    conn = connect_db()
    cur = conn.cursor()
    sql = """INSERT INTO tuyen_xe (ma_tuyen, ten_tuyen, diem_di, diem_den, khoang_cach, gia_ve)
             VALUES (%s,%s,%s,%s,%s,%s)"""
    cur.execute(sql, (ma_tuyen, ten, di, den, kc, gia))
    conn.commit()
    conn.close()

def update_tuyen(ma_tuyen, ten, di, den, kc, gia):
    conn = connect_db()
    cur = conn.cursor()
    sql = """UPDATE tuyen_xe SET ten_tuyen=%s, diem_di=%s, diem_den=%s, khoang_cach=%s, gia_ve=%s
             WHERE ma_tuyen=%s"""
    cur.execute(sql, (ten, di, den, kc, gia, ma_tuyen))
    conn.commit()
    conn.close()

def delete_tuyen(ma_tuyen):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM tuyen_xe WHERE ma_tuyen=%s", (ma_tuyen,))
    conn.commit()
    conn.close()

def search_tuyen_by_ma(ma_tuyen):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tuyen_xe WHERE ma_tuyen=%s", (ma_tuyen,))
    row = cur.fetchone()
    conn.close()
    return row

# XE CRUD 
def get_all_xe():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM xe")
    rows = cur.fetchall()
    conn.close()
    return rows

def insert_xe(ma_xe, bien_so, so_ghe, hang_xe, trang_thai):
    conn = connect_db()
    cur = conn.cursor()
    sql = "INSERT INTO xe(ma_xe, bien_so, so_ghe, hang_xe, trang_thai) VALUES (%s,%s,%s,%s,%s)"
    cur.execute(sql, (ma_xe, bien_so, so_ghe, hang_xe, trang_thai))
    conn.commit()
    conn.close()

def update_xe(ma_xe, bien_so, so_ghe, hang_xe, trang_thai):
    conn = connect_db()
    cur = conn.cursor()
    sql = """UPDATE xe SET bien_so=%s, so_ghe=%s, hang_xe=%s, trang_thai=%s WHERE ma_xe=%s"""
    cur.execute(sql, (bien_so, so_ghe, hang_xe, trang_thai, ma_xe))
    conn.commit()
    conn.close()

def delete_xe(ma_xe):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM xe WHERE ma_xe=%s", (ma_xe,))
    conn.commit()
    conn.close()

# TAI_XE CRUD 
def get_all_taixe():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tai_xe")
    rows = cur.fetchall()
    conn.close()
    return rows

def insert_taixe(ma_tai_xe, ho_ten, sdt, bang_lai, kn):
    conn = connect_db()
    cur = conn.cursor()
    sql = "INSERT INTO tai_xe(ma_tai_xe, ho_ten, so_dien_thoai, bang_lai, kinh_nghiem) VALUES (%s,%s,%s,%s,%s)"
    cur.execute(sql, (ma_tai_xe, ho_ten, sdt, bang_lai, kn))
    conn.commit()
    conn.close()

def update_taixe(ma_tai_xe, ho_ten, sdt, bang_lai, kn):
    conn = connect_db()
    cur = conn.cursor()
    sql = """UPDATE tai_xe SET ho_ten=%s, so_dien_thoai=%s, bang_lai=%s, kinh_nghiem=%s WHERE ma_tai_xe=%s"""
    cur.execute(sql, (ho_ten, sdt, bang_lai, kn, ma_tai_xe))
    conn.commit()
    conn.close()

def delete_taixe(ma_tai_xe):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM tai_xe WHERE ma_tai_xe=%s", (ma_tai_xe,))
    conn.commit()
    conn.close()

# CHUYEN_XE CRUD 
def get_all_chuyen():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM chuyen_xe")
    rows = cur.fetchall()
    conn.close()
    return rows

def insert_chuyen(ma_chuyen, ma_tuyen, ma_xe, ma_tai_xe, t_khoi, t_du_kien, gia):
    conn = connect_db()
    cur = conn.cursor()
    sql = """INSERT INTO chuyen_xe (ma_chuyen, ma_tuyen, ma_xe, ma_tai_xe, thoi_gian_khoi_hanh, thoi_gian_du_kien, gia_ve)
             VALUES (%s,%s,%s,%s,%s,%s,%s)"""
    cur.execute(sql, (ma_chuyen, ma_tuyen, ma_xe, ma_tai_xe, t_khoi, t_du_kien, gia))
    conn.commit()
    conn.close()

def update_chuyen(ma_chuyen, ma_tuyen, ma_xe, ma_tai_xe, t_khoi, t_du_kien, gia):
    conn = connect_db()
    cur = conn.cursor()
    sql = """UPDATE chuyen_xe SET ma_tuyen=%s, ma_xe=%s, ma_tai_xe=%s, thoi_gian_khoi_hanh=%s, thoi_gian_du_kien=%s, gia_ve=%s
             WHERE ma_chuyen=%s"""
    cur.execute(sql, (ma_tuyen, ma_xe, ma_tai_xe, t_khoi, t_du_kien, gia, ma_chuyen))
    conn.commit()
    conn.close()

def delete_chuyen(ma_chuyen):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM chuyen_xe WHERE ma_chuyen=%s", (ma_chuyen,))
    conn.commit()
    conn.close()

# HỖ TRỢ CHO GIAO DIỆN
def fetch_tuyen_for_combobox():
    rows = get_all_tuyen()
    return [(r[0], r[1]) for r in rows]   # (ma_tuyen, ten_tuyen)

def fetch_xe_for_combobox():
    rows = get_all_xe()
    return [(r[0], r[1]) for r in rows]   # (ma_xe, bien_so)

def fetch_taixe_for_combobox():
    rows = get_all_taixe()
    return [(r[0], r[1]) for r in rows]   # (ma_tai_xe, ho_ten)

def fetch_chuyen_with_details():
    # Join để hiển thị thông tin chi tiết chuyến: ma_chuyen, ten_tuyen, bien_so, ho_ten, thoi_gian_khoi_hanh, thoi_gian_du_kien, gia
    conn = connect_db()
    cur = conn.cursor()
    sql = """
        SELECT c.ma_chuyen, c.ma_tuyen, t.ten_tuyen,
               c.ma_xe, x.bien_so,
               c.ma_tai_xe, tx.ho_ten,
               c.thoi_gian_khoi_hanh, c.thoi_gian_du_kien, c.gia_ve
        FROM chuyen_xe c
        LEFT JOIN tuyen_xe t ON c.ma_tuyen = t.ma_tuyen
        LEFT JOIN xe x ON c.ma_xe = x.ma_xe
        LEFT JOIN tai_xe tx ON c.ma_tai_xe = tx.ma_tai_xe
    """
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows

# init main
if __name__ == "__main__":
    init_database()
    print("Database init done.")
