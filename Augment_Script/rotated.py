import cv2
import math
import numpy as np
import os
import glob

import argparse

parser = argparse.ArgumentParser(description='rotate Data Augment')
parser.add_argument('--img_dir', type=str, default="E:/test/mirror", help='original images path')
parser.add_argument('--img_write_dir', type=str, default="E:/test/mixup2", help='processed images')
args = parser.parse_args()

def getRotatedImg(Pi_angle,img_path,img_write_path):
    img = cv2.imread(img_path)
    rows, cols = img.shape[:2]
    a, b = cols / 2, rows / 2
    M = cv2.getRotationMatrix2D((a, b), angle, 1)
    rotated_img = cv2.warpAffine(img, M, (cols, rows))  # 旋转后的图像保持大小不变
    cv2.imwrite(img_write_path,rotated_img)
    return a,b

def rotate(angle,img_dir,img_write_dir):
    if not os.path.exists(img_write_dir):
        os.makedirs(img_write_dir)

    Pi_angle = -angle * math.pi / 180.0  # 弧度制，后面旋转坐标需要用到，注意负号！！！
    img_names=os.listdir(img_dir)
    for img_name in img_names:
        img_path=os.path.join(img_dir,img_name)
        img_write_path=os.path.join(img_write_dir,img_name[:-4]+'R'+str(angle)+'.jpg')
        a,b=getRotatedImg(Pi_angle,img_path,img_write_path)

angle=45  #旋转角度

rotate(angle,args.img_dir,args.img_write_dir)