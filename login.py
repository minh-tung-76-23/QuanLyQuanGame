import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Import Pillow
from main import open_main_window  # Import hàm open_main_window từ file main.py

def login(event=None):
    username = entry_username.get()
    password = entry_password.get()

        # Kiểm tra nếu các ô trống
    if not username or not password:
        messagebox.showwarning("Warning", "Bạn chưa nhập thông tin để đăng nhập!")
        return

    # Kiểm tra đăng nhập trực tiếp
    if username == "admin" and password == "1":
        messagebox.showinfo("Login", "Đăng nhập thành công!")
        entry_username.delete(0, tk.END)  # Đặt lại dữ liệu cho ô username
        entry_password.delete(0, tk.END)  # Đặt lại dữ liệu cho ô password
        root.withdraw()  # Ẩn form đăng nhập
        open_main_window(root)
    else:
        messagebox.showerror("Login", "Tài khoản hoặc mật khẩu không chính xác!")

        root.withdraw()  # Ẩn form đăng nhập
        open_main_window(root)

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f'{width}x{height}+{x}+{y}')

# Tạo cửa sổ đăng nhập
root = tk.Tk()
root.title("Quản lý quán game - Đăng nhập")
center_window(root, 600, 400)

# Thêm nhãn tiêu đề
label_title = tk.Label(root, text="Quản lý quán game", font=("Arial", 24))
label_title.pack(pady=20)

# Tạo khung chứa ảnh và form đăng nhập
frame_main = tk.Frame(root)
frame_main.pack(fill='both', expand=True)

# Khung chứa ảnh
frame_image = tk.Frame(frame_main, width=300, height=300)
frame_image.pack(side='left', fill='both', expand=True)
frame_image.pack_propagate(False)

# Thêm ảnh (cần thay đổi đường dẫn đến ảnh của bạn)
try:
    # Mở ảnh và thay đổi kích thước
    original_image = Image.open('F:\\LT_IT\\PY\\Woskspace\\QuanLyQuanGame\\img\\bg.png')  # Thay đổi đường dẫn đến ảnh của bạn
    resized_image = original_image.resize((300, 300), Image.Resampling.LANCZOS)
    image = ImageTk.PhotoImage(resized_image)
    label_image = tk.Label(frame_image, image=image)
    label_image.image = image  # Lưu tham chiếu đến ảnh
    label_image.pack(expand=True)
except Exception as e:
    print(f"Error loading image: {e}")
    label_image = tk.Label(frame_image, text="Image not found")
    label_image.pack(expand=True)

# Khung chứa form đăng nhập
frame_login = tk.Frame(frame_main, width=300, padx=20, pady=20)
frame_login.pack(side='right', fill='both', expand=True)
frame_login.pack_propagate(False)

# Định nghĩa các widget trên form đăng nhập
label_login = tk.Label(frame_login, text="Đăng nhập", font=("Arial", 16))
label_login.grid(row=0, column=1, padx=0 , pady=5)

label_username = tk.Label(frame_login, text="Username:")
label_username.grid(row=1, column=0, padx=5, pady=5)
entry_username = tk.Entry(frame_login)
entry_username.grid(row=1, column=1, padx=10, pady=5)

label_password = tk.Label(frame_login, text="Password:")
label_password.grid(row=2, column=0, padx=5, pady=5)
entry_password = tk.Entry(frame_login, show="*")
entry_password.grid(row=2, column=1, padx=10, pady=5)

button_login = tk.Button(frame_login, text="Login", command=login)
button_login.grid(row=3, column=1, padx=5, pady=5)

# Ràng buộc sự kiện Enter với hàm login
entry_username.bind('<Return>', login)
entry_password.bind('<Return>', login)

root.mainloop()
