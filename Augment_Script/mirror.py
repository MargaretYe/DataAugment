import cv2
import math
import numpy as np
import os
import glob
import argparse

parser = argparse.ArgumentParser(description='Mirror Data Augment')
parser.add_argument('--img_dir', type=str, default="E:/test/mirror", help='original images path')
parser.add_argument('--img_write_dir', type=str, default="E:/test/mixup2", help='processed images')
args = parser.parse_args()

def h_MirrorImg(img_path,img_write_path):
    img = cv2.imread(img_path)
    mirror_img = cv2.flip(img, 1)  #水平翻转
    cv2.imwrite(img_write_path,mirror_img)
def v_MirrorImg(img_path,img_write_path):
    img = cv2.imread(img_path)
    mirror_img = cv2.flip(img, 0)  # #垂直翻转
    cv2.imwrite(img_write_path,mirror_img)
def a_MirrorImg(img_path,img_write_path):
    img = cv2.imread(img_path)
    mirror_img = cv2.flip(img, -1)  #垂直水平翻轉
    cv2.imwrite(img_write_path,mirror_img)

def mirror(img_dir,img_write_dir):
    if not os.path.exists(img_write_dir):
        os.makedirs(img_write_dir)

    img_names=os.listdir(img_dir)
    for img_name in img_names:
        img_path=os.path.join(img_dir,img_name)
        h_img_write_path=os.path.join(img_write_dir,img_name[:-4]+'h'+'.jpg')

        v_img_write_path = os.path.join(img_write_dir, img_name[:-4] + 'v' + '.jpg')

        a_img_write_path = os.path.join(img_write_dir, img_name[:-4] + 'a' + '.jpg')

        h_MirrorImg(img_path,h_img_write_path)
        v_MirrorImg(img_path,v_img_write_path)
        a_MirrorImg(img_path, a_img_write_path)

mirror(args.img_dir,args.img_write_dir)
