import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
from manage_services_window import ManageServicesWindow
from manage_customers_window import ManageCustomersWindow
from manage_bills_window import ManageBillsWindow
from manage_rev_window import ManageRevenueWindow
from insert_bill_window import BillWindow
from update_bill_window import UpdateBillWindow
import datetime

def connect_to_database():
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

# Biến lưu trữ ID của máy đang được hiển thị chi tiết
current_machine_id = None

def display_machine_list(frame_may, frame_may_detail):
    for widget in frame_may.winfo_children():
        widget.destroy()
    
    connection, cursor = connect_to_database()
    if connection and cursor:
        try:
            # Truy vấn dữ liệu từ bảng HoaDon và MayTram
            cursor.execute("SELECT HoaDon.hoadon_id, HoaDon.may_id, HoaDon.thoi_gian_ket_thuc, MayTram.trang_thai AS trang_thai_may, HoaDon.nguoi_dung_id, HoaDon.tong_tien FROM HoaDon JOIN MayTram ON HoaDon.may_id = MayTram.may_id")
            machines = cursor.fetchall()

            print(f"Total rows fetched: {len(machines)}")

            current_time = datetime.datetime.now()

            for machine in machines:
                hoadon_id, may_id, thoi_gian_ket_thuc, trang_thai_may, nguoi_dung_id, tong_tien = machine

                # Debug: In ra toàn bộ dữ liệu của từng máy
                print(f'Machine ID: {may_id}, Thời gian kết thúc: {thoi_gian_ket_thuc}, Trạng thái máy: {trang_thai_may}')
                if trang_thai_may == "Hoạt động":
                    # So sánh phần date
                    if thoi_gian_ket_thuc.date() < current_time.date():
                        print(f'{thoi_gian_ket_thuc} - {current_time}')
                        # Cập nhật trạng thái máy thành "Đang nghỉ"
                        update_money_user = f"UPDATE NguoiDung SET so_tien = so_tien - {tong_tien} WHERE nguoi_dung_id = {nguoi_dung_id}"
                        cursor.execute(update_money_user)
                        connection.commit() 

                        update_tthd = f"UPDATE HoaDon SET trang_thai_hoa_don = '1' WHERE hoadon_id = {hoadon_id}"
                        cursor.execute(update_tthd)
                        connection.commit() 

                        update_query = f"UPDATE MayTram SET trang_thai = 'Đang nghỉ' WHERE may_id = {may_id}"
                        cursor.execute(update_query)
                        connection.commit()  
                    elif thoi_gian_ket_thuc.date() == current_time.date():
                        # So sánh phần time
                        if thoi_gian_ket_thuc.time() <= current_time.time():
                            print(f'{thoi_gian_ket_thuc} - {current_time}')
                            update_money_user = f"UPDATE NguoiDung SET so_tien = so_tien - {tong_tien} WHERE nguoi_dung_id = {nguoi_dung_id}"
                            cursor.execute(update_money_user)
                            connection.commit() 

                            update_tthd = f"UPDATE HoaDon SET trang_thai_hoa_don = '1' WHERE hoadon_id = {hoadon_id}"
                            cursor.execute(update_tthd)
                            connection.commit()  

                            update_query = f"UPDATE MayTram SET trang_thai = 'Đang nghỉ' WHERE may_id = {may_id}"
                            cursor.execute(update_query)
                            connection.commit()
                        else:
                            # Cập nhật trạng thái máy thành "Hoạt động"
                            update_query = f"UPDATE MayTram SET trang_thai = 'Hoạt động' WHERE may_id = {may_id}"
                            cursor.execute(update_query)
                            connection.commit()  
                    else:
                        # Cập nhật trạng thái máy thành "Hoạt động"
                        update_query = f"UPDATE MayTram SET trang_thai = 'Hoạt động' WHERE may_id = {may_id}"
                        cursor.execute(update_query)
                        connection.commit()  # Thực hiện lưu thay đổi vào cơ sở dữ liệu

            # Truy vấn dữ liệu từ bảng MayTram
            cursor.execute("SELECT * FROM MayTram")
            machines = cursor.fetchall()

            # Hiển thị các máy trong frame_may
            row_num = 0
            col_num = 0
            for machine in machines:
                may_id, ten_may, trang_thai, mo_ta, may_don_gia, anh_may = machine
                # Xác định màu nền và màu chữ dựa trên trạng thái của máy
                bg_color = 'red' if trang_thai == 'Hoạt động' else 'green'
                fg_color = 'black' if trang_thai == 'Hoạt động' else 'white'

                # Tạo nút cho mỗi máy
                btn_machine = tk.Button(frame_may, text=ten_may, bg=bg_color, fg=fg_color,
                                        width=8, height=2,
                                        command=lambda may_id=may_id, ten_may=ten_may, mo_ta=mo_ta, anh_may=anh_may, trang_thai=trang_thai, may_don_gia=may_don_gia:
                                        show_machine_details(frame_may_detail, may_id, ten_may, mo_ta, anh_may, trang_thai, may_don_gia))
                btn_machine.grid(row=row_num, column=col_num, padx=10, pady=10)

                col_num += 1
                if col_num > 4:
                    col_num = 0
                    row_num += 1
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi hiển thị danh sách máy: {e}")
        finally:
            cursor.close()
            connection.close()

