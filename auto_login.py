import os
import time
import subprocess

def is_connect_internet(testip):
    timeout = 5
    # Windows 下用 -n，Linux 下用 -c
    param = '-n' if os.name == 'nt' else '-c'
    status = os.system(f"ping {param} 8 {testip}")
    # 使用 subprocess.call 来执行 ping 命令，不显示输出
    # with open(os.devnull, 'w') as DEVNULL:
    #     status = subprocess.call(
    #         f"ping {param} 8 {testip}",
    #         shell=True,
    #         stdout=DEVNULL,
    #         stderr=DEVNULL
    #     )
    return status == 0

def main1(path):
    if os.path.exists(path):
        try:
            ret = subprocess.call(path + ' login', shell=True)
            print('main1 return {}'.format(ret))
        except Exception as e:
            print(f'Error in main1: {e}')
            pass
    else:
        print(f'Path {path} does not exist')

def always_login(checkinterval=1, testip='baidu.com', path='srun.exe'):
    timestamp = lambda: print(time.asctime(time.localtime(time.time())))
    timestamp()

    try:
        main1(path)
    except Exception as e:
        print(f'Initial call to main1 failed: {e}')
        pass

    while 1:
        time.sleep(checkinterval)
        if not is_connect_internet(testip):
            timestamp()
            try:
                main1(path)
            except Exception as e:
                print(f'Error in always_login loop: {e}')
                pass

if __name__ == "__main__":
    path = 'srun.exe'
    if not os.path.exists(path):
        print(f'Executable path {path} does not exist. Please check the path.')
        exit(1)
    test_ip = 'baidu.com'  # You can change this to any reliable IP
    always_login(checkinterval=1, testip=test_ip, path=path)