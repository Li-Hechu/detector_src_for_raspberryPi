#-*- coding:gbk -*-
"""
本代码用于连接摄像头，拍照计算缝隙宽度
"""

from copy import deepcopy
import cv2 as cv
import numpy as np
import gl

__all__ = ["detect"]

def detect(picture):
    """
    图像检测函数
    """
    
    std = 0                     #标志物边长
    factor = 0                  #比例因子
    pixel_distance=0            #实际像素值
    distance = 0                #实际长度
    ok=False                    #是否检测成功
    img = deepcopy(picture)     #图片变量
    
    #获取宽度
    img_w = img.shape[1]
    #转换为hsv图片
    hsv = cv.cvtColor(img,cv.COLOR_BGR2HSV)
    #提取绿色部分
    grabout = cv.inRange(hsv,np.array([35, 50, 35]),np.array([77, 255, 255]))
    #提取轮廓
    contours, hierarchy = cv.findContours(grabout,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    #寻找轮廓最大值
    try:
        cnt = sorted(contours,key=cv.contourArea,reverse=True)[0]
    except IndexError:
        ok = False
        return [img,std,factor,pixel_distance,distance,ok]
    #为最大的轮廓绘制面积最小外接矩形
    rect = cv.minAreaRect(cnt)
    #获取参照物长和宽，由于为实际为正方形，考虑误差，认为边长像素为长宽平均值
    std = (rect[1][0] + rect[1][1]) / 2
    #获取像素宽度和实际宽度的换算值
    try:
        factor = gl.RealLength/std
    except ZeroDivisionError:
        ok = False
        return [img,std,factor,pixel_distance,distance,ok]

    #形态学操作
    image = cv.erode(img,np.ones((5,5),np.uint8),iterations=5)
    image = cv.dilate(image,np.ones((5,5),np.uint8),iterations=4)
    image = cv.cvtColor(image,cv.COLOR_BGR2HSV)
    #高斯模糊，省略掉不重要的细节
    blur = cv.GaussianBlur(image,(3,3),0)
    #提取黑色部分
    black = cv.inRange(blur,np.array([0,0,0]),np.array([160,255,46]))
    #提取轮廓
    b_contours, b_hierarchy = cv.findContours(black,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    #寻找黑色轮廓最大值
    try:
        b_cnt = sorted(b_contours,key=cv.contourArea,reverse=True)[0]
    except IndexError:
        ok = False
        return [img,std,factor,pixel_distance,distance,ok]
    #为最大轮廓绘制最小外接矩形
    b_rect = cv.minAreaRect(b_cnt)

    #将参照物画出，绘制最小外接矩形
    cv.drawContours(img,[np.int0(cv.boxPoints(rect))],-1,(0,255,0),2)
    #画出缝隙最小外接矩形
    cv.drawContours(img,[np.int0(cv.boxPoints(b_rect))],-1,(255,0,0),2)

    #获取缝隙外接矩形的宽
    pixel_distance = b_rect[1][1] if b_rect[1][0] > b_rect[1][1] else b_rect[1][0]

    #修正
    pixel_distance += 0.1409*pixel_distance - 0.2559*(rect[1][0]-rect[1][1]) + 10.8101*(b_rect[0][0]/img_w) + 0.2145*rect[1][0] - 30.9329
    
    #计算距离
    distance = pixel_distance * factor

    #检测是否成功标志位
    ok = True

    return [img,std,factor,pixel_distance,distance,ok]
