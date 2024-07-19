#-*-coding:gbk-*-

"""
创建说明文档窗口
"""

from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import *
import gl

__all__ = ["IntroductionWindow"]

class IntroductionWindow:
    """
    软件使用说明窗口
    """
    def __init__(self,rootwinow):
        #说明文档路径
        self.intropath = "intro.txt"
        #读取到的说明文档内容
        self.textdata = []
        
        #创建顶层窗口
        self.win = Toplevel(rootwinow)
        self.win.title(gl.IntroWindowName)          #窗口名称
        self.win.geometry(gl.IntroWindowSize)       #窗口大小
        self.win.resizable(False,False)             #窗口大小是否可以改变

        #创建文本域
        self.text = ScrolledText(self.win)
        self.text.pack(side="top",anchor="center",fill="both")

        #创建按钮
        self.btn = Button(self.win,text="确定",command=self.__destroy)
        self.btn.pack(side="top",anchor="center")

        #读取文件内容
        self.__loadtext()

        #写入文本域
        for line in self.textdata:
            self.text.insert("end",line)
        
        #改变窗口打开状态
        gl.IntroWindowOpened = True
        
        #绑定关闭窗口事件
        self.win.protocol("WM_DELETE_WINDOW",self.__introwindowclosed)

    def __loadtext(self):
        """
        读取介绍内容
        """
        with open(self.intropath,"r",encoding="utf8") as f:
            self.textdata = f.readlines()

    def __destroy(self):
        """
        销毁窗口
        """
        gl.IntroWindowOpened = False
        self.win.destroy()
        
    def __introwindowclosed(self):
        """
        将窗口打开状态设置为关闭
        """
        gl.IntroWindowOpened = False
