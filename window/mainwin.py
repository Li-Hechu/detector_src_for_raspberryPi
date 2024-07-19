#-*-coding:gbk-*-

"""
���������ڴ�����GUI����
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
    ����ͼ�λ�����
    """
    def __init__(self):
        #ʵ������
        self.mode = gl.Mode_Cap                 #ϵͳ����ģʽ
        self.frame = None                       #��ʾ��ͼƬ����,cv2.Mat��
        self.whichbtn = gl.ClickNone            #�������һ����ť,��"detect"��"image"��"none"����
        self.detectok = False                   #�Ƿ���ɹ�
        
        self.std = 0                            #������߳�����
        self.factor = 0                         #��������
        self.real_pixel = 0                     #��϶ʵ������ֵ
        self.width = 0                          #��϶ʵ�ʿ��

        #��������
        self.win = Tk()
        self.win.geometry(gl.MainWindowSize)    #���ô��ڴ�С
        self.win.title(gl.MainWindowName)        #��������
        self.win.resizable(False,False)           #���ڴ�С�Ƿ���Ըı�

        #��������
        self.top_frame = Frame(self.win,width=700,height=380,relief="sunken")
        self.top_frame.pack(fill="x",anchor="center",side="top")
        self.bottom_frame = Frame(self.win,width=700,height=100,relief="sunken")
        self.bottom_frame.pack(fill="both",anchor="center",side="top")
        
        #��ť�����ͽ����ʾ����
        self.buttonframe = Frame(self.bottom_frame,width=350,height=100,relief="sunken")
        self.buttonframe.pack(side="left",anchor="center")
        self.infoframe = Frame(self.bottom_frame,relief="sunken")
        self.infoframe.pack(side="left",fill="both",anchor="center")

        #�˵���
        self.menubar = Menu(self.win)
        #�ļ�
        self.filemenu = Menu(self.menubar,tearoff=0)
        self.filemenu.add_command(label="��������ͷ",command=self.__opencamera)
        self.filemenu.add_command(label="����ͼƬ",command=self.__savepicture)
        self.menubar.add_cascade(label="�ļ�",menu=self.filemenu) #�ڲ˵������롰�ļ���
        #˵��
        self.menubar.add_command(label="˵��",command=self.__introduction)
        #�˳�
        self.menubar.add_command(label="�˳�",command=self.__quit)
        #���ò˵���
        self.win.config(menu=self.menubar)

        #����
        self.canvas = Canvas(self.top_frame,width=700,height=380)
        self.canvas.pack(fill="both")

        #��ť
        self.detectBtn = Button(self.buttonframe,text="���",command=self.__toModeDet)
        self.imageBtn = Button(self.buttonframe,text="��̬ͼ��",command=self.__toModeCap)
        self.detectBtn.pack(side="left",anchor="center")
        self.imageBtn.pack(side="left",anchor="center")

        #�ı���
        self.textinfo = Text(self.infoframe)
        self.textinfo.pack(fill="both",side="left",anchor="center")

        #��ʾͼƬ�߳�
        self.imgrabthread = Thread(target=self.showimage)
        #�ػ��̣߳����߳̽��������߳���֮����
        self.imgrabthread.setDaemon(True)
        #�߳̿�ʼ
        self.imgrabthread.start()
        
        self.win.update()
        #��ʾ����
        self.win.mainloop()

    def __opencamera(self):
        """
        ��������ͷ
        """
        if gl.CapLinked == True:
            return
        
        #������ͷ
        gl.Capture = cv.VideoCapture(0)
        #����Ƿ��
        if gl.Capture.isOpened():
            showinfo("��ʾ","����ͷ�Ѿ���")
            gl.CapLinked = True
            gl.Capture.set(cv.CAP_PROP_FRAME_WIDTH,640)
            gl.Capture.set(cv.CAP_PROP_FRAME_HEIGHT,480)
        else:
            showwarning("����","δ��������ͷ�������Ӻ�����")
            gl.CapLinked = False

    def __savepicture(self):
        """
        ����ͼƬ
        """
        #��ȡ�ļ�·��
        path = asksaveasfilename(title="ͼƬ���Ϊ",initialdir=".\\saved",initialfile="figure",\
            filetypes=[("JPEG�ļ�","*.jpg"),("PNG�ļ�","*.png")],defaultextension=".*")
        if path == "":
            return
        #����ͼƬ
        cv.imwrite(path,self.frame)

    def __introduction(self):
        """
        ʹ��˵��
        """
        if gl.IntroWindowOpened == False:
            IntroductionWindow(self.win)
        else:
            pass

    def __quit(self):
        """
        �˳�����
        """
        state = askyesno("�˳�����","�Ƿ��˳�����")
        if state:
            exit(0)
        else:
            pass

    def __toModeDet(self):
        """
        ����ǰ״̬ת��Ϊ���״̬
        """
        self.whichbtn = gl.ClickDetectBtn

    def __toModeCap(self):
        """
        ����ǰ״̬ת��Ϊ��ʾ��̬ͼ��״̬
        """
        self.whichbtn = gl.ClickImageBtn
        
    def showimage(self):
        """
        ��ʾͼƬ
        """
        while True:     #��ѭ��
            #�����������ͷ
            if gl.CapLinked:
                #����Ƕ�̬��ʾģʽ
                if self.mode == gl.Mode_Cap:
                    #��ȡ��ǰ����
                    ret, self.frame = gl.Capture.read()
                #��������ⰴť
                if self.whichbtn == gl.ClickDetectBtn:
                    #���µ����ť��־λ
                    self.whichbtn = gl.ClickNone
                    #�����ظ����
                    if self.mode != gl.Mode_Det:
                        #״̬ת��
                        self.mode = gl.Mode_Det
                        #��⣬�������ֵ
                        self.frame,self.std,self.factor,self.real_pixel,self.width,self.detectok = detect(self.frame)
                        #����ı���
                        self.textinfo.delete("1.0",END)
                        #������Ϣ
                        if self.detectok:
                            #��ʾ��Ϣ
                            self.textinfo.insert("end","������߳�Ϊ %.2f ������\n" % (self.std))
                            self.textinfo.insert("end","��������Ϊ: %.6f\n" % (self.factor))
                            self.textinfo.insert("end","��϶���Ϊ %.2f ������\n" % (self.real_pixel))
                            self.textinfo.insert("end","��϶ʵ�ʾ���Ϊ��%.2fmm\n" % (self.width))
                        else:
                            self.textinfo.insert("end","δ��⵽��Ч��־��ͷ�϶\n����ʵ�����\n")
                #��������̬ͼ��ť
                if self.whichbtn == gl.ClickImageBtn:
                    #���°�ť��־λ
                    self.whichbtn = gl.ClickNone
                    #����ı���
                    self.textinfo.delete("1.0",END)
                    #״̬ת��
                    self.mode = gl.Mode_Cap
                #ѭ����ʾ
                cam_imageTk = gl.cv2ImageTk(cv.resize(self.frame,(507,380)))   #��ȡͼƬ
                self.canvas.create_image(0,0,anchor="nw",image=cam_imageTk) #��ʾͼƬ
                #����obr�����Ʋ���Ҫ�������뽫ͼƬ��ֵ��ĳһ����������������ͼƬ��˸��ʾ������
                obr = cam_imageTk   #!!!!!!����Ҫ!!!!!!!!
            #���û����������ͷ
            else:
                pass