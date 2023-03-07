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


# 格式化bin()函数处理后的ascii码
def plus(string):
    return string.zfill(8)
# 将文本密文转化为bit流
def toBit(ciphertext):
    string = ""
    for i in range(len(ciphertext)):
        string = string + "" + plus(bin(ciphertext[i]).replace('0b', ''))
    list = re.findall(r'.{1}', string)
    return list

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
        # 隐写图像二值化
        imgCiphertext = imgCiphertext.convert("1")
        ciphertext = numpy.array(imgCiphertext)
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
    return ciphertext

# 比特流随机映射到载体图像空间域

# 颜色通道选择函数
def choiceColor(img, RGB):
    r, g, b = img.split()
    if RGB == "r":
        return r
    elif RGB == "g":
        return g
    elif RGB == "b":
        return b



pic = carry()
print(pic)
pic_r,pic_g,pic_b = pic.split()
for p in (pic_r,pic_g,pic_b):
    print(p)

pic_r = pic_r.convert("L")
pic_rArray = np.array(pic_r)
pic_gArray = np.array(pic_g)
pic_bArray = np.array(pic_b)

m = 0
n = 0
size = pic.height*pic.width
for i in range(pic_r.height):
    for j in range(pic_r.width):
        pic_rArray[i][j]=pic_rArray[i][j]&(2**6-1)
        m = m + 1
        sys.stdout.write(("\r当前完成 :{0}/"+str(size)).format(m))
        sys.stdout.flush()
pic_r = Image.fromarray(pic_rArray)
pic_r = pic_r.convert("RGB")
pic_r.show()



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