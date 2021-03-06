#!/usr/bin/env python
# -*- coding: utf-8 -*-
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest
from aliyunsdkcore.client import AcsClient
import uuid
from moduleGlobal import app

class sendSMS(object):
    def __init__(self,type, number, msg):

        self.TemplateCode = app.config.get('SMS_MODEL_ID_CODE')
        self.para = msg
        if type=='noti_v':
            self.TemplateCode = app.config.get('SMS_MODEL_NOTI_CODE_V')
        if type=='noti_a':
            self.TemplateCode = app.config.get('SMS_MODEL_NOTI_CODE_A')


        self.access_key_id = app.config.get('SMS_ACCESS_KEY')
        self.access_key_secret = app.config.get('SMS_ACCESS_SECRET')
        self.server_address = app.config.get('SMS_URL')
        self.region = "cn-hangzhou"  # 暂时不支持多region
        self.num = int(number)
        self.SignName = app.config.get('SMS_SIGN_NAME').encode('utf-8')
        self.acs_client = AcsClient(self.access_key_id, self.access_key_secret, self.region)
        self.uuid = uuid.uuid1()
    def send(self):
        smsRequest = SendSmsRequest.SendSmsRequest()
        smsRequest.set_TemplateCode(self.TemplateCode)
        if self.para is not None:
            smsRequest.set_TemplateParam(self.para)
        smsRequest.set_OutId(self.uuid)
        smsRequest.set_SignName( self.SignName)
        smsRequest.set_PhoneNumbers(self.num )
        smsResponse = self.acs_client.do_action_with_exception(smsRequest)
        return smsResponse
        # # 定义参数
        # user_params = {'Action': 'SingleSendSms', 'ParamString': '%s' % self.para, 'RecNum': '%d' % self.num,
        #                'SignName': self.SignName,
        #                'TemplateCode': self.TemplateCode}
        # self.make_request(user_params)

    # def percent_encode(self,encodeStr):
    #     encodeStr = str(encodeStr)
    #
    #     res = urllib.quote(encodeStr.decode('utf-8').encode('utf-8'), '')
    #     res = res.replace('+', '%20')
    #     res = res.replace('*', '%2A')
    #     res = res.replace('%7E', '~')
    #     return res
    #
    # def compute_signature(self,parameters, access_key_secret):
    #     sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])
    #     canonicalizedQueryString = ''
    #     for (k, v) in sortedParameters:
    #         canonicalizedQueryString += '&' + self.percent_encode(k) + '=' + self.percent_encode(v)
    #     stringToSign = 'GET&%2F&' + self.percent_encode(canonicalizedQueryString[1:])
    #     print "stringToSign:  " + stringToSign
    #     h = hmac.new(access_key_secret + "&", stringToSign, sha1)
    #     signature = base64.encodestring(h.digest()).strip()
    #     return signature
    #
    # def compose_url(self,user_params):
    #     timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time()))
    #     parameters = {
    #         'Format': 'JSON',
    #         'Version': '2016-09-27',
    #         'AccessKeyId': self.access_key_id,
    #         'SignatureVersion': '1.0',
    #         'SignatureMethod': 'HMAC-SHA1',
    #         'SignatureNonce': str(uuid.uuid1()),
    #         'RegionId': 'cn-hangzhou',
    #         'Timestamp': timestamp
    #     }
    #     for key in user_params.keys():
    #         parameters[key] = user_params[key]
    #     signature = self.compute_signature(parameters, self.access_key_secret)
    #     parameters['Signature'] = signature
    #     print parameters
    #     url = self.server_address + "/?" + urllib.urlencode(parameters)
    #     return url
    #
    # def make_request(self,user_params, quiet=False):
    #     url = self.compose_url(user_params)
    #     request = urllib2.Request(url)
    #     try:
    #         conn = urllib2.urlopen(request)
    #         response = conn.read()
    #     except urllib2.HTTPError, e:
    #         print(e.read().strip())
    #     try:
    #         obj = json.loads(response)
    #         if quiet:
    #             return obj
    #     except ValueError, e:
    #         raise SystemExit(e)
    #     json.dump(obj, sys.stdout, sort_keys=True, indent=2)
    #     sys.stdout.write('\n')
