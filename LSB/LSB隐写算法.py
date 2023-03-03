import math
import os
import random
import re

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
def reColor(img, newCarray, RGB):
    r, g, b = img.split()
    if RGB == "r":
        return Image.merge("RGB", (newCarray, g, b))
    elif RGB == "g":
        return Image.merge("RGB", (r, newCarray, b))
    elif RGB == "b":
        return Image.merge("RGB", (r, g, newCarray))

# 逐bit提取文本隐写内容
def getBit(img, width, height):
    ciphertext = ""
    for i in range(height):
        for j in range(width):
            ciphertext = ciphertext + "" + str(img[i][j] % 2)
    list = re.findall(r'.{8}', ciphertext)
    return list

# 提取文本隐写内容
def getCtext(newManger, RGB, x, y, width, height):
    cImg = newManger.crop((x, y, x + width, y + height))
    r, g, b = cImg.split()
    if RGB == "r":
        massage = ""
        r = r.convert("L")
        r = np.array(r)
        ciphertextList = getBit(r, width, height)
        # print(ciphertextList)
        for i in range(len(ciphertextList)):
            massage = massage + "" + str(chr(int(ciphertextList[i], 2)))
        return massage
    elif RGB == "g":
        massage = ""
        g = g.convert("L")
        g = np.array(g)
        ciphertextList = getBit(g, width, height)
        # print(ciphertextList)
        for i in range(len(ciphertextList)):
            massage = massage + "" + str(chr(int(ciphertextList[i], 2)))
        return massage
    elif RGB == "b":
        massage = ""
        b = b.convert("L")
        b = np.array(b)
        ciphertextList = getBit(b, width, height)
        # print(ciphertextList)
        for i in range(len(ciphertextList)):
            massage = massage + "" + str(chr(int(ciphertextList[i], 2)))
        return massage

# 获取隐写图像
def getCiphertextImg(newImage, RGB, x, y, width, height):
    ciphertextListimg = newImage.crop((x, y, x + width, y + height))
    r, g, b = ciphertextListimg.split()
    if RGB == "r":
        r = r.convert("L")
        rArray = np.array(r)
        massageArray = np.zeros((height, width))
        for i in range(0, height):
            for j in range(0, width):
                massageArray[i][j] = rArray[i][j] % 2
        return massageArray
    if RGB == "g":
        g = g.convert("L")
        gArray = np.array(g)
        massageArray = np.zeros((height, width))
        for i in range(height):
            for j in range(width):
                massageArray[i][j] = gArray[i][j] % 2
        return massageArray
    if RGB == "b":
        b = b.convert("L")
        bArray = np.array(b)
        massageArray = np.zeros((height, width))
        for i in range(0, height):
            for j in range(0, width):
                massageArray[i][j] = bArray[i][j] % 2
        return massageArray
#从txt中读取图片数据
def readfile(filename):
    with open(filename, 'r') as f:
        list1 = []
        for line in f.readlines():
            line_str = line.strip()
            for element in line_str:
                if element != " ":
                    list1.append(int(element))
    return list1

#计算隐写性能
#计算峰值信噪比
def psnr(img_1, img_2):
    img_1int = np.array(img_1)
    img_2int = np.array(img_2)
    mse = np.mean((img_1int / 1.0 - img_2int / 1.0) ** 2)
    if mse < 1.0e-10:
        return 100
    return 10 * math.log10(255.0 ** 2 / mse)
#计算图像密文错误率
def falseRate(img1,img2):
    img1_float = np.array(img1)
    img2_float = np.array(img2)
    return np.mean(abs(img1_float-img2_float))/256
#计算文本密文错误率
def wordsFP(oldMassageList,newmassage):
    newMassageList=list(newmassage)
    for i in range(0, len(newMassageList)):
        newMassageList[i] = ord(newMassageList[i])
    massageList=toBit(newMassageList)
    FR=0
    for i in range(len(newMassageList)):
        FR = FR+(int(massageList[i])-int(oldMassageList[i]))
    FR = '{:.2%}'.format(FR)
    return FR

#计算二值图分布
def towIndex(img):
    imgArray = np.array(img)
    imgSize = img.width*img.height
    b = 0
    w = 0
    for i in range(img.height):
        for j in range(img.width):
            if imgArray[i][j] == 255:
                w = w + 1
            elif imgArray[i][j] == 0:
                b = b + 1
    b = b/float(imgSize)
    w = w/float(imgSize)
    I = 0-(b*math.log2(b)+(w*math.log2(w)))
    I = '{:.2}'.format(I)
    print("图像信息量为："+str(I)+"dB")

# 初始化相关参数(x,y)隐写原点、(width,height)隐写区域大小
x = 0
y = 0
width = 0
height = 0

# 初始化一个信息载体
carrayImg = carry()
print("载体图像信息："+str(carrayImg))

# 将载体进行RGB分离，并选中其中一个颜色通道
RGB = input("输入要选择的颜色通道(r,g,b):")
imgSplit = choiceColor(carrayImg, RGB)
imgGrew = imgSplit.convert("L")

# 将选中的颜色通道取灰度图像后进行矩阵化
imgArray = np.array(imgGrew)

# 初始化文本型密文
ciphertext = creatCiphertext()
if isinstance(ciphertext, list):
    for i in range(0, len(ciphertext)):
        ciphertext[i] = ord(ciphertext[i])
    ciphertext = toBit(ciphertext)
    print(len(ciphertext))
