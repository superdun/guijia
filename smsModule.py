#!/usr/bin/env python
#coding: utf-8
import sys,os
import urllib,urllib2
import base64
import hmac
import hashlib
from hashlib import sha1
import time
import uuid
import json
from moduleGlobal import app


access_key_id = app.config.get('SMS_ACCESS_KEY')
access_key_secret = app.config.get('SMS_ACCESS_SECRET')
server_address = 'https://sms.aliyuncs.com'
para = '{"idCode":"%d"}'%12345
num=13061938526
SignName = app.config.get('SMS_SIGN_NAME').encode('utf-8')
TemplateCode = app.config.get('SMS_MODEL_CODE')
#定义参数
user_params = {'Action': 'SingleSendSms', 'ParamString': '%s'%para, 'RecNum': '%d'%num,'SignName': SignName,'TemplateCode': TemplateCode }

def percent_encode(encodeStr):

    encodeStr = str(encodeStr)
    res = urllib.quote(encodeStr.decode('utf8').encode('utf8'), '')
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    return res

def compute_signature(parameters, access_key_secret):
    sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])
    canonicalizedQueryString = ''
    for (k,v) in sortedParameters:
        canonicalizedQueryString += '&' + percent_encode(k) + '=' + percent_encode(v)
    stringToSign = 'GET&%2F&' + percent_encode(canonicalizedQueryString[1:])
    print "stringToSign:  "+stringToSign
    h = hmac.new(access_key_secret + "&", stringToSign, sha1)
    signature = base64.encodestring(h.digest()).strip()
    return signature

def compose_url(user_params):
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time()))
    parameters = {
            'Format'        : 'JSON',
            'Version'       : '2016-09-27',
            'AccessKeyId'   : access_key_id,
            'SignatureVersion'  : '1.0',
            'SignatureMethod'   : 'HMAC-SHA1',
            'SignatureNonce'    : str(uuid.uuid1()),
            'RegionId': 'cn-hangzhou',
            'Timestamp'     : timestamp
    }
    for key in user_params.keys():
        parameters[key] = user_params[key]
    signature = compute_signature(parameters, access_key_secret)
    parameters['Signature'] = signature
    url = server_address + "/?" + urllib.urlencode(parameters)
    return url

def make_request(user_params, quiet=False):
    url = compose_url(user_params)
    request = urllib2.Request(url)
    try:
        conn = urllib2.urlopen(request)
        response = conn.read()
    except urllib2.HTTPError, e:
        print(e.read().strip())
    try:
        obj = json.loads(response)
        if quiet:
            return obj
    except ValueError, e:
        raise SystemExit(e)
    json.dump(obj, sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write('\n')

print sys.stdin.encoding
make_request(user_params)