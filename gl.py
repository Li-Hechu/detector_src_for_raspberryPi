#-*-coding:gbk-*-

"""
�洢ȫ�ֱ���
"""

#��־��ʵ�ʿ��
RealLength = 5

#����������
MainWindowName = "ת�޻���϶���ϵͳ"
#�����ڴ�С��λ��
MainWindowSize = "700x480+50+40"

#ʹ��˵����������
IntroWindowName = "���ʹ��˵��"
#ʹ��˵�����ڴ�С
IntroWindowSize = "300x250+120+100"
#ʹ��˵�������Ƿ��
IntroWindowOpened = False

#ѵ����������������
TrainningWindowName = "����ѵ����"
#ѵ�����������ڴ�С
TrainningWindowSize = "500x350+500+250"
#ѵ�������������Ƿ��
TrainningWindowOpened = False

#����ͷʵʱ��ʾģʽ
Mode_Cap = "cap"
#��ʾ�����
Mode_Det = "det"

#����ˡ���⡱��ť
ClickDetectBtn = "detect"
#�����ͼ����ʾ����ť
ClickImageBtn = "image"
#û�е���κΰ�ť
ClickNone = "none"

#����ͷ����
Capture = None
#����ͷ�Ƿ��
CapLinked = False


imtk = 0    #ת��ͼƬȫ�ֱ���

from PIL import Image, ImageTk
import cv2 as cv

def cv2ImageTk(cvframe):
    """
    ��opencvͼƬת��ΪImageTk����
    """
    global imtk
    #����Image��
    img = Image.fromarray(cv.cvtColor(cvframe,cv.COLOR_BGR2RGB))  #!!!!��ʽת��,opencv��BGR��canvas��ʾΪRGB
    #��Image����ת��ΪImageTk����
    imtk = ImageTk.PhotoImage(image=img)
    #���أ�һ����ȫ�ֱ���
    return imtk
