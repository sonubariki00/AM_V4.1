import tkinter as tk
from tkinter import messagebox
from log_view_dashboard import LogViewDashboard
import requests
class AdminMenu:
    def __init__(self, master, username):
        self.master = master
        self.username = username
        self.master.title("Admin Menu")
        self.master.geometry("1024x768")
        self.master.configure(bg="#f0f0f0")
        self.master.state('zoomed')

        # Admin Menu Label
        tk.Label(self.master, text="Admin Menu", font=("Arial", 24), bg="#f0f0f0").pack(pady=20)

        # Asset Management Frame
        self.asset_frame = tk.Frame(self.master, bg="black", width=300, highlightthickness=2, bd=2,
                                    highlightbackground="white", relief=tk.RAISED)
        tk.Label(self.asset_frame, text="Asset Management", font=("Arial", 16), bg="black", fg="white").pack(pady=10)
        tk.Label(self.asset_frame, text="Asset Name", bg="black", fg="white").pack()
        self.asset_name = tk.Entry(self.asset_frame)
        self.asset_name.pack(pady=5)
        tk.Label(self.asset_frame, text="Asset ID", bg="black", fg="white").pack()
        self.asset_id = tk.Entry(self.asset_frame)
        self.asset_id.pack(pady=5)
        tk.Button(self.asset_frame, text="Add Asset", command=self.add_asset).pack(pady=10)
        tk.Button(self.asset_frame, text="Remove Asset", command=self.remove_asset).pack(pady=10)
        self.asset_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.Y)

        # Employee Management Frame
        self.employee_frame = tk.Frame(self.master, bg="black", width=300, highlightthickness=2, bd=2,
                                       highlightbackground="white", relief=tk.RAISED)
        tk.Label(self.employee_frame, text="Employee Management", font=("Arial", 16), bg="black", fg="white").pack(
            pady=10)
        tk.Label(self.employee_frame, text="Employee Name", bg="black", fg="white").pack()
        self.employee_name = tk.Entry(self.employee_frame)
        self.employee_name.pack(pady=5)
        tk.Label(self.employee_frame, text="Employee ID", bg="black", fg="white").pack()
        self.employee_id = tk.Entry(self.employee_frame)
        self.employee_id.pack(pady=5)
        tk.Button(self.employee_frame, text="Add Employee", command=self.add_employee).pack(pady=10)
        tk.Button(self.employee_frame, text="Remove Employee", command=self.remove_employee).pack(pady=10)
        self.employee_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.Y)

        # View Frame
        self.view_frame = tk.Frame(self.master, bg="#f0f0f0", relief=tk.SUNKEN, bd=2)
        tk.Label(self.view_frame, text="Requests", font=("Arial", 18), bg="#000000", fg="white").pack(pady=10)
        self.request_listbox = tk.Listbox(self.view_frame, width=80, height=20)
        self.request_listbox.pack(pady=10)
        self.view_frame.pack(pady=20, expand=True)
        tk.Button(self.view_frame, text="VIEW Requests", command=self.view_requests).pack(pady=10)
        tk.Button(self.master, text="View LOGS", command=self.view_logs).pack(pady=10)
        tk.Button(self.master, text="Logout", command=self.logout).pack(pady=10)

    def add_asset(self):
        # TO DO: Implement add asset logic
        asset_name = self.asset_name.get()
        asset_id = self.asset_id.get()
        response = requests.post("http://remote-server.com/api/admin/add_asset",
                                json={"asset_name": asset_name,"asset_id": asset_id})
        response.status_code = 200  # Trial check
        if response.status_code == 200:
            messagebox.showinfo("Add Asset", f"Asset{asset_name}added successfully!")
        else:
            messagebox.showerror("Error", "Failed to Add asset")

    def remove_asset(self):
        # TO DO: Implement remove asset logic
        asset_name = self.asset_name.get()
        asset_id = self.asset_id.get()
        response = requests.post("http://remote-server.com/api/admin/remove_asset",
                                 json={"asset_name": asset_name, "asset_id": asset_id})
        response.status_code = 200  # Trial check
        if response.status_code == 200:
            messagebox.showinfo("Remove Asset", f"Asset{asset_name}removed successfully!")
        else:
            messagebox.showerror("Error", "Failed to Remove asset")

    def add_employee(self):
        # TO DO: Implement add employee logic
        employee_name = self.employee_name.get()
        employee_id = self.employee_id.get()
        response = requests.post("http://remote-server.com/api/admin/add_employee",
                                 json={"employee_name": employee_name, "asset_id": employee_id})
        response.status_code = 200  # Trial check
        if response.status_code == 200:
            messagebox.showinfo("Add Employee", f"Employee{employee_name}added successfully!")
        else:
            messagebox.showerror("Error", "Failed to Add Employee")

    def remove_employee(self):
        # TO DO: Implement remove employee logic
        employee_name = self.employee_name.get()
        employee_id = self.employee_id.get()
        response = requests.post("http://remote-server.com/api/admin/remove_employee",
                                 json={"employee_name": employee_name, "employee_id": employee_id})
        response.status_code = 200  # Trial check
        if response.status_code == 200:
            messagebox.showinfo("Add Employee", f"Employee{employee_name}added successfully!")
        else:
            messagebox.showerror("Error", "Failed to Remove Employee")
    def view_requests(self):
        response = requests.post("http://remote-server.com/api/admin/view_requests")
        if response.status_code ==200:
            view= response.json()
            pass
        messagebox.showinfo()

    def view_logs(self):
        self.master.withdraw()
        log_view_root = tk.Toplevel(self.master)
        _ = LogViewDashboard(log_view_root)

        messagebox.showinfo()

    def logout(self):
        self.master.destroy()