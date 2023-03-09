import math
import os
import random
import re
import sys

import numpy
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


# LSB隐写算法
# 载体初始化函数
def carry():
    filelist = os.listdir(".\data\carray")
    for i in range(0, len(filelist)):
        width = Image.open(".\data\carray\\" + filelist[i]).width
        height = Image.open(".\data\carray\\" + filelist[i]).height
        print(str(i+1) + "." + filelist[i] + " " + str(width) + "*" + str(height) + "\n")
    number = int(input("请选择密文载体图像(输入序号)："))
    return Image.open(".\data\carray\\" + filelist[number-1])

# 文本型隐写密文处理函数
# 格式化bin()函数处理后的ascii码
def plus(string):
    return string.zfill(8)
# 将文本密文转化为bit矩阵
def toBit(ciphertext):
    string = ""
    for i in range(len(ciphertext)):
        string = string + "" + plus(bin(ord(ciphertext[i])).replace('0b', ''))
    list = re.findall(r'.{1}', string)
    listLen = len(list)
    print(listLen)
    width = listLen
    height = 1
    n=0
    # 规定矩阵行列
    while width%2==0:
        if width==height:
            break
        n=n+1
        width = int(width/2)
        height = int(2**n)
    # 初始化bit矩阵
    bitArray = np.zeros((height,width))
    n = 0
    # 将列表中的bit按位写入矩阵
    for i in range(height):
        for j in range(width):
            bitArray[i][j] = list[n]
            n = n + 1
    return bitArray
# 格式化文本密文输出图像
def getBitImage(ciphertextArray):
    height,width = ciphertextArray.shape
    for i in range(height):
        for j in range(width):
            if ciphertextArray[i][j]==0:
                continue
            else:
                ciphertextArray[i][j]=255
    return ciphertextArray
# 计算文本型密文的信息量和信息熵
def getInformation(ciphertextArray):
    black = 0
    white = 0
    height, width = ciphertextArray.shape
    for i in range(height):
        for j in range(width):
            if ciphertextArray[i][j]==0:
                black = black + 1
            else:
                white = white + 1
    # 计算信息量
    information = -(math.log2(black/(width*height))+math.log2(white/(width*height)))
    # 计算信息熵
    informationEntropy = -((black/(width*height))*math.log2(black/(width*height))+(white/(width*height)*math.log2(white/(width*height))))
    return information,informationEntropy

# 图片型隐写密文处理函数
# 将密文图片转化位bit矩阵
def toBitImg(img):
    height,width = img.shape
    string = ""
    for i in range(height):
        for j in range(width):
            string = string + "" + plus(bin(img[i][j]).replace('0b',''))
    list = re.findall(r'.{1}',string)
    return list
# 将密文图片基于混沌Logistic映射加密算法加密
# 0<x<1 , 3.5699<u<4 , times为迭代次数
def logistic(Img, x, u,times):
    M = Img.size[0]
    N = Img.size[1]
    for i in range(1, times):
        x = u * x * (1 - x)
    array = np.zeros(M * N)
    array[1] = x
    for i in range(1, M * N - 1):
        array[i + 1] = u * array[i] * (1 - array[i])
    array = np.array(array * 255, dtype='uint8')
    code = np.reshape(array, (M, N))
    xor = Img ^ code
    v = xor
    return v
# 密文图像加密
def imgToCiphertext(img):
    # 定义logistic运算参数
    x = 0.1
    u = 4
    times = 500
    # 将图片分割成三个颜色通道
    r,g,b = img.split()
    R = logistic(r, x, u, times)
    G = logistic(g, x, u, times)
    B = logistic(b, x, u, times)

    R = Image.fromarray(R)
    G = Image.fromarray(G)
    B = Image.fromarray(B)


    cimg = Image.merge("RGB",(R,G,B))
    cimg.show()
    return cimg

# 密文初始化函数
def creatCiphertext():
    print("支持的密文类型：1.图像 2.文本")
    number = input("请选择密文类型：")
    if number == "1":
        filelist = os.listdir(".\data\ciphertext\pic")
        for i in range(1, len(filelist)+1):
            print(str(i) + "." + filelist[i-1] + "\n")
        number = int(input("请选择密文图像(输入序号)："))
        imgCiphertext = Image.open(".\data\ciphertext\pic\\" + filelist[number-1])
        # 隐写图像灰度化
        imgCiphertext = imgCiphertext.convert("RGB")
        imgCiphertext = imgToCiphertext(imgCiphertext)
        imgCiphertext = imgCiphertext.convert("L")
        ciphertext = numpy.array(imgCiphertext)
        ciphertext = toBitImg(ciphertext)
    elif number == "2":
        print("文本密文输入方式：1.手动输入 2.记事本输入")
        num = input("请选择文本输入方式：")
        if num == "1":
            ciphertext = input("请输入密文：")
            ciphertext = re.findall(r'.{2}', ciphertext)
        elif num == "2":
            print("可选择的密文文件如下：")
            filelist = os.listdir(".\data\ciphertext\words")
            for i in range(1, len(filelist)+1):
                print(str(i) + "." + filelist[i-1] + "\n")
            number = int(input("请选择密文文本(输入序号)："))
            file = open(".\data\ciphertext\words\\" + filelist[number-1])
            ciphertext = ""
            ciphertextList = []
            for word in file.read():
                word = word.strip("\n")
                ciphertextList.append(word)
            ciphertext = "".join(word for word in ciphertextList if word.isalnum())
            ciphertext = list(ciphertext)
            ciphertext = toBit(ciphertext)
    return ciphertext

# 载体图像处理
# 颜色通道选择函数
def choiceColor(img, RGB):
    r, g, b = img.split()
    if RGB == "r":
        return r
    elif RGB == "g":
        return g
    elif RGB == "b":
        return b


c = creatCiphertext()



# pic = carry()
# print(pic)
# pic_r,pic_g,pic_b = pic.split()
# for p in (pic_r,pic_g,pic_b):
#     print(p)
#
# pic_r = pic_r.convert("L")
# pic_rArray = np.array(pic_r)
# pic_gArray = np.array(pic_g)
# pic_bArray = np.array(pic_b)
#
# m = 0
# n = 0
# size = pic.height*pic.width
# for i in range(pic_r.height):
#     for j in range(pic_r.width):
#         pic_rArray[i][j]=pic_rArray[i][j]&(2**6-1)
#         m = m + 1
#         sys.stdout.write(("\r当前完成 :{0}/"+str(size)).format(m))
#         sys.stdout.flush()
# pic_r = Image.fromarray(pic_rArray)
# pic_r = pic_r.convert("RGB")
# pic_r.show()



# 1100 1100

# 1100 0000
# plt.subplot(311)
# plt.imshow(pic_r)
# plt.axis()
# plt.subplot(312)
# plt.imshow(pic_g)
# plt.axis()
# plt.subplot(313)
# plt.imshow(pic_b)
# plt.axis()
# plt.show()