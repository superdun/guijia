# -*- coding:utf-8 -*-

import requests




class FaceSet(object):
    def __init__(self,apiSecret,apiKey):
        self.addFaceUrl = ' https://api-cn.faceplusplus.com/facepp/v3/faceset/addface'
        self.createSetUrl = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/create'
        self.getSetUrl = 'https://api-cn.faceplusplus.com/facepp/v3/faceset/getfacesets'
        self.deleteSetsUrl = ' https://api-cn.faceplusplus.com/facepp/v3/faceset/removeface'
        self.getFaceToken = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
        self.apiSecret = apiSecret
        self.apiKey = apiKey
    def createSet(self,name,tags):
        payload={'api_key':self.apiKey,'api_secret':self.apiSecret,'display_name':tags+name,'outer_id':tags+name,'tags':tags}
        r=requests.post(url=self.createSetUrl,data=payload)
        return r.json()
    def getSets(self,tag=''):
        payload={'api_key':self.apiKey,'api_secret':self.apiSecret,'tags':tag}
        r=requests.post(url=self.getSetUrl,data=payload)
        return r.json()
    def uploadFaces(self,urls,tag):

        sets = self.getSets(tag)['facesets']
        names=[]
        for  i in sets:
            names.append(int(i['outer_id'].split('_')[-1]))
        lastName= max(names)
        failed=[]
        total = len(urls)
        successCount = 0
        for i in range(total):

            payloadForToken={'api_key':self.apiKey,'api_secret':self.apiSecret,'image_url':urls[i],'return_landmark':1,'return_attributes':1}
            rForToken = requests.post(url='self.getFaceToken',data=payloadForToken)
            tokenResult = rForToken.json()
            if not tokenResult.has_key('error_message'):
                token=tokenResult['face_token']
                payloadForAdd={'api_key':self.apiKey,'api_secret':self.apiSecret,'outer_id':tag+str(lastName),'face_tokens':token}
                rForAdd = requests.post(url=self.addFaceUrl,data=payloadForAdd)
                addResult= rForAdd.json()
                if not addResult.has_key('error_message'):
                    if addResult['failure_detail']['reason']=='QUOTA_EXCEEDED':
                        lastName+=1
                        createResult=self.createSet(lastName,tag)
                        if addResult['failure_detail']:
                            failed.append(addResult['failure_detail'])
                        else:
                            successCount += 1
                    elif addResult['failure_detail']:
                        failed.append(addResult['failure_detail'])
                    else:
                        successCount+=1


    def deleteSets(self,id):
        payload={'api_key':self.apiKey,'api_secret':self.apiSecret,'outer_id':id,'face_tokens':'RemoveAllFaceTokens'}
        r= requests.post(url=self.deleteSetsUrl,data=payload)
        return r.json()
f= FaceSet('F2pl2jjyeTtSFPIllQ-MCF9HT2DPqRv5','ZfZkvZVgtmq023KgiYjj8zYp-eGmG-wJ')
print f.getSets('')


