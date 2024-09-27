import mysql.connector

# Thiết lập kết nối
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="quanlyquangame"
)

# Tạo một con trỏ
cursor = connection.cursor()

# Thực thi câu lệnh SQL
# Tạo bảng MayTram
cursor.execute('''
CREATE TABLE IF NOT EXISTS MayTram (
    may_id INT AUTO_INCREMENT PRIMARY KEY,
    ten_may VARCHAR(50) NOT NULL,
    trang_thai VARCHAR(20) NOT NULL,
    mo_ta TEXT,
    may_don_gia INT,
    anh_may VARCHAR(255)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS NguoiDung (
        nguoi_dung_id INT AUTO_INCREMENT PRIMARY KEY,
        ten VARCHAR(100) NOT NULL,
        tai_khoan VARCHAR(50) NOT NULL,
        mat_khau VARCHAR(50) NOT NULL,
        email VARCHAR(100),
        so_dien_thoai VARCHAR(15),
        so_tien INT
    )
''')

# Tạo bảng DichVu
cursor.execute('''
CREATE TABLE IF NOT EXISTS DichVu (
    dich_vu_id INT AUTO_INCREMENT PRIMARY KEY,
    ten_dich_vu VARCHAR(100) NOT NULL,
    anh_dich_vu VARCHAR(100),
    gia FLOAT NOT NULL
)
''')

# Tạo bảng HoaDon
cursor.execute('''
CREATE TABLE IF NOT EXISTS HoaDon (
    hoadon_id INT AUTO_INCREMENT PRIMARY KEY,
    nguoi_dung_id INT NOT NULL,
    may_id INT NOT NULL,
    thoi_gian_bat_dau DATETIME NOT NULL,
    thoi_gian_ket_thuc DATETIME,
    tong_tien FLOAT,
    trang_thai_hoa_don INT DEFAULT 0,
    FOREIGN KEY (nguoi_dung_id) REFERENCES NguoiDung(nguoi_dung_id),
    FOREIGN KEY (may_id) REFERENCES MayTram(may_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS ChiTietHoaDonDichVu (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hoa_don_id INT NOT NULL,
    dich_vu_id INT NOT NULL,
    so_luong INT NOT NULL,
    thanh_tien FLOAT NOT NULL,
    FOREIGN KEY (hoa_don_id) REFERENCES HoaDon(hoadon_id),
    FOREIGN KEY (dich_vu_id) REFERENCES DichVu(dich_vu_id)
)
''')

# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 1", "Đang nghỉ", "Asus 20 inch 120Hz Intel Core i5 RAM 8GB 250GB SATA 7200rpm", "7000", "phancungcobantrenmaytinh1-1614184775.jpg");''')
# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 2", "Đang nghỉ", "Asus 20 inch 120Hz Intel Core i5 RAM 8GB 250GB SATA 7200rpm", "7000", "phancungcobantrenmaytinh1-1614184775.jpg");''')
# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 3", "Đang nghỉ", "Asus 20 inch 120Hz Intel Core i5 RAM 8GB 250GB SATA 7200rpm", "7000", "phancungcobantrenmaytinh1-1614184775.jpg");''')
# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 4", "Đang nghỉ", "Asus 20 inch 120Hz Intel Core i5 RAM 8GB 250GB SATA 7200rpm", "7000", "phancungcobantrenmaytinh1-1614184775.jpg");''')
# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 5", "Đang nghỉ", "Asus 20 inch 120Hz Intel Core i5 RAM 8GB 250GB SATA 7200rpm", "7000", "phancungcobantrenmaytinh1-1614184775.jpg");''')
# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 6", "Đang nghỉ", "LG 22 inch 120Hz Intel Core i5-3470 RAM 8GB 500GB SATA 7200rpm Cooler Master 400w Fan 12", "9000", "phancungcobantrenmaytinh1-1614184775.jpg");''')
# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 7", "Đang nghỉ", "LG 22 inch 120Hz Intel Core i5-3470 RAM 8GB 500GB SATA 7200rpm Cooler Master 400w Fan 12", "9000", "phancungcobantrenmaytinh1-1614184775.jpg");''')
# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 8", "Hoạt động", "LG 22 inch 120Hz Intel Core i5-3470 RAM 8GB 500GB SATA 7200rpm Cooler Master 400w Fan 12", "9000", "phancungcobantrenmaytinh1-1614184775.jpg");''')
# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 9", "Đang nghỉ", "LG 22 inch 120Hz Intel Core i5-3470 RAM 8GB 500GB SATA 7200rpm Cooler Master 400w Fan 12", "9000", "phancungcobantrenmaytinh1-1614184775.jpg");''')
# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 10", "Đang nghỉ", "LG 22 inch 120Hz Intel Core i5-3470 RAM 8GB 500GB SATA 7200rpm Cooler Master 400w Fan 12", "9000", "phancungcobantrenmaytinh1-1614184775.jpg");''')
# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 11", "Hoạt động", "LG 22 inch 144Hz Intel Core i5-6500 Socket 1151 VGA Card Zotac GTX 1080 AMP Case KNIGHT SILENT", "10000", "phancungcobantrenmaytinh1-1614184775.jpg");''')
# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 12", "Đang nghỉ", "LG 22 inch 144Hz Intel Core i5-6500 Socket 1151 VGA Card Zotac GTX 1080 AMP Case KNIGHT SILENT", "10000", "phancungcobantrenmaytinh1-1614184775.jpg");''')
# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 13", "Đang nghỉ", "LG 22 inch 144Hz Intel Core i5-6500 Socket 1151 VGA Card Zotac GTX 1080 AMP Case KNIGHT SILENT", "10000", "phancungcobantrenmaytinh1-1614184775.jpg");''')
# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 14", "Hoạt động", "LG 22 inch 144Hz Intel Core i5-6500 Socket 1151 VGA Card Zotac GTX 1080 AMP Case KNIGHT SILENT", "10000", "phancungcobantrenmaytinh1-1614184775.jpg");''')
# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 15", "Đang nghỉ", "LG 22 inch 144Hz Intel Core i5-6500 Socket 1151 VGA Card Zotac GTX 1080 AMP Case KNIGHT SILENT", "10000", "may-tinh-quan-net-thanh-ly-4.jpg");''')
# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 16", "Đang nghỉ", "Asus 22 inch 144Hz Intel Core i3-12100F Box SSD Patriot 128Gb P210 Sata3 2.5 VGA Asus 6GB DUAL RTX 2060 O6G EVO Case Asus TUF Gaming GT301", "12000", "phancungcobantrenmaytinh1-1614184775.jpg");''')
# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 17", "Đang nghỉ", "Asus 22 inch 144Hz Intel Core i3-12100F Box SSD Patriot 128Gb P210 Sata3 2.5 VGA Asus 6GB DUAL RTX 2060 O6G EVO Case Asus TUF Gaming GT301", "12000", "phancungcobantrenmaytinh1-1614184775.jpg");''')
# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 18", "Hoạt động", "Asus 22 inch 144Hz Intel Core i3-12100F Box SSD Patriot 128Gb P210 Sata3 2.5 VGA Asus 6GB DUAL RTX 2060 O6G EVO Case Asus TUF Gaming GT301", "12000", "phancungcobantrenmaytinh1-1614184775.jpg");''')
# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 19", "Đang nghỉ", "Asus 22 inch 144Hz Intel Core i3-12100F Box SSD Patriot 128Gb P210 Sata3 2.5 VGA Asus 6GB DUAL RTX 2060 O6G EVO Case Asus TUF Gaming GT301", "12000", "may-tinh-quan-net-thanh-ly-4.jpg");''')
# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 20", "Đang nghỉ", "Asus 22 inch 144Hz Intel Core i3-12100F Box SSD Patriot 128Gb P210 Sata3 2.5 VGA Asus 6GB DUAL RTX 2060 O6G EVO Case Asus TUF Gaming GT301", "12000", "may-tinh-quan-net-thanh-ly-4.jpg");''') 
# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 21", "Hoạt động", "Asus 22 inch 144Hz Intel Core i3-12100F Box SSD Patriot 128Gb P210 Sata3 2.5 VGA Asus 6GB DUAL RTX 2060 O6G EVO Case Asus TUF Gaming GT301", "12000", "may-tinh-quan-net-thanh-ly-4.jpg");''') 
# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 22", "Đang nghỉ", "Asus 22 inch 144Hz Intel Core i3-12100F Box SSD Patriot 128Gb P210 Sata3 2.5 VGA Asus 6GB DUAL RTX 2060 O6G EVO Case Asus TUF Gaming GT301", "12000", "may-tinh-quan-net-thanh-ly-4.jpg");''') 
# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 23", "Đang nghỉ", "Asus 22 inch 144Hz Intel Core i3-12100F Box SSD Patriot 128Gb P210 Sata3 2.5 VGA Asus 6GB DUAL RTX 2060 O6G EVO Case Asus TUF Gaming GT301", "12000", "may-tinh-quan-net-thanh-ly-4.jpg");''') 
# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 24", "Đang nghỉ", "Asus 22 inch 144Hz Intel Core i3-12100F Box SSD Patriot 128Gb P210 Sata3 2.5 VGA Asus 6GB DUAL RTX 2060 O6G EVO Case Asus TUF Gaming GT301", "12000", "may-tinh-quan-net-thanh-ly-4.jpg");''') 
# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 25", "Đang nghỉ", "27 ICNH 240HZ CPU Intel i9 9900k RAM 16G Bus 2666 VGA GTX 2060 6G GDDR5 Nguồn Ximatek 600W chuột Logitech G403", "15000", "may-tinh-quan-net-thanh-ly-4.jpg");''') 
# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 26", "Đang nghỉ", "27 ICNH 240HZ CPU Intel i9 9900k RAM 16G Bus 2666 VGA GTX 2060 6G GDDR5 Nguồn Ximatek 600W chuột Logitech G403", "15000", "may-tinh-quan-net-thanh-ly-4.jpg");''') 
# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 27", "Đang nghỉ", "27 ICNH 240HZ CPU Intel i9 9900k RAM 16G Bus 2666 VGA GTX 2060 6G GDDR5 Nguồn Ximatek 600W chuột Logitech G403", "15000", "may-tinh-quan-net-thanh-ly-4.jpg");''') 
# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 28", "Đang nghỉ", "27 ICNH 240HZ CPU Intel i9 9900k RAM 16G Bus 2666 VGA GTX 2060 6G GDDR5 Nguồn Ximatek 600W chuột Logitech G403", "15000", "may-tinh-quan-net-thanh-ly-4.jpg");''') 
# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 29", "Đang nghỉ", "27 ICNH 240HZ CPU Intel i9 9900k RAM 16G Bus 2666 VGA GTX 2060 6G GDDR5 Nguồn Ximatek 600W chuột Logitech G403", "15000", "may-tinh-quan-net-thanh-ly-4.jpg");''') 
# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 30", "Đang nghỉ", "27 ICNH 240HZ CPU Intel i9 9900k RAM 16G Bus 2666 VGA GTX 2060 6G GDDR5 Nguồn Ximatek 600W chuột Logitech G403", "15000", "may-tinh-quan-net-thanh-ly-4.jpg");''') 
# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 31", "Đang nghỉ", " 27 inch Full HD, IPS 144HZ  Core i5 9400F / 9M Cache RAM  DDR4 16GB bus 2666 VGA GTX 1660ti 6G DDR5 Mainboard B365 Ximatek A450  450W công xuất thực", "18000", "may-tinh-quan-net-thanh-ly-4.jpg");''') 
# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 32", "Đang nghỉ", " 27 inch Full HD, IPS 144HZ  Core i5 9400F / 9M Cache RAM  DDR4 16GB bus 2666 VGA GTX 1660ti 6G DDR5 Mainboard B365 Ximatek A450  450W công xuất thực", "18000", "may-tinh-quan-net-thanh-ly-4.jpg");''') 
# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 33", "Đang nghỉ", " 27 inch Full HD, IPS 144HZ  Core i5 9400F / 9M Cache RAM  DDR4 16GB bus 2666 VGA GTX 1660ti 6G DDR5 Mainboard B365 Ximatek A450  450W công xuất thực", "18000", "may-tinh-quan-net-thanh-ly-4.jpg");''') 
# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 34", "Đang nghỉ", " 27 inch Full HD, IPS 144HZ  Core i5 9400F / 9M Cache RAM  DDR4 16GB bus 2666 VGA GTX 1660ti 6G DDR5 Mainboard B365 Ximatek A450  450W công xuất thực", "18000", "may-tinh-quan-net-thanh-ly-4.jpg");''') 
# cursor.execute('''INSERT INTO MayTram (ten_may, trang_thai, mo_ta, may_don_gia, anh_may) VALUES ("Máy 35", "Đang nghỉ", " 27 inch Full HD, IPS 144HZ  Core i5 9400F / 9M Cache RAM  DDR4 16GB bus 2666 VGA GTX 1660ti 6G DDR5 Mainboard B365 Ximatek A450  450W công xuất thực", "18000", "may-tinh-quan-net-thanh-ly-4.jpg");''') 

