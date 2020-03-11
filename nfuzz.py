#! /usr/bin/python3
# -*- coding: utf-8 -*

import threading , sys , os , gc , argparse , re
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

# global IS_EXIT
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}



colorama.init(autoreset=True)

class Brute:
    def __init__(self , args):
        self.urls = args.urls
        self.wordlists = args.wordlists
        self.data = args.data
        self.method = args.method
        self.thread_num = args.thread_num
        self.queue = Queue()
        

    def to_do(self):
        f = open(self.wordlists,'r')
        if self.data != None and "FUZZ" in self.data:
            sys.stdout.write('\r'+colorama.Fore.GREEN + '   \tResponse\tChars\t\datas'+'\r'+'\r')
            for i in f.readlines():
                self.queue.put(re.sub(r"FUZZ", i.strip() ,self.data))
            thread_count = int(self.thread_num)
            for i in range(thread_count):
                t = threading.Thread(target= self.fuzz2)
                t.start()
                t.join()
        elif self.urls and self.wordlists and "FUZZ" in self.urls:
            sys.stdout.write('\r'+colorama.Fore.GREEN + '   \tResponse\tChars\t\turls'+'\r'+'\r')
            for i in f.readlines():
                self.queue.put(re.sub(r"FUZZ",i.strip(),self.urls))
            thread_count = int(self.thread_num)
            for i in range(thread_count):
                t = threading.Thread(target=self.fuzz)
                t.start()
                t.join()

    def fuzz(self):
        gc.collect()
        while not self.queue.empty():
            if self.method.strip() == "post":
                urls = self.queue.get()
                resp = requests.post(urls,headers = headers,verify=False)
            elif self.method.strip() == "get":
                urls = self.queue.get()
                resp = requests.get(urls,headers = headers,verify=False)
            try:
                if resp.status_code == 200 :
                    sys.stdout.write('\r'+colorama.Fore.GREEN + '[+]\t200\t\t\t{}\n'.format(urls))
                elif resp.status_code == 403 :
                    sys.stdout.write('\r'+colorama.Fore.CYAN  + '[!]\t403\t\t\t{}\n'.format(urls))
                elif resp.status_code == 302 :
                    sys.stdout.write('\r'+colorama.Fore.BLUE  + '[+]\t302\t\t\t{}\n'.format(urls))
                elif resp.status_code == 301 :
                    sys.stdout.write('\r'+colorama.Fore.BLUE  + '[+]\t301\t\t\t{}\n'.format(urls))
                elif resp.status_code == 405 :
                    sys.stdout.write('\r'+colorama.Fore.CYAN  + '[!]\t405\t\t\t{}\n'.format(urls))
                elif resp.status_code == 400 :
                    sys.stdout.write('\r'+colorama.Fore.CYAN  + '[-]\t400\t\t\t{}\n'.format(urls))
                elif resp.status_code == 500 :
                    sys.stdout.write('\r'+colorama.Fore.RED   + '[-]\t500\t\t\t{}\n'.format(urls))
                elif resp.status_code == 404 :
                    sys.stdout.write('\r'+colorama.Fore.RED   + '[-]\t404\t\t\t{}\n'.format(urls))
            except Exception as e:
                print(e)
                pass
                # sys.exit(1)

    def fuzz2(self):
        gc.collect()
        while not self.queue.empty():
            datas = self.queue.get()
            resp = requests.post(self.urls , headers = headers , data= datas ,verify=False)
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
            except Exception as e:
                print("error")
                self.queue.put(datas)
                threading.Thread(target=self.fuzz2)
                sys.exit(1)

def main():
    print(colorama.Fore.GREEN+ banner)
    if sys.version_info < (3,0):
        sys.stdout.write('nfuzz requires Python 3.x')
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
        resp = requests.get(args.urls,verify = False)
        print(resp.status_code)
        print(resp.headers)
        sys.exit(1)
    elif args.urls and args.wordlists and args.data != None:
        if "FUZZ" in args.data:
            brute = Brute(args)
            brute.to_do()
            sys.exit(1)
        else:
            print(colorama.Fore.RED+"u need FUZZ word =。= ")
            sys.exit(1)
    elif args.urls and args.wordlists:
        if "FUZZ" in args.urls:
            brute = Brute(args)
            brute.to_do()
            sys.exit(1)
        else:
            print(colorama.Fore.RED+"u need FUZZ word =。= ")
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
