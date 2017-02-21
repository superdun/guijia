# -*- coding: utf-8 -*-

import requests
import math
import random
from PIL import Image, ImageDraw
import thumb
from moduleGlobal import qiniu_store, QINIU_DOMAIN, UPLOAD_URL
from StringIO import StringIO
import urllib2


class faceDetect(object):
    def __init__(self, fileUrl, apiKey, apiSecret):
        # self.filename = filename
        self.file = fileUrl
        self.apiKey = apiKey
        self.apiSecret = apiSecret
        self.payLoad = {'api_key': apiKey, 'api_secret': apiSecret
            , 'return_attributes': 'gender,age,smiling,glass,headpose', 'return_landmark': 1, 'image_url': self.file}
        self.feelGrade = 0
        self.eyeGrade = 0
        self.noseGrade = 0
        self.mouthGrade = 0
        self.chinGrade = 0
        self.status = False

    def postData(self):
        r = requests.post("https://api-cn.faceplusplus.com/facepp/v3/detect", data=self.payLoad)
        self.result = r.json()
        if self.result.has_key('error_message'):
            self.status = False
            self.error = u'面部分析接口忙，请稍后再试'
        else:
            self.status = True
            self.error = False

    def anayFace(self):
        if self.status:
            self.faceNum = len(self.result['faces'])
            if self.faceNum > 1:
                self.status = False
                self.error = u'请上传只有一张脸的照片，不要贪心'
                return 1
            if self.faceNum == 0:
                self.status = False
                self.error = u'sorry,没检测到脸...'
                return 1
            face = self.result['faces'][0]
            self.gender = face['attributes']['gender']['value']
            self.age = face['attributes']['age']['value']
            if face['attributes']['smile']['value'] > face['attributes']['smile']['threshold']:
                self.isSmilling = True
            else:
                self.isSmilling = False
            headAngels = face['attributes']['headpose']
            self.headPutRight = True
            for i in headAngels.values():
                if i >= 10:
                    self.headPutRight = False
            self.glassStatus = face['attributes']['glass']['value']
            self.faceLandmark = face['landmark']
            self.faceWidth = 1.0 * self.faceLandmark['contour_right1']['x'] - self.faceLandmark['contour_left1']['x']
            self.noseWidth = 1.0 * self.faceLandmark['nose_right']['x'] - self.faceLandmark['nose_left']['x']
            self.noseLength = 1.0 * self.faceLandmark['nose_contour_lower_middle']['y'] - (self.faceLandmark[
                                                                                               'nose_contour_right1'][
                                                                                               'y'] +
                                                                                           self.faceLandmark[
                                                                                               'nose_contour_left1'][
                                                                                               'y']) / 2.0
            self.leftEyeWidth = 1.0 * self.faceLandmark['left_eye_right_corner']['x'] - \
                                self.faceLandmark['left_eye_left_corner']['x']
            self.rightEyeWidth = 1.0 * self.faceLandmark['right_eye_right_corner']['x'] - \
                                 self.faceLandmark['right_eye_left_corner']['x']
            self.leftEyeHeight = 1.0 * self.faceLandmark['left_eye_bottom']['y'] - \
                                 self.faceLandmark['left_eye_top']['y']
            self.rightEyeHeight = 1.0 * self.faceLandmark['right_eye_bottom']['y'] - \
                                  self.faceLandmark['right_eye_top']['y']
            self.chinMouthLength = 1.0 * self.faceLandmark['contour_chin']['y'] - \
                                   self.faceLandmark['mouth_upper_lip_bottom'][
                                       'y']
            self.chinNoseLength = 1.0 * self.faceLandmark['contour_chin']['y'] - \
                                  self.faceLandmark['nose_contour_lower_middle']['y']
            self.browNoseLength = 1.0 * self.faceLandmark['nose_contour_lower_middle']['y'] - (self.faceLandmark[
                                                                                                   'right_eyebrow_left_corner'][
                                                                                                   'y'] +
                                                                                               self.faceLandmark[
                                                                                                   'right_eyebrow_right_corner'][
                                                                                                   'y']) / 2.0
            self.quanWidth = 1.0 * self.faceLandmark['contour_right2']['x'] - self.faceLandmark['contour_left2']['x']
            self.heWidth1 = 1.0 * self.faceLandmark['contour_right7']['x'] - self.faceLandmark['contour_left7']['x']
            self.heWidth2 = 1.0 * self.faceLandmark['contour_right8']['x'] - self.faceLandmark['contour_left8']['x']
            chinAngle = getAngle([self.faceLandmark['contour_right9'], self.faceLandmark['contour_right8']],
                                 [self.faceLandmark['contour_left9'], self.faceLandmark['contour_left8']])
            self.chinAngle = chinAngle

            self.mouthWidth = 1.0 * self.faceLandmark['mouth_right_corner']['x'] - \
                              self.faceLandmark['mouth_left_corner']['x']
            self.eyesCenterWidth = 1.0 * self.faceLandmark['right_eye_center']['x'] - \
                                   self.faceLandmark['left_eye_center'][
                                       'x']

            self.rateBrowNoseChinLength = self.browNoseLength / self.chinNoseLength - 1.0
            self.rateEyesWidth = self.leftEyeWidth / self.rightEyeWidth - 1.0
            self.rateEyesHeight = self.faceLandmark['right_eye_top']['y'] * 1.0 / self.faceLandmark['left_eye_top'][
                'y'] - 1.0
            self.rateLeftEyeFaceWidth = self.leftEyeWidth / self.faceWidth - 0.2
            self.rateRightEyeFaceWidth = self.rightEyeWidth / self.faceWidth - 0.2
            self.rateQuanHeWidth = self.quanWidth / self.heWidth1 - (1 / 0.681)
            self.rateNoseFaceWidth = self.noseWidth / self.faceWidth - 0.2
            self.rateEyesCenterMouthWidth = self.eyesCenterWidth / self.mouthWidth - 1.0
            self.rateChinMouthNoseLength = self.chinMouthLength / self.chinNoseLength - (2.0 / 3)
            self.rateNoseWidthLength = self.noseWidth / self.browNoseLength - 0.58

            self.rateDict = {'rateBrowNoseChinLength': self.rateBrowNoseChinLength, 'rateEyesWidth': self.rateEyesWidth,
                             'rateEyesHeight': self.rateEyesHeight,
                             'rateLeftEyeFaceWidth': self.rateLeftEyeFaceWidth,
                             'rateRightEyeFaceWidth': self.rateRightEyeFaceWidth,
                             'rateQuanHeWidth': self.rateQuanHeWidth, 'rateNoseFaceWidth': self.rateNoseFaceWidth,
                             'rateEyesCenterMouthWidth': self.rateEyesCenterMouthWidth,
                             'rateChinMouthNoseLength': self.rateChinMouthNoseLength,
                             'rateNoseWidthLength': self.rateNoseWidthLength}
        else:
            self.faceNum = 0

    def showResult(self):
        if not self.status:
            return 1
        try:
            im = Image.open(StringIO(urllib2.urlopen(self.file, timeout=1).read()))
        except urllib2.URLError, e:
            self.status = False
            self.error = u'服务器忙，请稍候再试'
            return 1

        draw = ImageDraw.Draw(im)
        self.points = []
        for i in self.result['faces'][0]['landmark'].values():
            self.points.append((i['x'], i['y']))
            draw.ellipse([i['x'] - 1.5, i['y'] - 1.5, i['x'] + 1.5, i['y'] + 1.5], fill='red')
        draw.line([(self.faceLandmark['left_eye_center']['x'], self.faceLandmark['left_eye_center']['y'])
                      , (self.faceLandmark['right_eye_center']['x'], self.faceLandmark['right_eye_center']['y'])],
                  fill='green', width=2)
        draw.line([((self.faceLandmark['left_eyebrow_right_corner']['x'] +
                     self.faceLandmark['right_eyebrow_left_corner']['x']) / 2,
                    self.faceLandmark['left_eye_center']['y'])
                      , (self.faceLandmark['nose_tip']['x'], self.faceLandmark['nose_tip']['y'])],
                  fill='black', width=2)
        draw.line([(self.faceLandmark['nose_left']['x'], self.faceLandmark['nose_left']['y'])
                      , (self.faceLandmark['nose_right']['x'], self.faceLandmark['nose_right']['y'])],
                  fill='red', width=2)
        draw.line([(self.faceLandmark['mouth_right_corner']['x'], self.faceLandmark['mouth_right_corner']['y'])
                      , (self.faceLandmark['mouth_left_corner']['x'], self.faceLandmark['mouth_left_corner']['y'])],
                  fill='blue', width=2)
        draw.line([(self.faceLandmark['nose_tip']['x'], self.faceLandmark['nose_tip']['y'])
                      , (self.faceLandmark['contour_chin']['x'], self.faceLandmark['contour_chin']['y'])],
                  fill='black', width=2)
        del draw

        result = thumb.upload_file_by_pillow(im, 'result.jpg', UPLOAD_URL, QINIU_DOMAIN, qiniu_store)
        if result['result'] != 1:
            self.status = False
            self.error = u'服务器忙，请稍候再试'
        pornResult = detectPorn(im)[0]
        if pornResult:
            self.status = False
            self.error = u'你上传的图片不正经啊！分析不了，换一个试试？'
            return 1
        del im
        return result
        # im.save(self.filename[:-4] + 'ok.jpg', 'JPEG')

    def score(self):
        if not self.status:
            return 1
        rateDict = self.rateDict
        for i in rateDict:
            if abs(rateDict[i]) > 0.1:
                rateDict[i] = rateDict[i] * 2

        score = abs(rateDict['rateBrowNoseChinLength']) + abs(rateDict['rateEyesWidth'] / 3) + abs(
            rateDict['rateEyesHeight'] / 3) + abs(rateDict['rateChinMouthNoseLength']) + abs(
            rateDict['rateNoseWidthLength'])
        self.feelGrade = self.feelGrade + abs(rateDict['rateBrowNoseChinLength']) + abs(
            rateDict['rateEyesWidth'] / 3) + abs(
            rateDict['rateEyesHeight'] / 3)
        self.chinGrade = self.chinGrade + abs(rateDict['rateChinMouthNoseLength'])
        self.noseGrade = self.noseGrade + abs(
            rateDict['rateNoseWidthLength'])

        if rateDict['rateEyesHeight'] > 0 and rateDict['rateEyesHeight'] < 0.3:
            score = score - rateDict['rateQuanHeWidth'] / 3
        elif rateDict['rateEyesHeight'] <= 0 and rateDict['rateEyesHeight'] > -0.1:
            score = score - rateDict['rateQuanHeWidth'] / 3
        elif rateDict['rateEyesHeight'] >= 0.3:
            score = score + rateDict['rateQuanHeWidth'] / 3
        else:
            score = score - rateDict['rateQuanHeWidth']

        if rateDict['rateLeftEyeFaceWidth'] < 0 and rateDict['rateRightEyeFaceWidth'] < 0:
            score = score + abs(rateDict['rateLeftEyeFaceWidth'] * 30) + abs(rateDict['rateRightEyeFaceWidth'] * 30)
            self.eyeGrade = self.eyeGrade + abs(rateDict['rateLeftEyeFaceWidth'] * 30) + abs(
                rateDict['rateRightEyeFaceWidth'] * 30)
        else:
            score = score + abs(rateDict['rateLeftEyeFaceWidth'] / 30) + abs(rateDict['rateRightEyeFaceWidth'] / 30)
            self.eyeGrade = self.eyeGrade + abs(rateDict['rateLeftEyeFaceWidth'] / 30) + abs(
                rateDict['rateRightEyeFaceWidth'] / 30)
        # if rateDict['rateRightEyeFaceWidth']< 0:
        #     score = score + abs(rateDict['rateRightEyeFaceWidth'] * 30)
        # else:
        #     score = score + rateDict['rateRightEyeFaceWidth']
        if rateDict['rateNoseFaceWidth'] < 0:
            score = score + abs(rateDict['rateNoseFaceWidth'] * 0.5)
            self.noseGrade = self.noseGrade + abs(rateDict['rateNoseFaceWidth'] * 0.5)
        else:
            score = score + rateDict['rateNoseFaceWidth']
            self.noseGrade = self.noseGrade + abs(rateDict['rateNoseFaceWidth'])

        if rateDict['rateEyesCenterMouthWidth'] < 0:
            score = score + abs(rateDict['rateEyesCenterMouthWidth'] * 3.5)
            self.mouthGrade = self.mouthGrade + abs(rateDict['rateEyesCenterMouthWidth'] * 3.5)
        else:
            score = score + abs(rateDict['rateNoseFaceWidth'] / 2)
            self.mouthGrade = self.mouthGrade + abs(rateDict['rateNoseFaceWidth'] / 2)

        if self.chinAngle > 140:
            score = score + 0.1
            self.chinGrade = self.chinGrade + 0.1
        elif self.chinAngle < 90:
            score = score + 0.06
            self.chinGrade = self.chinGrade - 0.03
        ageGrade = (1.02 ** (self.age - 18) - 1) if self.age >= 18 else 0
        if self.gender == 'Female':
            score = score + ageGrade
        self.feelGrade = 200 / ((6 ** self.feelGrade - 1 + 2))
        self.eyeGrade = 200 / ((6 ** self.eyeGrade - 1 + 2))
        self.noseGrade = 200 / ((6 ** self.noseGrade - 1 + 2))
        self.mouthGrade = 200 / ((6 ** self.mouthGrade - 1 + 2))
        self.chinGrade = 200 / ((6 ** self.chinGrade - 1 + 2))
        self.grade = 800 / ((3 ** score - 1 + 8))
        return {'grade': round(self.grade, 3), 'eye': round(self.eyeGrade, 3), 'nose': round(self.noseGrade, 3),
                'mouth': round(self.mouthGrade, 3), 'chin': round(self.chinGrade, 3), 'feel': round(self.feelGrade, 3)}

    def message(self):
        if not self.status:
            return 1
        if self.gender == 'Male':
            if self.age > 30:
                baseMessage = u'Hello,先生！'
            elif self.age < 15:
                baseMessage = u'Hello,小子！'
            else:
                baseMessage = u'Hello,哥们儿！'
        else:
            if self.age > 30:
                baseMessage = u'Hello,女士！'
            elif self.age < 15:
                baseMessage = u'Hello,小丫头！'
            else:
                baseMessage = u'Hello,妹纸！'

        if self.glassStatus == 'Normal':
            baseMessage = baseMessage + u'戴眼镜很文艺，不过会影响检测结果哦。'
        elif self.glassStatus == 'Dark':
            baseMessage = baseMessage + u'你戴着墨镜让我怎么检测？！'
        if self.isSmilling:
            baseMessage = baseMessage + u'笑得很开心，有啥好事说来听听。'
        else:
            baseMessage = baseMessage + u'不要这么严肃嘛，开心点！'
        if not self.headPutRight:
            baseMessage = baseMessage + u'记得下次头要摆的正一些，否则会影响检测结果哦！'

        goodPoint = []
        weakPoint = []
        messageDict = {'rateBrowNoseChinLength': [u'面部中鼻尖往下占的比例略低，眉心到鼻尖的比例较低', u'面部总体比例匀称', u'在您的面部中鼻尖往下占的比例略高'],
                       'rateEyesWidth': [u'眼睛看上去好像不一样大，是不是照片摆歪了', u'', u'眼睛看上去好像不一样大，是不是照片摆歪了'],
                       'rateEyesHeight': [u'眼睛看上去好像不一样大，是不是照片摆歪了', u'', u'眼睛看上去好像不一样大，是不是照片摆歪了'],
                       'rateLeftEyeFaceWidth': [u'有双大的眼睛', u'有双漂亮的眼睛', u'眼睛看上去比较小'],
                       'rateRightEyeFaceWidth': [u'有双大的眼睛', u'有双漂亮的眼睛', u'眼睛看上去比较小'],
                       'rateQuanHeWidth': [u'脸比较尖', u'有着优雅的面部曲线', u'脸有些宽'],
                       'rateNoseFaceWidth': [u'鼻子有点宽', u'鼻子很漂亮', u'鼻子细细的'],
                       'rateEyesCenterMouthWidth': [u'是个樱桃小嘴', u'嘴大小适中', u'，呃，你的嘴有点大哦'],
                       'rateChinMouthNoseLength': [u'下巴偏长', u'下巴比例合适', u'下巴偏短'],
                       'rateNoseWidthLength': [u'鼻子有点宽', u'鼻子大小合适刚刚好', u'鼻子长宽比有些奇怪，有点太长了']
                       }
        rateDict = self.rateDict
        isPerfact = True
        zhuanZhe = [u' 不过，还有一些瑕疵哦，如，您', u' 可是，并不是完美无缺哦，您', u' 但是，您', u' 然而，还有一些问题，您', u' but ，not 十全十美，您']
        bingLie = [u' 并且', u' 而且', u' 且', u' 同时', u' 还', u' 还有', u' 看上去', u'，']
        wanMei = [u'您几乎有一张完美的颜，基本上挑不出什么缺点，您', u'您几乎的颜接近完美，基本上挑不出什么缺点，您', u'这张脸毫无瑕疵，您']
        notWanMei = [u'您的颜值还不错啦，您', u'您的颜值已经超越路人啦，您']
        chouLou = [u'是不是照片没选好，电脑分析您的颜值比较低哦，我本人是不信的！您', u'呃.......您', u'怎么和你形容呢....你']
        for i in rateDict:
            if i == 'rateBrowNoseChinLength' and abs(rateDict[i]) > 0.1:
                isPerfact = False
                if rateDict[i] > 0.1:
                    weakPoint.append(messageDict[i][0])
                else:
                    weakPoint.append(messageDict[i][2])
            if i == 'rateEyesWidth' and abs(rateDict[i]) > 0.1:
                isPerfact = False
                if rateDict[i] > 0.1:
                    weakPoint.append(messageDict[i][0])
                else:
                    weakPoint.append(messageDict[i][2])
            if i == 'rateEyesHeight' and abs(rateDict[i]) > 0.1:
                isPerfact = False
                if rateDict[i] > 0.1:
                    weakPoint.append(messageDict[i][0])
                else:
                    weakPoint.append(messageDict[i][2])
            if i == 'rateNoseFaceWidth' and abs(rateDict[i]) > 0.1:
                isPerfact = False
                if rateDict[i] > 0.1:
                    weakPoint.append(messageDict[i][0])
                else:
                    weakPoint.append(messageDict[i][2])
            if i == 'rateEyesCenterMouthWidth' and abs(rateDict[i]) > 0.1:
                isPerfact = False
                if rateDict[i] > 0.1:
                    weakPoint.append(messageDict[i][0])
                else:
                    weakPoint.append(messageDict[i][2])
            if i == 'rateChinMouthNoseLength' and abs(rateDict[i]) > 0.1:
                isPerfact = False
                if rateDict[i] > 0.1:
                    weakPoint.append(messageDict[i][0])
                else:
                    weakPoint.append(messageDict[i][2])
            if i == 'rateNoseWidthLength' and abs(rateDict[i]) > 0.1:
                isPerfact = False
                if rateDict[i] > 0.1:
                    weakPoint.append(messageDict[i][0])
                else:
                    weakPoint.append(messageDict[i][2])
            elif (i == 'rateLeftEyeFaceWidth' or i == 'rateRightEyeFaceWidth') and (rateDict[i] < -0.01):
                isPerfact = False
                weakPoint.append(messageDict[i][2])

            elif (i == 'rateLeftEyeFaceWidth' or i == 'rateRightEyeFaceWidth') and (rateDict[i] > 0.01):
                goodPoint.append(messageDict[i][0])
            elif i == 'rateQuanHeWidth' and rateDict[i] < -0.1:
                isPerfact = False
                weakPoint.append(messageDict[i][2])
            else:
                goodPoint.append(messageDict[i][1])

        if self.chinAngle < 90:
            weakPoint.append(u'下巴太尖了，真的不是PS的吗')
        elif self.chinAngle > 130:
            weakPoint.append(u'脸貌似有点方')
        else:
            goodPoint.append(u'下颌的角度也刚刚好')

        goodPoint = makeSentence(bingLie, goodPoint)
        weakPoint = makeSentence(bingLie, weakPoint)
        if isPerfact:
            comment = goodPoint
            baseMessage = baseMessage + wanMei[random.randint(0, len(wanMei) - 1)]
        elif self.grade > 85:
            comment = connectSentences(zhuanZhe, [goodPoint, weakPoint])
            baseMessage = baseMessage + wanMei[random.randint(0, len(wanMei) - 1)]
        elif self.grade < 65:
            comment = connectSentences(zhuanZhe, [goodPoint, weakPoint])
            baseMessage = baseMessage + chouLou[random.randint(0, len(chouLou) - 1)]
        else:
            comment = connectSentences(zhuanZhe, [goodPoint, weakPoint])
            baseMessage = baseMessage + notWanMei[random.randint(0, len(notWanMei) - 1)]
        comment = baseMessage + comment
        return comment