elif isinstance(ciphertext, numpy.ndarray):
    np.savetxt(".\data\ciphertext.txt",ciphertext,fmt="%d")

# 初始化密钥
# x,y,width,height=creatKey(CarrayImg,Ctext,x,y,width,height)
#计算载体图像大小
lenght = carrayImg.width * carrayImg.height
#若隐写信息为文本
if isinstance(ciphertext, list):
    if lenght > len(ciphertext):
        if isinstance(ciphertext, list):
            max_x = int(carrayImg.width / 2)
            max_y = int(carrayImg.height / 2)
            x = random.randint(0, int(max_x))
            y = random.randint(0, int(max_y))
            max_w = carrayImg.width - x
            max_h = carrayImg.height - y
            while (width * height) < len(ciphertext):
                width = random.randint(1, int(max_w))
                height_stary = int(width / 2)
                height = int(len(ciphertext) / width)
    elif (lenght == len(ciphertext)):
        x = 0
        y = 0
        width = carrayImg.width
        height = carrayImg.height
#若隐写信息为图像
elif isinstance(ciphertext, numpy.ndarray):
    cImgWidth = Image.fromarray(ciphertext).width
    cImgHeight = Image.fromarray(ciphertext).height
    if lenght > (cImgWidth * cImgHeight):
        Cimg = Image.fromarray(ciphertext)
        x = random.randint(0, int(carrayImg.width - Cimg.width))
        y = random.randint(0, int(carrayImg.height - Cimg.height))
        width = Cimg.width
        height = Cimg.height
    elif (lenght == (cImgWidth * cImgHeight)):
        x = 0
        y = 0
        width = carrayImg.width
        height = carrayImg.height
#输出密钥
print("隐写位置原点坐标:(" + str(x) + "," + str(y) + ")")
print("隐写区域长度:" + str(width) + " 隐写区域宽度:" + str(height))
print("隐写面积:" + str(width * height)+"\n")
# 信息隐写
n = 0
m = 0
if isinstance(ciphertext, list):
    for i in range(y, y + height):
        for j in range(x, x + width):
            imgArray[i][j] = (imgArray[i][j] - (imgArray[i][j] % 2)) + int(ciphertext[n])
            n = n + 1
elif isinstance(ciphertext, numpy.ndarray):
    for i in range(y, y + height):
        for j in range(x, x + width):
            imgArray[i][j] = (imgArray[i][j] - (imgArray[i][j] % 2)) + int(ciphertext[i - y][j - x])

# 写入结果展示
print(imgArray)
newCarray = Image.fromarray(imgArray)
# newCarray.show()
# 写入结果二值图
bitArray = np.zeros((carrayImg.height,carrayImg.width))
for i in range(carrayImg.height):
    for j in range(carrayImg.width):
        if imgArray[i][j]%2==0:
            bitArray[i][j]=0
        elif imgArray[i][j]%2==1:
            bitArray[i][j]=255

bitArray = np.matrix(bitArray)
print(bitArray)
bitImage = Image.fromarray(bitArray)
plt.subplot(111)
plt.imshow(bitImage)
plt.axis()
plt.show()

# 还原载体图像
newImage = reColor(carrayImg, newCarray, RGB)
# newImage.show()

# 展示隐写性能
print("信息隐写成功！\n隐写性能如下：")
PSNR = psnr(carrayImg,newImage)
print("峰值信噪比 PSNR=%.1f dB"%(PSNR))

# 提取信息,使用密钥进行提取
if isinstance(ciphertext, list):
    massage = getCtext(newImage, RGB, x, y, width, height)
    # for i in range(len(ciphertextBit)):
    FR = wordsFP(ciphertext,massage)
    #格式化提取出的密文
    print("错误率 FalseRate=%s" % (FR))
    # print(type(massage))
    print("提取出的文本密文："+massage)

#密文图像提取（二值图）
elif isinstance(ciphertext, numpy.ndarray):
    massage = getCiphertextImg(newImage, RGB, x, y, width, height)
    # print("隐写图像尺寸："+str(massage.shape))
    massage = np.reshape(massage,(width,height))
    np.savetxt(".\data\cImg.txt",massage,fmt="%d")
    list_result = readfile(".\data\cImg.txt")
    # 测试的txt中，只有0和1，目标是把1显示为“白色”，0显示为“黑色”；
    # 所以将列表中的1替换为255，而0替换为0
    for i in range(0, len(list_result)):
        if list_result[i] == 1:
            list_result[i] = 255
        else:
            list_result[i] = 0
    # 再利用numpy将列表包装为数组
    array1 = np.array(list_result)
    # 进一步将array包装成矩阵
    data = np.matrix(array1)
    # 重新reshape一个矩阵为一个方阵
    data = np.reshape(data, (height, width))
    # 调用Image的formarray方法将矩阵数据转换为图像PIL类型的数据
    new_map = Image.fromarray(data)
    #提取原始图像做对比
    ciphertext = np.array(readfile(".\data\ciphertext.txt"))
    for i in range(0, len(ciphertext)):
        if ciphertext[i] == 1:
            ciphertext[i] = 255
        else:
            ciphertext[i] = 0
    ciphertext = np.matrix(ciphertext)
    ciphertext = np.reshape(ciphertext, (height,width))
    newciphertext = Image.fromarray(ciphertext)
    #输出错误率
    FR = falseRate(newciphertext, new_map)
    FR = '{:.2%}'.format(FR)
    print("错误率 FalseRate=%s" % (FR))
    towIndex(new_map)
    # 显示图像
    # new_map.show()