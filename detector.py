#-*- coding:gbk -*-
"""
������������������ͷ�����ռ����϶���
"""

from copy import deepcopy
import cv2 as cv
import numpy as np
import gl

__all__ = ["detect"]

def detect(picture):
    """
    ͼ���⺯��
    """
    
    std = 0                     #��־��߳�
    factor = 0                  #��������
    pixel_distance=0            #ʵ������ֵ
    distance = 0                #ʵ�ʳ���
    ok=False                    #�Ƿ���ɹ�
    img = deepcopy(picture)     #ͼƬ����
    
    #��ȡ���
    img_w = img.shape[1]
    #ת��ΪhsvͼƬ
    hsv = cv.cvtColor(img,cv.COLOR_BGR2HSV)
    #��ȡ��ɫ����
    grabout = cv.inRange(hsv,np.array([35, 50, 35]),np.array([77, 255, 255]))
    #��ȡ����
    contours, hierarchy = cv.findContours(grabout,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    #Ѱ���������ֵ
    try:
        cnt = sorted(contours,key=cv.contourArea,reverse=True)[0]
    except IndexError:
        ok = False
        return [img,std,factor,pixel_distance,distance,ok]
    #Ϊ�����������������С��Ӿ���
    rect = cv.minAreaRect(cnt)
    #��ȡ�����ﳤ�Ϳ�����Ϊʵ��Ϊ�����Σ���������Ϊ�߳�����Ϊ����ƽ��ֵ
    std = (rect[1][0] + rect[1][1]) / 2
    #��ȡ���ؿ�Ⱥ�ʵ�ʿ�ȵĻ���ֵ
    try:
        factor = gl.RealLength/std
    except ZeroDivisionError:
        ok = False
        return [img,std,factor,pixel_distance,distance,ok]

    #��̬ѧ����
    image = cv.erode(img,np.ones((5,5),np.uint8),iterations=5)
    image = cv.dilate(image,np.ones((5,5),np.uint8),iterations=4)
    image = cv.cvtColor(image,cv.COLOR_BGR2HSV)
    #��˹ģ����ʡ�Ե�����Ҫ��ϸ��
    blur = cv.GaussianBlur(image,(3,3),0)
    #��ȡ��ɫ����
    black = cv.inRange(blur,np.array([0,0,0]),np.array([160,255,46]))
    #��ȡ����
    b_contours, b_hierarchy = cv.findContours(black,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    #Ѱ�Һ�ɫ�������ֵ
    try:
        b_cnt = sorted(b_contours,key=cv.contourArea,reverse=True)[0]
    except IndexError:
        ok = False
        return [img,std,factor,pixel_distance,distance,ok]
    #Ϊ�������������С��Ӿ���
    b_rect = cv.minAreaRect(b_cnt)

    #�������ﻭ����������С��Ӿ���
    cv.drawContours(img,[np.int0(cv.boxPoints(rect))],-1,(0,255,0),2)
    #������϶��С��Ӿ���
    cv.drawContours(img,[np.int0(cv.boxPoints(b_rect))],-1,(255,0,0),2)

    #��ȡ��϶��Ӿ��εĿ�
    pixel_distance = b_rect[1][1] if b_rect[1][0] > b_rect[1][1] else b_rect[1][0]

    #����
    pixel_distance += 0.1409*pixel_distance - 0.2559*(rect[1][0]-rect[1][1]) + 10.8101*(b_rect[0][0]/img_w) + 0.2145*rect[1][0] - 30.9329
    
    #�������
    distance = pixel_distance * factor

    #����Ƿ�ɹ���־λ
    ok = True

    return [img,std,factor,pixel_distance,distance,ok]
