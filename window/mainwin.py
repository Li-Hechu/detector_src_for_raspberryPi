#-*-coding:gbk-*-

"""
本代码用于创建主GUI界面
"""

from tkinter import *
from tkinter.filedialog import asksaveasfilename
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import *
from tkinter.messagebox import *
import cv2 as cv
from threading import Thread
from window.introwin import IntroductionWindow

from detector import detect
import gl

__all__ = ["Window"]

class Window:
    """
    建立图形化界面
    """
    def __init__(self):
        #实例属性
        self.mode = gl.Mode_Cap                 #系统所处模式
        self.frame = None                       #显示的图片对象,cv2.Mat类
        self.whichbtn = gl.ClickNone            #点击了哪一个按钮,有"detect"和"image"和"none"三类
        self.detectok = False                   #是否检测成功
        
        self.std = 0                            #参照物边长像素
        self.factor = 0                         #比例因子
        self.real_pixel = 0                     #缝隙实际像素值
        self.width = 0                          #缝隙实际宽度

        #创建窗口
        self.win = Tk()
        self.win.geometry(gl.MainWindowSize)    #设置窗口大小
        self.win.title(gl.MainWindowName)        #窗口名称
        self.win.resizable(False,False)           #窗口大小是否可以改变

        #两个容器
        self.top_frame = Frame(self.win,width=700,height=380,relief="sunken")
        self.top_frame.pack(fill="x",anchor="center",side="top")
        self.bottom_frame = Frame(self.win,width=700,height=100,relief="sunken")
        self.bottom_frame.pack(fill="both",anchor="center",side="top")
        
        #按钮容器和结果显示容器
        self.buttonframe = Frame(self.bottom_frame,width=350,height=100,relief="sunken")
        self.buttonframe.pack(side="left",anchor="center")
        self.infoframe = Frame(self.bottom_frame,relief="sunken")
        self.infoframe.pack(side="left",fill="both",anchor="center")

        #菜单栏
        self.menubar = Menu(self.win)
        #文件
        self.filemenu = Menu(self.menubar,tearoff=0)
        self.filemenu.add_command(label="连接摄像头",command=self.__opencamera)
        self.filemenu.add_command(label="保存图片",command=self.__savepicture)
        self.menubar.add_cascade(label="文件",menu=self.filemenu) #在菜单栏加入“文件”
        #说明
        self.menubar.add_command(label="说明",command=self.__introduction)
        #退出
        self.menubar.add_command(label="退出",command=self.__quit)
        #配置菜单栏
        self.win.config(menu=self.menubar)

        #画布
        self.canvas = Canvas(self.top_frame,width=700,height=380)
        self.canvas.pack(fill="both")

        #按钮
        self.detectBtn = Button(self.buttonframe,text="检测",command=self.__toModeDet)
        self.imageBtn = Button(self.buttonframe,text="动态图像",command=self.__toModeCap)
        self.detectBtn.pack(side="left",anchor="center")
        self.imageBtn.pack(side="left",anchor="center")

        #文本框
        self.textinfo = Text(self.infoframe)
        self.textinfo.pack(fill="both",side="left",anchor="center")

        #显示图片线程
        self.imgrabthread = Thread(target=self.showimage)
        #守护线程，主线程结束，子线程随之结束
        self.imgrabthread.setDaemon(True)
        #线程开始
        self.imgrabthread.start()
        
        self.win.update()
        #显示窗口
        self.win.mainloop()

    def __opencamera(self):
        """
        连接摄像头
        """
        if gl.CapLinked == True:
            return
        
        #打开摄像头
        gl.Capture = cv.VideoCapture(0)
        #检测是否打开
        if gl.Capture.isOpened():
            showinfo("提示","摄像头已经打开")
            gl.CapLinked = True
            gl.Capture.set(cv.CAP_PROP_FRAME_WIDTH,640)
            gl.Capture.set(cv.CAP_PROP_FRAME_HEIGHT,480)
        else:
            showwarning("警告","未连接摄像头，请连接后重试")
            gl.CapLinked = False

    def __savepicture(self):
        """
        保存图片
        """
        #获取文件路径
        path = asksaveasfilename(title="图片另存为",initialdir=".\\saved",initialfile="figure",\
            filetypes=[("JPEG文件","*.jpg"),("PNG文件","*.png")],defaultextension=".*")
        if path == "":
            return
        #保存图片
        cv.imwrite(path,self.frame)

    def __introduction(self):
        """
        使用说明
        """
        if gl.IntroWindowOpened == False:
            IntroductionWindow(self.win)
        else:
            pass

    def __quit(self):
        """
        退出程序
        """
        state = askyesno("退出程序","是否退出程序？")
        if state:
            exit(0)
        else:
            pass

    def __toModeDet(self):
        """
        将当前状态转换为检测状态
        """
        self.whichbtn = gl.ClickDetectBtn

    def __toModeCap(self):
        """
        将当前状态转换为显示动态图像状态
        """
        self.whichbtn = gl.ClickImageBtn
        
    def showimage(self):
        """
        显示图片
        """
        while True:     #死循环
            #如果连接摄像头
            if gl.CapLinked:
                #如果是动态显示模式
                if self.mode == gl.Mode_Cap:
                    #读取当前画面
                    ret, self.frame = gl.Capture.read()
                #如果点击检测按钮
                if self.whichbtn == gl.ClickDetectBtn:
                    #更新点击按钮标志位
                    self.whichbtn = gl.ClickNone
                    #避免重复检测
                    if self.mode != gl.Mode_Det:
                        #状态转换
                        self.mode = gl.Mode_Det
                        #检测，解包返回值
                        self.frame,self.std,self.factor,self.real_pixel,self.width,self.detectok = detect(self.frame)
                        #清除文本域
                        self.textinfo.delete("1.0",END)
                        #插入信息
                        if self.detectok:
                            #显示信息
                            self.textinfo.insert("end","参照物边长为 %.2f 个像素\n" % (self.std))
                            self.textinfo.insert("end","比例因子为: %.6f\n" % (self.factor))
                            self.textinfo.insert("end","缝隙宽度为 %.2f 个像素\n" % (self.real_pixel))
                            self.textinfo.insert("end","缝隙实际距离为：%.2fmm\n" % (self.width))
                        else:
                            self.textinfo.insert("end","未检测到有效标志物和缝隙\n请检查实际情况\n")
                #如果点击动态图像按钮
                if self.whichbtn == gl.ClickImageBtn:
                    #更新按钮标志位
                    self.whichbtn = gl.ClickNone
                    #清除文本域
                    self.textinfo.delete("1.0",END)
                    #状态转换
                    self.mode = gl.Mode_Cap
                #循环显示
                cam_imageTk = gl.cv2ImageTk(cv.resize(self.frame,(507,380)))   #获取图片
                self.canvas.create_image(0,0,anchor="nw",image=cam_imageTk) #显示图片
                #变量obr的名称不重要，但必须将图片赋值给某一个变量，否则会出现图片闪烁显示的问题
                obr = cam_imageTk   #!!!!!!很重要!!!!!!!!
            #如果没有连接摄像头
            else:
                pass