import os
import random
import re

import numpy
import numpy as np
from PIL import Image


# LSB隐写算法
# 载体初始化函数
def carry():
    filelist = os.listdir(".\data\carry")
    for i in range(0, len(filelist)):
        Width = Image.open(".\data\carry\\" + filelist[i]).width
        Height = Image.open(".\data\carry\\" + filelist[i]).height
        print(str(i) + "." + filelist[i] + " " + str(Width) + "*" + str(Height) + "\n")
    number = int(input("请选择密文载体图像(输入序号)："))
    return Image.open(".\data\carry\\" + filelist[number])


# 格式化bin()函数处理后的ascii码
def plus(string):
    return string.zfill(8)


# 将文本密文转化为bit流
def toBit(Ctext):
    string = ""
    for i in range(len(Ctext)):
        string = string + "" + plus(bin(Ctext[i]).replace('0b', ''))
    list = re.findall(r'.{1}', string)
    return list


# def toNumber(value):
#     if value==True:
#         return 1
#     elif value==False:
#         return 0
# #二值化图像
# def toBitImg(Ctext,imgCiphertext):
#     for i in range(imgCiphertext.height):
#         for j in range(imgCiphertext.width):
#             Ctext[i][j]=toNumber(Ctext[i][j])
# 密文初始化函数
def creatCiphertext():
    print("支持的密文类型：1.图像 2.文本")
    number = input("请选择密文类型：")
    if number == "1":
        filelist = os.listdir(".\data\ciphertext\pic")
        for i in range(0, len(filelist)):
            print(str(i) + "." + filelist[i] + "\n")
        number = int(input("请选择密文图像(输入序号)："))
        imgCiphertext = Image.open(".\data\ciphertext\pic\\" + filelist[number])
        # 隐写图像二值化
        imgCiphertext = imgCiphertext.convert("1")
        Ctext = numpy.array(imgCiphertext)
    elif number == "2":
        print("文本密文输入方式：1.手动输入 2.记事本输入")
        num = input("请选择文本输入方式：")
        if num == "1":
            Ctext = input("请输入密文：")
            Ctext = re.findall(r'.{2}', Ctext)
        elif num == "2":
            print("可选择的密文文件如下：")
            filelist = os.listdir(".\data\ciphertext\words")
            for i in range(0, len(filelist)):
                print(str(i) + "." + filelist[i] + "\n")
            number = int(input("请选择密文文本(输入序号)："))
            file = open(".\data\ciphertext\words\\" + filelist[number])
            Ctext = ""
            Clist = []
            for word in file.read():
                word = word.strip("\n")
                Clist.append(word)
            Ctext = "".join(word for word in Clist if word.isalnum())
            Ctext = list(Ctext)
    return Ctext


# 颜色通道选择函数
def choiceColor(img, RGB):
    r, g, b = img.split()
    if RGB == "r":
        return r
    elif RGB == "g":
        return g
    elif RGB == "b":
        return b


# 载体图像还原函数
def reColor(img, NewImg, RGB):
    r, g, b = img.split()
    if RGB == "r":
        return Image.merge("RGB", (NewImg, g, b))
    elif RGB == "g":
        return Image.merge("RGB", (r, NewImg, b))
    elif RGB == "b":
        return Image.merge("RGB", (r, g, NewImg))


# 密钥生成函数
'''
def creatKey(CarrayImg,Ctext,x,y,width,height):
    lenght = CarrayImg.width * CarrayImg.height
    if lenght > len(Ctext):
        if isinstance(Ctext,list) == True:
            max_x=int(CarrayImg.width/2)
            max_y=int(CarrayImg.height/2)
            x = random.randint(0, int(max_x))
            y = random.randint(0, int(max_y))
            max_w=CarrayImg.width - x
            max_h=CarrayImg.height - y
            while (width * height) < len(Ctext):
                width = random.randint(int(max_x), int(max_w))
                height_stary=int(width/2)
                height = random.randint(height_stary, int(max_h))
        elif isinstance(Ctext,array) == True:
            x = random.randint(0, int(CarrayImg.width - Ctext.width))
            y = random.randint(0, int(CarrayImg.height - Ctext.height))
            width = Ctext.width
            height = Ctext.height
    elif (lenght == len(Ctext)):
        x = 0
        y = 0
        width = CarrayImg.width
        height = CarrayImg.height
    return x,y,width,height
'''


# 逐bit提取文本隐写内容
def getBit(cImg, width, height):
    Ctext = ""
    for i in range(height):
        for j in range(width):
            Ctext = Ctext + "" + str(cImg[i][j] % 2)
    list = re.findall(r'.{8}', Ctext)
    return list


# 提取文本隐写内容
def getCtext(newManger, RGB, x, y, width, height):
    cImg = newManger.crop((x, y, x + width, y + height))
    r, g, b = cImg.split()

    if RGB == "r":
        massage = ""
        r = r.convert("L")
        r = np.array(r)
        Clist = getBit(r, width, height)
        print(Clist)
        for i in range(len(Clist)):
            massage = massage + "" + str(chr(int(Clist[i], 2)))
        return massage
    elif RGB == "g":
        massage = ""
        g = g.convert("L")
        g = np.array(g)
        Clist = getBit(g, width, height)
        print(Clist)
        for i in range(len(Clist)):
            massage = massage + "" + str(chr(int(Clist[i], 2)))
        return massage
    elif RGB == "b":
        massage = ""
        b = b.convert("L")
        b = np.array(b)
        Clist = getBit(b, width, height)
        print(Clist)
        for i in range(len(Clist)):
            massage = massage + "" + str(chr(int(Clist[i], 2)))
        return massage


