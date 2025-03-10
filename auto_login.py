import os
import time
import subprocess

def is_connect_internet(testip):
    timeout = 5
    status = os.system(u"ping {} -c 8".format(testip))
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

def always_login(checkinterval=1, testip='114.114.114.114', path='./srun-linux'):
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
    path = '/home/fzh/srun_login/srun-linux'
    test_ip = '114.114.114.114'
    always_login(checkinterval=1, testip=test_ip, path=path)