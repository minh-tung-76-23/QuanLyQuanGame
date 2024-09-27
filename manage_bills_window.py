import tkinter as tk
from tkinter import simpledialog, messagebox, Toplevel, Scrollbar, Canvas, Entry, Label, StringVar
import mysql.connector
import csv

class ManageBillsWindow:
    def __init__(self, root, main_window):
        self.root = root
        self.main_window = main_window

        self.root.title("Quản lý quán game - Thống kê Hoá đơn")
        self.root.geometry('1100x600+200+100')

        # Thiết lập kết nối
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="quanlyquangame"
        )
        self.cursor = self.connection.cursor()

        # Tạo PanedWindow để chia giao diện làm hai phần
        self.paned_window = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashwidth=5, sashrelief=tk.RAISED)
        self.paned_window.pack(expand=True, fill=tk.BOTH)

        # Frame để chứa các thành phần tìm kiếm và nút xóa
        self.bills_frame = tk.Frame(self.paned_window)
        self.paned_window.add(self.bills_frame)

        # Label "Tìm kiếm theo:"
        self.search_label = tk.Label(self.bills_frame, text="Tìm kiếm theo:")
        self.search_label.pack(side=tk.TOP, padx=2)

        # Option menu cho lựa chọn
        self.search_options = ['Máy', 'Tên tài khoản', 'Thời gian sử dụng']
        self.search_option_var = StringVar(self.bills_frame)
        self.search_option_var.set(self.search_options[0])  # Mặc định là 'Máy'
        self.option_menu = tk.OptionMenu(self.bills_frame, self.search_option_var, *self.search_options)
        self.option_menu.pack(side=tk.TOP, padx=2)

        # Entry và nút tìm kiếm
        self.search_var = StringVar()
        self.search_entry = Entry(self.bills_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side=tk.TOP, padx=2)
        self.search_entry.bind("<KeyRelease>", self.search_bills)

        # Nút xóa hóa đơn
        self.delete_button = tk.Button(self.bills_frame, text="Xóa", command=self.delete_bill)
        self.delete_button.pack(side=tk.TOP, padx=2)

        # Canvas để chứa danh sách hóa đơn và scrollbar
        self.canvas = Canvas(self.bills_frame, width=500)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame để chứa danh sách các hóa đơn trong canvas
        self.scrollable_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)

        # Scrollbar cho frame danh sách hóa đơn
        bills_scrollbar = Scrollbar(self.bills_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        bills_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Thiết lập scrollbar cho Canvas
        self.canvas.config(yscrollcommand=bills_scrollbar.set)
        
        # Hiển thị danh sách các hóa đơn
        self.show_bills()

        # Frame để hiển thị chi tiết hóa đơn
        self.detail_frame = tk.Frame(self.paned_window)
        self.paned_window.add(self.detail_frame)

        self.label = tk.Label(self.detail_frame, text="Chi tiết hóa đơn", font=("Arial", 16))
        self.label.pack(pady=10)

        self.detail_text = tk.Text(self.detail_frame, font=("Arial", 12), wrap=tk.WORD)
        self.detail_text.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)

        # Tạo thanh Scrollbar
        detail_scrollbar = Scrollbar(self.detail_frame, command=self.detail_text.yview)
        detail_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Liên kết Scrollbar với Text
        self.detail_text.config(yscrollcommand=detail_scrollbar.set)

        # Tạo frame con để chứa nút in và thoát
        button_frame = tk.Frame(self.detail_frame)
        button_frame.pack(side=tk.BOTTOM, padx=10, pady=10)

        # Nút In
        self.print_button = tk.Button(button_frame, text="In", command=self.print_current_bill, width=10, height=2)
        self.print_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Nút Thoát
        self.exit_button = tk.Button(button_frame, text="Thoát", command=self.exit_window, width=10, height=2)
        self.exit_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def show_bills(self):
        # Xóa các widget cũ trong frame danh sách hóa đơn
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Truy vấn dữ liệu từ bảng HoaDon và kết hợp với bảng NguoiDung
        self.cursor.execute("""
            SELECT hd.hoadon_id, nd.tai_khoan, hd.may_id, hd.thoi_gian_bat_dau, hd.thoi_gian_ket_thuc, hd.tong_tien, hd.trang_thai_hoa_don
            FROM HoaDon hd
            JOIN NguoiDung nd ON hd.nguoi_dung_id = nd.nguoi_dung_id
            ORDER BY hd.hoadon_id DESC
        """)
        bills = self.cursor.fetchall()

        # Hiển thị từng hóa đơn trong frame
        for bill in bills:
            bill_id = bill[0]
            user_account = bill[1]
            may_id = bill[2]
            thoi_gian_bat_dau = bill[3]
            thoi_gian_ket_thuc = bill[4]
            tong_tien = "{:,.0f}".format(bill[5])
            trang_thai_hoa_don = bill[6]
            trang_thai_hoa_don = "Chưa thanh toán" if trang_thai_hoa_don == 0 else "Đã thanh toán"

            # Tạo một label để hiển thị thông tin hóa đơn
            bill_label_text = f"Hóa đơn {bill_id} - TK: {user_account} - Máy: {may_id} - Time start: {thoi_gian_bat_dau} - Time end:{thoi_gian_ket_thuc} - Tổng: {tong_tien} đ- TT: {trang_thai_hoa_don}"
            bill_label = Label(self.scrollable_frame, text=bill_label_text, wraplength=500, justify=tk.LEFT)
            bill_label.pack(pady=5)

            # Bắt sự kiện click để hiển thị chi tiết hóa đơn
            bill_label.bind("<Button-1>", lambda e, bill_id=bill_id: self.show_bill_detail(bill_id))
            bill_label.bind("<Button-3>", lambda e, bill_id=bill_id: self.select_bill(bill_id))

        # Đảm bảo rằng truy vấn đã được xử lý hoàn tất
        self.connection.commit() 

    def select_bill(self, bill_id):
        # Lưu bill_id được chọn vào biến instance
        self.selected_bill_id = bill_id

    def delete_bill(self):
        # Lấy hóa đơn được chọn
        selected_bill_id = getattr(self, 'selected_bill_id', None)

        if selected_bill_id:
            # Hỏi người dùng có chắc chắn muốn xóa không
            confirm = messagebox.askokcancel("Xác nhận xóa", f"Bạn có chắc chắn muốn xóa hóa đơn {selected_bill_id}?")

            if confirm:
                try:
                    # Xóa chi tiết hóa đơn trước
                    self.cursor.execute("DELETE FROM ChiTietHoaDonDichVu WHERE hoa_don_id = %s", (selected_bill_id,))
                    
                    # Xóa hóa đơn
                    self.cursor.execute("DELETE FROM HoaDon WHERE hoadon_id = %s", (selected_bill_id,))
                    
                    # Commit thay đổi vào cơ sở dữ liệu
                    self.connection.commit()

                    # Hiển thị thông báo xóa thành công
                    messagebox.showinfo("Thông báo", f"Đã xóa hóa đơn {selected_bill_id} thành công")

                    # Reload danh sách hóa đơn sau khi xóa
                    self.show_bills()

                except Exception as e:
                    # Rollback nếu có lỗi xảy ra
                    self.connection.rollback()
                    messagebox.showerror("Lỗi", f"Lỗi xóa hóa đơn: {str(e)}")

        else:
            messagebox.showwarning("Chưa chọn hóa đơn", "Vui lòng chọn hóa đơn để xóa")

    def show_bill_detail(self, bill_id):
        # Xóa nội dung chi tiết hóa đơn cũ
        self.detail_text.delete(1.0, tk.END)

        # Truy vấn dữ liệu từ bảng ChiTietHoaDonDichVu để lấy chi tiết hóa đơn
        self.cursor.execute("""
            SELECT 
                hd.hoadon_id, nd.ten, nd.tai_khoan, hd.may_id, 
                hd.thoi_gian_bat_dau, hd.thoi_gian_ket_thuc, hd.tong_tien,
                GROUP_CONCAT(CONCAT('Tên dịch vụ: ', dv.ten_dich_vu, '\nĐơn giá: ', FORMAT(dv.gia, 0), ' VNĐ\nSố lượng: ', ct.so_luong, '\nThành tiền: ', FORMAT(ct.thanh_tien, 0), ' VNĐ') SEPARATOR '\n\n') AS services
            FROM 
                HoaDon hd
                JOIN ChiTietHoaDonDichVu ct ON hd.hoadon_id = ct.hoa_don_id
                JOIN DichVu dv ON ct.dich_vu_id = dv.dich_vu_id
                JOIN NguoiDung nd ON hd.nguoi_dung_id = nd.nguoi_dung_id
            WHERE 
                hd.hoadon_id = %s
            GROUP BY
                hd.hoadon_id, nd.ten, nd.tai_khoan, hd.may_id, 
                hd.thoi_gian_bat_dau, hd.thoi_gian_ket_thuc, hd.tong_tien
        """, (bill_id,))
        
        # Lấy dòng dữ liệu từ kết quả truy vấn
        bill_detail = self.cursor.fetchone()

        # Hiển thị chi tiết hóa đơn vào Text detail_text
        if bill_detail:
            hoadon_id, ten, tai_khoan, may_id, thoi_gian_bat_dau, thoi_gian_ket_thuc, tong_tien, services = bill_detail
            
            # Đổi dấu xuống dòng thành ký tự xuống dòng
            formatted_services = services.replace(' - ', '\n')

            detail_text_content = (
                f"\tHóa đơn: {hoadon_id}\n\n"
                f"Người dùng: {ten} - Tài khoản: {tai_khoan}\n"
                f"Sử dụng máy: {may_id}\n"
                f"Thời gian bắt đầu: {thoi_gian_bat_dau}\n"
                f"Thời gian kết thúc: {thoi_gian_ket_thuc}\n\n"
                f"\tChi tiết dịch vụ:\n{formatted_services}\n\n"
                f"\tTổng tiền: {tong_tien:,} VNĐ" 
            )

            self.detail_text.insert(tk.END, detail_text_content)
        else:
            self.detail_text.insert(tk.END, "Không tìm thấy chi tiết hóa đơn")

    def search_bills(self, event=None):
        # Xóa các widget cũ trong frame danh sách hóa đơn
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Lấy lựa chọn từ OptionMenu
        search_option = self.search_option_var.get()

        # Lấy giá trị nhập vào từ Entry
        search_value = self.search_var.get()

        # Thực hiện truy vấn dựa trên lựa chọn
        if search_option == 'Máy':
            query = """
                SELECT hd.hoadon_id, nd.tai_khoan, hd.may_id, hd.thoi_gian_bat_dau, hd.thoi_gian_ket_thuc, hd.tong_tien, hd.trang_thai_hoa_don
                FROM HoaDon hd
                JOIN NguoiDung nd ON hd.nguoi_dung_id = nd.nguoi_dung_id
                WHERE hd.may_id LIKE %s
            """
            search_value = f'%{search_value}%'
        elif search_option == 'Tên tài khoản':
            query = """
                SELECT hd.hoadon_id, nd.tai_khoan, hd.may_id, hd.thoi_gian_bat_dau, hd.thoi_gian_ket_thuc, hd.tong_tien, hd.trang_thai_hoa_don
                FROM HoaDon hd
                JOIN NguoiDung nd ON hd.nguoi_dung_id = nd.nguoi_dung_id
                WHERE nd.tai_khoan LIKE %s
            """
            search_value = f'%{search_value}%'
        elif search_option == 'Thời gian sử dụng':
            query = """
                SELECT hd.hoadon_id, nd.tai_khoan, hd.may_id, hd.thoi_gian_bat_dau, hd.thoi_gian_ket_thuc, hd.tong_tien, hd.trang_thai_hoa_don
                FROM HoaDon hd
                JOIN NguoiDung nd ON hd.nguoi_dung_id = nd.nguoi_dung_id
                WHERE hd.thoi_gian_bat_dau LIKE %s OR hd.thoi_gian_ket_thuc LIKE %s
            """
            search_value = f'%{search_value}%'

        # Thực hiện truy vấn với giá trị tương ứng
        self.cursor.execute(query, (search_value,))
        bills = self.cursor.fetchall()

        # Hiển thị từng hóa đơn trong frame
        for bill in bills:
            bill_id = bill[0]
            user_account = bill[1]
            may_id = bill[2]
            thoi_gian_bat_dau = bill[3]
            thoi_gian_ket_thuc = bill[4]
            tong_tien = "{:,.0f}".format(bill[5])
            trang_thai_hoa_don = bill[6]
            trang_thai_hoa_don = "Chưa thanh toán" if trang_thai_hoa_don == 0 else "Đã thanh toán"

            # Tạo một label để hiển thị thông tin hóa đơn
            bill_label_text = f"Hóa đơn {bill_id} - TK: {user_account} - Máy: {may_id} - Time start: {thoi_gian_bat_dau} - Time end:{thoi_gian_ket_thuc} - Tổng: {tong_tien} đ- TT: {trang_thai_hoa_don}"
            bill_label = Label(self.scrollable_frame, text=bill_label_text, wraplength=500, justify=tk.LEFT)
            bill_label.pack(pady=5)

            # Bắt sự kiện click để hiển thị chi tiết hóa đơn
            bill_label.bind("<Button-1>", lambda e, bill_id=bill_id: self.show_bill_detail(bill_id))
            bill_label.bind("<Button-3>", lambda e, bill_id=bill_id: self.select_bill(bill_id))

        # Đảm bảo rằng truy vấn đã được xử lý hoàn tất
        self.connection.commit()

    def print_current_bill(self):
        # Lấy nội dung từ Text widget detail_text
        bill_detail_text = self.detail_text.get("1.0", tk.END).strip()

        if bill_detail_text:
            # Hiển thị cửa sổ nhập tên file
            filename = simpledialog.askstring("Nhập tên file CSV", "Nhập tên file CSV để lưu hóa đơn:")

            if filename:
                # Tạo tên file CSV
                csv_filename = f"{filename}.csv"

                # Mở file CSV để ghi
                with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)

                    # Ghi từng dòng nội dung vào file CSV
                    for line in bill_detail_text.splitlines():
                        writer.writerow([line])

                messagebox.showinfo("Thông báo", f"Đã in chi tiết hóa đơn vào file CSV: {csv_filename}")
            else:
                messagebox.showwarning("Tên file không hợp lệ", "Bạn chưa nhập tên file.")

        else:
            messagebox.showwarning("Không có dữ liệu hóa đơn", "Không có nội dung hóa đơn để in")

    def exit_window(self):
        self.root.destroy()  # Đóng cửa sổ quản lý dịch vụ
        self.main_window.deiconify()  # Hiện lại cửa sổ main
        
# Phần chạy ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    app = ManageBillsWindow(root)
    root.mainloop()
