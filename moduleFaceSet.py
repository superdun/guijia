# -*- coding:utf-8 -*-
from gevent import monkey; monkey.patch_socket()
import gevent
import requests
from dbORM import Findingchildren,Childrenface,Missingchildren,db
from moduleGlobal import app
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
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
            print searchResult
            if searchResult.has_key('error_message'):
                return {'error': searchResult['error_message'],'detail':json.dumps(searchResult)}
            if searchResult.has_key('results'):
                if searchResult['results']:
                    faceToken = searchResult['results'][0]['face_token']
                    confidence = searchResult['results'][0]['confidence']
                    thresholds = searchResult['thresholds']
                    if confidence<=thresholds['1e-3']:
                        return {'status':0,'confidence':confidence,'thresholds':thresholds,'token':faceToken,'detail':json.dumps(searchResult)}
                    elif  confidence>=thresholds['1e-3'] and confidence<=thresholds['1e-4'] :
                        return {'status':1,'confidence':confidence,'thresholds':thresholds,'token':faceToken,'detail':json.dumps(searchResult)}
                    elif confidence>=thresholds['1e-4'] and confidence<=thresholds['1e-5'] :
                        return {'status':2,'confidence':confidence,'thresholds':thresholds,'token':faceToken,'detail':json.dumps(searchResult)}
                    elif confidence>=thresholds['1e-5']:
                        return {'status':3,'confidence':confidence,'thresholds':thresholds,'token':faceToken,'detail':json.dumps(searchResult)}
                else:
                    return {'error':'noface','detail':json.dumps(searchResult)}
            else:
                return {'error': 'noface','detail':json.dumps(searchResult)}

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
def searchResultHandleForWechat(searchResult):
    title=description=url=''
    status='ok'
    if searchResult.has_key('error'):
        if searchResult['error'] == 'noface':
            title = u'对不起'
            description = u'请上传更清晰的图片'
            url = app.config.get('HOST')
            status='bad'
        else:
            title = u'对不起服务器正忙'
            description = u'请上传更清晰的图片'
            status = 'bad'
            url = app.config.get('HOST')
    elif searchResult['status'] == 0:
        title = u'对不起,没有匹配到合适的图片'
        description = u'感谢您的爱心，请在5分钟内回复此图片的拍摄地点，我们将把信息上传至数据库，如之后有匹配成功会及时通知您'
        url = app.config.get('HOST')
    elif searchResult['status'] == 1:
        title = u'找到一张相似度%d的照片' % searchResult['confidence']
        description = u'我们会立刻处理此信息，请在5分钟内回复此图片的[拍摄地点,您的联系方式]，我们将推送给您给您详细匹配信息'
    elif searchResult['status'] == 2:
        title = u'找到一张相似度%d的照片，相似度比较高' % searchResult['confidence']
        description = u'我们会立刻处理此信息，请立刻回复此图片的[拍摄地点,您的联系方式]，我们将推送给您给您详细匹配信息'
    elif searchResult['status'] == 3:
        title = u'找到一张相似度%d的照片！！！，相似度非常高' % searchResult['confidence']
        description = u'这种情况十分紧急，我们会立刻处理此信息，请立刻回复此图片的[拍摄地点,您的联系方式]，我们将推送给您给您详细匹配信息，或直接与13061938526联系'
    return {'status':status,'title':title,'description':description,'url':url}
def searchResultHandleForWeb(searchResult):
    title=description=url=''
    status='ok'
    if searchResult.has_key('error'):
        if searchResult['error'] == 'noface':
            title = u'对不起'
            description = u'请上传更清晰的图片'
            url = app.config.get('HOST')
            status='bad'
        else:
            title = u'对不起服务器正忙'
            description = u'请上传更清晰的图片'
            status = 'bad'
            url = app.config.get('HOST')
    elif searchResult['status'] == 0:
        title = u'对不起,没有匹配到合适的图片'
        description = u'感谢您的爱心，请在5分钟内回复此图片的拍摄地点，我们将把信息上传至数据库，如之后有匹配成功会及时通知您'
        url = app.config.get('HOST')
    elif searchResult['status'] == 1:
        title = u'找到一张相似度%d的照片' % searchResult['confidence']
        description = u'我们会立刻处理此信息,并可能随时联系您'
    elif searchResult['status'] == 2:
        title = u'找到一张相似度%d的照片，相似度比较高' % searchResult['confidence']
        description = u'我们会立刻处理此信息,并可能随时联系您'
    elif searchResult['status'] == 3:
        title = u'找到一张相似度%d的照片！！！，相似度非常高' % searchResult['confidence']
        description = u'这种情况十分紧急，我们会立刻处理此信息,并可能随时联系您，或直接与13061938526联系'
    return {'status':status,'title':title,'description':description,'url':url}

def main():
    children=Missingchildren.query.all()
    total = len(children)
    tCount = 1
    per_page= int(total/tCount)
    secret = app.config.get('FACE_SECRET_TEST')
    apiKey = app.config.get('FACE_API_KEY_TEST')
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


secret = app.config.get('FACE_SECRET_TEST')
apiKey = app.config.get('FACE_API_KEY_TEST')
Face = FaceSet(secret, apiKey)
# main()