# Hàm hiển thị chi tiết máy khi click
def show_machine_details(frame_may_detail, may_id, ten_may, mo_ta, anh_may, trang_thai, may_don_gia):
    global current_machine_id

    # Kiểm tra nếu máy đang được hiển thị chi tiết và click lại vào máy đó
    if current_machine_id == may_id:
        print(trang_thai)
        if trang_thai == "Đang nghỉ":
            # Mở form chỉnh sửa thông tin máy
            insert_bill_window = tk.Toplevel()
            app = BillWindow(insert_bill_window, may_id, ten_may, trang_thai, may_don_gia)
        else:
            connection, cursor = connect_to_database()
            if connection and cursor:
                try:
                    # Lấy thông tin tất cả các hóa đơn của máy
                    query = f"SELECT hoadon_id, trang_thai_hoa_don FROM HoaDon WHERE may_id = {may_id}"
                    cursor.execute(query)
                    results = cursor.fetchall()

                    found_active_bill = False

                    # Kiểm tra từng hóa đơn
                    for result in results:
                        hoadon_id, trang_thai_hoa_don = result
                        if trang_thai_hoa_don == 0:
                            # Mở form Update thông tin hóa đơn
                            update_bill_window = tk.Toplevel()
                            app = UpdateBillWindow(update_bill_window, may_id, ten_may, trang_thai, may_don_gia, hoadon_id)
                            found_active_bill = True
                            break

                    if not found_active_bill:
                        messagebox.showinfo("Thông báo", "Máy đang hoạt động và đã thanh toán!.")

                except Exception as e:
                    messagebox.showerror("Lỗi", f"Lỗi khi hiển thị danh sách máy: {e}")
                finally:
                    cursor.close()
                    connection.close()

    # Cập nhật current_machine_id
    current_machine_id = may_id

    # Xóa nội dung cũ trong frame_may_detail
    for widget in frame_may_detail.winfo_children():
        widget.destroy()

    # Hiển thị thông tin chi tiết của máy
    lbl_ten_may = tk.Label(frame_may_detail, text=f"Tên máy: {ten_may}", font=("Arial", 14, "bold"), height=1)
    lbl_ten_may.pack(anchor=tk.W, padx=70, pady=5)

    lbl_mo_ta = tk.Label(frame_may_detail, text=f"Mô tả: {mo_ta}", wraplength=300, height=5)
    lbl_mo_ta.pack(anchor=tk.W, padx=10)

    # Hiển thị ảnh máy (nếu có)
    if anh_may:
        try:
            # Mở và thay đổi kích thước ảnh
            original_image = Image.open(f'F:\\LT_IT\\PY\\Woskspace\\QuanLyQuanGame\\img\\{anh_may}')
            resized_image = original_image.resize((200, 200), Image.Resampling.LANCZOS)
            image = ImageTk.PhotoImage(resized_image)
            lbl_anh_may = tk.Label(frame_may_detail, image=image)
            lbl_anh_may.image = image  # Lưu tham chiếu đến ảnh
            lbl_anh_may.pack(anchor=tk.W, padx=(50))
        except FileNotFoundError:
            print(f"Không tìm thấy tệp: {anh_may}")
        except Exception as e:
            print(f"Lỗi khi tải ảnh: {e}")

    formatted_price = "{:,.0f}".format(may_don_gia)
    lbl_may_don_gia = tk.Label(frame_may_detail, text=f"Giá: {formatted_price}đ/h", wraplength=300, height=5)
    lbl_may_don_gia.pack(anchor=tk.W, padx=(110), pady=0)

    fg_color = 'red' if trang_thai == 'Hoạt động' else 'blue'
    lbl_trang_thai = tk.Label(frame_may_detail, text=f"Tình trạng: {trang_thai}", wraplength=300, height=5, fg=fg_color)
    lbl_trang_thai.pack(anchor=tk.W, padx=(90, 0))