# # class fortuneTelling(object):
#     def __init__(self,face):detectPorn
def getAngle(v1, v2):
    k1 = (v1[0]['y'] - v1[1]['y']) / (v1[0]['x'] - v1[1]['x'] + 0.000001)
    k2 = (v2[0]['y'] - v2[1]['y']) / (v2[0]['x'] - v2[1]['x'] + 0.000001)
    if math.atan(abs(k2 - k1) / abs(1 + k1 * k2)) * 180 / math.pi < 80:
        return 180 - math.atan(abs(k2 - k1) / abs(1 + k1 * k2)) * 180 / math.pi
    else:
        return math.atan(abs(k2 - k1) / abs(1 + k1 * k2)) * 180 / math.pi


def delEmptyAndUniq(l):
    l = list(set(l))
    while '' in l:
        l.remove('')
    return l


def connectSentences(words, sentences):
    result = sentences[0] if len(sentences) > 0 else ''
    if len(sentences) > 1:
        for i in range(1, len(sentences)):
            result = result + words[random.randint(0, len(words) - 1)] + sentences[i]
    return result


def makeSentence(words, rawSentence):
    sentences = delEmptyAndUniq(rawSentence)
    return connectSentences(words, sentences)


# porn detect

SIZE = 150, 150
THRESHOLD = 0.5


