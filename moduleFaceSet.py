# -*- coding:utf-8 -*-
from gevent import monkey; monkey.patch_socket()
import gevent
import requests
from dbORM import Findingchildren,Childrenface,Missingchildren,db
from moduleGlobal import app
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
class FaceSet(object):
    def __init__(self, apiSecret, apiKey):
        self.addFaceUrl = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/addface'
        self.createSetUrl = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/create'
        self.getSetUrl = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/getfacesets'
        self.deleteSetsUrl = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/removeface'
        self.getFaceToken = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
        self.getDetailUrl = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/getdetail'
        self.searchUrl = 'https://api-cn.faceplusplus.com/facepp/v3/search'
        self.apiSecret = apiSecret
        self.apiKey = apiKey

    def createSet(self, name, tags, tokens):
        payload = {'api_key': self.apiKey, 'api_secret': self.apiSecret, 'display_name': tags + '_'+ str(name),
                   'outer_id': tags + '_'+str(name), 'tags': tags, 'face_tokens': tokens}
        r = requests.post(url=self.createSetUrl, data=payload,verify=False)
        return r.json()
    def getDetail(self,id):
        payload = {'api_key': self.apiKey, 'api_secret': self.apiSecret, 'outer_id':id}
        r = requests.post(url=self.getDetailUrl,data=payload)
        return r.json()
    def getSets(self, tag=''):
        payload = {'api_key': self.apiKey, 'api_secret': self.apiSecret, 'tags': tag}
        r = requests.post(url=self.getSetUrl, data=payload,verify=False)
        return r.json()

    def uploadFaces(self, urls, tag):

        sets = self.getSets(tag)['facesets']
        names = []
        for i in sets:
            names.append(int(i['outer_id'].split('_')[-1]))
        if names:

            lastName = max(names)
        else:
            lastName = '0'
            self.createSet('0',tag,'')
        failed = []
        result=[]
        total = len(urls)
        successCount = 0
        for i in range(total):
            payloadForToken = {'api_key': self.apiKey, 'api_secret': self.apiSecret, 'image_url': urls[i],
                               'return_landmark': 1, 'return_attributes': 'gender,age'}
            rForToken = requests.post(url=self.getFaceToken, data=payloadForToken,verify=False)
            tokenResult = rForToken.json()
            if not tokenResult.has_key('error_message'):
                if not tokenResult['faces']:
                    result.append('')
                    failed.append([urls[i], 'NOFACE'])
                else:
                    token = tokenResult['faces'][0]['face_token']
                    payloadForAdd = {'api_key': self.apiKey, 'api_secret': self.apiSecret,
                                     'outer_id': tag + '_' + str(lastName),
                                     'face_tokens': token}
                    rForAdd = requests.post(url=self.addFaceUrl, data=payloadForAdd,verify=False)
                    addResult = rForAdd.json()
                    if not addResult.has_key('error_message'):
                        if addResult['failure_detail'] and addResult['failure_detail'][0]['reason'] == 'QUOTA_EXCEEDED':
                            lastName += 1
                            createResult = self.createSet(lastName, tag, token)
                            print createResult
                            if createResult['failure_detail']:
                                result.append('')
                                failed.append(addResult['failure_detail'])
                            else:
                                result.append(token)
                                successCount += 1
                        elif addResult['failure_detail']:
                            result.append('')
                            failed.append(addResult['failure_detail'])
                        else:
                            result.append(token)
                            successCount += 1
                    else:
                        result.append('')
                        failed.append([urls[i], addResult['error_message']])

            else:
                result.append('')
                failed.append([urls[i], tokenResult['error_message']])
        return result

    def deleteSet(self, id):
        payload = {'api_key': self.apiKey, 'api_secret': self.apiSecret, 'outer_id': id,
                   'face_tokens': 'RemoveAllFaceTokens'}
        r = requests.post(url=self.deleteSetsUrl, data=payload,verify=False)
        return r.json()
    def search(self,image,tag):
        sets = self.getSets(tag)
        for i in sets['facesets']:
            payload = {'api_key': self.apiKey, 'api_secret': self.apiSecret, 'image_url': image,
                       'outer_id': i['outer_id']}
            r = requests.post(url=self.searchUrl, data=payload)
            searchResult = r.json()
            if searchResult.has_key('error_message'):
                return {'error': searchResult['error_message']}
            if searchResult.has_key('result'):
                if searchResult['result']:
                    faceToken = searchResult['result'][0]['face_token']
                    confidence = searchResult['result'][0]['confidence']
                    thresholds = searchResult['thresholds']
                    if confidence<=thresholds['1e-3']:
                        return {'status':0,'confidence':confidence,'thresholds':thresholds,'token':faceToken}
                    elif  confidence>=thresholds['1e-3'] and confidence<=thresholds['1e-4'] :
                        return {'status':1,'confidence':confidence,'thresholds':thresholds,'token':faceToken}
                    elif confidence>=thresholds['1e-4'] and confidence<=thresholds['1e-5'] :
                        return {'status':2,'confidence':confidence,'thresholds':thresholds,'token':faceToken}
                    elif confidence>=thresholds['1e-5']:
                        return {'status':3,'confidence':confidence,'thresholds':thresholds,'token':faceToken}
                else:
                    return {'error':'noface'}
            else:
                return {'error': 'noface'}

def t(children,face):

    for i in children:
        print gevent.getcurrent(), i
        if not Childrenface.query.filter_by(childrenId=i.id).first():
            url = app.config.get('BAOBEIHUIJIA_IMG_DOMAIN') + i.image
            result = face.uploadFaces([url], 'missingchildren')
            print result
            cf = Childrenface(childrenId=i.id, token=result[0])
            db.session.add(cf)
            db.session.commit()
        else:
            print 'pass'

def main():
    children=Missingchildren.query.all()
    total = len(children)
    tCount = 1
    per_page= int(total/tCount)
    secret = app.config.get('FACE_SECRET')
    apiKey = app.config.get('FACE_API_KEY')
    face = FaceSet(secret, apiKey)
    # print face.getSets('')
    # print face.getDetail('missingchildren_4')
    g = []
    for  i in range(tCount):
        print per_page

        offset=i*per_page
        print offset
        c = Missingchildren.query.offset(offset).limit(per_page).all()
        g.append(gevent.spawn(t, c,face))
    print len(g)
    gevent.joinall(g)

main()