# cursor.execute('''INSERT INTO DichVu (ten_dich_vu, anh_dich_vu, gia) VALUES ("20 gói tăm cay que cay", "tamcay.jpg", "30000");''')
# cursor.execute('''INSERT INTO DichVu (ten_dich_vu, anh_dich_vu, gia) VALUES ("500G Bim Bim Tăm Đậu Hà Lan, Snack Que Bim Tăm Thái, đồ ăn vặt hot, đồ 1k", "que.jpg", "15000");''')
# cursor.execute('''INSERT INTO DichVu (ten_dich_vu, anh_dich_vu, gia) VALUES ("Bim Bim Cà Chua Khổng Lồ", "vn-11134207-7r98o-ltqgfpzxx1cdfc.jpg", "45000");''')
# cursor.execute('''INSERT INTO DichVu (ten_dich_vu, anh_dich_vu, gia) VALUES ("Snack bim bim cánh gà chiên giòn (gói 26g)", "0b2111257ff7cb12ffad61017c47c0a7.jpg", "3000");''')
# cursor.execute('''INSERT INTO DichVu (ten_dich_vu, anh_dich_vu, gia) VALUES ("Snack bim bim que Mix Vfoods 50g", "15a3ae66e37d204e34899af807b05050.jpg", "15000");''')
# cursor.execute('''INSERT INTO DichVu (ten_dich_vu, anh_dich_vu, gia) VALUES ("Oishi - Snack cay tôm", "vn-11134207-7r98o-lnmfl6k7wjqlf1.jpg", "7000");''')
# cursor.execute('''INSERT INTO DichVu (ten_dich_vu, anh_dich_vu, gia) VALUES ("Combo oishi", "vn-11134207-7r98o-lnmfl6k7bh7xe6.jpg", "10000");''')
# cursor.execute('''INSERT INTO DichVu (ten_dich_vu, anh_dich_vu, gia) VALUES ("Nước Ép Táo Xanh AUFINE 150ml", "sg-11134201-23020-cjld23i8fdnv47.jpg", "15000");''')
# cursor.execute('''INSERT INTO DichVu (ten_dich_vu, anh_dich_vu, gia) VALUES ("CoCa CoLa", "vn-11134207-7r98o-lw7f2ff9vbvdd6.jpg", "8000");''')
# cursor.execute('''INSERT INTO DichVu (ten_dich_vu, anh_dich_vu, gia) VALUES ("Sting", "sg-11134201-22110-qcdc1e95g5jv1e.jpg", "15000");''')
# cursor.execute('''INSERT INTO DichVu (ten_dich_vu, anh_dich_vu, gia) VALUES ("Mirinda", "vn-11134207-7r98o-lptal6stjy6qb2.jpg", "15000");''')
# cursor.execute('''INSERT INTO DichVu (ten_dich_vu, anh_dich_vu, gia) VALUES ("Nước cốt hoa Atiso đỏ BerryLand chai 500ml", "4874b2f865e536938bc7dfc0adbcd665.jpg", "39000");''')

