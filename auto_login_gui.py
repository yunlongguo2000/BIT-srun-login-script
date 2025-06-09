import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
import sys
import subprocess

# 导入auto_login.py中的always_login函数
import auto_login

class AutoLoginGUI:
    def __init__(self, master):
        self.master = master
        master.title("自动登录工具")
        master.geometry("400x400")

        tk.Label(master, text="检测间隔(秒):").pack()
        self.interval_entry = tk.Entry(master)
        self.interval_entry.insert(0, "5")
        self.interval_entry.pack()

        tk.Label(master, text="测试IP或域名:").pack()
        self.ip_entry = tk.Entry(master)
        self.ip_entry.insert(0, "baidu.com")
        self.ip_entry.pack()

        tk.Label(master, text="srun.exe 路径:").pack()
        self.path_entry = tk.Entry(master)
        self.path_entry.insert(0, "F:\BIT-srun-login-script\srun.exe")
        self.path_entry.pack()

        btn_frame = tk.Frame(master)
        btn_frame.pack(pady=5)

        self.browse_btn = tk.Button(btn_frame, text="浏览", command=self.browse_file)
        self.browse_btn.pack(side=tk.LEFT, padx=5)

        self.start_btn = tk.Button(btn_frame, text="启动", command=self.start)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = tk.Button(btn_frame, text="停止", command=self.stop, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        self.log_text = tk.Text(master, height=20)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        self.thread = None
        self.stop_flag = threading.Event()
        self.proc = None  # 保存子进程对象

    def browse_file(self):
        path = filedialog.askopenfilename(title="选择srun.exe", filetypes=[("可执行文件", "*.exe")])
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)

    def log(self, msg):
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)

    def run_command_with_output(self, cmd):
        # 实时读取子进程输出并显示到日志
        try:
            self.proc = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
                universal_newlines=True,
                encoding="utf-8"
            )
            for line in self.proc.stdout:
                self.log(line.rstrip())
            self.proc.stdout.close()
            self.proc.wait()
            return self.proc.returncode
        except Exception as e:
            self.log(f'运行命令出错: {e}')
            return -1
        finally:
            self.proc = None  # 子进程结束后清空

    def run_login(self, interval, testip, path):
        import time
        def timestamp():
            msg = time.asctime(time.localtime(time.time()))
            self.log(msg)
        try:
            self.log("首次尝试登录...")
            self.run_command_with_output(f'"{path}" login')
        except Exception as e:
            self.log(f'Initial call to main1 failed: {e}')
        while not self.stop_flag.is_set():
            time.sleep(interval)
            if not auto_login.is_connect_internet(testip):
                timestamp()
                try:
                    self.log("检测到断网，尝试重新登录...")
                    self.run_command_with_output(f'"{path}" login')
                except Exception as e:
                    self.log(f'Error in always_login loop: {e}')

    def start(self):
        try:
            interval = float(self.interval_entry.get())
            testip = self.ip_entry.get()
            path = self.path_entry.get()
            if not os.path.exists(path):
                messagebox.showerror("错误", f"文件 {path} 不存在")
                return
            self.stop_flag.clear()
            self.proc = None
            self.thread = threading.Thread(target=self.run_login, args=(interval, testip, path), daemon=True)
            self.thread.start()
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.log("自动登录已启动")
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def stop(self):
        self.stop_flag.set()
        # 杀掉子进程（如果存在且还在运行）
        if self.proc and self.proc.poll() is None:
            try:
                self.proc.terminate()
                self.proc.wait(timeout=3)
            except Exception:
                try:
                    self.proc.kill()
                except Exception:
                    pass
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.log("自动登录已停止")

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoLoginGUI(root)
    root.mainloop()