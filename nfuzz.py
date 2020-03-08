#! /usr/bin/python3

import threading , sys , os , gc , time , argparse , json , re , itertools
import third.requests as requests
import third.colorama as colorama
from queue import Queue
import platform 
import pdb


banner ='''
          __                 ____  
 _ __    / _|  _   _   ____ |___ \ 
| '_ \  | |_  | | | | |_  /   __) |
| | | | |  _| | |_| |  / /   / __/ 
|_| |_| |_|    \__,_| /___| |_____|
                                   
author : n00B@khan
'''

global IS_EXIT
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}

colorama.init(autoreset=True)

#webscan
class DirScan:
    def __init__(self , args):
        self.urls = args.urls
        self.thread_num = args.thread_num
        self.wordlists = args.wordlists
        self.method = args.method

    def start(self,timeout = None):
        queue = Queue()
        f = open(self.wordlists,'r')
        for i in f.readlines():
            queue.put(self.urls + '/' + i.strip('\n'))
        total = queue.qsize()
        threads = []
        thread_count = int(self.thread_num)
        for i in range(thread_count):
            threads.append(self.request(queue,total))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout)

    class request(threading.Thread):
        def __init__(self, queue , total):
            threading.Thread.__init__(self)
            self._queue = queue
            self._total = total

            
        def run(self):
            gc.collect()
            while not self._queue.empty():
                urls = self._queue.get()
                resp = requests.get(urls , headers = headers)
                try:
                    if resp.status_code == 200 :
                        sys.stdout.write('\r'+colorama.Fore.GREEN + '[+]\t200\t{}\t\t{}\n'.format(resp.headers['content-length'],urls))
                    elif resp.status_code == 403 :
                        sys.stdout.write('\r'+colorama.Fore.CYAN  + '[!]\t403\t{}\t\t{}\n'.format(resp.headers['content-length'],urls))
                    elif resp.status_code == 302 :
                        sys.stdout.write('\r'+colorama.Fore.BLUE  + '[+]\t302\t{}\t\t{}\n'.format(resp.headers['content-length'],urls))
                    elif resp.status_code == 301 :
                        sys.stdout.write('\r'+colorama.Fore.BLUE  + '[+]\t301\t{}\t\t{}\n'.format(resp.headers['content-length'],urls))
                    elif resp.status_code == 405 :
                        sys.stdout.write('\r'+colorama.Fore.CYAN  + '[!]\t405\t{}\t\t{}\n'.format(resp.headers['content-length'],urls))
                    elif resp.status_code == 400 :
                        sys.stdout.write('\r'+colorama.Fore.CYAN  + '[-]\t400\t{}\t\t{}\n'.format(resp.headers['content-length'],urls))
                    elif resp.status_code == 500 :
                        sys.stdout.write('\r'+colorama.Fore.RED   + '[-]\t500\t{}\t\t{}\n'.format(resp.headers['content-length'],urls))
                    elif resp.status_code == 404 :
                        sys.stdout.write('\r'+colorama.Fore.RED   + '[-]\t404\t{}\t\t{}\n'.format(resp.headers['content-length'],urls))
                except EOFError as e:
                    sys.exit(1)