# cursor.execute('''INSERT INTO HoaDon (nguoi_dung_id, may_id, thoi_gian_bat_dau, thoi_gian_ket_thuc, tong_tien, trang_thai_hoa_don)
#                   VALUES ("2", "1", "2024-07-02 12:00:00", "2024-07-02 15:00:00", 100000, 1);''')
# cursor.execute('''INSERT INTO HoaDon (nguoi_dung_id, may_id, thoi_gian_bat_dau, thoi_gian_ket_thuc, tong_tien, trang_thai_hoa_don)
#                   VALUES ("4", "2", "2024-07-02 12:00:00", "2024-07-02 15:00:00", 100000, 1);''')
# cursor.execute('''INSERT INTO HoaDon (nguoi_dung_id, may_id, thoi_gian_bat_dau, thoi_gian_ket_thuc, tong_tien, trang_thai_hoa_don)
#                   VALUES ("5", "3", "2024-07-02 12:00:00", "2024-07-02 15:00:00", 100000, 1);''')

cursor.execute('''INSERT INTO ChiTietHoaDonDichVu (hoa_don_id, dich_vu_id, so_luong, thanh_tien)
                  VALUES ("1", "3", "2", 100000);''')
cursor.execute('''INSERT INTO ChiTietHoaDonDichVu (hoa_don_id, dich_vu_id, so_luong, thanh_tien)
                  VALUES ("3", "7", "4", 100000);''')
cursor.execute('''INSERT INTO ChiTietHoaDonDichVu (hoa_don_id, dich_vu_id, so_luong, thanh_tien)
                  VALUES ("4", "8", "3", 100000);''')

# cursor.execute(sql, val)
connection.commit()

print(cursor.rowcount, "record inserted.")

# Đóng kết nối
cursor.close()
connection.close()
