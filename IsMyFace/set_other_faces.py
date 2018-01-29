import sys
import os
import cv2
import dlib
from urllib import request
import tarfile

#
#wget http://vis-www.cs.umass.edu/lfw/lfw.tgz

input_dir = './input_img'
output_dir = './other_faces'
size = 64

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

detector = dlib.get_frontal_face_detector()

# 下载http://vis-www.cs.umass.edu/lfw/lfw.tgz 并解压到 ./input_img
if not os.path.exists(input_dir):
    os.makedirs(input_dir)
url = 'http://vis-www.cs.umass.edu/lfw/lfw.tgz'

def down(_save_path, _url):
    try:
        print("开始下载http://vis-www.cs.umass.edu/lfw/lfw.tgz...")
        request.urlretrieve(_url,_save_path)
        print("下载http://vis-www.cs.umass.edu/lfw/lfw.tgz结束")
        return True
    except Exception as e:
        print('\nError when retrieving the URL:', _save_path,e)
        return False

# 解压文件lfw.tgz 并解压到 ./input_img
def uzipFile():
    tarobj = tarfile.open(input_dir + '/' + 'lfw.tgz', "r:gz")
    for tarinfo in tarobj:
        tarobj.extract(tarinfo.name, input_dir)
    tarobj.close()


def detectFaces():
    index = 1
    for (path,dirnames,filenames) in os.walk(input_dir):
        for filename in filenames:
            if filename.endswith('.jpg'):
                print("开始获取头像 %s" % index)
                img_path = path + '/' + filename
                img = cv2.imread(img_path)
                #转化为灰度图片
                gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                # 进行人脸检测，dets为返回值
                dets = detector(gray_img,1)
                # 使用enumerate 函数遍历序列中的元素以及它们的下标
                # 下标i即为人脸序号
                # left：人脸左边距离图片左边界的距离 ；right：人脸右边距离图片左边界的距离
                # top：人脸上边距离图片上边界的距离 ；bottom：人脸下边距离图片上边界的距离
                for i, d in enumerate(dets):
                    x1 = d.top() if d.top() > 0 else 0
                    y1 = d.bottom() if d.bottom() > 0 else 0
                    x2 = d.left() if d.left() > 0 else 0
                    y2 = d.right() if d.right() > 0 else 0
                    # img[y:y+h, x:x+w]
                    face = img[x1:y1, x2:y2]
                    # 调整图片的尺寸
                    face = cv2.resize(face, (size, size))
                    cv2.imshow('image', face)
                    # 保存图片
                    cv2.imwrite(output_dir + '/' + str(index) + '.jpg', face)
                    index += 1
                key = cv2.waitKey(30) & 0xff
                if key == 27:
                    sys.exit(0)

lfw = input_dir + '/lfw.tgz'
if not os.path.exists(lfw):
    isdown = down(input_dir + '/lfw.tgz', url)
if isdown:
    if not os.path.exists(input_dir + '/lfw'):
        uzipFile()
    detectFaces()
