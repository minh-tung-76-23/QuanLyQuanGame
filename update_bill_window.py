import tkinter as tk
from tkinter import *
from tkinter import messagebox
import mysql.connector
from PIL import Image, ImageTk
import os
from datetime import datetime

class UpdateBillWindow:
    def __init__(self, root, may_id, ten_may, trang_thai, may_don_gia, hoadon_id):
        self.root = root
        self.may_id = may_id
        self.ten_may = ten_may
        self.trang_thai = trang_thai
        self.may_don_gia = may_don_gia
        self.hoadon_id = hoadon_id
        
        if isinstance(self.hoadon_id, tuple) and len(self.hoadon_id) == 1:
            self.hoadon_id = self.hoadon_id[0]  

        self.root.title("Quản lý quán game - Hoá đơn đang dùng")
        self.root.geometry('1530x750+0+20')

        # Thiết lập kết nối
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="quanlyquangame"
        )
        self.cursor = self.connection.cursor()

        # Khởi tạo giao diện
        self.init_ui()
        self.selected_services = []  

    def init_ui(self):
        # Tạo frame chính
        main_frame = Frame(self.root)
        main_frame.pack(fill=BOTH, expand=True)

        # Frame bên trái để hiển thị danh sách dịch vụ
        left_frame = Frame(main_frame, width=300, bd=1, relief=RIDGE)
        left_frame.pack(side=LEFT, fill=Y)

        # Tạo một vùng có thể cuộn được
        self.canvas = Canvas(left_frame)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        # Thêm thanh cuộn bên phải và di chuyển sang bên phải 200 pixel
        scrollbar = Scrollbar(left_frame, orient=VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Tạo frame con để chứa nội dung của Canvas
        self.services_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.services_frame, anchor=NW)

        # Hiển thị danh sách dịch vụ
        self.display_services()

        # Bind sự kiện cuộn cho Canvas
        self.services_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Cài đặt độ rộng của thanh cuộn bên phải
        scrollbar_width = 20  # Độ rộng của thanh cuộn
        self.canvas.config(width=870 + scrollbar_width)

        # Frame bên phải để hiển thị thông tin của máy
        right_frame = Frame(main_frame, bd=1, relief=RIDGE)
        right_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # Hiển thị thông tin của máy
        self.display_machine_info(right_frame,self.trang_thai, self.hoadon_id)

    def display_services(self):
        try:
            self.cursor.execute("SELECT dich_vu_id, ten_dich_vu, anh_dich_vu, gia FROM DichVu")
            services = self.cursor.fetchall()

            # Tính toán số dịch vụ trên mỗi hàng
            num_services_per_row = 3
            for i, (id_dich_vu, ten_dich_vu, anh_dich_vu, gia) in enumerate(services):
                # Tính toán vị trí của dịch vụ trong grid
                row = i // num_services_per_row
                col = i % num_services_per_row

                # Tạo một Frame con để chứa thông tin dịch vụ
                service_frame = Frame(self.services_frame, bd=2, relief=GROOVE, width=300, height=220)
                service_frame.grid(row=row, column=col, padx=30, pady=10, sticky=NSEW)

                # Tạo một Label để hiển thị tên dịch vụ
                label_name = Label(service_frame, text=ten_dich_vu, height=3, font=("Arial", 13, "bold"), fg="red", wraplength=250)
                label_name.pack(pady=2)

                # Hiển thị ảnh dịch vụ
                image_path = f'F:\\LT_IT\\PY\\Woskspace\\QuanLyQuanGame\\img\\{anh_dich_vu}'
                if os.path.exists(image_path):
                    image = Image.open(image_path)
                    image = image.resize((100, 100), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    label_image = Label(service_frame, image=photo)
                    label_image.image = photo  # Giữ tham chiếu để không bị hủy
                    label_image.pack(pady=10)
                else:
                    messagebox.showerror("Lỗi", f"Không tìm thấy ảnh: {image_path}")

                # Hiển thị giá dịch vụ
                formatted_price = "{:,.0f}".format(gia)
                label_price = Label(service_frame, text=f"Giá: {formatted_price} đ", font=("Arial", 10))
                label_price.pack(pady=5)

                # Xử lý sự kiện click để hiển thị thông tin chi tiết dịch vụ
                service_frame.bind("<Button-1>", lambda event,dich_vu_id = id_dich_vu, service_name=ten_dich_vu, service_price = gia: self.show_service_info(dich_vu_id, service_name, service_price))

        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Lỗi khi truy vấn dữ liệu: {err}")

    def display_machine_info(self, frame,trang_thai, hoadon_id):
        # Hiển thị thông tin của máy
        lbl_title = Label(frame, text=f"Hóa đơn máy {self.may_id}", font=("Arial", 16, "bold"))
        lbl_title.pack(pady=20)

        # Label giá thuê máy
        lbl_may_don_gia = Label(frame, text=f"Giá thuê: {self.may_don_gia}đ/h", font=("Arial", 11))
        lbl_may_don_gia.pack()

        # Tạo frame con để chứa phần thông tin trạng thái và dịch vụ được chọn
        info_frame = Frame(frame)
        info_frame.pack(pady=10)

        # Label để chỉ định phần trạng thái
        lbl_trang_thai_title = Label(info_frame, text="Trạng thái máy:", font=("Arial", 12))
        lbl_trang_thai_title.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        # Biến để lưu trạng thái máy
        self.var_trang_thai = StringVar(self.root)
        self.var_trang_thai.set(trang_thai)  

        # Danh sách các tùy chọn
        trang_thai_options = ["Đang nghỉ", "Hoạt động"]

        # OptionMenu để chọn trạng thái
        option_menu = OptionMenu(info_frame, self.var_trang_thai, *trang_thai_options)
        option_menu.grid(row=0, column=1, padx=10, pady=10, sticky=W)

        # Label để hiển thị thông tin tài khoản và số dư
        lbl_account_title = Label(info_frame, text="Tài khoản:", font=("Arial", 12))
        lbl_account_title.grid(row=1, column=0, padx=10, pady=10, sticky=W)

        self.lbl_account_name = Label(info_frame, text="", font=("Arial", 12))
        self.lbl_account_name.grid(row=1, column=1, padx=10, pady=10, sticky=W)

        lbl_balance_title = Label(info_frame, text="Số dư:", font=("Arial", 12))
        lbl_balance_title.grid(row=1, column=2, padx=10, pady=10, sticky=W)

        self.lbl_balance_amount = Label(info_frame, text="", font=("Arial", 12))
        self.lbl_balance_amount.grid(row=1, column=3, padx=10, pady=10, sticky=W)

        # Entry để nhập thời gian bắt đầu
        self.var_thoi_gian_bat_dau = StringVar(self.root)
        entry_thoi_gian_bat_dau = Entry(info_frame, font=("Arial", 12), textvariable=self.var_thoi_gian_bat_dau)
        entry_thoi_gian_bat_dau.grid(row=2, column=1, padx=10, pady=10, sticky=W)
        lbl_thoi_gian_bat_dau = Label(info_frame, text="Thời gian bắt đầu:", font=("Arial", 12))
        lbl_thoi_gian_bat_dau.grid(row=2, column=0, padx=10, pady=10, sticky=W)

        # Entry để nhập thời gian kết thúc
        self.var_thoi_gian_ket_thuc = StringVar(self.root)
        entry_thoi_gian_ket_thuc = Entry(info_frame, font=("Arial", 12), textvariable=self.var_thoi_gian_ket_thuc)
        entry_thoi_gian_ket_thuc.grid(row=3, column=1, padx=10, pady=10, sticky=W)
        lbl_thoi_gian_ket_thuc = Label(info_frame, text="Thời gian kết thúc:", font=("Arial", 12))
        lbl_thoi_gian_ket_thuc.grid(row=3, column=0, padx=10, pady=10, sticky=W)

        # Label để hiển thị số giờ
        self.lbl_so_gio = Label(info_frame, text="", font=("Arial", 12))
        self.lbl_so_gio.grid(row=2, column=2, padx=10, pady=10, sticky=W)

        # Label để hiển thị số tiền theo giờ
        self.lbl_tien = Label(info_frame, text="", font=("Arial", 12))
        self.lbl_tien.grid(row=3, column=2, padx=10, pady=10, sticky=W)

        # Theo dõi thay đổi của entry_thoi_gian_ket_thuc
        self.var_thoi_gian_ket_thuc.trace_add("write", lambda *args: self.update_hours())

        # Tạo frame con để chứa nút thanh toán và lưu
        button_frame = Frame(frame)
        button_frame.pack(side=BOTTOM, padx=10, pady=10)

        # Button để thanh toán
        btn_thanh_toan = Button(button_frame, text="Thanh toán", font=("Arial", 12), command=self.thanh_toan)
        btn_thanh_toan.pack(side=LEFT, padx=10, pady=10)

        # Button để lưu
        btn_luu = Button(button_frame, text="Lưu", font=("Arial", 12))
        btn_luu.pack(side=LEFT, padx=10, pady=10)

        # Label để hiển thị thông tin dịch vụ đã chọn
        lbl_selected_services_title = Label(frame, text="Dịch vụ đã chọn:", font=("Arial", 12))
        lbl_selected_services_title.pack(pady=10)

        # Tạo một frame để hiển thị danh sách dịch vụ đã chọn
        self.selected_services_frame = Frame(frame)
        self.selected_services_frame.pack()

        # Danh sách để lưu các widget dịch vụ đã chọn
        self.selected_service_widgets = []
        self.selected_service_prices = {}

        # Label để hiển thị tổng tiền
        self.lbl_tong_tien = Label(frame, text="Tổng tiền: 0đ", font=("Arial", 12, "bold"))
        self.lbl_tong_tien.pack(pady=10)

        self.load_rev_save(hoadon_id)

    def select_user_by_id(self, nguoi_dung_id):
        # Thực hiện truy vấn SQL để lấy thông tin người dùng từ nguoi_dung_id
        query = "SELECT tai_khoan, so_tien FROM NguoiDung WHERE nguoi_dung_id = %s"
        self.cursor.execute(query, (nguoi_dung_id,))
        return self.cursor.fetchone()

    def load_rev_save(self, hoadon_id):
        # Trích xuất hoadon_id từ tuple

        # Truy vấn hóa đơn để lấy nguoi_dung_id
        query = "SELECT nguoi_dung_id, thoi_gian_bat_dau, thoi_gian_ket_thuc FROM HoaDon WHERE hoadon_id = %s"
        self.cursor.execute(query, (hoadon_id,))
        result = self.cursor.fetchone()

        if result:
            nguoi_dung_id = result[0]
            thoi_gian_bat_dau = result[1]
            thoi_gian_ket_thuc = result[2]

            # Lấy thông tin người dùng từ nguoi_dung_id
            user_info = self.select_user_by_id(nguoi_dung_id)

            if user_info:
                tai_khoan = user_info[0]
                so_du = user_info[1]

                # Hiển thị thông tin tên và số dư
                self.lbl_account_name.config(text=tai_khoan)
                formatted_price = "{:,.0f}".format(so_du)
                self.lbl_balance_amount.config(text=f"{formatted_price} đ")

            # Gán giá trị cho các Entry
            self.var_thoi_gian_bat_dau.set(thoi_gian_bat_dau)
            self.var_thoi_gian_ket_thuc.set(thoi_gian_ket_thuc)

        # Hiển thị danh sách dịch vụ đã chọn
        # Xóa các widget cũ trong selected_services_frame trước khi thêm mới
        for widget in self.selected_service_widgets:
            widget['frame'].destroy()
        self.selected_service_widgets = []
        self.selected_services = []
        # Truy vấn SQL để lấy thông tin từ ChiTietHoaDonDichVu dựa trên hoa_don_id
        query = '''
        SELECT dv.ten_dich_vu, dv.gia, cthd.so_luong, cthd.thanh_tien, cthd.dich_vu_id
        FROM ChiTietHoaDonDichVu cthd
        JOIN DichVu dv ON cthd.dich_vu_id = dv.dich_vu_id
        WHERE cthd.hoa_don_id = %s
        '''
        self.cursor.execute(query, (hoadon_id,))
        chi_tiet_dich_vu = self.cursor.fetchall()

        # Hiển thị thông tin lên giao diện
        for row in chi_tiet_dich_vu:
            ten_dich_vu = row[0]
            gia = row[1]
            so_luong = row[2]
            gia = row[3]
            dich_vu_id = row[4]
            
            # Nếu dịch vụ chưa tồn tại trong danh sách đã chọn, thêm mới
            service_frame = Frame(self.selected_services_frame)
            service_frame.pack(pady=5, padx=10, fill=X)

            lbl_ten_dich_vu = Label(service_frame, text=ten_dich_vu, font=("Arial", 12), width=20, wraplength=150)
            lbl_ten_dich_vu.grid(row=0, column=0, padx=10, pady=5, sticky=W)

            lbl_gia = Label(service_frame, text=f"{gia} đ", font=("Arial", 12), width=10)
            lbl_gia.grid(row=0, column=1, padx=10, pady=5, sticky=W)

            var_so_luong = IntVar(service_frame, value=so_luong)
            var_so_luong.set(1)
            entry_so_luong = Entry(service_frame, font=("Arial", 12), textvariable=var_so_luong, width=4)
            entry_so_luong.grid(row=0, column=2, padx=20, pady=5, sticky=W)

            # Button tăng số lượng
            btn_tang = Button(service_frame, text="+", command=lambda: self.tang_so_luong(var_so_luong))
            btn_tang.grid(row=0, column=2, padx=(0, 10), pady=5, sticky=E)

            # Button giảm số lượng
            btn_giam = Button(service_frame, text="-", command=lambda: self.giam_so_luong(var_so_luong))
            btn_giam.grid(row=0, column=2, padx=(0, 80), pady=5, sticky=E)

            lbl_thanh_tien_value = Label(service_frame, text=f"{gia} đ", font=("Arial", 12))
            lbl_thanh_tien_value.grid(row=0, column=3, padx=10, pady=5, sticky=W)

            btn_xoa = Button(service_frame, text="Xóa", command=lambda: self.xoa_dich_vu_chon(service_frame))
            btn_xoa.grid(row=0, column=4, padx=10, pady=5, sticky=W)

            self.selected_service_widgets.append({
                'frame': service_frame,
                'lbl_ten_dich_vu': lbl_ten_dich_vu,
                'lbl_gia': lbl_gia,
                'var_so_luong': var_so_luong,
                'lbl_thanh_tien_value': lbl_thanh_tien_value,
                'gia': gia,
                'dich_vu_id': dich_vu_id  
            })

            self.selected_services.append({
                'ten_dich_vu': ten_dich_vu,
                'gia': gia,
                'var_so_luong': var_so_luong,
                'lbl_thanh_tien_value': lbl_thanh_tien_value
            })
        self.update_thanh_tien()
        
        print(self.selected_services)

    def update_hours(self):
        try:
            thoi_gian_bat_dau = datetime.strptime(self.var_thoi_gian_bat_dau.get(), '%Y-%m-%d %H:%M:%S')
            thoi_gian_ket_thuc = datetime.strptime(self.var_thoi_gian_ket_thuc.get(), '%Y-%m-%d %H:%M:%S')

            # Tính số giờ giữa thời gian bắt đầu và thời gian kết thúc
            delta = thoi_gian_ket_thuc - thoi_gian_bat_dau
            hours = delta.total_seconds() / 3600  # Chuyển đổi sang giờ

            # Làm tròn số giờ đến 2 chữ số sau dấu thập phân
            rounded_hours = round(hours, 2)
            
            # Hiển thị số giờ lên giao diện
            self.lbl_so_gio.config(text=f"{rounded_hours} tiếng")

            # Tính số tiền thuê máy
            total_rent_cost = rounded_hours * self.may_don_gia
            formatted_rent_cost = "{:,.0f}".format(total_rent_cost)
            self.lbl_tien.config(text=f"{formatted_rent_cost} đ")

            # Cập nhật tổng tiền
            self.update_thanh_tien()
        except ValueError:
            pass

    def show_service_info(self, dich_vu_id, ten_dich_vu, gia):
        print(self.selected_services)
        for service in self.selected_services:
            if service['ten_dich_vu'] == ten_dich_vu:
                # Nếu tồn tại rồi thì tăng số lượng lên 1 và cập nhật lại giao diện
                service['var_so_luong'].set(service['var_so_luong'].get() + 1)
                self.update_thanh_tien()
                return

        # Nếu dịch vụ chưa tồn tại trong danh sách đã chọn, thêm mới
        service_frame = Frame(self.selected_services_frame)
        service_frame.pack(pady=5, padx=10, fill=X)

        lbl_ten_dich_vu = Label(service_frame, text=ten_dich_vu, font=("Arial", 12), width=20, wraplength=150)
        lbl_ten_dich_vu.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        lbl_gia = Label(service_frame, text=f"{gia} đ", font=("Arial", 12), width=10)
        lbl_gia.grid(row=0, column=1, padx=10, pady=5, sticky=W)

        var_so_luong = IntVar(service_frame)
        var_so_luong.set(1)
        entry_so_luong = Entry(service_frame, font=("Arial", 12), textvariable=var_so_luong, width=4)
        entry_so_luong.grid(row=0, column=2, padx=20, pady=5, sticky=W)

        # Button tăng số lượng
        btn_tang = Button(service_frame, text="+", command=lambda: self.tang_so_luong(var_so_luong))
        btn_tang.grid(row=0, column=2, padx=(0, 10), pady=5, sticky=E)

        # Button giảm số lượng
        btn_giam = Button(service_frame, text="-", command=lambda: self.giam_so_luong(var_so_luong))
        btn_giam.grid(row=0, column=2, padx=(0, 80), pady=5, sticky=E)

        lbl_thanh_tien_value = Label(service_frame, text=f"{gia} đ", font=("Arial", 12))
        lbl_thanh_tien_value.grid(row=0, column=3, padx=10, pady=5, sticky=W)

        btn_xoa = Button(service_frame, text="Xóa", command=lambda: self.xoa_dich_vu_chon(service_frame))
        btn_xoa.grid(row=0, column=4, padx=10, pady=5, sticky=W)

        self.selected_service_widgets.append({
            'frame': service_frame,
            'lbl_ten_dich_vu': lbl_ten_dich_vu,
            'lbl_gia': lbl_gia,
            'var_so_luong': var_so_luong,
            'lbl_thanh_tien_value': lbl_thanh_tien_value,
            'gia': gia,
            'dich_vu_id': dich_vu_id  
        })

        # Thêm dịch vụ vào danh sách đã chọn
        self.selected_services.append({
            'ten_dich_vu': ten_dich_vu,
            'gia': gia,
            'var_so_luong': var_so_luong,
            'lbl_thanh_tien_value': lbl_thanh_tien_value
        })
        self.update_thanh_tien()


    def update_thanh_tien(self):
        # Lấy giá trị từ lbl_tien và loại bỏ các ký tự không phải số
        tien_str = self.lbl_tien.cget("text")
        if tien_str:
            tien_str = tien_str.replace("đ", "").replace(",", "").strip()
            rent_cost = float(tien_str) if tien_str else 0
        else:
            rent_cost = 0

        total_cost = rent_cost
        for widget in self.selected_service_widgets:
            gia = widget['gia']  # Đã là kiểu float
            so_luong = widget['var_so_luong'].get()
            thanh_tien = gia * so_luong
            total_cost += thanh_tien
            formatted_price = "{:,.0f}".format(thanh_tien)
            widget['lbl_thanh_tien_value'].config(text=f"{formatted_price} đ")

        # Update total cost label
        formatted_total_cost = "{:,.0f}".format(total_cost)
        self.lbl_tong_tien.config(text=f"Tổng tiền: {formatted_total_cost} đ")


    def tang_so_luong(self, var_so_luong):
        current_qty = var_so_luong.get()
        var_so_luong.set(current_qty + 1)
        self.update_thanh_tien()

    def giam_so_luong(self, var_so_luong):
        current_qty = var_so_luong.get()
        if current_qty > 0:
            var_so_luong.set(current_qty - 1)
            self.update_thanh_tien()

    def xoa_dich_vu_chon(self, service_frame):
        # Xóa dịch vụ được chọn khỏi danh sách và khung hiển thị
        for widget in self.selected_service_widgets:
            if widget['frame'] == service_frame:
                widget['frame'].destroy()
                self.selected_service_widgets.remove(widget)
                break

        self.update_thanh_tien()

    def thanh_toan(self):
        try:
            # Lấy thông tin cần thiết
            tai_khoan = self.lbl_account_name.cget("text")
            thoi_gian_bat_dau = self.var_thoi_gian_bat_dau.get()
            thoi_gian_ket_thuc = self.var_thoi_gian_ket_thuc.get()
            may_id = self.may_id
            tong_tien_text = self.lbl_tong_tien.cget("text")
            tong_tien_value = tong_tien_text.split(": ")[1]  # Lấy phần số tiền sau dấu hai chấm
            tong_tien_value = tong_tien_value.replace("đ", "").replace(",", "").strip()
            rent_total = float(tong_tien_value)
            print(rent_total)

            # Cập nhật trạng thái máy
            self.cursor.execute("UPDATE MayTram SET trang_thai = %s WHERE may_id = %s", (self.var_trang_thai.get(), may_id))

            # Cập nhật số dư người dùng
            self.cursor.execute("SELECT so_tien FROM NguoiDung WHERE tai_khoan = %s", (tai_khoan,))
            current_balance = self.cursor.fetchone()[0]
            new_balance = current_balance - rent_total
            self.cursor.execute("UPDATE NguoiDung SET so_tien = %s WHERE tai_khoan = %s", (new_balance, tai_khoan))

            # Update hóa đơn
            self.cursor.execute('''
                UPDATE HoaDon 
                SET tong_tien = %s, trang_thai_hoa_don = "1" 
                WHERE hoadon_id = %s
            ''', (rent_total, self.hoadon_id,))

            # Xóa các chi tiết hóa đơn cũ
            self.cursor.execute("DELETE FROM ChiTietHoaDonDichVu WHERE hoa_don_id = %s", (self.hoadon_id,))

            # Tạo chi tiết hóa đơn mới cho các dịch vụ đã chọn
            for widget in self.selected_service_widgets:
                dich_vu_id = widget['dich_vu_id']
                so_luong = widget['var_so_luong'].get()
                thanh_tien = widget['gia'] * so_luong
                self.cursor.execute('''
                    INSERT INTO ChiTietHoaDonDichVu (hoa_don_id, dich_vu_id, so_luong, thanh_tien) 
                    VALUES (%s, %s, %s, %s)
                ''', (self.hoadon_id, dich_vu_id, so_luong, thanh_tien))

            # Commit transaction
            self.connection.commit()

            # Hiển thị thông báo thanh toán thành công
            messagebox.showinfo("Thanh toán", "Thanh toán thành công!")

            # Gửi thông báo đến main.py để load lại danh sách máy
            self.root.destroy()

        except Exception as e:
            # Rollback transaction nếu có lỗi
            self.connection.rollback()
            messagebox.showerror("Lỗi", f"Đã có lỗi xảy ra: {str(e)}")


    def save_rev(self):
        try:
            # Lấy thông tin cần thiết
            tai_khoan = self.lbl_account_name.cget("text")
            thoi_gian_bat_dau = self.var_thoi_gian_bat_dau.get()
            thoi_gian_ket_thuc = self.var_thoi_gian_ket_thuc.get()
            may_id = self.may_id
            tong_tien_text = self.lbl_tong_tien.cget("text")
            tong_tien_value = tong_tien_text.split(": ")[1]  # Lấy phần số tiền sau dấu hai chấm
            tong_tien_value = tong_tien_value.replace("đ", "").replace(",", "").strip()
            rent_total = float(tong_tien_value)
            print(rent_total)

            # Cập nhật trạng thái máy
            self.cursor.execute("UPDATE MayTram SET trang_thai = %s WHERE may_id = %s", (self.var_trang_thai.get(), may_id))

            # Cập nhật số dư người dùng
            # self.cursor.execute("SELECT so_tien FROM NguoiDung WHERE tai_khoan = %s", (tai_khoan,))
            # current_balance = self.cursor.fetchone()[0]
            # new_balance = current_balance - rent_total
            # self.cursor.execute("UPDATE NguoiDung SET so_tien = %s WHERE tai_khoan = %s", (new_balance, tai_khoan))

            # Update hóa đơn
            self.cursor.execute('''
                UPDATE HoaDon 
                SET tong_tien = %s, trang_thai_hoa_don = "0" 
                WHERE hoadon_id = %s
            ''', (rent_total, self.hoadon_id,))

            # Tạo chi tiết hóa đơn cho các dịch vụ đã chọn
            for widget in self.selected_service_widgets:
                dich_vu_id = widget['dich_vu_id']
                so_luong = widget['var_so_luong'].get()
                thanh_tien = widget['gia'] * so_luong
                self.cursor.execute('''
                    INSERT INTO ChiTietHoaDonDichVu (hoa_don_id, dich_vu_id, so_luong, thanh_tien) 
                    VALUES (%s, %s, %s, %s)
                ''', (self.hoadon_id, dich_vu_id, so_luong, thanh_tien))

            # Commit transaction
            self.connection.commit()

            # Hiển thị thông báo thanh toán thành công
            messagebox.showinfo("Thanh toán", "Lưu hóa đơn thành công!")
            self.root.destroy()

        except Exception as e:
            # Rollback transaction nếu có lỗi
            self.connection.rollback()
            messagebox.showerror("Lỗi", f"Đã có lỗi xảy ra: {str(e)}")

# Phần chạy ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    app = UpdateBillWindow(root)
    root.mainloop()
