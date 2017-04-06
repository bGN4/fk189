# F**k China Telecom Login

中国电信使用HTTP登录，并且采用固定的密钥加密，导致可使用本脚本嗅探登陆信息  
还有这个[登录页面](http://ifree.bj.189.cn/)，未加密的密码明文传输  

### 依赖  
* [winpcapy.py](http://www.winpcap.org/)  
* [pkcs7.py](https://github.com/janglin/crypto-pkcs7-example/blob/master/pkcs7.py)  

### 执行  
* 运行 basic_dump_ex.py  
* 选择 Adapter  
* 探测到的手机号/密码会显示出来  

![screen](/screen.gif?raw=true)

                                                                      2016-06-24  