#post form brute
class Brute:
    def __init__(self , args):
        self.urls = args.urls
        self.wordlists = args.wordlists
        self.data = args.data
        self.method = args.method
        self.thread_num = args.thread_num
        self.queue = Queue()
        f = open(self.wordlists,'r')
        for i in f.readlines():
            self.queue.put(re.sub(r"FUZZ",i,args.data))

    def to_do(self):
        if self.method == "Post" and self.data == None:
            thread_count = int(self.thread_num)
            for i in range(thread_count):
                t = threading.Thread(target=self.fuzz)
                t.start()
                t.join()
        if self.data != None:
            thread_count = int(self.thread_num)
            for i in range(thread_count):
                t = threading.Thread(target= self.fuzz)
                t.start()
                t.join()

    def PostWebScan(self):
        gc.collect()
        while not self.queue.empty():
                urls = self.queue.get()
                resp = requests.post(urls , headers = headers)
                try:
                    if resp.status_code == 200 :
                        sys.stdout.write('\r'+colorama.Fore.GREEN + '[+]\t200\t{}\t\t{}\n'.format(resp.headers['content-length'],urls))
                    elif resp.status_code == 403 :
                        sys.stdout.write('\r'+colorama.Fore.CYAN  + '[!]\t403\t{}\t\t{}\n'.format(resp.headers['content-length'],urls))
                    elif resp.status_code == 302 :
                        sys.stdout.write('\r'+colorama.Fore.BLUE  + '[+]\t302\t{}\t\t{}\n'.format(resp.headers['content-length'],urls))
                    elif resp.status_code == 301 :
                        sys.stdout.write('\r'+colorama.Fore.BLUE  + '[+]\t301\t{}\t\t{}\n'.format(resp.headers['content-length'],urls))
                    elif resp.status_code == 405 :
                        sys.stdout.write('\r'+colorama.Fore.CYAN  + '[!]\t405\t{}\t\t{}\n'.format(resp.headers['content-length'],urls))
                    elif resp.status_code == 400 :
                        sys.stdout.write('\r'+colorama.Fore.CYAN  + '[-]\t400\t{}\t\t{}\n'.format(resp.headers['content-length'],urls))
                    elif resp.status_code == 500 :
                        sys.stdout.write('\r'+colorama.Fore.RED   + '[-]\t500\t{}\t\t{}\n'.format(resp.headers['content-length'],urls))
                    elif resp.status_code == 404 :
                        sys.stdout.write('\r'+colorama.Fore.RED   + '[-]\t404\t{}\t\t{}\n'.format(resp.headers['content-length'],urls))
                except EOFError as e:
                    sys.exit(1)

    def fuzz(self):
        gc.collect()
        while not self.queue.empty():
            datas = self.queue.get()
            resp = requests.post(self.urls , headers = headers , data= datas)
            try:
                if resp.status_code == 200 :
                    sys.stdout.write('\r'+colorama.Fore.GREEN + '[+]\t200\t{}\t\t{}\n'.format(resp.headers['content-length'],datas))
                elif resp.status_code == 403 :
                    sys.stdout.write('\r'+colorama.Fore.CYAN  + '[!]\t403\t{}\t\t{}\n'.format(resp.headers['content-length'],datas))
                elif resp.status_code == 302 :
                    sys.stdout.write('\r'+colorama.Fore.BLUE  + '[+]\t302\t{}\t\t{}\n'.format(resp.headers['content-length'],datas))
                elif resp.status_code == 301 :
                    sys.stdout.write('\r'+colorama.Fore.BLUE  + '[+]\t301\t{}\t\t{}\n'.format(resp.headers['content-length'],datas))
                elif resp.status_code == 405 :
                    sys.stdout.write('\r'+colorama.Fore.CYAN  + '[!]\t405\t{}\t\t{}\n'.format(resp.headers['content-length'],datas))
                elif resp.status_code == 400 :
                    sys.stdout.write('\r'+colorama.Fore.CYAN  + '[-]\t400\t{}\t\t{}\n'.format(resp.headers['content-length'],datas))
                elif resp.status_code == 500 :
                    sys.stdout.write('\r'+colorama.Fore.RED   + '[-]\t500\t{}\t\t{}\n'.format(resp.headers['content-length'],datas))
                elif resp.status_code == 404 :
                    sys.stdout.write('\r'+colorama.Fore.RED   + '[-]\t404\t{}\t\t{}\n'.format(resp.headers['content-length'],datas))
            except EOFError as e:
                sys.exit(1)

def main():
    print(colorama.Fore.GREEN+ banner)
    if platform.system == "windows":
        from third.colorama import win32
    parser = argparse.ArgumentParser()
    flag_parser = parser.add_mutually_exclusive_group(required=False)
    flag_parser.add_argument('-I',dest='show',action='store_true',help="CURL -I mode")
    parser.add_argument('-t',dest='thread_num',type=int,help="thread options",default=10)
    parser.add_argument('-u',dest='urls',type=str,help="url options")
    parser.add_argument('-w',dest='wordlists',type=str,help="wordlists options")
    parser.add_argument('-X',dest='method',type=str,help="http-method options",choices=['get','post'],default='get')
    parser.add_argument('-d',dest='data',type=str,help="post data")
    args = parser.parse_args()
    if args.show and args.urls:
        resp = requests.get(args.urls)
        print(resp.status_code)
        print(resp.headers)
        sys.exit(1)
    elif args.urls and args.wordlists and args.data != None:
        if "FUZZ" in args.data:
            brute = Brute(args)
            brute.to_do()
            sys.exit(1)
        else:
            print("u need FUZZ word =。= ")
            sys.exit(1)
    elif args.urls and args.wordlists:
        dirscan = DirScan(args)
        dirscan.start()
        sys.exit(1)
    else:
        txt = '''
        -w Please enter the WORDLIST file address
        -t Please enter the THREAD number
        -u Please enter the URL number
        -I CURL -I mode
        -d Post data FUZZ need "FUZZ" word in data , data usage:"username=admin&password=FUZZ"
        -X http-method support Post and Get (default)
        '''
        print(txt)
        sys.exit(1)

if __name__ == '__main__':
    main()
