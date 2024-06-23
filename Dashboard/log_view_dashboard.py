# import tkinter as tk
# from tkinter import ttk
# class LogViewDashboard:
#     def __init__(self, master):
#         self.master = master
#         self.master.title("Log View Dashboard")
#         self.master.geometry("800x600")
#
#         self.log_tree = ttk.Treeview(self.master)
#         self.log_tree.pack(fill="both", expand=True)
#
#         self.log_tree["columns"] = ("Date", "Time", "Level", "Message")
#
#         self.log_tree.column("#0", width=0, stretch=tk.NO)
#         self.log_tree.column("Date", anchor=tk.W, width=120)
#         self.log_tree.column("Time", anchor=tk.W, width=100)
#         self.log_tree.column("Level", anchor=tk.W, width=80)
#         self.log_tree.column("Message", anchor=tk.W, width=400)
#
#         self.log_tree.heading("#0", text="", anchor=tk.W)
#         self.log_tree.heading("Date", text="Date", anchor=tk.W)
#         self.log_tree.heading("Time", text="Time", anchor=tk.W)
#         self.log_tree.heading("Level", text="Level", anchor=tk.W)
#         self.log_tree.heading("Message", text="Message", anchor=tk.W)
#
#         self.log_tree.insert("", tk.END, values=("2024-06-21", "11:43:51,234", "WARNING", "* Debugger is active!"))
#         self.log_tree.insert("", tk.END, values=("2024-06-21", "11:43:51,244", "INFO", "* Debugger PIN: 169-277-652"))
#
#         tk.Button(self.master, text="Logout", command=self.logout).pack()
#
#
#     def logout(self):
#         self.master.destroy()


import tkinter as tk
from tkinter import messagebox
import requests


class LogViewDashboard:
    def __init__(self, master):
        self.master = master
        self.master.title("Log Viewer")

        self.log_type_label = tk.Label(master, text="Log Type:")
        self.log_type_label.pack()
        self.log_type_entry = tk.Entry(master)
        self.log_type_entry.pack()

        self.start_date_label = tk.Label(master, text="Start Date (YYYY-MM-DD):")
        self.start_date_label.pack()
        self.start_date_entry = tk.Entry(master)
        self.start_date_entry.pack()

        self.end_date_label = tk.Label(master, text="End Date (YYYY-MM-DD):")
        self.end_date_label.pack()
        self.end_date_entry = tk.Entry(master)
        self.end_date_entry.pack()

        self.view_logs_button = tk.Button(master, text="View Logs", command=self.view_logs)
        self.view_logs_button.pack()

    def view_logs(self):
        log_type = self.log_type_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        params = {"type": log_type, "start_date": start_date, "end_date": end_date}
        response = requests.get("http://localhost:5000/get_logs", params=params)

        if response.status_code == 200:
            logs = response.json()
            logs_str = "\n".join([str(log) for log in logs])
            messagebox.showinfo("Logs", logs_str)
        else:
            messagebox.showerror("Error", "Failed to retrieve logs")


if __name__ == "__main__":
    root = tk.Tk()
    app = LogViewerApp(root)
    root.mainloop()
