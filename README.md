# nfuzz
本脚本程序仅为学习交流分享，请遵守《中华人民共和国网络安全法》,勿用于非授权测试,如作他用所承受的法律责任一概与作者无关。  
***
  
author : n00B@khan  
nfuzz.py 是个具备 / web目录扫描器 / web post form 爆破 / curl -I / 功能的脚本    
****

## 2020-3-11更新，修复报错，目录扫描模块修改（现 在 目 录 扫 描 也 需 要 "FUZZ" 占位符）
****
windows 下也具备颜色输出 ，本工具依赖与 python3  

缺点：windows 下没有ctrl-c 终止程序

用法：
```
web目录扫描:
python3 nfuzz.py -w /usr/share/wordlists/wfuzz/general/common.txt -u http://192.168.1.1/FUZZ -t 5
其他例子：
usage:"http://192.168.1.1/FUZZ" or "http://192.168.1.1/FUZZ/n00b.py" or "http://FUZZ/n00b"


post爆破（ FUZZ 占 位 符 和 -d 是 必 须 的 ，传 递 的 参 数 格 式 也 要 合 规 ）:
python3 nfuzz.py -w password.txt -u xxxxxxxx.com -d "username=admin&password=FUZZ"
usage:"username=admin&password=FUZZ"

curl -I（个人用的比较多，所以添上了）:
python3 nfuzz.py -u xxxxxxxxxxxxx.com -I
```

```
python3 nfuzz.py -h
          __                 ____  
 _ __    / _|  _   _   ____ |___ \ 
| '_ \  | |_  | | | | |_  /   __) |
| | | | |  _| | |_| |  / /   / __/ 
|_| |_| |_|    \__,_| /___| |_____|
                                   
author : n00B@khan

usage: nfuzz.py [-h] [-I] [-t THREAD_NUM] [-u URLS] [-w WORDLISTS]
                [-X {get,post}] [-d DATA] 

optional arguments:
        -w Please enter the WORDLIST file address
        -t Please enter the THREAD number
        -u Please enter the URL , need "FUZZ"
        -I CURL -I mode
        -d Post data , need "FUZZ"
        -X http-method support Post and Get (default)                   
```