# Hàm mở cửa sổ chính
def open_main_window(root):
    main_window = tk.Toplevel(root)
    main_window.geometry('1000x600+250+100')
    main_window.title("Quản lý quán game - trang chủ")

    # Khung cho danh sách máy
    frame_may = tk.Frame(main_window, width=600, height= 600, pady=30, padx=0)
    frame_may.grid(row=2, column=0, padx=0, pady=0)

    # Khung cho chi tiết máy
    frame_may_detail = tk.Frame(main_window, width=300)
    frame_may_detail.grid(row=2, column=1, padx=(100,0), pady=1)

    # Hiển thị danh sách máy ban đầu
    display_machine_list(frame_may, frame_may_detail)

    # Khung cho các nút (dịch vụ, hóa đơn, người dùng, doanh thu, đăng xuất)
    frame_buttons = tk.Frame(main_window)
    frame_buttons.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

    # Các nút quản lý dịch vụ, hóa đơn, người dùng, doanh thu, và đăng xuất
    btn_manage_services = tk.Button(frame_buttons, text="Quản lý dịch vụ", command=lambda: manage_services(main_window))
    btn_manage_services.grid(row=0, column=0, padx=10, pady=10)

    btn_manage_orders = tk.Button(frame_buttons, text="Quản lý hóa đơn", command=lambda: manage_bills(main_window))
    btn_manage_orders.grid(row=0, column=1, padx=10, pady=10)

    btn_manage_customers = tk.Button(frame_buttons, text="Quản lý người dùng", command=lambda: manage_customers(main_window))
    btn_manage_customers.grid(row=0, column=2, padx=10, pady=10)

    btn_manage_rev = tk.Button(frame_buttons, text="Quản lý doanh thu", command=lambda: manage_revenue(main_window))
    btn_manage_rev.grid(row=0, column=3, padx=10, pady=10)

    btn_load = tk.Button(frame_buttons, text="Load", command=lambda: load_list(root, main_window, frame_may, frame_may_detail))
    btn_load.grid(row=0, column=4, padx=(200,0), pady=10)

    btn_logout = tk.Button(frame_buttons, text="Đăng xuất", command=lambda: logout(root, main_window))
    btn_logout.grid(row=0, column=5, padx=10, pady=10)

    # Chạy vòng lặp ứng dụng chính
    main_window.mainloop()

# Các hàm mở cửa sổ quản lý dịch vụ, người dùng, hóa đơn, doanh thu
def manage_services(main_window):
    manage_services_window = tk.Toplevel()
    app = ManageServicesWindow(manage_services_window, main_window)
    main_window.withdraw()

def manage_customers(main_window):
    manage_customers_window = tk.Toplevel()
    app = ManageCustomersWindow(manage_customers_window, main_window)
    main_window.withdraw()

def manage_bills(main_window):
    manage_bills_window = tk.Toplevel()
    app = ManageBillsWindow(manage_bills_window, main_window)
    main_window.withdraw()

def manage_revenue(main_window):
    manage_rev_window = tk.Toplevel()
    app = ManageRevenueWindow(manage_rev_window)
    main_window.withdraw()

def load_list(root, main_window, frame_may, frame_may_detail):
    # Cập nhật lại danh sách máy sau khi cập nhật trạng thái
    display_machine_list(frame_may, frame_may_detail)


def logout(root, main_window):
    # Hiển thị hộp thoại xác nhận đăng xuất
    response = messagebox.askyesno("Thông báo", "Bạn có chắc chắn muốn đăng xuất?")
    if response:  # Nếu người dùng chọn "Yes"
        root.deiconify()  # Hiển thị cửa sổ đăng nhập
        main_window.destroy()  # Đóng cửa sổ chính

# Chạy ứng dụng chính
if __name__ == "__main__":
    root = tk.Tk()
    open_main_window(root)
    root.mainloop()
