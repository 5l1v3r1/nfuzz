#! /usr/bin/python3
# -*- coding: utf-8 -*

import threading , sys , os , gc , argparse , re
import third.requests as requests
import third.colorama as colorama
from queue import Queue
import platform 
# import pdb


banner ='''
          __                 ____  
 _ __    / _|  _   _   ____ |___ \ 
| '_ \  | |_  | | | | |_  /   __) |
| | | | |  _| | |_| |  / /   / __/ 
|_| |_| |_|    \__,_| /___| |_____|
                                   
author : n00B@khan
'''

IS_EXIT = False
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
        self.filter = args.filter
        

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
        global IS_EXIT
        gc.collect()
        while not self.queue.empty() and IS_EXIT == False:
            if self.method.strip() == "post":
                urls = self.queue.get()
                resp = requests.post(urls,headers = headers,verify=False)
            elif self.method.strip() == "get":
                urls = self.queue.get()
                resp = requests.get(urls,headers = headers,verify=False)
            try:
                if resp.status_code == 200 :
                    if self.filter == None or 200 not in self.filter :
                        sys.stdout.write('\r'+colorama.Fore.GREEN + '[+]\t200\t\t\t{}\n'.format(urls))
                elif resp.status_code == 403:
                    if self.filter == None or 403 not in self.filter:
                        sys.stdout.write('\r'+colorama.Fore.CYAN  + '[!]\t403\t\t\t{}\n'.format(urls))
                elif resp.status_code == 302:
                    if self.filter == None or 302 not in self.filter:
                        sys.stdout.write('\r'+colorama.Fore.BLUE  + '[+]\t302\t\t\t{}\n'.format(urls))
                elif resp.status_code == 301:
                    if self.filter == None or 301 not in self.filter:
                        sys.stdout.write('\r'+colorama.Fore.BLUE  + '[+]\t301\t\t\t{}\n'.format(urls))
                elif resp.status_code == 405:
                    if self.filter == None or 405 not in self.filter :
                        sys.stdout.write('\r'+colorama.Fore.CYAN  + '[!]\t405\t\t\t{}\n'.format(urls))
                elif resp.status_code == 400:
                    if self.filter == None or 400 not in self.filter :
                        sys.stdout.write('\r'+colorama.Fore.CYAN  + '[-]\t400\t\t\t{}\n'.format(urls))
                elif resp.status_code == 500:
                    if self.filter == None or 500 not in self.filter :
                        sys.stdout.write('\r'+colorama.Fore.RED   + '[-]\t500\t\t\t{}\n'.format(urls))
                elif resp.status_code == 404:
                    if self.filter == None or 404 not in self.filter :
                        sys.stdout.write('\r'+colorama.Fore.RED   + '[-]\t404\t\t\t{}\n'.format(urls))
                    else:
                        pass
            except Exception as e:
                print("error")
                sys.exit(1)

    def fuzz2(self):
        gc.collect()
        while not self.queue.empty():
            datas = self.queue.get()
            resp = requests.post(self.urls , headers = headers , data= datas ,verify=False)
            try:
                if resp.status_code == 200:
                    if self.filter == None or 200 not in self.filter :
                        sys.stdout.write('\r'+colorama.Fore.GREEN + '[+]\t200\t{}\t\t{}\n'.format(resp.headers['content-length'],datas))
                elif resp.status_code == 403:
                    if self.filter == None or 403 not in self.filter :
                        sys.stdout.write('\r'+colorama.Fore.CYAN  + '[!]\t403\t{}\t\t{}\n'.format(resp.headers['content-length'],datas))
                elif resp.status_code == 302:
                    if self.filter == None or 302 not in self.filter :
                        sys.stdout.write('\r'+colorama.Fore.BLUE  + '[+]\t302\t{}\t\t{}\n'.format(resp.headers['content-length'],datas))
                elif resp.status_code == 301:
                    if self.filter == None or 301 not in self.filter :
                        sys.stdout.write('\r'+colorama.Fore.BLUE  + '[+]\t301\t{}\t\t{}\n'.format(resp.headers['content-length'],datas))
                elif resp.status_code == 405:
                    if self.filter == None or 405 not in self.filter :
                        sys.stdout.write('\r'+colorama.Fore.CYAN  + '[!]\t405\t{}\t\t{}\n'.format(resp.headers['content-length'],datas))
                elif resp.status_code == 400:
                    if self.filter == None or 400 not in self.filter :
                        sys.stdout.write('\r'+colorama.Fore.CYAN  + '[-]\t400\t{}\t\t{}\n'.format(resp.headers['content-length'],datas))
                elif resp.status_code == 500:
                    if self.filter == None or 500 not in self.filter :
                        sys.stdout.write('\r'+colorama.Fore.RED   + '[-]\t500\t{}\t\t{}\n'.format(resp.headers['content-length'],datas))
                elif resp.status_code == 404:
                    if self.filter == None or 404 not in self.filter :
                        sys.stdout.write('\r'+colorama.Fore.RED   + '[-]\t500\t{}\t\t{}\n'.format(resp.headers['content-length'],datas))
            except Exception as e:
                print("error")
                sys.exit(1)

def main():
    print(colorama.Fore.GREEN+ banner)
    if sys.version_info < (3,0):
        sys.stdout.write('nfuzz requires Python 3.x')
    if platform.system == "windows":
        from third.colorama import win32
    parser = argparse.ArgumentParser()
    flag_parser = parser.add_mutually_exclusive_group(required=False)
    flag_parser.add_argument('-I',dest='CURL_I',action='store_true',help="CURL -I mode")
    flag_parser.add_argument('-C',dest='CURL',action='store_true',help="CURL mode")
    parser.add_argument('-t',dest='thread_num',type=int,help="thread options",default=10)
    parser.add_argument('-u',dest='urls',type=str,help="url options")
    parser.add_argument('-w',dest='wordlists',type=str,help="wordlists options")
    parser.add_argument('-X',dest='method',type=str,help="http-method options",choices=['get','post'],default='get')
    parser.add_argument('-d',dest='data',type=str,help="post data")
    parser.add_argument('--hc',dest='filter',type=int,help="http status code filter",nargs='*')
    args = parser.parse_args()
    if args.CURL_I and args.urls:
        if args.method.strip() == "get":
            resp = requests.get(args.urls,verify = False)
            print(resp.status_code)
            print(resp.headers)
            sys.exit(1)
        elif args.method.strip() == "post":
            resp = requests.post(args.urls , verify = False)
            print(resp.status_code)
            print(resp.headers)
            sys.exit(1)
    elif args.CURL and args.urls:
        if args.method.strip() == "get":
            resp = requests.get(args.urls , verify = False)
            print(resp.text)
            sys.exit(1)
        elif args.method.strip() == "post":
            resp = requests.post(args.urls , verify = False)
            print(resp.text)
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
        -u Please enter the URL number , usage:"http://www.baidu.com/FUZZ/error.html"
        -I CURL -I mode
        -C CURL mode
        -d Post data  , usage:"username=admin&password=FUZZ"
        -X http-method support Post and Get (default)
        '''
        print(txt)
        sys.exit(1)

if __name__ == '__main__':
    main()