# 获取隐写图像
def getCimg(newManger, RGB, x, y, width, height):
    cImg = newManger.crop((x, y, x + width, y + height))
    r, g, b = cImg.split()
    if RGB == "r":
        r = r.convert("L")
        rArray = np.array(r)
        massageArray = np.zeros((width, height))
        for i in range(0, height):
            for j in range(0,width):
                # if(rArray[i][j]%2==1):
                #     massageArray[i][j]=0
                # elif(rArray[i][j]%2==0):
                #     massageArray[i][j]=255
                massageArray[i][j] = rArray[i][j] % 2
        return massageArray
    if RGB == "g":
        g = g.convert("L")
        gArray = np.array(g)
        massageArray = np.zeros((width, height))
        for i in range(0, height):
            for j in range(0, width):
                massageArray[i][j] = gArray[i][j] % 2
        return massageArray
    if RGB == "b":
        b = b.convert("L")
        bArray = np.array(b)
        massageArray = np.zeros((width, height))
        for i in range(0, height):
            for j in range(0, width):
                massageArray[i][j] = bArray[i][j] % 2
        return massageArray


# 初始化相关参数
x = 0
y = 0
width = 0
height = 0

# 初始化一个信息载体
CarrayImg = carry()
print(CarrayImg)
# 将载体进行RGB分离，并选中其中一个颜色通道
RGB = input("输入要选择的颜色通道(r,g,b):")
imgSplit = choiceColor(CarrayImg, RGB)
imgGrew = imgSplit.convert("L")
# 将选中的颜色通道取灰度图像后进行矩阵化
imgArray = np.array(imgGrew)
print(imgArray.shape)
# 初始化文本型密文
Ctext = creatCiphertext()
if isinstance(Ctext, list) == True:
    for i in range(0, len(Ctext)):
        Ctext[i] = ord(Ctext[i])
    print(Ctext)
    Ctext = toBit(Ctext)
    print(len(Ctext))
elif isinstance(Ctext, numpy.ndarray) == True:
    Image.fromarray(Ctext).show()
    print(type(Ctext))
# 初始化密钥
# x,y,width,height=creatKey(CarrayImg,Ctext,x,y,width,height)
lenght = CarrayImg.width * CarrayImg.height
if isinstance(Ctext, list) == True:
    if lenght > len(Ctext):
        if isinstance(Ctext, list) == True:
            max_x = int(CarrayImg.width / 2)
            max_y = int(CarrayImg.height / 2)
            x = random.randint(0, int(max_x))
            y = random.randint(0, int(max_y))
            max_w = CarrayImg.width - x
            max_h = CarrayImg.height - y
            while (width * height) < len(Ctext):
                width = random.randint(1, int(max_w))
                height_stary = int(width / 2)
                height = int(len(Ctext) / width)
        elif isinstance(Ctext, numpy.ndarray) == True:
            Cimg = Image.fromarray(Ctext)
            x = random.randint(0, int(CarrayImg.width - Cimg.width))
            y = random.randint(0, int(CarrayImg.height - Cimg.height))
            width = Cimg.width
            height = Cimg.height
    elif (lenght == len(Ctext)):
        x = 0
        y = 0
        width = CarrayImg.width
        height = CarrayImg.height
elif isinstance(Ctext, numpy.ndarray) == True:
    cImgWidth = Image.fromarray(Ctext).width
    cImgHeight = Image.fromarray(Ctext).height
    if lenght > (cImgWidth * cImgHeight):
        Cimg = Image.fromarray(Ctext)
        x = random.randint(0, int(CarrayImg.width - Cimg.width))
        y = random.randint(0, int(CarrayImg.height - Cimg.height))
        width = Cimg.width
        height = Cimg.height
    elif (lenght == (cImgWidth * cImgHeight)):
        x = 0
        y = 0
        width = CarrayImg.width
        height = CarrayImg.height

print("隐写位置起始坐标:(" + str(x) + "," + str(y) + ")")
print("隐写区域长度:" + str(width) + " 隐写区域宽度:" + str(height))
print("隐写面积:" + str(width * height))
# 信息隐写
n = 0
m = 0
if isinstance(Ctext, list) == True:
    for i in range(y, y + height):
        for j in range(x, x + width):
            imgArray[i][j] = (imgArray[i][j] - (imgArray[i][j] % 2)) + int(Ctext[n])
            n = n + 1
elif isinstance(Ctext, numpy.ndarray) == True:
    for i in range(y, y + height):
        for j in range(x, x + width):
            imgArray[i][j] = (imgArray[i][j] - (imgArray[i][j] % 2)) + int(Ctext[i - y][j - x])
# 写入结果展示
newImg = Image.fromarray(imgArray)
newImg.show()
# 还原载体图像
newManger = reColor(CarrayImg, newImg, RGB)
newManger.show()
# 提取信息
if isinstance(Ctext, list) == True:
    massage = getCtext(newManger, RGB, x, y, width, height)
    print(type(massage))
    print(massage)
elif isinstance(Ctext, numpy.ndarray) == True:
    massage = getCimg(newManger, RGB, x, y, width, height)
    np.savetxt(".\data\cImg.txt",massage,fmt="%d")
    massageImg = Image.fromarray(massage,mode="L")
    massageImg.show()
    print(massageImg)
    print(massage.shape)
