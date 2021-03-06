import pet_chain
import requests
import time
import json
import configparser
import os
import base64
from PIL import Image,ImageDraw,ImageFile

import cv2
import numpy as np
from matplotlib import pyplot as plt
import reshape
import autoCheckCaptcha
import train2
import tensorflow as tf
import time

ImageFile.LOAD_TRUNCATED_IMAGES = True


class Pic():
    def __init__(self):
        self.degree_map = {
            0: "common",
            1: "rare",
            2: "excellence",
            3: "epic",
            4: "mythical"
        }
        self.isAuto=False
        self.degree_conf = {}
        self.interval = 1
        self.seed = ''
        self.cookies = ''
        self.username = ''
        self.password = ''
        self.captcha = ''
        self.headers = {}
        self.get_headers()
        self.get_config()

    def get_config(self):
        config = configparser.ConfigParser()
        config.read("pet-chain/config/config.ini")
        self.isAuto = config.getboolean("Pet-Chain", "isAuto")
        for i in range(5):
            try:
                amount = config.getfloat("Pet-Chain", 'dog' + str(i))
            except Exception as e:
                print(e)
                amount = 100
            self.degree_conf[i] = amount

    def get_headers(self):
        with open("pet-chain/config/headers.txt") as f:
            lines = f.readlines()
            for line in lines:
                splited = line.strip().split(":")
                key = splited[0].strip()
                value = ":".join(splited[1:]).strip()
                self.headers[key] = value
    def genCaptcha(self):
        data = {
            "appId": 1,
            "requestId": int(round(time.time() * 1000)),
            "tpl": "",
        }
        try:
            page = requests.post("https://pet-chain.baidu.com/data/captcha/gen", headers=self.headers, data=json.dumps(data), timeout=2)
            jPage = page.json()
            if jPage.get(u"errorMsg") == "success":
                seed = jPage.get(u"data").get(u"seed")
                img = jPage.get(u"data").get(u"img")
                with open('pet-chain/captcha/' + seed + '.jpg', 'wb') as f:
                    f.write(base64.b64decode(img))
                return seed
            else:
                print('获取验证码失败！')
                return -1
        except:
            return -1

#二值判断,如果确认是噪声,用改点的上面一个点的灰度进行替换  
#该函数也可以改成RGB判断的,具体看需求如何  
def getPixel(image,x,y,G,N):  
    L = image.getpixel((x,y))  
    if L > G:  
        L = True  
    else:  
        L = False  

    nearDots = 0  
    if L == (image.getpixel((x - 1,y - 1)) > G):  
        nearDots += 1  
    if L == (image.getpixel((x - 1,y)) > G):  
        nearDots += 1  
    if L == (image.getpixel((x - 1,y + 1)) > G):  
        nearDots += 1  
    if L == (image.getpixel((x,y - 1)) > G):  
        nearDots += 1  
    if L == (image.getpixel((x,y + 1)) > G):  
        nearDots += 1  
    if L == (image.getpixel((x + 1,y - 1)) > G):  
        nearDots += 1  
    if L == (image.getpixel((x + 1,y)) > G):  
        nearDots += 1  
    if L == (image.getpixel((x + 1,y + 1)) > G):  
        nearDots += 1  

    if nearDots < N:  
        return image.getpixel((x,y-1))  
    else:  
        return None  

    # 降噪   
    # 根据一个点A的RGB值，与周围的8个点的RBG值比较，设定一个值N（0 <N <8），当A的RGB值与周围8个点的RGB相等数小于N时，此点为噪点   
    # G: Integer 图像二值化阀值   
    # N: Integer 降噪率 0 <N <8   
    # Z: Integer 降噪次数   
    # 输出   
    #  0：降噪成功   
    #  1：降噪失败   
def clearNoise(image,G,N,Z):  
    draw = ImageDraw.Draw(image)  

    for i in range(0,Z):  
        for x in range(1,image.size[0] - 1):  
            for y in range(1,image.size[1] - 1):  
                color = getPixel(image,x,y,G,N)  
                if color != None:  
                    draw.point((x,y),color)


# 去除干扰线算法
def depoint(img):   #input: gray image
    pixdata = img.load()
    w,h = img.size
    for y in range(1,h-1):
        for x in range(1,w-1):
            count = 0
            if pixdata[x,y-1] > 245:
                count = count + 1
            if pixdata[x,y+1] > 245:
                count = count + 1
            if pixdata[x-1,y] > 245:
                count = count + 1
            if pixdata[x+1,y] > 245:
                count = count + 1
            if count > 2:
                pixdata[x,y] = 255
    return img

# 二值化算法
def binarizing(img,threshold):
    pixdata = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    return img

