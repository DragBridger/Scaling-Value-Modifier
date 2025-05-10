import winreg
import ctypes
import sys
import os
import webbrowser
from colorama import init, Fore, Style
import time
import tkinter as tk
from tkinter import ttk, messagebox
import platform
import threading
import requests
from io import BytesIO
from PIL import Image, ImageTk

# Initialize colorama
init(autoreset=True)

# Constants
GITHUB_URL = "https://github.com/DragBridger/Scaling-Value-Modifier"
REGISTRY_PATH = r"SYSTEM\ControlSet001\Control\GraphicsDrivers\Configuration"
DEFAULT_SCALING = 4
TARGET_SCALING = 3

# UI Colors
PRIMARY_COLOR = "#2c3e50"
SECONDARY_COLOR = "#3498db"
SUCCESS_COLOR = "#2ecc71"
WARNING_COLOR = "#f39c12"
ERROR_COLOR = "#e74c3c"
TEXT_COLOR = "#ecf0f1"
BG_COLOR = "#34495e"

class ScalingModifier:
    def __init__(self):
        self.setup_ui()
        
    def setup_ui(self):
        self.root = tk.Tk()
        self.root.title("Display Scaling Modifier")
        self.root.geometry("600x450")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_COLOR)

        # Icon
        icon_url = "https://i.ibb.co/SbPmVXC/d414767d37eae66fddc845db4673f5bf.png"
        try:
            response = requests.get(icon_url)
            img_data = BytesIO(response.content)
            icon_image = Image.open(img_data)
            icon_photo = ImageTk.PhotoImage(icon_image)
            self.root.iconphoto(False, icon_photo)
        except Exception as e:
            print(f"Failed to load icon: {e}")

        self.root.attributes("-topmost", True)
        self.center_window()
        self.setup_styles()
        self.create_widgets()
        
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background=BG_COLOR)
        style.configure('TLabel', background=BG_COLOR, foreground=TEXT_COLOR, font=('Segoe UI', 10))
        style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'))
        style.configure('TButton', font=('Segoe UI', 10), padding=6)
        style.configure('Primary.TButton', background=SECONDARY_COLOR, foreground='white')
        style.configure('Success.TButton', background=SUCCESS_COLOR, foreground='white')
        style.configure('Warning.TButton', background=WARNING_COLOR, foreground='white')
        style.configure('Error.TButton', background=ERROR_COLOR, foreground='white')
        style.configure('TProgressbar', thickness=20)
        
    def create_widgets(self):
        header_frame = ttk.Frame(self.root)
        header_frame.pack(pady=(20, 10), padx=20, fill='x')

        ttk.Label(header_frame, text="Display Scaling Modifier", style='Title.TLabel').pack()
        ttk.Label(header_frame, text="Stretch your screen with any laptop (without external monitor)").pack(pady=5)

        info_frame = ttk.Frame(self.root)
        info_frame.pack(pady=10, padx=20, fill='x')

        self.system_info = tk.Text(info_frame, height=6, width=60, bg=PRIMARY_COLOR, fg=TEXT_COLOR,
                                   font=('Consolas', 9), relief='flat', padx=10, pady=10)
        self.system_info.pack()
        self.system_info.insert('end', self.get_system_info())
        self.system_info.config(state='disabled')

        self.progress = ttk.Progressbar(self.root, orient='horizontal', length=400, mode='determinate')
        self.progress.pack(pady=10)

        self.status_label = ttk.Label(self.root, text="Ready to modify display scaling settings ?", font=('Segoe UI', 10, 'italic'))
        self.status_label.pack(pady=5)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="Modify Scaling", command=self.on_modify_click, style='Primary.TButton').grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="Restart PC", command=self.restart_pc, style='Warning.TButton').grid(row=0, column=1, padx=10)
        ttk.Button(button_frame, text="GitHub", command=self.open_github, style='Success.TButton').grid(row=0, column=2, padx=10)
        ttk.Button(button_frame, text="Exit", command=self.root.quit, style='Error.TButton').grid(row=0, column=3, padx=10)

        if not self.is_admin():
            self.show_admin_warning()

    def get_system_info(self):
        info = [
            f"OS: {platform.system()} {platform.release()}",
            f"Python: {platform.python_version()}",
            f"Admin: {'Yes' if self.is_admin() else 'No'}"
        ]
        return '\n'.join(info)
    
    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def show_admin_warning(self):
        warning_win = tk.Toplevel(self.root)
        warning_win.title("Administrator Rights Required")
        warning_win.configure(bg=ERROR_COLOR)
        warning_win.geometry("450x250")
        warning_win.resizable(False, False)
        warning_win.attributes("-topmost", True)
        self.center_custom_window(warning_win)

        tk.Label(warning_win, text="⚠ ADMINISTRATOR PRIVILEGES REQUIRED ⚠", font=("Segoe UI", 12, "bold"),
                 bg=ERROR_COLOR, fg="white", pady=10).pack()

        tk.Label(warning_win, text="\nThis tool needs ADMINISTRATOR permissions.\n\nPlease relaunch as:\n➡ 'Run as Administrator'",
                 font=("Segoe UI", 10), bg=ERROR_COLOR, fg="white", justify="center").pack(padx=20)

        ttk.Button(warning_win, text="Exit Application", command=lambda: [warning_win.destroy(), self.root.quit()],
                   style="Error.TButton").pack(pady=20)

        warning_win.grab_set()
        warning_win.protocol("WM_DELETE_WINDOW", lambda: [warning_win.destroy(), self.root.quit()])
        self.root.wait_window(warning_win)
        sys.exit(0)

    def center_custom_window(self, win):
        win.update_idletasks()
        width = win.winfo_width()
        height = win.winfo_height()
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f'{width}x{height}+{x}+{y}')

    def on_modify_click(self):
        if not self.is_admin():
            self.show_admin_warning()
            return

        confirm = messagebox.askyesno("Confirmation", "This will modify your display scaling registry settings.\n\nDo you want to continue?", parent=self.root)
        if confirm:
            threading.Thread(target=self.modify_scaling, daemon=True).start()

    def backup_registry(self):
        """Backs up the registry settings to a .reg file on the desktop"""
        try:
            desktop_path = os.path.join(os.environ["USERPROFILE"], "Desktop")
            backup_file = os.path.join(desktop_path, "Scaling Value Modifier.reg")
            command = f'reg export "HKLM\\{REGISTRY_PATH}" "{backup_file}" /y'
            result = os.system(command)
            if result == 0:
                print("Registry backup successful.")
            else:
                print("Failed to export registry.")
        except Exception as e:
            print(f"Error backing up registry: {e}")

    def modify_scaling(self):
        self.update_status("Backing up registry...", WARNING_COLOR)
        self.backup_registry()
        self.update_status("Modifying registry settings...", WARNING_COLOR)
        self.progress['value'] = 0

        try:
            modified_count = 0
            total_count = 0

            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, REGISTRY_PATH, 0, winreg.KEY_READ | winreg.KEY_WRITE) as config_key:
                i = 0
                while True:
                    try:
                        winreg.EnumKey(config_key, i)
                        total_count += 1
                        i += 1
                    except OSError:
                        break

            config_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, REGISTRY_PATH, 0, winreg.KEY_READ | winreg.KEY_WRITE)

            for i in range(total_count):
                try:
                    subkey_name = winreg.EnumKey(config_key, i)
                    subkey_path = f"{REGISTRY_PATH}\\{subkey_name}\\00\\00"

                    try:
                        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey_path, 0, winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE) as subkey:
                            scaling_value, regtype = winreg.QueryValueEx(subkey, "Scaling")
                            if scaling_value == DEFAULT_SCALING:
                                winreg.SetValueEx(subkey, "Scaling", 0, regtype, TARGET_SCALING)
                                modified_count += 1
                    except FileNotFoundError:
                        pass

                    self.progress['value'] = ((i + 1) / total_count) * 100
                    self.root.update()
                except Exception as e:
                    print(f"Error processing key: {e}")

            if modified_count > 0:
                self.update_status(f"Successfully modified {modified_count} registry entries!", SUCCESS_COLOR)
                messagebox.showinfo("Success", f"Updated {modified_count} entries.\nRestart may be required.", parent=self.root)
            else:
                self.update_status("No changes were needed", TEXT_COLOR)
                messagebox.showinfo("No Changes", "Your display scaling settings are already optimized.", parent=self.root)

        except Exception as e:
            self.update_status(f"Error: {str(e)}", ERROR_COLOR)
            messagebox.showerror("Error", f"An error occurred:\n\n{str(e)}", parent=self.root)

        messagebox.showinfo("Thank You!", "Thanks for using Display Scaling Modifier!\nPlease star the repo on GitHub.", parent=self.root)
        self.open_github()
        self.progress['value'] = 100

    def update_status(self, message, color=TEXT_COLOR):
        self.status_label.config(text=message, foreground=color)
        self.root.update()

    def restart_pc(self):
        warning_win = tk.Toplevel(self.root)
        warning_win.title("⚠ SYSTEM RESTART WARNING ⚠")
        warning_win.configure(bg=WARNING_COLOR)
        warning_win.geometry("500x300")
        warning_win.resizable(False, False)
        warning_win.attributes("-topmost", True)
        self.center_custom_window(warning_win)

        tk.Label(warning_win, text="⚠ IMMEDIATE SYSTEM RESTART WARNING ⚠", font=("Segoe UI", 12, "bold"),
                 bg=WARNING_COLOR, fg="white", pady=15).pack()

        msg = ("\nWARNING: This will RESTART your computer immediately!\n\n"
               "• All unsaved work will be PERMANENTLY LOST\n"
               "• All running applications will be FORCE CLOSED\n"
               "• Any ongoing processes will be INTERRUPTED\n\n"
               "Are you sure you want to continue?")
        tk.Label(warning_win, text=msg, font=("Segoe UI", 10), bg=WARNING_COLOR,
                 fg="white", justify="center").pack(padx=20, pady=10)

        button_frame = tk.Frame(warning_win, bg=WARNING_COLOR)
        button_frame.pack(pady=15)

        ttk.Button(button_frame, text="RESTART NOW", command=lambda: [
            self.update_status("Preparing to restart...", WARNING_COLOR),
            warning_win.destroy(),
            os.system("shutdown /r /t 0")
        ], style="Warning.TButton").pack(side="left", padx=10)

        ttk.Button(button_frame, text="CANCEL", command=warning_win.destroy, style="TButton").pack(side="right", padx=10)

        warning_win.grab_set()
        warning_win.protocol("WM_DELETE_WINDOW", warning_win.destroy)
        self.root.wait_window(warning_win)

    def open_github(self):
        webbrowser.open(GITHUB_URL)
        self.update_status("Opened GitHub repository", SECONDARY_COLOR)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ScalingModifier()
    app.run()
