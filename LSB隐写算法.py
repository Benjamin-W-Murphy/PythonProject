import numpy
import numpy as np
from PIL import Image
import random
import os

#LSB算法原理
#载体初始化函数
def carry():
    filelist=os.listdir(".\data\carry")
    for i in range(0, len(filelist)):
        Width=Image.open(".\data\carry\\"+filelist[i]).width
        Height=Image.open(".\data\carry\\"+filelist[i]).height
        print(str(i)+"."+filelist[i]+" "+str(Width)+"*"+str(Height)+"\n")
    number=int(input("请选择密文载体图像(输入序号)："))
    return Image.open(".\data\carry\\"+filelist[number])
#密文初始化函数
def creatCiphertext():
    print("支持的密文类型：1.图像 2.文本")
    number=input("请选择密文类型：")
    if number=="1":
        filelist=os.listdir(".\data\ciphertext\pic")
        for i in range(0, len(filelist)):
            print(str(i) + "." + filelist[i] + "\n")
        number = int(input("请选择密文图像(输入序号)："))
        imgCiphertext=Image.open(".\data\ciphertext\pic\\"+filelist[number])
        imgCiphertext=imgCiphertext.convert("L")
        Ctext=numpy.array(imgCiphertext)
    elif number=="2":
        print("文本密文输入方式：1.手动输入 2.记事本输入")
        num=input("请选择文本输入方式：")
        if num=="1":
            Ctext=input("请输入密文：")
            Ctext=Ctext.split()
        elif num=="2":
            print("可选择的密文文件如下：")
            filelist=os.listdir(".\data\ciphertext")
            for i in range(0, len(filelist)):
                print(str(i) + "." + filelist[i] + "\n")
            number=int(input("请选择密文文本(输入序号)："))
            file=open(".\data\ciphertext\\"+filelist[number])
            Ctext=""
            Clist=[]
            for word in file.read():
                word=word.strip("\n")
                Clist.append(word)
            Ctext="".join(word for word in Clist if word.isalnum())
            Ctext=list(Ctext)
    return Ctext
#颜色通道选择函数
def choiceColor(img,RGB):
    r,g,b=img.split()
    if RGB=="r":
        return r
    elif RGB=="g":
        return g
    elif RGB=="b":
        return b
#载体图像还原函数
def reColor(img,NewImg,RGB):
    r,g,b=img.split()
    if RGB=="r":
        return Image.merge("RGB",(NewImg,g,b))
    elif RGB=="g":
        return Image.merge("RGB",(r,NewImg,b))
    elif RGB=="b":
        return Image.merge("RGB",(r,g,NewImg))

#密钥生成函数
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

#提取隐写内容
def getCtext(CarrayImg,newManger,RGB,x,y,width,height):
    desImg=CarrayImg.crop((x,y,x+width,y+height))
    cImg=newManger.crop((x,y,x+width,y+height))

    r1,g1,b1=desImg.split()
    r2,g2,b2=cImg.split()

    if RGB=="r":
        r1=np.array(r1)
        r2=np.array(r2)
        for i in range(0,desImg.height):
            for j in range(0,desImg.width):
                r1[i][j]=r1[i][j]|r2[i][j]
        return r1
    elif RGB=="g":
        g1 = np.array(g1)
        g2 = np.array(g2)
        for i in range(0,desImg.height):
            for j in range(0,desImg.width):
                g1[i][j]=g1[i][j]|g2[i][j]
        return g1
    elif RGB=="b":
        b1 = np.array(b1)
        b2 = np.array(b2)
        for i in range(0,desImg.height):
            for j in range(0,desImg.width):
                b1[i][j]=b1[i][j]|b2[i][j]
        return b1

#初始化相关参数
x=0
y=0
width=0
height=0

#初始化一个信息载体
CarrayImg = carry()
print(CarrayImg)
#将载体进行RGB分离，并选中其中一个颜色通道
RGB=input("输入要选择的颜色通道(r,g,b):")
imgSplit=choiceColor(CarrayImg,RGB)
imgGrew=imgSplit.convert("L")
#将选中的颜色通道取灰度图像后进行矩阵化
imgArray=np.array(imgGrew)
print(type(imgArray))
print(imgArray.size)
#初始化密文
Ctext=creatCiphertext()
if isinstance(Ctext, list) == True:
    for i in range(0,len(Ctext)):
        Ctext[i]=ord(Ctext[i])
print(Ctext)
#print(Ctext)
#初始化密钥
#x,y,width,height=creatKey(CarrayImg,Ctext,x,y,width,height)
lenght = CarrayImg.width * CarrayImg.height
if lenght > len(Ctext):
    if isinstance(Ctext, list) == True:
        max_x = int(CarrayImg.width / 2)
        max_y = int(CarrayImg.height / 2)
        x = random.randint(0, int(max_x))
        y = random.randint(0, int(max_y))
        max_w = CarrayImg.width - x
        max_h = CarrayImg.height - y
        while (width * height) < len(Ctext):
            width = random.randint(int(max_x), int(max_w))
            height_stary = int(width / 2)
            height = random.randint(1, int(max_h))
    elif isinstance(Ctext, numpy.ndarray) == True:
        Cimg=Image.fromarray(Ctext)
        x = random.randint(0, int(CarrayImg.width - Cimg.width))
        y = random.randint(0, int(CarrayImg.height - Cimg.height))
        width = Cimg.width
        height = Cimg.height
elif (lenght == len(Ctext)):
    x = 0
    y = 0
    width = CarrayImg.width
    height = CarrayImg.height

print("隐写位置起始坐标:("+str(x)+","+str(y)+")")
print("隐写区域长度:"+str(width)+" 隐写区域宽度:"+str(height))
print("隐写面积:"+str(width*height))
#信息隐写
n=0
m=0
if isinstance(Ctext, list) == True:
    for i in range(y,y+height):
        for j in range(x,x+width):
            imgArray[i][j]=imgArray[i][j]|int(Ctext[n])
            n=n+1
            if n >= len(Ctext):
                break
        if n >= len(Ctext):
            break
elif isinstance(Ctext, numpy.ndarray) == True:
    for i in range(y,y+height):
        for j in range(x,x+width):
            imgArray[i][j]= imgArray[i][j]|Ctext[i-y][j-x]

#写入结果展示
newImg=Image.fromarray(imgArray)
newImg.show()
for i in range(y, y + height):
    for j in range(x, x + width):
        print(imgArray[i][j])
#还原载体图像
newManger=reColor(CarrayImg,newImg,RGB)
newManger.show()
#提取信息
massage=getCtext(CarrayImg,newManger,RGB,x,y,width,height)
if isinstance(Ctext, list) == True:
    massageList=[]
    for i in range(0,height):
        for j in range(0,width):
            massageList.append(chr(massage[i][j]))
    print(massageList)
elif isinstance(Ctext, numpy.ndarray) == True:
    massage=Image.fromarray(massage)
    print(massage)
    massage.show()
#message=newImg.crop((x,y,width,height))
#messageArray=np.array(message)
#print(messageArray)




