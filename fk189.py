#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import base64
import hashlib
from Crypto.Cipher import AES
from pkcs7 import PKCS7Encoder

# key和iv的明文在中国电信登录页的JS代码里
KEY = hashlib.md5('login.189.cn').hexdigest()
IV  = '1234567812345678'

def PasswordEncrypt(pwd):
    return base64.b64encode( AES.new(KEY, AES.MODE_CBC, IV).encrypt( PKCS7Encoder().encode(pwd) ) )

def PasswordDecrypt(pwd):
    return PKCS7Encoder().decode( AES.new(KEY, AES.MODE_CBC, IV).decrypt( base64.b64decode(pwd) ) )

if __name__ == '__main__':
    e = PasswordEncrypt('123456')
    print e
    d = PasswordDecrypt(e)
    print d
