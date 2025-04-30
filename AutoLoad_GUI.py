import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from AutoLoad import write_pid_file
from selenium.common.exceptions import WebDriverException
import ctypes

# 全局标志位，用于控制 loopLoad 的运行状态
running_flag = threading.Event()

def loopLoad_with_flag(usrname, passwd, browserChoice='firefox'):
    """带有运行标志位的 loopLoad"""
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver import FirefoxOptions, ChromeOptions
    import time
    import random

    while running_flag.is_set():  # 检查运行标志位
        try:
            if browserChoice == 'firefox':
                opts = FirefoxOptions()
                opts.add_argument("--headless")
                browser = webdriver.Firefox(options=opts)
            elif browserChoice == 'chrome':
                opts = ChromeOptions()
                opts.add_argument("--headless")
                browser = webdriver.Chrome(options=opts)
            else:
                raise ValueError("Unsupported browser choice")

            el = lambda id: browser.find_element(By.ID, id)
            browser.get('http://10.0.0.55/')
            time.sleep(1)

            try:
                if el("logout"):
                    print("Bit-Web still OK!")
                    browser.close()
                    time.sleep(random.randint(3, 7))
                    continue
            except:
                el("username").clear()
                el("password").clear()
                el("username").send_keys(usrname)
                el("password").send_keys(passwd)
                el("login").click()
                time.sleep(2)
                print("Bit-Web OK!")

        except WebDriverException as e:
            print("WebDriver Error:", e)
        except Exception as e:
            print("Error:", e)
        finally:
            try:
                browser.close()
            except:
                pass

        time.sleep(1)  # 避免过于频繁的循环

class AutoLoadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BIT-Web AutoLogin")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        # 用户名输入
        tk.Label(root, text="用户名:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.username_entry = tk.Entry(root, width=30)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        # 密码输入
        tk.Label(root, text="密码:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.password_entry = tk.Entry(root, width=30, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # 浏览器选择
        tk.Label(root, text="选择浏览器:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.browser_choice = ttk.Combobox(root, values=["Firefox", "Chrome"], state="readonly", width=28)
        self.browser_choice.grid(row=2, column=1, padx=10, pady=10)
        self.browser_choice.current(0)

        # 启动和停止按钮
        self.start_button = tk.Button(root, text="启动", command=self.start_autoload, width=15)
        self.start_button.grid(row=3, column=0, padx=10, pady=20)

        self.stop_button = tk.Button(root, text="停止", command=self.stop_autoload, width=15, state="disabled")
        self.stop_button.grid(row=3, column=1, padx=10, pady=20)

        # 状态显示
        self.status_label = tk.Label(root, text="状态: 未启动", fg="red")
        self.status_label.grid(row=4, column=0, columnspan=2, pady=10)

        self.autoload_thread = None

    def start_autoload(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        browser = self.browser_choice.get().lower()

        if not username or not password:
            messagebox.showerror("错误", "用户名和密码不能为空！")
            return

        # 设置运行标志位
        running_flag.set()

        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.status_label.config(text="状态: 运行中", fg="green")

        # 启动线程运行 loopLoad_with_flag
        self.autoload_thread = threading.Thread(target=loopLoad_with_flag, args=(username, password, browser))
        self.autoload_thread.daemon = True
        self.autoload_thread.start()

    def stop_autoload(self):
        # 清除运行标志位
        running_flag.clear()

        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.status_label.config(text="状态: 未启动", fg="red")

        # 强制终止当前 Python 进程
        messagebox.showinfo("提示", "自动登录已停止！")
        os._exit(0)  # 强制退出整个程序

if __name__ == "__main__":
    # 初始化运行标志位
    running_flag.clear()

    root = tk.Tk()
    app = AutoLoadApp(root)
    root.mainloop()