def prepare_image(image):
    if not image.mode == 'RGB':
        image = image.convert(mode='RGB')
    image.thumbnail(SIZE, Image.ANTIALIAS)
    return image


def get_ycbcr(image):
    ret = []

    def rgb2ycbcr(r, g, b):
        return (
            16 + (65.738 * r + 129.057 * g + 25.064 * b) / 256,
            128 + (-37.945 * r - 74.494 * g + 112.439 * b) / 256,
            128 + (112.439 * r - 94.154 * g - 18.285 * b) / 256
        )

    x, y = image.size
    for i in range(0, x):
        for j in range(0, y):
            ret.append(rgb2ycbcr(*image.getpixel((i, j))))

    return ret


def detectPorn(image):
    def judge(sample):
        y, cb, cr = sample

        return 80 <= cb <= 120 and 133 <= cr <= 173

    image = prepare_image(image)
    ycbcr = get_ycbcr(image)

    judged = map(judge, ycbcr)

    rating = float(judged.count(True)) / len(judged)
    return rating > THRESHOLD, rating


def detect(fileUrl, key, apiKey):
    d = faceDetect(fileUrl, key, apiKey)
    d.postData()
    d.anayFace()
    imgResult = d.showResult()
    if d.status:
        grades = d.score()
        comment = d.message()
        status = d.status
        result = {'status': status, 'grades': grades, 'imgResult': imgResult, 'comment': comment, 'gender': d.gender,'age':d.age}
        return result
    else:
        status = d.status
        error = d.error
        result = {'status': status, 'error': error}
        return result
