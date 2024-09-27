import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, Scrollbar, Canvas, Entry, Label
import mysql.connector
from PIL import Image, ImageTk
import os

class ManageServicesWindow:
    def __init__(self, root, main_window):
        self.root = root
        self.main_window = main_window

        self.root.title("Quản lý quán game - Dịch vụ")
        self.root.geometry('1100x600+200+100')

        # Thiết lập kết nối
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="quanlyquangame"
        )
        self.cursor = self.connection.cursor()

        # Tạo một Frame để chứa hai nút chức năng
        button_frame = tk.Frame(self.root)
        button_frame.pack(side=tk.BOTTOM, padx=20, pady=20)

        # Nút chức năng thêm
        btn_add = tk.Button(button_frame, text="Thêm dịch vụ", width=15, command=self.add_service)
        btn_add.pack(side=tk.LEFT, padx=10)

        # Nút chức năng thoát
        btn_exit = tk.Button(button_frame, text="Thoát", width=15, command=self.exit_window)
        btn_exit.pack(side=tk.LEFT, padx=10)

        # Tạo một vùng có thể cuộn được
        self.canvas = Canvas(root)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Thêm thanh cuộn
        scrollbar = Scrollbar(root, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Frame để chứa danh sách dịch vụ
        self.services_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.services_frame, anchor=tk.NW)

        # Hiển thị các dịch vụ
        self.show_services()

        # Bắt sự kiện để điều chỉnh vùng có thể cuộn
        self.services_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Label hiển thị thông tin chi tiết dịch vụ khi click
        self.detail_label = tk.Label(root, text="", font=("Arial", 12))
        self.detail_label.pack(pady=10)

        self.new_image_filename = None

    def show_services(self):
        self.cursor.execute("SELECT dich_vu_id, ten_dich_vu, anh_dich_vu, gia FROM DichVu")
        services = self.cursor.fetchall()

        # Tính toán số dịch vụ trên mỗi hàng
        num_services_per_row = 3
        for i, (id_dich_vu, ten_dich_vu, anh_dich_vu, gia) in enumerate(services):
            # Tính toán vị trí của dịch vụ trong grid
            row = i // num_services_per_row
            col = i % num_services_per_row
            
            # Tạo một Frame con để chứa thông tin dịch vụ
            service_frame = tk.Frame(self.services_frame, bd=2, relief=tk.GROOVE, width=300, height=220)
            service_frame.pack_propagate(False)  # Không cho phép frame tự điều chỉnh kích thước
            service_frame.grid(row=row, column=col, padx=30, pady=10, sticky=tk.NSEW)

            # Tạo một Label để hiển thị tên dịch vụ, màu đỏ
            label_name = tk.Label(service_frame, text=ten_dich_vu, height= 3, font=("Arial", 13, "bold"), fg="red", wraplength=250)
            label_name.pack(pady=2)

            # Hiển thị ảnh dịch vụ
            try:
                image = Image.open(f'F:\\LT_IT\\PY\\Woskspace\\QuanLyQuanGame\\img\\{anh_dich_vu}')
                image = image.resize((100, 100), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                label_image = tk.Label(service_frame, image=photo)
                label_image.image = photo  # Giữ tham chiếu để không bị hủy
                label_image.pack(pady=10)
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi tải ảnh: {str(e)}")

            # Hiển thị giá dịch vụ
            formatted_price = "{:,.0f}".format(gia)
            label_price = tk.Label(service_frame, text=f"Giá: {formatted_price} đ", font=("Arial", 10))
            label_price.pack(pady=5)

            # Bắt sự kiện click vào dịch vụ để hiển thị chi tiết
            label_name.bind("<Button-1>", lambda event,id_dvu= id_dich_vu, ten_dv=ten_dich_vu, anh_dv=anh_dich_vu, gia=gia: self.show_service_details(id_dvu,ten_dv, anh_dv, gia))

    def show_service_details(self, id_dvu, ten_dich_vu, anh_dich_vu, gia):
        # Tạo cửa sổ chi tiết mới
        service_window = Toplevel(self.root)
        service_window.title(f"Chi tiết dịch vụ - {ten_dich_vu}")
        service_window.geometry('500x600+500+120')

        # Label "Chi tiết dịch vụ" ở giữa trên cùng
        label_title = tk.Label(service_window, text="Chi tiết dịch vụ", font=("Arial", 18, "bold"))
        label_title.grid(row=0, column=0, columnspan=3, padx=0, pady=50)

        # Label và entry cho Tên dịch vụ
        label_name = tk.Label(service_window, text="Tên dịch vụ:", font=("Arial", 16))
        label_name.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
        entry_name_service = tk.Entry(service_window, font=("Arial", 14))
        entry_name_service.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
        entry_name_service.insert(tk.END, ten_dich_vu)

        # Label và entry cho Giá dịch vụ
        label_price = tk.Label(service_window, text="Giá:", font=("Arial", 14))
        label_price.grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)
        entry_price = Entry(service_window, font=("Arial", 14))
        entry_price.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)
        entry_price.insert(tk.END, gia)

        # Hiển thị ảnh dịch vụ
        try:
            image = Image.open(f'F:\\LT_IT\\PY\\Woskspace\\QuanLyQuanGame\\img\\{anh_dich_vu}')
            image = image.resize((300, 300), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            label_image = tk.Label(service_window, image=photo)
            label_image.image = photo  # Giữ tham chiếu để không bị hủy
            label_image.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tải ảnh: {str(e)}")

        # Nút chọn ảnh mới
        btn_select_image = tk.Button(service_window, text="Chọn ảnh mới", command=lambda: self.select_new_image(label_image))
        btn_select_image.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        # Nút lưu thay đổi
        btn_save = tk.Button(service_window, text="Lưu", width=15, command=lambda: self.save_service_changes(id_dvu, entry_name_service.get(), entry_price.get()))
        btn_save.grid(row=5, column=1, padx=10, pady=10)

        # Nút xóa
        btn_delete = tk.Button(service_window, text="Xóa", width=15, command=lambda: self.delete_service(id_dvu, service_window))
        btn_delete.grid(row=5, column=0, padx=10, pady=10)

        # Nút thoát
        btn_exit = tk.Button(service_window, text="Thoát", width=15, command=service_window.destroy)
        btn_exit.grid(row=5, column=2, padx=10, pady=10)

        # Thiết lập các cột và hàng để cửa sổ có layout chặt chẽ
        service_window.grid_columnconfigure(1, weight=1)  # Cột entry đàn hồi theo kích thước cửa sổ
        service_window.grid_rowconfigure(3, weight=1)  # Hàng đàn hồi dựa trên kích thước cửa sổ


    def select_new_image(self, label_image):
        # Hàm để chọn ảnh mới từ tệp trên máy tính
        file_path = filedialog.askopenfilename(title="Chọn ảnh", filetypes=[("Image Files", "*.png; *.jpg; *.jpeg")])
        if file_path:
            try:
                image = Image.open(file_path)
                image = image.resize((300, 300), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                label_image.config(image=photo)
                label_image.image = photo  # Giữ tham chiếu để không bị hủy
                label_image.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
                self.new_image_filename = os.path.basename(file_path)
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi tải ảnh: {str(e)}")

    def exit_window(self):
        self.root.destroy()  # Đóng cửa sổ quản lý dịch vụ
        self.main_window.deiconify()  # Hiện lại cửa sổ main

    def save_service_changes(self, id_dvu, ten_dich_vu, gia):
        # Xử lý lưu các thay đổi vào cơ sở dữ liệu
        try:
            # Cập nhật giá của dịch vụ
            update_query = "UPDATE DichVu SET gia = %s, ten_dich_vu = %s WHERE dich_vu_id = %s"
            self.cursor.execute(update_query, (gia, ten_dich_vu, id_dvu))

            # Nếu có ảnh mới được chọn, cập nhật tên file ảnh
            if self.new_image_filename:
                update_image_query = "UPDATE DichVu SET anh_dich_vu = %s WHERE dich_vu_id = %s"
                self.cursor.execute(update_image_query, (self.new_image_filename, id_dvu))

            self.connection.commit()
            self.show_services()
            messagebox.showinfo("Thông báo", "Cập nhật thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi cập nhật: {str(e)}")

    def delete_service(self, id_dvu, service_window):
        # Xử lý xóa dịch vụ khỏi cơ sở dữ liệu
        try:
            response = messagebox.askyesno("Thông báo", "Bạn có chắc chắn muốn xóa dịch vụ này?")
            if response:  # Nếu người dùng chọn "Yes"
                delete_query = "DELETE FROM DichVu WHERE dich_vu_id = %s"
                self.cursor.execute(delete_query, (id_dvu,))
                self.connection.commit()
                self.show_services()
                messagebox.showinfo("Thông báo", "Xóa dịch vụ thành công!")
                service_window.destroy()  
        except mysql.connector.Error as error:
            self.connection.rollback()
            messagebox.showerror("Lỗi", f"Lỗi khi xóa dịch vụ: {error.msg}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa dịch vụ: {str(e)}")
            
    def add_service(self):
        # Tạo cửa sổ thêm mới dịch vụ
        add_window = Toplevel(self.root)
        add_window.title("Thêm dịch vụ mới")
        add_window.geometry('500x670+550+70')

        # Label "Thêm dịch vụ mới" ở giữa trên cùng
        label_title = tk.Label(add_window, text="Thêm dịch vụ mới", font=("Arial", 18, "bold"))
        label_title.grid(row=0, column=0, columnspan=3, padx=0, pady=50)

        # Label và entry cho Tên dịch vụ
        label_name = tk.Label(add_window, text="Tên dịch vụ:", font=("Arial", 16))
        label_name.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
        entry_name_service = tk.Entry(add_window, font=("Arial", 14))
        entry_name_service.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        # Label và entry cho Giá dịch vụ
        label_price = tk.Label(add_window, text="Giá:", font=("Arial", 14))
        label_price.grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)
        entry_price = tk.Entry(add_window, font=("Arial", 14))
        entry_price.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        # Frame để chứa label hiển thị ảnh và nút chọn ảnh
        image_frame = tk.Frame(add_window)
        image_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W)

        # Label hiển thị ảnh
        label_image = tk.Label(image_frame, text="Chọn ảnh:", font=("Arial", 14))
        label_image.grid(row=0, column=0, padx=(0, 10), pady=10, sticky=tk.E)

        # Nút chọn ảnh
        btn_select_image = tk.Button(image_frame, text="Chọn ảnh", command=lambda: self.select_new_image(label_image))
        btn_select_image.grid(row=0, column=1, padx=(0, 10), pady=10, sticky=tk.W)

        # Nút lưu dịch vụ mới
        btn_save = tk.Button(add_window, text="Lưu", width=15, command=lambda: self.save_new_service(entry_name_service.get(), entry_price.get()))
        btn_save.grid(row=5, column=1, padx=10, pady=10)

        # Nút thoát
        btn_exit = tk.Button(add_window, text="Thoát", width=15, command=add_window.destroy)
        btn_exit.grid(row=5, column=2, padx=10, pady=10, sticky=tk.E)

        # Thiết lập các cột và hàng để cửa sổ có layout chặt chẽ
        add_window.grid_columnconfigure(1, weight=1)  # Cột entry đàn hồi theo kích thước cửa sổ
        add_window.grid_rowconfigure(4, weight=1)  # Hàng đàn hồi dựa trên kích thước cửa sổ

    def save_new_service(self, ten_dich_vu, gia):
        # Kiểm tra điều kiện nếu tên dịch vụ hoặc giá rỗng
        if not ten_dich_vu or not gia:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin (Tên dịch vụ và Giá).")
            return

        try:
            # Thực hiện INSERT dữ liệu vào bảng DichVu
            insert_query = "INSERT INTO DichVu (ten_dich_vu, gia) VALUES (%s, %s)"
            self.cursor.execute(insert_query, (ten_dich_vu, gia))
            service_id = self.cursor.lastrowid  # Lấy ID của dịch vụ vừa được thêm vào

            # Nếu có tên file ảnh mới được chọn, cập nhật tên file ảnh
            if self.new_image_filename:
                update_image_query = "UPDATE DichVu SET anh_dich_vu = %s WHERE dich_vu_id = %s"
                self.cursor.execute(update_image_query, (self.new_image_filename, service_id))
                self.connection.commit()
                self.show_services()
                messagebox.showinfo("Thông báo", "Thêm mới dịch vụ thành công!")
            else:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn ảnh để thêm mới dịch vụ.")
                # Nếu không có ảnh, rollback transaction để không lưu dữ liệu vào bảng DichVu
                self.connection.rollback()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi thêm mới dịch vụ: {str(e)}")

# Phần chạy ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    app = ManageServicesWindow(root)
    root.mainloop()
