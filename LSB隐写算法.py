import numpy as np
from PIL import Image
import random
#LSB算法原理
#初始化一个信息载体
img = Image.new("RGB",(320,480),(255,150,33))
#将载体进行RGB分离，并选中其中一个颜色通道
r,g,b=img.split()
width=r.width
height=r.height
r_grew=r.convert("L")
#将选中的颜色通道取灰度图像后进行矩阵化
rArray=np.array(r)
print(rArray)
print(rArray.size)
#写入信息并记录密钥，在此为（50，200）
for i in range(50,200):
    for j in range(50,200):
        rArray[i][j]=rArray[i][j]-50
#写入结果展示
newImg=Image.fromarray(rArray)
newImg.show()
#还原载体图像
#newManger=Image.merge("RGB",(r,g,b))
#newManger.show()
#提取信息
message=newImg.crop((50,50,150,150))
messageArray=np.array(message)
print(messageArray)