def imgConvert(image):
    # 转化为灰度图
    image = image.convert('L')
    # 把图片变成二值图像
    image = binarizing(image, 190)

    img=depoint(image)
    img=img.resize((63,23),Image.ANTIALIAS)
    # img.save('pet-chain/captcha.jpg')
    return img

# 将back中的图片按照比例每个切成四个 14-24 24-34 37-47 47-57 切分为四个字符图片
def splitimage(name, fixlen,srcpath,dstpath):
    img = Image.open(srcpath + name)
    print('开始处理图片切割, 请稍候...')
    basename = name.split('.')[0]
    for i in range(len(basename)):
        dstname = basename + "_" + basename[i] + '.jpg'
        box = (fixlen[i][0], 0, fixlen[i][1], 23)
        img.crop(box).save(dstpath + dstname)

def splitimageOrder(img,fixlen,dstpath):
    for i in range(4):
        dstname = str(i) + '.jpg'
        box = (fixlen[i][0], 0, fixlen[i][1], 23)
        img.crop(box).save(dstpath + dstname)
        # cv2.imshow("img" + str(i),img[fixlen[i][0]:fixlen[i][1],0:23])
        # imgOrder.append(img[0:23,fixlen[i][0]:fixlen[i][1]])
        # cv2.imwrite('pet-chain/divide/' + str(i) + '.jpg',img[0:23,fixlen[i][0]:fixlen[i][1]])

  

if __name__ == "__main__":
    # 将back中的图片按照比例每个切成四个 14-24 24-34 37-47 47-57 切分为四个字符图片
    fixlen = [[14,24],[24,34],[34,44],[47,57]]
    dz = train2.Train()
    output = dz.crack_captcha_cnn()
    saver = tf.train.Saver()
    sess =  tf.Session()
    saver.restore(sess,tf.train.latest_checkpoint('pet-chain/model'))
    i = 0
    pic = Pic()
    while i < 3000:
        time.sleep(1)
        seed = pic.genCaptcha()
        if seed == -1 :
            continue
        else:
            try:
                path = 'pet-chain/captcha/' + seed + '.jpg'

                img = Image.open(path)
                imgConvert(img)
                splitimageOrder(imgConvert(img),fixlen,'pet-chain/divide/')
                # img.show()
                txt = ''
                for i in range(4):
                    txt += autoCheckCaptcha.autoCheck("pet-chain/divide/" + str(i) + ".jpg",dz,sess,output)
                if txt != '':
                    print("开始重命名" + path  + "为pet-chain/captcha/" + txt + ".jpg")
                    os.rename(path,'pet-chain/captcha/' + txt + '.jpg')
            except Exception as e:
                print(e)
                continue

        
    
    # for file in os.listdir('pet-chain/back'):
    #     if len(file) == 8:
    #         splitimage(file,fixlen,'pet-chain/back/','pet-chain/split/')
    #     else:
    #         print("file 不合法：" + file)

    # dz = train2.Train()
    # output = dz.crack_captcha_cnn()
    # saver = tf.train.Saver()
    # sess =  tf.Session()
    # saver.restore(sess,tf.train.latest_checkpoint('pet-chain/model'))
    # pic = Pic()
    # pic.genCaptcha()

    # start = time.time()
    # img = Image.open("pet-chain/captcha.jpg")
    # imgConvert(img)
    # splitimageOrder(fixlen,'pet-chain/divide/')
    # # img.show()
    # txt = ''
    # for i in range(4):
    #     txt += autoCheckCaptcha.autoCheck("pet-chain/divide/" + str(i) + ".jpg",dz,sess,output)
    # end = time.time()
    # print('code = ',txt)
    # print("cost : ", end -start)
    #autoCheckCaptcha.autoCheck('pet-chain/back/2SF4.jpg',dz)

    # for file in os.listdir('pet-chain/captcha'):    
    #     img = Image.open('pet-chain/captcha/' + file)
    #     dst = imgConvert(img)
    #     #img.show()
    #     dst.save('pet-chain/captcha/' + file)
    # #降噪处理图片
    # pc = Pic()
    # #打开图片  
    # image = Image.open("pet-chain/captcha/mP58.jpg")  
  
    # #将图片转换成灰度图片  
    # image = image.convert("L") 
    # clearNoise(image,80,4,2)
    # image.save("pet-chain/captcha/mP58.jpg")  
    # 新建文件夹
    # if not os.path.exists('pet-chain/captcha'):
    #     os.makedirs('pet-chain/captcha')
    # 
    # #pc.genCaptcha()
    # i = 0
    # while True:
    #     i += 1
    #     if i > 1000:
    #         break
    #     try:
    #         pc.genCaptcha()
    #     except:
    #         continue
    #     time.sleep(3) # 每隔三秒执行一次