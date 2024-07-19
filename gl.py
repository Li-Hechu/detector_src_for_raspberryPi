#-*-coding:gbk-*-

"""
存储全局变量
"""

#标志物实际宽度
RealLength = 5

#主窗口名称
MainWindowName = "转辙机缝隙检测系统"
#主窗口大小和位置
MainWindowSize = "700x480+50+40"

#使用说明窗口名称
IntroWindowName = "软件使用说明"
#使用说明窗口大小
IntroWindowSize = "300x250+120+100"
#使用说明窗口是否打开
IntroWindowOpened = False

#训练集制作窗口名称
TrainningWindowName = "制作训练集"
#训练集制作窗口大小
TrainningWindowSize = "500x350+500+250"
#训练集制作窗口是否打开
TrainningWindowOpened = False

#摄像头实时显示模式
Mode_Cap = "cap"
#显示检测结果
Mode_Det = "det"

#点击了“检测”按钮
ClickDetectBtn = "detect"
#点击“图像显示“按钮
ClickImageBtn = "image"
#没有点击任何按钮
ClickNone = "none"

#摄像头对象
Capture = None
#摄像头是否打开
CapLinked = False


imtk = 0    #转换图片全局变量

from PIL import Image, ImageTk
import cv2 as cv

def cv2ImageTk(cvframe):
    """
    将opencv图片转换为ImageTk对象
    """
    global imtk
    #创建Image类
    img = Image.fromarray(cv.cvtColor(cvframe,cv.COLOR_BGR2RGB))  #!!!!格式转换,opencv是BGR，canvas显示为RGB
    #将Image对象转换为ImageTk对象
    imtk = ImageTk.PhotoImage(image=img)
    #返回，一定是全局变量
    return imtk
