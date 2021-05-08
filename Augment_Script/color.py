import cv2
import math
import numpy as np
import os
import glob
import argparse

parser = argparse.ArgumentParser(description='Color Data Augment')
parser.add_argument('--img_dir', type=str, default="E:/test/mirror", help='original images path')
parser.add_argument('--img_write_dir', type=str, default="E:/test/mixup2", help='processed images')
args = parser.parse_args()

def getColorImg(alpha,beta,img_path,img_write_path):
    img = cv2.imread(img_path)
    colored_img = np.uint8(np.clip((alpha * img + beta), 0, 255))
    cv2.imwrite(img_write_path,colored_img)

def color(alpha,beta,img_dir,img_write_dir):
    if not os.path.exists(img_write_dir):
        os.makedirs(img_write_dir)

    img_names=os.listdir(img_dir)
    for img_name in img_names:
        img_path=os.path.join(img_dir,img_name)
        img_write_path=os.path.join(img_write_dir,img_name[:-4]+'color'+str(int(alpha*10))+'.jpg')
        getColorImg(alpha,beta,img_path,img_write_path)

alphas=[1.1,1.0]   #对比度调整
beta=10     #亮度调整

for alpha in alphas:
    color(alpha,beta,args.img_dir,args.img_write_dir)