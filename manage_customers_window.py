import tkinter as tk
from tkinter import messagebox, Scrollbar, Canvas, Label, Entry, Button, Listbox, END
import mysql.connector

class ManageCustomersWindow:
    def __init__(self, root, main_window):
        self.root = root
        self.main_window = main_window
        self.root.title("Quản lý quán game - Người dùng")
        self.root.geometry('1100x600+200+100')

        # Thiết lập kết nối đến MySQL
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="quanlyquangame"
        )
        self.cursor = self.connection.cursor()

        # Frame chứa danh sách người dùng (Listbox)
        self.listbox_frame = tk.Frame(self.root, width=400)
        self.listbox_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Listbox để hiển thị danh sách người dùng
        self.listbox = Listbox(self.listbox_frame, width=80, height=20)
        self.listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Tạo thanh cuộn cho listbox
        scrollbar = Scrollbar(self.listbox_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Binding sự kiện để cập nhật entry fields khi chọn item trong listbox
        self.listbox.bind('<<ListboxSelect>>', self.on_select)

        # Frame chứa các label, entry và button
        self.entry_frame = tk.Frame(self.root, width=600)
        self.entry_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Label "Thêm dịch vụ mới" ở giữa trên cùng
        label_title = tk.Label(self.entry_frame, text="Quản lý người dùng", font=("Arial", 18, "bold"))
        label_title.grid(row=0, column=0, columnspan=3, padx=0, pady=50)

        # Label và Entry cho Tên người dùng
        self.label_name = Label(self.entry_frame, text="Tên người dùng:")
        self.label_name.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
        self.entry_name = Entry(self.entry_frame, width=50)
        self.entry_name.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        # Label và Entry cho Tài khoản
        self.label_account = Label(self.entry_frame, text="Tài khoản:")
        self.label_account.grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)
        self.entry_account = Entry(self.entry_frame, width=50)
        self.entry_account.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        # Label và Entry cho Mật khẩu
        self.label_password = Label(self.entry_frame, text="Mật khẩu:")
        self.label_password.grid(row=3, column=0, padx=10, pady=10, sticky=tk.E)
        self.entry_password = Entry(self.entry_frame, width=50, show='*')
        self.entry_password.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)

        # Label và Entry cho Email
        self.label_email = Label(self.entry_frame, text="Email:")
        self.label_email.grid(row=4, column=0, padx=10, pady=10, sticky=tk.E)
        self.entry_email = Entry(self.entry_frame, width=50)
        self.entry_email.grid(row=4, column=1, padx=10, pady=10, sticky=tk.W)

        # Label và Entry cho Số điện thoại
        self.label_phone = Label(self.entry_frame, text="Số điện thoại:")
        self.label_phone.grid(row=5, column=0, padx=10, pady=10, sticky=tk.E)
        self.entry_phone = Entry(self.entry_frame, width=50)
        self.entry_phone.grid(row=5, column=1, padx=10, pady=10, sticky=tk.W)

        # Label và Entry cho Số tiền
        self.label_money = Label(self.entry_frame, text="Số tiền:")
        self.label_money.grid(row=6, column=0, padx=10, pady=10, sticky=tk.E)
        self.entry_money = Entry(self.entry_frame, width=50)
        self.entry_money.grid(row=6, column=1, padx=10, pady=10, sticky=tk.W)

        # Buttons: Thêm, Sửa, Xóa, thoát
        self.button_add = Button(self.entry_frame, text="Thêm người dùng", command=self.add_user)
        self.button_add.grid(row=7, column=0, padx=1, pady=10)
        self.button_edit = Button(self.entry_frame, text="Sửa thông tin người dùng", command=self.edit_user)
        self.button_edit.grid(row=7, column=1, padx=1, pady=10)
        self.button_delete = Button(self.entry_frame, text="Xóa người dùng", command=self.delete_user)
        self.button_delete.grid(row=7, column=2, padx=1, pady=10)
        self.button_exit = Button(self.entry_frame, text="Thoát", command=self.exit_window)
        self.button_exit.grid(row=8, column=1, padx=1, pady=10)

        # Load danh sách người dùng ban đầu
        self.load_users()

    def exit_window(self):
        self.root.destroy()  # Đóng cửa sổ quản lý dịch vụ
        self.main_window.deiconify()  # Hiện lại cửa sổ main



    def load_users(self):
        try:
            self.cursor.execute("SELECT * FROM NguoiDung")
            users = self.cursor.fetchall()
            self.listbox.delete(0, END)
            
            # Định dạng cho từng cột trong bảng
            header = "ID".ljust(5) + "Tên người dùng".ljust(20) + "Mật khẩu".ljust(20) + "Email".ljust(35) + "SĐT".ljust(15) + "Số dư".rjust(15)
            self.listbox.insert(END, header)
            
            for user in users:
                user_id, name, account, password, email, phone, money = user
                formatted_money = "{:,.0f}".format(money)
                
                # Định dạng dữ liệu của từng cột
                formatted_data = f"{user_id}".ljust(5) + \
                                f"{name}({account})".ljust(20) + \
                                f"{password}".ljust(18) + \
                                f"{email}".ljust(25) + \
                                f"{phone}".ljust(15) + \
                                f"{formatted_money} đ".rjust(15)
                
                self.listbox.insert(END, formatted_data)
    
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tải danh sách người dùng: {str(e)}")

    def on_select(self, event):
        try:
            index = self.listbox.curselection()[0]
            selected_user = self.listbox.get(index)
            user_id = selected_user.split(':')[0].strip()
            self.cursor.execute("SELECT * FROM NguoiDung WHERE nguoi_dung_id = %s", (user_id,))
            user = self.cursor.fetchone()
            if user:
                _, name, account, password, email, phone, money = user
                self.entry_name.delete(0, END)
                self.entry_name.insert(END, name)
                self.entry_account.delete(0, END)
                self.entry_account.insert(END, account)
                self.entry_password.delete(0, END)
                self.entry_password.insert(END, password)
                self.entry_email.delete(0, END)
                self.entry_email.insert(END, email)
                self.entry_phone.delete(0, END)
                self.entry_phone.insert(END, phone)
                self.entry_money.delete(0, END)
                self.entry_money.insert(END, money)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi chọn người dùng: {str(e)}")

    def add_user(self):
        name = self.entry_name.get().strip()
        account = self.entry_account.get().strip()
        password = self.entry_password.get().strip()
        email = self.entry_email.get().strip()
        phone = self.entry_phone.get().strip()
        money = self.entry_money.get().strip()

        if not (name and account and password):  # Kiểm tra các trường bắt buộc
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin (Tên, Tài khoản, Mật khẩu).")
            return

        try:
            insert_query = "INSERT INTO NguoiDung (ten, tai_khoan, mat_khau, email, so_dien_thoai, so_tien) VALUES (%s, %s, %s, %s, %s, %s)"
            self.cursor.execute(insert_query, (name, account, password, email, phone, money))
            self.connection.commit()
            self.load_users()
            messagebox.showinfo("Thông báo", "Thêm người dùng thành công!")
            self.entry_name.delete(0, END)
            self.entry_account.delete(0, END)
            self.entry_password.delete(0, END)
            self.entry_email.delete(0, END)
            self.entry_phone.delete(0, END)
            self.entry_money.delete(0, END)

        except Exception as e:
            self.connection.rollback()
            messagebox.showerror("Lỗi", f"Lỗi khi thêm người dùng: {str(e)}")

    def edit_user(self):
        name = self.entry_name.get().strip()
        account = self.entry_account.get().strip()
        password = self.entry_password.get().strip()
        email = self.entry_email.get().strip()
        phone = self.entry_phone.get().strip()
        money = self.entry_money.get().strip()

        if not (name and account and password):  # Kiểm tra các trường bắt buộc
            messagebox.showerror("Lỗi", "Vui lòng chọn người dùng và nhập đầy đủ thông tin (Tên, Tài khoản, Mật khẩu).")
            return

        try:
            index = self.listbox.curselection()[0]
            selected_user = self.listbox.get(index)
            user_id = selected_user.split(':')[0].strip()

            update_query = "UPDATE NguoiDung SET ten = %s, tai_khoan = %s, mat_khau = %s, email = %s, so_dien_thoai = %s, so_tien = %s WHERE nguoi_dung_id = %s"
            self.cursor.execute(update_query, (name, account, password, email, phone, money, user_id))
            self.connection.commit()
            self.load_users()
            messagebox.showinfo("Thông báo", "Cập nhật người dùng thành công!")
            self.entry_name.delete(0, END)
            self.entry_account.delete(0, END)
            self.entry_password.delete(0, END)
            self.entry_email.delete(0, END)
            self.entry_phone.delete(0, END)
            self.entry_money.delete(0, END)
        except Exception as e:
            self.connection.rollback()
            messagebox.showerror("Lỗi", f"Lỗi khi cập nhật người dùng: {str(e)}")

    def delete_user(self):
        try:
            index = self.listbox.curselection()[0]
            selected_user = self.listbox.get(index)
            user_id = selected_user.split(':')[0].strip()

            delete_query = "DELETE FROM NguoiDung WHERE nguoi_dung_id = %s"
            self.cursor.execute(delete_query, (user_id,))
            self.connection.commit()
            self.load_users()
            messagebox.showinfo("Thông báo", "Xóa người dùng thành công!")
            self.entry_name.delete(0, END)
            self.entry_account.delete(0, END)
            self.entry_password.delete(0, END)
            self.entry_email.delete(0, END)
            self.entry_phone.delete(0, END)
            self.entry_money.delete(0, END)
        except Exception as e:
            self.connection.rollback()
            messagebox.showerror("Lỗi", f"Lỗi khi xóa người dùng: {str(e)}")

# Phần chạy ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    app = ManageCustomersWindow(root)
    root.mainloop()
