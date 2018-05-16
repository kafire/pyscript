#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re
import sys
import json
import requests
import threading
import argparse
from Queue import Queue
from bs4 import BeautifulSoup

RESULT={}

share_queue=Queue()


reload(sys)
sys.setdefaultencoding( "utf-8" )

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:52.0) Gecko/20100101',
          "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
          "Connection": "close",
          "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
          }

proxies = {'https':'socks5://127.0.0.1:1080'}



class MyThread(threading.Thread):
    def __init__(self, func):
        super(MyThread, self).__init__()
        self.func = func
    def run(self):
        self.func()



def bing():
    info={}
    html=''
    while share_queue.qsize() > 0:
        ip=share_queue.get()
        query="https://www.bing.com/search?q=ip:" + ip
        try:
            html = requests.get(url=query,headers=header,timeout=5).content
        except BaseException as e:
            pass
        if html:
            soup = BeautifulSoup(html, 'lxml')
            rows = soup.findChildren('li', attrs={'class': 'b_algo'})
            for row in rows:
                url = row.find_all('a')[0].get('href')
                title = row.findChildren('a')[0].string
                # domain = url.split('://')[-1].split('/')[0]
                info.update({title:url})
            if info:
                RESULT.update({ip:info})
                print json.dumps({ip:info},ensure_ascii=False,indent=2)



def get_ips(_file=None,ip=None):
    ips = []
    regx_ip=re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if ip:
        if regx_ip.match(ip):
            ips.append(ip)
        else:
            print 'IP address error !'
    if _file:
        with open(_file) as f:
            result = re.findall(r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b",f.read())
            for i in result:
                ips.append(i)
    return set(ips)




def search(_file=None,ip=None,ts=10):
    for ip in get_ips(_file,ip):
        share_queue.put(ip)
    print "Total have {} tasks , now starting.....".format(share_queue.qsize())
    threads = []
    for i in xrange(ts):
        thread = MyThread(bing)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    with open('result.txt',"wb") as f:
        f.write(json.dumps(RESULT,ensure_ascii=False,indent=2))


def cmdParser():
    parser = argparse.ArgumentParser(usage='python %s -i 218.28.223.5'%__file__)
    parser.add_argument('-f','--file',metavar="",help='ips filename')
    parser.add_argument('-i','--ip',metavar="",help='singe host')
    parser.add_argument('-t','--threads',metavar="",default=10,type=int,help='Threads numbers,default 10')

    if len(sys.argv) == 1:
        sys.argv.append('-h')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args=cmdParser()
    if not (args.file or args.ip):
        print sys.exit('-h for help')
    else:
        search(args.file,args.ip,args.threads)

