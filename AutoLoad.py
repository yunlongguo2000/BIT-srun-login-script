# Create date: 2021.08.31
# Author: Sunhr
# Keep BIT-Web online

import os
import time
import random
import getpass
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import FirefoxOptions, ChromeOptions

# 在程序启动时保存当前进程的 PID
def write_pid_file():
    pid_file_path = "F:\\BIT-srun-login-script\\autoload.pid"
    with open(pid_file_path, "w") as f:
        f.write(str(os.getpid()))
        print("PID number is:", os.getpid())
        print("PID file created at", pid_file_path)

def loopLoad(usrname, passwd, browserChoice='firefox'):
    while True:
        if browserChoice == 'firefox':
            opts = FirefoxOptions()
            opts.add_argument("--headless")
            browser = webdriver.Firefox(options=opts)
        elif browserChoice == 'chrome':
            opts = ChromeOptions()
            opts.add_argument("--headless")
            browser = webdriver.Chrome(options=opts)
        time.sleep(1)
        
        el = lambda id: browser.find_element(By.ID, id)
        try:
            browser.get('http://10.0.0.55/')
            time.sleep(1)
            try:
                if el("logout"):
                    print("Bit-Web still OK!")
                    browser.close()
                    time.sleep(random.randint(3,7))
                    continue
            except:
                el("username").clear()
                el("password").clear()
                el("username").send_keys(usrname)
                el("password").send_keys(passwd)
                el("login").click()
                time.sleep(2)
                print("Bit-Web OK!")
            
        except Exception as e:
            browser.close()
            print("Bit-Web Failed! Error:", e)
            continue

if __name__ == '__main__':
    write_pid_file()
    browerDict = {'1':'firefox','2':'chrome'}
    browerIdx = input('Please choose your brower number ( 1 for Firefox; 2 for Chrome ):')
    usrname = input("Please input username: ")
    passwd = getpass.getpass("Please input passwd: ") 
    
    
    # 在顶层使用无限循环捕获所有异常，避免脚本异常退出
    while True:
        try:
            loopLoad(usrname, passwd, browerDict[browerIdx])
        except Exception as err:
            print("Unhandled exception:", err)
            time.sleep(10)