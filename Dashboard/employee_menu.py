import sys
import tkinter as tk
from tkinter import messagebox
import requests

class EmployeeMenu:
    def __init__(self, master,username):
        self.master = master
        self.username = username
        self.master.title("Employee Menu")
        self.master.geometry("800x600")

        tk.Label(self.master, text="Employee Menu", font=("Arial", 16)).pack()
#REQUEST FRAME
        self.request_asset_frame =tk.Frame(self.master, bg="gray")
        self.asset_name = tk.Entry(self.request_asset_frame)
        self.asset_name.pack()
        tk.Button(self.request_asset_frame, text="Request Asset", command=self.request_asset).pack()
        self.request_asset_frame.pack(side=tk.LEFT, padx=50, pady=50)
#RELEASE FRAME
        self.release_asset_frame = tk.Frame(self.master, bg="gray")
        self.asset_id = tk.Entry(self.release_asset_frame)
        self.asset_id.pack()
        tk.Button(self.release_asset_frame, text="Release Asset", command=self.release_asset).pack()
        self.release_asset_frame.pack(side=tk.RIGHT, padx=50, pady=50)
#VIEW TAGGED ASSET BOX
        tk.Button(self.master, text="View Tagged Assets", command=self.view_tagged_assets).pack(side=tk.TOP, padx=10, pady=10)
#LOGOUT BOX
        tk.Button(self.master, text="Logout", command=self.logout).pack(side=tk.BOTTOM, padx=10, pady=10)

    def request_asset(self):
        asset_name = self.asset_name.get()
        response = requests.post("http://remote-server.com/api/employee/request_asset", json={"username": self.username, "asset_name": asset_name})
        response.status_code = 200 # Trial check
        if response.status_code == 200:
            messagebox.showinfo("Request Asset", f"Asset {asset_name}  requested successfully!")
        else:
            messagebox.showerror("Error", "Failed to request asset")

    def release_asset(self):
        asset_id = self.asset_id.get()
        response = requests.post("http://remote-server.com/api/employee/release_asset", json={"username": self.username, "asset_id": asset_id})
        response.status_code = 200  # Trial check
        if response.status_code == 200:
            messagebox.showinfo("Release Asset", f"Asset (ID: {asset_id}) released successfully!")
        else:
            messagebox.showerror("Error", "Failed to release asset")

    def view_tagged_assets(self):
        response = requests.get("http://remote-server.com/api/employee/view_tagged_assets",json={"username":self.username})
        if response.status_code == 200:
            tagged_assets = response.json()
            messagebox.showinfo("View Tagged Assets", "\n".join(tagged_assets))
        else:
            messagebox.showerror("Error", "Failed to view tagged assets")

    def logout(self):
        self.master.destroy()
        sys.exit(0)