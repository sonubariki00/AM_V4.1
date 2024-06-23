import tkinter as tk
from tkinter import messagebox
import requests
from admin_menu import AdminMenu
from employee_menu import EmployeeMenu

class Login:
    def __init__(self, master):
        self.master = master
        self.master.title("Asset Management Login")
        self.master.geometry("800x600")

        # Admin Login Frame
        self.admin_frame = tk.Frame(self.master, bg="black",cursor="hand2",width=200,
        highlightthickness=2,bd=2,highlightbackground="white",relief=tk.RAISED )
        self.admin_frame.pack(side=tk.LEFT, padx=100)

        tk.Label(self.admin_frame, text="Admin Login", font=("Arial", 16)).pack()
        tk.Label(self.admin_frame, text="Username:").pack()
        self.admin_username = tk.Entry(self.admin_frame)
        self.admin_username.pack()
        tk.Label(self.admin_frame, text="Password:").pack()
        self.admin_password = tk.Entry(self.admin_frame, show="*")
        self.admin_password.pack()
        tk.Button(self.admin_frame, text="Login", command=self.admin_login).pack()

        # Employee Login Frame
        self.employee_frame = tk.Frame(self.master, bg="black",cursor="hand2",width=200,
        highlightthickness=2,bd=2,highlightbackground="white",relief=tk.RAISED)
        self.employee_frame.pack(side=tk.RIGHT, padx=100)

        tk.Label(self.employee_frame, text="Employee Login", font=("Arial", 16)).pack()
        tk.Label(self.employee_frame, text="Username:").pack()
        self.employee_username = tk.Entry(self.employee_frame)
        self.employee_username.pack()
        tk.Label(self.employee_frame, text="Password:").pack()
        self.employee_password = tk.Entry(self.employee_frame, show="*")
        self.employee_password.pack()
        tk.Button(self.employee_frame, text="Login", command=self.employee_login).pack()

    def admin_login(self):
        username = self.admin_username.get()
        password = self.admin_password.get()

        response = requests.post("http://localhost:5000/api/admin/login", json={"username": username, "password": password})
        # response.status_code = 200 # Trial Check
        if response.status_code == 200:
            self.master.withdraw()
            admin_menu_root = tk.Toplevel(self.master)
            _ =AdminMenu(admin_menu_root,username)
        else:
            messagebox.showerror("Invalid Credentials", "Invalid username or password")

    def employee_login(self):
        username = self.employee_username.get()
        password = self.employee_password.get()

        response = requests.post("http://localhost:5000/api/employee/login", json={"username": username, "password": password})
        #response.status_code =200   # Trial Check
        if response.status_code == 200:
            self.master.withdraw()
            employee_menu_root = tk.Toplevel(self.master)
            _ = EmployeeMenu(employee_menu_root,username)
        else:
            messagebox.showerror("Invalid Credentials", "Invalid username or password")

if __name__ == "__main__":
    root = tk.Tk()
    app = Login(root)
    root.mainloop()

