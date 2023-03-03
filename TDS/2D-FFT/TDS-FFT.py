import cv2
import math
import re
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# 格式化bin()函数处理后的ascii码
def plus(string):
    return string.zfill(8)

# 将文本密文转化为bit流
def toBit(ciphertext):
    string = ""
    for i in range(len(ciphertext)):
        ciphertext[i] = ord(ciphertext[i])
    for i in range(len(ciphertext)):
        string = string + "" + plus(bin(ciphertext[i]).replace('0b', ''))
    list = re.findall(r'.{1}', string)
    return list

#判断width是否能再分
def dewidth(width):
    for i in range(2,9):
        if width%i!=0:
            return True
        else:
            return False

# 将文本密文转化为矩阵
def listToArray(ciphertextlist):
    integer = len(ciphertextlist)
    start = int(np.sqrt(integer))
    factor = integer / start
    while not is_integer(factor):
        start += 1
        factor = integer / start
    factor = int(factor)
    array = np.zeros((start,factor))
    n = 0
    for i in range(start):
        for j in range(factor):
            if ciphertextlist[n]=="0":
                array[i][j]=0
            elif ciphertextlist[n]=="1":
                array[i][j]=255
            n=n+1
    return array


def is_integer(number):
    if int(number) == number:
        return True
    else:
        return False

# 选择载体图片
def getCarray():
    imgList = os.listdir(".\data\carray")
    for i in range(len(imgList)):
        img = cv2.imread('.\data\carray\\'+imgList[i])
        width,height = img.shape[:2]
        print(str(i+1) + "." + imgList[i] + " " + str(width) + "*" + str(height) + "\n")
    number = int(input("请选择密文载体图像(输入序号)："))
    return str("D:\Study\Codes\PythonProject\TDS\\2D-FFT\data\carray\\" + imgList[number-1])

#选择隐写内容
def creatCiphertext():
    print("支持的密文类型：1.图像 2.文本")
    number = input("请选择密文类型：")
    if number == "1":
        #读取文件名
        filelist = os.listdir(".\data\ciphertext\pic")
        for i in range(1, len(filelist)+1):
            print(str(i) + "." + filelist[i-1] + "\n")
        number = int(input("请选择密文图像(输入序号)："))
        # 格式化图像地址
        path = "D:\Study\Codes\PythonProject\TDS\\2D-FFT\data\ciphertext\pic\\"+filelist[number-1]
        # 读取灰度图
        imgCiphertext = cv2.imread(path,0)
        # 将图像转化为数组
        ciphertext = np.array(imgCiphertext)
        # 将图像转化为bit流
        height, width = ciphertext.shape
        for i in range(height):
            for j in range(width):
                if ciphertext[i][j]>127:
                    ciphertext[i][j]=1
                else:
                    ciphertext[i][j]=0
    elif number == "2":
        print("文本密文输入方式：1.手动输入 2.记事本输入")
        num = input("请选择文本输入方式：")
        if num == "1":
            ciphertext = input("请输入密文：")
            ciphertext = re.findall(r'.{2}', ciphertext)
        elif num == "2":
            print("可选择的密文文件如下：")
            # 读取文件名
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
            ciphertextlist = toBit(list(ciphertext))
            ciphertext = listToArray(ciphertextlist)
    return ciphertext

#将信息隐写到傅里叶变换后的频带图中
def encrypt(carrayImg,ciphertext):
    height,width = ciphertext.shape
    cheight,cwidth = carrayImg.shape
    for i in range(height):
        for j in range(width):
            carrayImg[i][j]=carrayImg[i][j]+ciphertext[i][j]
    return carrayImg

#隐写性能计算，峰值信噪比
def psnr(carrayImg, newCarrayImg):
    # img_1int = np.array(img_1)
    # img_2int = np.array(img_2)
    mse = np.mean((carrayImg /1.0 - newCarrayImg ) ** 2)
    if mse < 1.0e-10:
        return 100
    return 10 * math.log10(255.0 ** 2 / mse)

#输出频带图
def showfrequencyband(imgArray):
    size = imgArray.shape
    Y = np.arange(0, size[0], 1)
    X = np.arange(0, size[1], 1)

    X, Y = np.meshgrid(X, Y)
    fig = plt.figure()
    ax = plt.axes(projection="3d")
    ax.plot_surface(X, Y, imgArray, cmap=cm.hot)
    plt.show()

path = getCarray()
img = cv2.imread(path,0)
ciphertext = creatCiphertext()
# 对密文进行傅里叶变换
cfft2 = np.fft.fft2(ciphertext)
cfft2img = 20*np.log(np.abs(cfft2))

#傅里叶变换
fft2 = np.fft.fft2(img)             #快速傅里叶变换得到频率分布
fftShift = np.fft.fftshift(fft2)    #将图像中的低频部分移动到图像中心
fftShiftimg = 20*np.log(np.abs(fftShift))  #将复数数组重新标定范围，设置频谱范围到[0-255]，设置为20
fft2img = 20*np.log(np.abs(fft2))
showfrequencyband(fft2img)

#将图像进行写入
cfftimg = encrypt(fft2img,cfft2img)

#逆傅里叶变换
icfft = np.fft.ifft2(cfftimg)
icffimg = 20*np.log(np.abs(icfft))


#作图

showfrequencyband(cfftimg)