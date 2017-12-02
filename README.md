#### 1、pyscript
##### 适用场景
  脚本主要用于过滤BurpSuite日志。我们做HTTP测试利用BurpSuite的日志记录了所有请求，BURP免费版是不支持logging的，user options --->misc--->logging：
##### 主要功能
- 按照自定义域名过滤请求
- 过滤静态资源请求，如果有遗漏可以手动添加black_list
- 过滤URL，即相同URL和参数的请求，只会留其一

##### 脚本缺陷

- 下面两个GET请求无法去重 <br>
  - http://www.xx.com/index.php?id=1&tpye=3 <br>
  - http://www.xx.com/index.php?id=1 <br>

- 下面两个POST请求会遗漏其中一个 <br>

    - http://www.xx.com/index.php <br>
      id=1&tpye=3
    - http://www.xx.com/index.php <br>
      style=1&keyword=3
 
 ##### 基本用法
 
  python burp_log_filter.py -f /tmp/burp.log -d='www.xxx.com'
  
  sqlmap -l sqli_for_check.txt --batch -smart
  
 MAC查看结果 <br>
/usr/local/Cellar/sqlmap/1.1.11/libexec/output/
