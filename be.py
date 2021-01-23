
import requests, json, time, threading, urllib3
from queue import Queue
from colorama import Fore, init
urllib3.disable_warnings()

init()

class viewTub():
    def __init__(self,token):
        super(viewTub, self).__init__()
        self.headers = {
            'Authorization': 'Bearer {}'.format(token),
            'User-Agent': 'okhttp/3.12.1'
        }
    
    def getJobs(self, type_video):
        self.type_video = type_video
        payload = {
            'type_video': type_video,
            # 'subscribe': '1'
        }
        r = requests.post("https://viewtub.amai-team.com/api/v1/farmer/video", data=payload, headers=self.headers, verify=0)
        return r.json()
    
    def start(self, id):
        payload = {
            'video_id': str(id),
            'type_video': self.type_video
        }
        r = requests.post("https://viewtub.amai-team.com/api/v1/farmer/video/start", data=payload, headers=self.headers, verify=0)
        return r.json()['message']

    def end(self,id, token):
        payload = {
            'video_id': str(id),
            'type_video': self.type_video
        }
        r = requests.post("https://viewtub.amai-team.com/api/v1/farmer/video/end", data=payload, headers=self.headers, verify=0)
        requests.put("http://nxhdev.pro/api/viewTub/index.php", data={'token': token, 'type': 0})
        return r.json()['message']



def workSub(token):
    name = Fore.RED + getInfo(token) + Fore.WHITE
    url = 'https://viewtub.amai-team.com/api/v1/farmer/video'
    hd = {'authorization': 'Bearer ' + token}
    r = requests.post(url, data={'type_video': '1', 'subscribe': '1'}, headers=hd, verify=0)
    rs = r.json()
    print(f"{name}: {rs['message']}")
    if (len(rs['data']) > 0):
        r = requests.post("https://viewtub.amai-team.com/api/v1/farmer/video/start", data={'video_id': r.json()['data']['id'], 'type_video': '1'}, headers=hd, verify=0)
        print(f"{name}: {r.json()['message']}")
        time.sleep(rs['data']['time'])
        r = requests.post("https://viewtub.amai-team.com/api/v1/farmer/video/end", data={'video_id':rs['data']['id'], 'type_video': '1'}, headers=hd, verify=0)
        requests.put("http://nxhdev.pro/api/viewTub/index.php", data={'token': token, 'type': 0})
        print(f"{name}: {r.json()['message']}")


def work(token):
    fail = 0
    name = Fore.RED + getInfo(token) + Fore.WHITE
    while 1:
        if (fail >= 10):
            print (f"{name}: Fail >= 10")
            requests.put("http://nxhdev.pro/api/viewTub/index.php", data={'token': token, 'type': 1})
            break
        for i in range(3):
            while 1:
                w = viewTub(token)
                job = w.getJobs(str(i+1))
                print(f"{name}: {job['message']}")
                try:
                    print(f"{name}: {w.start(job['data']['id'])}")
                    time.sleep(job['data']['time'])
                    print(f"{name}: {w.end(job['data']['id'], token)}")
                except:
                    fail += 1
                    break
                time.sleep(15)

def getInfo(token):
    r = requests.get("https://viewtub.amai-team.com/api/v1/auth/me?", headers={'authorization': 'Bearer ' + token}, verify=0)
    return r.json()['data']['name']


def worker():
    while True:
        print("[{}]  => Đang get job\n".format(threading.current_thread().name))
        item = q.get()
        if (item is None):
            print("[{}]  => Hết job".format(threading.current_thread().name))
            q.task_done()
            break
        print("[{}]  => Success -> Working\n".format(threading.current_thread().name))
        work(item)
        q.task_done()

if __name__ == '__main__':
    get_tk = requests.get("http://nxhdev.pro/api/viewTub/index.php?user=" + input("user hana: ")).json()
    thread_num = int(input("Số Thread: "))

    q = Queue()

    for i in range(thread_num):
        threading.Thread(target=worker).start()

    for i in get_tk:
        q.put(i)

    for i in range(thread_num):
        q.put(None)
