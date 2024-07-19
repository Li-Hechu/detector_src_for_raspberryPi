#-*-coding:gbk-*-

"""
����˵���ĵ�����
"""

from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import *
import gl

__all__ = ["IntroductionWindow"]

class IntroductionWindow:
    """
    ���ʹ��˵������
    """
    def __init__(self,rootwinow):
        #˵���ĵ�·��
        self.intropath = "intro.txt"
        #��ȡ����˵���ĵ�����
        self.textdata = []
        
        #�������㴰��
        self.win = Toplevel(rootwinow)
        self.win.title(gl.IntroWindowName)          #��������
        self.win.geometry(gl.IntroWindowSize)       #���ڴ�С
        self.win.resizable(False,False)             #���ڴ�С�Ƿ���Ըı�

        #�����ı���
        self.text = ScrolledText(self.win)
        self.text.pack(side="top",anchor="center",fill="both")

        #������ť
        self.btn = Button(self.win,text="ȷ��",command=self.__destroy)
        self.btn.pack(side="top",anchor="center")

        #��ȡ�ļ�����
        self.__loadtext()

        #д���ı���
        for line in self.textdata:
            self.text.insert("end",line)
        
        #�ı䴰�ڴ�״̬
        gl.IntroWindowOpened = True
        
        #�󶨹رմ����¼�
        self.win.protocol("WM_DELETE_WINDOW",self.__introwindowclosed)

    def __loadtext(self):
        """
        ��ȡ��������
        """
        with open(self.intropath,"r",encoding="utf8") as f:
            self.textdata = f.readlines()

    def __destroy(self):
        """
        ���ٴ���
        """
        gl.IntroWindowOpened = False
        self.win.destroy()
        
    def __introwindowclosed(self):
        """
        �����ڴ�״̬����Ϊ�ر�
        """
        gl.IntroWindowOpened = False
