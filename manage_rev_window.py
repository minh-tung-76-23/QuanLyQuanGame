import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from tkcalendar import DateEntry
from datetime import timedelta

class ManageRevenueWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý quán game - Doanh thu")
        self.root.geometry('1100x600+200+100')

        # Connect to the database
        self.connection, self.cursor = self.connect_to_database()

        # Main label for revenue statistics
        label_statistics = tk.Label(root, text="Thống kê doanh thu", font=('Arial', 20, 'bold'))
        label_statistics.pack(pady=20)

       # OptionMenu for selecting day, week, month
        frame_option_menu = tk.Frame(self.root)
        frame_option_menu.pack(pady=20)

        label_option = tk.Label(frame_option_menu, text="Chọn khoảng thời gian:")
        label_option.grid(row=0, column=0, padx=10, pady=10)

        option_var = tk.StringVar()
        option_menu = ttk.Combobox(frame_option_menu, width=20, textvariable=option_var, state='readonly')
        option_menu['values'] = ('Theo ngày', 'Theo tuần', 'Theo tháng', 'Tất cả')
        option_menu.current(0)
        option_menu.grid(row=0, column=1, padx=10, pady=10)

        label_date_or_week_or_month = tk.Label(frame_option_menu, text="Chọn ngày/tuần/tháng:")
        label_date_or_week_or_month.grid(row=0, column=2, padx=10, pady=10)

        self.entry_date_or_week_or_month = DateEntry(frame_option_menu, width=12, background='darkblue',
                                                     foreground='white', borderwidth=2)
        self.entry_date_or_week_or_month.grid(row=0, column=3, padx=10, pady=10)

        button_ok = tk.Button(frame_option_menu, text="OK", command=lambda:self.handle_ok(option_var.get()))
        button_ok.grid(row=0, column=4, padx=10, pady=10)

        # Frame for revenue summary
        frame_revenue_summary = tk.Frame(root)
        frame_revenue_summary.pack(pady=20)

        self.label_total_revenue = tk.Label(frame_revenue_summary, text="Tổng thu nhập:",font=('Arial', 13, 'bold'))
        self.label_total_revenue.grid(row=0, column=0, padx=10, pady=10)

        self.label_machine_revenue = tk.Label(frame_revenue_summary, text="Thu nhập từ máy:",font=('Arial', 13, 'bold'))
        self.label_machine_revenue.grid(row=0, column=1, padx=10, pady=10)

        self.label_service_revenue = tk.Label(frame_revenue_summary, text="Thu nhập từ dịch vụ:",font=('Arial', 13, 'bold'))
        self.label_service_revenue.grid(row=0, column=2, padx=10, pady=10)

        # Frame for displaying machine revenue
        frame_machine_revenue = tk.Frame(root, bd=2, relief=tk.GROOVE)
        frame_machine_revenue.pack(pady=20, padx=10, side=tk.LEFT, fill=tk.BOTH, expand=True)

        label_machine_revenue_title = tk.Label(frame_machine_revenue, text="Doanh thu từng máy", font=('Arial', 16, 'bold'))
        label_machine_revenue_title.pack(pady=10)

        scrollbar_machine = tk.Scrollbar(frame_machine_revenue)
        scrollbar_machine.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox_machine_revenue = tk.Listbox(frame_machine_revenue, yscrollcommand=scrollbar_machine.set, width=40, height=20,font=('Arial', 11))
        self.listbox_machine_revenue.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        scrollbar_machine.config(command=self.listbox_machine_revenue.yview)

        # Frame for displaying service revenue
        frame_service_revenue = tk.Frame(root, bd=2, relief=tk.GROOVE)
        frame_service_revenue.pack(pady=20, padx=10, side=tk.LEFT, fill=tk.BOTH, expand=True)

        label_service_revenue_title = tk.Label(frame_service_revenue, text="Doanh thu từ dịch vụ", font=('Arial', 16, 'bold'))
        label_service_revenue_title.pack(pady=10)

        scrollbar_service = tk.Scrollbar(frame_service_revenue)
        scrollbar_service.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox_service_revenue = tk.Listbox(frame_service_revenue, yscrollcommand=scrollbar_service.set, width=80, height=20,font=('Arial', 11))
        self.listbox_service_revenue.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        scrollbar_service.config(command=self.listbox_service_revenue.yview)

        # Load initial revenue statistics
        self.load_revenue_statistics()
        root.mainloop()


    def connect_to_database(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="quanlyquangame"
            )
            cursor = connection.cursor()
            return connection, cursor
        except mysql.connector.Error as error:
            print(f"Error connecting to MySQL: {error}")
            return None, None

    def load_revenue_statistics(self):
        print("all")

        try:
            if not self.connection or not self.cursor:
                messagebox.showerror("Lỗi", "Không thể kết nối đến cơ sở dữ liệu.")
                return

            # Tính tổng thu nhập từ tất cả hóa đơn
            query_total_revenue = "SELECT SUM(tong_tien) FROM HoaDon"
            self.cursor.execute(query_total_revenue)
            total_revenue_result = self.cursor.fetchone()[0]
            total_revenue = total_revenue_result if total_revenue_result else 0
            formatted_total_revenue = "{:,.0f}".format(total_revenue)
            self.label_total_revenue.config(text=f"Tổng thu nhập: {formatted_total_revenue} đ")

            # Tính thu nhập từ máy
            query_machine_revenue = "SELECT SUM(TIMESTAMPDIFF(HOUR, thoi_gian_bat_dau, thoi_gian_ket_thuc) * may_don_gia) " \
                                    "FROM HoaDon JOIN MayTram ON HoaDon.may_id = MayTram.may_id"
            self.cursor.execute(query_machine_revenue)
            machine_revenue_result = self.cursor.fetchone()[0]
            machine_revenue = machine_revenue_result if machine_revenue_result else 0
            formatted_machine_revenue = "{:,.0f}".format(machine_revenue)
            self.label_machine_revenue.config(text=f"Thu nhập từ máy: {formatted_machine_revenue} đ")

            # Tính tổng thu nhập từ dịch vụ
            query_service_revenue = "SELECT SUM(thanh_tien) FROM ChiTietHoaDonDichVu"
            self.cursor.execute(query_service_revenue)
            service_revenue_result = self.cursor.fetchone()[0]
            service_revenue = service_revenue_result if service_revenue_result else 0
            formatted_service_revenue = "{:,.0f}".format(service_revenue)
            self.label_service_revenue.config(text=f"Thu nhập từ dịch vụ: {formatted_service_revenue} đ")

            # Xóa nội dung cũ trong listbox_machine_revenue
            self.listbox_machine_revenue.delete(0, tk.END)

            # Tính thu nhập của từng máy và hiển thị vào listbox_machine_revenue
            machine_revenue = {}
            # Thực hiện câu truy vấn
            query = '''
                SELECT 
                    HoaDon.hoadon_id, 
                    HoaDon.may_id, 
                    HoaDon.tong_tien, 
                    HoaDon.thoi_gian_bat_dau, 
                    HoaDon.thoi_gian_ket_thuc,
                    MayTram.ten_may, 
                    MayTram.may_don_gia,
                    ROUND(TIMESTAMPDIFF(SECOND, HoaDon.thoi_gian_bat_dau, HoaDon.thoi_gian_ket_thuc) / 3600.0, 2) AS thoi_gian_hoat_dong,
                    MayTram.may_don_gia * ROUND(TIMESTAMPDIFF(SECOND, HoaDon.thoi_gian_bat_dau, HoaDon.thoi_gian_ket_thuc) / 3600.0, 2) AS so_tien
                FROM 
                    HoaDon
                JOIN 
                    MayTram ON HoaDon.may_id = MayTram.may_id
            '''
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            # Lặp qua từng dòng dữ liệu
            for row in rows:
                hoadon_id, may_id, tong_tien, thoi_gian_bat_dau, thoi_gian_ket_thuc, ten_may, may_don_gia, thoi_gian_hoat_dong, so_tien = row

                # Chuyển đổi so_tien từ Decimal sang float
                so_tien = float(so_tien)

                # Tính tổng tiền của từng máy
                if may_id not in machine_revenue:
                    machine_revenue[may_id] = 0.0
                machine_revenue[may_id] += so_tien

            # Hiển thị vào listbox_machine_revenue
            self.listbox_machine_revenue.delete(0, tk.END)
            for may_id, total_revenue in machine_revenue.items():
                formatted_total_revenue = "{:,.0f}".format(total_revenue)
                self.listbox_machine_revenue.insert(tk.END, f"Máy {may_id} - Số tiền: {formatted_total_revenue} đ")

            # Tạo một từ điển để lưu trữ số lượng và thành tiền của từng dịch vụ
            self.listbox_service_revenue.delete(0, tk.END)
            service_revenue = {}

            # Thực hiện câu truy vấn để lấy số lượng và thành tiền của các chi tiết hóa đơn
            query = '''
                SELECT 
                    ChiTietHoaDonDichVu.so_luong, 
                    ChiTietHoaDonDichVu.thanh_tien,
                    DichVu.ten_dich_vu
                FROM 
                    ChiTietHoaDonDichVu
                JOIN 
                    DichVu ON ChiTietHoaDonDichVu.dich_vu_id = DichVu.dich_vu_id
            '''
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            # Lặp qua từng dòng kết quả
            for row in rows:
                so_luong, thanh_tien, ten_dich_vu = row

                # Nếu tên dịch vụ chưa có trong từ điển, thêm vào và khởi tạo số lượng và thành tiền
                if ten_dich_vu not in service_revenue:
                    service_revenue[ten_dich_vu] = {
                        'so_luong': 0,
                        'thanh_tien': 0.0
                    }

                # Cập nhật số lượng và thành tiền của dịch vụ
                service_revenue[ten_dich_vu]['so_luong'] += so_luong
                service_revenue[ten_dich_vu]['thanh_tien'] += thanh_tien

            # Hiển thị thông tin từng dịch vụ trong listbox_service_revenue
            for ten_dich_vu, data in service_revenue.items():
                so_luong = data['so_luong']
                thanh_tien = data['thanh_tien']
                formatted_thanh_tien = "{:,.0f}".format(thanh_tien)
                # Hiển thị thông tin dịch vụ trong listbox_service_revenue
                self.listbox_service_revenue.insert(tk.END, f"{ten_dich_vu} - Số lượng đã bán: {so_luong} - Thành tiền: {formatted_thanh_tien}đ")

        except mysql.connector.Error as error:
            print(f"Error executing MySQL query: {error}")
            messagebox.showerror("Lỗi", "Đã xảy ra lỗi khi truy vấn dữ liệu từ cơ sở dữ liệu.")

    def handle_ok(self, option):
        selected_date = self.entry_date_or_week_or_month.get_date()

        if option == "Theo ngày" and selected_date:
            self.load_revenue_day(selected_date)
        elif option == "Theo tuần" and selected_date:
            start_date, end_date = self.get_week_boundaries(selected_date)
            self.load_revenue(start_date, end_date)
        elif option == "Theo tháng" and selected_date:
            start_date, end_date = self.get_month_boundaries(selected_date)
            self.load_revenue(start_date, end_date)
        elif option == "Tất cả":
            self.load_revenue_statistics()
        else:
            # Handle other options if needed
            pass

    def load_revenue_day(self, selected_date):
        print(f"Loading revenue from {selected_date}")
        try:
            if not self.connection or not self.cursor:
                messagebox.showerror("Lỗi", "Không thể kết nối đến cơ sở dữ liệu.")
                return

            # Tính tổng thu nhập từ hóa đơn theo ngày
            query_total_revenue = f"SELECT SUM(tong_tien) FROM HoaDon WHERE DATE(thoi_gian_bat_dau) = '{selected_date}'"
            self.cursor.execute(query_total_revenue)
            total_revenue_result = self.cursor.fetchone()[0]
            total_revenue = total_revenue_result if total_revenue_result else 0
            formatted_total_revenue = "{:,.0f}".format(total_revenue)
            self.label_total_revenue.config(text=f"Tổng thu nhập: {formatted_total_revenue} đ")

            # Tính thu nhập từ máy theo ngày
            query_machine_revenue = f"SELECT SUM(TIMESTAMPDIFF(HOUR, thoi_gian_bat_dau, thoi_gian_ket_thuc) * may_don_gia) " \
                                    f"FROM HoaDon JOIN MayTram ON HoaDon.may_id = MayTram.may_id " \
                                    f"WHERE DATE(thoi_gian_bat_dau) = '{selected_date}'"
            self.cursor.execute(query_machine_revenue)
            machine_revenue_result = self.cursor.fetchone()[0]
            machine_revenue = machine_revenue_result if machine_revenue_result else 0
            formatted_machine_revenue = "{:,.0f}".format(machine_revenue)
            self.label_machine_revenue.config(text=f"Thu nhập từ máy: {formatted_machine_revenue} đ")

            # Tính thu nhập từ dịch vụ theo ngày
            query_service_revenue = f"SELECT HoaDon.hoadon_id, HoaDon.thoi_gian_bat_dau, HoaDon.thoi_gian_ket_thuc, DichVu.ten_dich_vu, ChiTietHoaDonDichVu.so_luong, SUM(ChiTietHoaDonDichVu.thanh_tien) " \
                                    f"FROM HoaDon JOIN ChiTietHoaDonDichVu ON HoaDon.hoadon_id = ChiTietHoaDonDichVu.hoa_don_id JOIN DichVu ON ChiTietHoaDonDichVu.dich_vu_id = DichVu.dich_vu_id " \
                                    f"WHERE DATE(thoi_gian_bat_dau) = '{selected_date}'"
            self.cursor.execute(query_service_revenue)
            service_revenue_result = self.cursor.fetchone()[5]
            service_revenue = service_revenue_result if service_revenue_result else 0
            formatted_service_revenue = "{:,.0f}".format(service_revenue)
            self.label_service_revenue.config(text=f"Thu nhập từ dịch vụ: {formatted_service_revenue} đ")

            # Xóa nội dung cũ trong listbox_machine_revenue
            self.listbox_machine_revenue.delete(0, tk.END)

            # Tính thu nhập của từng máy và hiển thị vào listbox_machine_revenue
            machine_revenue = {}
            query = f'''
                SELECT 
                    HoaDon.hoadon_id, 
                    HoaDon.may_id, 
                    HoaDon.tong_tien, 
                    HoaDon.thoi_gian_bat_dau, 
                    HoaDon.thoi_gian_ket_thuc,
                    MayTram.ten_may, 
                    MayTram.may_don_gia,
                    ROUND(TIMESTAMPDIFF(SECOND, HoaDon.thoi_gian_bat_dau, HoaDon.thoi_gian_ket_thuc) / 3600.0, 2) AS thoi_gian_hoat_dong,
                    MayTram.may_don_gia * ROUND(TIMESTAMPDIFF(SECOND, HoaDon.thoi_gian_bat_dau, HoaDon.thoi_gian_ket_thuc) / 3600.0, 2) AS so_tien
                FROM 
                    HoaDon
                JOIN 
                    MayTram ON HoaDon.may_id = MayTram.may_id
                WHERE 
                    DATE(HoaDon.thoi_gian_bat_dau) = '{selected_date}'
            '''
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            for row in rows:
                hoadon_id, may_id, tong_tien, thoi_gian_bat_dau, thoi_gian_ket_thuc, ten_may, may_don_gia, thoi_gian_hoat_dong, so_tien = row

                so_tien = float(so_tien)

                if may_id not in machine_revenue:
                    machine_revenue[may_id] = 0.0
                machine_revenue[may_id] += so_tien

            self.listbox_machine_revenue.delete(0, tk.END)
            for may_id, total_revenue in machine_revenue.items():
                formatted_total_revenue = "{:,.0f}".format(total_revenue)
                self.listbox_machine_revenue.insert(tk.END, f"Máy {may_id} - Số tiền: {formatted_total_revenue} đ")

            # Tính thu nhập của từng dịch vụ  và hiển thị vào listbox_service_revenue
            self.listbox_service_revenue.delete(0, tk.END)
            # Tính thu nhập từ dịch vụ theo ngày
            query_service_revenue = f'''
                SELECT DichVu.ten_dich_vu, SUM(ChiTietHoaDonDichVu.so_luong) AS so_luong, SUM(ChiTietHoaDonDichVu.thanh_tien) AS thanh_tien
                FROM HoaDon
                JOIN ChiTietHoaDonDichVu ON HoaDon.hoadon_id = ChiTietHoaDonDichVu.hoa_don_id
                JOIN DichVu ON ChiTietHoaDonDichVu.dich_vu_id = DichVu.dich_vu_id
                WHERE DATE(HoaDon.thoi_gian_bat_dau) = '{selected_date}'
                GROUP BY DichVu.ten_dich_vu
            '''
            self.cursor.execute(query_service_revenue)
            rows = self.cursor.fetchall()

            service_revenue = {}

            for row in rows:
                ten_dich_vu, so_luong, thanh_tien = row

                # Định dạng lại thành tiền để hiển thị
                formatted_thanh_tien = "{:,.0f}".format(thanh_tien)

                # Hiển thị thông tin dịch vụ trong listbox_service_revenue
                self.listbox_service_revenue.insert(tk.END, f"{ten_dich_vu} - Số lượng đã bán: {so_luong} - Thành tiền: {formatted_thanh_tien} đ")

        except mysql.connector.Error as error:
            print(f"Error executing MySQL query: {error}")
            messagebox.showerror("Lỗi", "Đã xảy ra lỗi khi truy vấn dữ liệu từ cơ sở dữ liệu.")

    def load_revenue(self, start_date, end_date):
        print(f"Loading revenue from {start_date} to {end_date}")
        try:
            if not self.connection or not self.cursor:
                messagebox.showerror("Lỗi", "Không thể kết nối đến cơ sở dữ liệu.")
                return

            # Tính tổng thu nhập từ hóa đơn trong khoảng thời gian từ start_date đến end_date
            query_total_revenue = f"SELECT SUM(tong_tien) FROM HoaDon WHERE DATE(thoi_gian_bat_dau) BETWEEN '{start_date}' AND '{end_date}'"
            self.cursor.execute(query_total_revenue)
            total_revenue_result = self.cursor.fetchone()[0]
            total_revenue = total_revenue_result if total_revenue_result else 0
            formatted_total_revenue = "{:,.0f}".format(total_revenue)
            self.label_total_revenue.config(text=f"Tổng thu nhập: {formatted_total_revenue} đ")

            # Tính thu nhập từ máy trong khoảng thời gian từ start_date đến end_date
            query_machine_revenue = f"SELECT SUM(TIMESTAMPDIFF(HOUR, thoi_gian_bat_dau, thoi_gian_ket_thuc) * may_don_gia) " \
                                    f"FROM HoaDon JOIN MayTram ON HoaDon.may_id = MayTram.may_id " \
                                    f"WHERE DATE(thoi_gian_bat_dau) BETWEEN '{start_date}' AND '{end_date}'"
            self.cursor.execute(query_machine_revenue)
            machine_revenue_result = self.cursor.fetchone()[0]
            machine_revenue = machine_revenue_result if machine_revenue_result else 0
            formatted_machine_revenue = "{:,.0f}".format(machine_revenue)
            self.label_machine_revenue.config(text=f"Thu nhập từ máy: {formatted_machine_revenue} đ")

            # Tính thu nhập từ dịch vụ trong khoảng thời gian từ start_date đến end_date
            query_service_revenue = f"SELECT HoaDon.hoadon_id, HoaDon.thoi_gian_bat_dau, HoaDon.thoi_gian_ket_thuc, DichVu.ten_dich_vu, " \
                                    f"ChiTietHoaDonDichVu.so_luong, SUM(ChiTietHoaDonDichVu.thanh_tien) " \
                                    f"FROM HoaDon JOIN ChiTietHoaDonDichVu ON HoaDon.hoadon_id = ChiTietHoaDonDichVu.hoa_don_id " \
                                    f"JOIN DichVu ON ChiTietHoaDonDichVu.dich_vu_id = DichVu.dich_vu_id " \
                                    f"WHERE DATE(thoi_gian_bat_dau) BETWEEN '{start_date}' AND '{end_date}'"
            self.cursor.execute(query_service_revenue)
            service_revenue_result = self.cursor.fetchone()[5]
            service_revenue = service_revenue_result if service_revenue_result else 0
            formatted_service_revenue = "{:,.0f}".format(service_revenue)
            self.label_service_revenue.config(text=f"Thu nhập từ dịch vụ: {formatted_service_revenue} đ")

            # Xóa nội dung cũ trong listbox_machine_revenue
            self.listbox_machine_revenue.delete(0, tk.END)

            # Tính thu nhập của từng máy và hiển thị vào listbox_machine_revenue
            machine_revenue = {}
            query = f'''
                SELECT 
                    HoaDon.hoadon_id, 
                    HoaDon.may_id, 
                    HoaDon.tong_tien, 
                    HoaDon.thoi_gian_bat_dau, 
                    HoaDon.thoi_gian_ket_thuc,
                    MayTram.ten_may, 
                    MayTram.may_don_gia,
                    ROUND(TIMESTAMPDIFF(SECOND, HoaDon.thoi_gian_bat_dau, HoaDon.thoi_gian_ket_thuc) / 3600.0, 2) AS thoi_gian_hoat_dong,
                    MayTram.may_don_gia * ROUND(TIMESTAMPDIFF(SECOND, HoaDon.thoi_gian_bat_dau, HoaDon.thoi_gian_ket_thuc) / 3600.0, 2) AS so_tien
                FROM 
                    HoaDon
                JOIN 
                    MayTram ON HoaDon.may_id = MayTram.may_id
                WHERE 
                    DATE(HoaDon.thoi_gian_bat_dau) BETWEEN '{start_date}' AND '{end_date}'
            '''
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            for row in rows:
                hoadon_id, may_id, tong_tien, thoi_gian_bat_dau, thoi_gian_ket_thuc, ten_may, may_don_gia, thoi_gian_hoat_dong, so_tien = row

                so_tien = float(so_tien)

                if may_id not in machine_revenue:
                    machine_revenue[may_id] = 0.0
                machine_revenue[may_id] += so_tien

            self.listbox_machine_revenue.delete(0, tk.END)
            for may_id, total_revenue in machine_revenue.items():
                formatted_total_revenue = "{:,.0f}".format(total_revenue)
                self.listbox_machine_revenue.insert(tk.END, f"Máy {may_id} - Số tiền: {formatted_total_revenue} đ")

            # Tính thu nhập của từng dịch vụ và hiển thị vào listbox_service_revenue
            self.listbox_service_revenue.delete(0, tk.END)
            query_service_revenue = f'''
                SELECT DichVu.ten_dich_vu, SUM(ChiTietHoaDonDichVu.so_luong) AS so_luong, SUM(ChiTietHoaDonDichVu.thanh_tien) AS thanh_tien
                FROM HoaDon
                JOIN ChiTietHoaDonDichVu ON HoaDon.hoadon_id = ChiTietHoaDonDichVu.hoa_don_id
                JOIN DichVu ON ChiTietHoaDonDichVu.dich_vu_id = DichVu.dich_vu_id
                WHERE DATE(HoaDon.thoi_gian_bat_dau) BETWEEN '{start_date}' AND '{end_date}'
                GROUP BY DichVu.ten_dich_vu
            '''
            self.cursor.execute(query_service_revenue)
            rows = self.cursor.fetchall()

            service_revenue = {}

            for row in rows:
                ten_dich_vu, so_luong, thanh_tien = row

                # Định dạng lại thành tiền để hiển thị
                formatted_thanh_tien = "{:,.0f}".format(thanh_tien)

                # Hiển thị thông tin dịch vụ trong listbox_service_revenue
                self.listbox_service_revenue.insert(tk.END, f"{ten_dich_vu} - Số lượng đã bán: {so_luong} - Thành tiền: {formatted_thanh_tien} đ")

        except mysql.connector.Error as error:
            print(f"Error executing MySQL query: {error}")
            messagebox.showerror("Lỗi", "Đã xảy ra lỗi khi truy vấn dữ liệu từ cơ sở dữ liệu.")

    def get_week_boundaries(self, date):
        # Tính ngày bắt đầu và ngày kết thúc của tuần chứa ngày đã cho
        start_date = date - timedelta(days=date.weekday())
        end_date = start_date + timedelta(days=6)
        return start_date, end_date

    def get_month_boundaries(self, date):
        #Tính ngày bắt đầu và ngày kết thúc của tháng có chứa ngày đã cho
        start_date = date.replace(day=1)
        next_month = date.replace(month=date.month+1, day=1) if date.month < 12 else date.replace(year=date.year+1, month=1, day=1)
        end_date = next_month - timedelta(days=1)
        return start_date, end_date

# Phần chạy ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    app = ManageRevenueWindow(root)
    root.mainloop()



