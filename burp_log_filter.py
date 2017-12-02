#!/usr/bin/env
# coding=utf-8


import re
import os
import sys
import argparse


reload(sys)
sys.setdefaultencoding('utf-8')

url_param_patterns = []

path_=os.path.abspath(os.path.dirname(__file__))+os.sep

black_list=["bmp", "bz2", "css","doc",
            "eot", "flv","gif", "gz",
            "ico","jpeg", "jpg", "js",
            "less", "mp[34]", "pdf",
            "png", "rar", "rtf","swf",
            "tar", "tgz","txt", "wav",
            "woff","xml", "zip",'JPG']


def get_blocks(filename):
    sep='='*54
    with open(filename) as f:
        content=f.read()
        blocks=re.findall(r'{}.*?{}.*?{}'.format(sep,sep,sep),content,re.S)
    print "The file contains %s blocks ......\n " % len(blocks)
    return blocks


def generate_pattern(method, url, params):
    pattern = []
    pattern.append(method)
    pattern.append(url)
    paramKeys = []
    for item in params.split("&"):
        paramKeys.append(item.split("=")[0])
    paramKeys.sort()
    pattern.extend(paramKeys)
    return pattern


def is_usefull_block(block,host):

    global url_param_patterns
    for line in block.split('\n'):
        if re.match("^GET", line):
            ext=line.split(" ")[1].split("?")[0].split(".")[-1]
            if ext in black_list:
                return False

        if host:
            m = re.match(r"^Host:(.*)", line)
            if m and host not in m.group(1).strip():
                return False

        if re.match("^GET", line) or re.match("^POST", line):
            params = ""
            url = line.split(" ")[1].split("?")[0]
            if "?" in line:
                params = line.split(" ")[1].split("?")[1]
            pattern = generate_pattern(line.split(" ")[0], url, params)
            if pattern in url_param_patterns:
                return False
            else:
                url_param_patterns.append(pattern)

    return True


def run(filename,host):
    setblocks = []
    for block in get_blocks(filename):
        if is_usefull_block(block, host):
            setblocks.append(block)
    with open(path_+'sqli_for_check.txt',"w") as f:
        for block in setblocks:
            f.write("\n" + block + "\n\n\n\n")
    print 'Total found {} useful blocks !'.format(len(setblocks))



def cmdParser():
    parser = argparse.ArgumentParser(usage='python %s [options]'% __file__)
    parser.add_argument('-f','--file',metavar="",help='Burp Suite filename')
    parser.add_argument('-d','--domin',metavar="",help='Domin or ip address')

    if len(sys.argv) == 1:
        sys.argv.append('-h')
    args = parser.parse_args()
    return args



if __name__ == '__main__':
    args=cmdParser()
    if not args.file:
        print sys.exit('You must typing burp logs filename ,"-h" for more message !')
    run(args.file,args.domin)
