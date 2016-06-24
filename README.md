# F**k China Telecom Login
今天不得已用服务密码登录了一下电信营业厅  
看见地址栏没有HTTPS隐隐觉得有点不放心  
F12看了一下，果然有问题。  
测试脚本中使用了[winpcapy.py](http://www.winpcap.org/)和[pkcs7.py](https://github.com/janglin/crypto-pkcs7-example/blob/master/pkcs7.py)：  
![screen](/screen.gif?raw=true)
电信使用HTTP登录，并且采用固定的密钥来加密数据  
根本没啥安全性可言。  
不得不与这种猪队友为伍，真是哔了狗了。。。  
2016-06-23  
 ---
还有这个[登录页面](http://ifree.bj.189.cn/)，直接就是明文传密码。  
连加密都懒得做了，给电信跪了。。。  
2016-06-24  
