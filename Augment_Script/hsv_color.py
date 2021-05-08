import os
import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Mirror Data Augment')
parser.add_argument('--img_dir', type=str, default="E:/test/color", help='original images path')
parser.add_argument('--img_write_dir', type=str, default="E:/test/hsv/2", help='processed images')
args = parser.parse_args()

def gamma_transform_s(img, gamma):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    illum = hsv[..., 1] / 255.
    illum = np.power(illum, gamma)
    v = illum * 255.
    v[v > 255] = 255
    v[v < 0] = 0
    hsv[..., 1] = v.astype(np.uint8)
    img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return img

def gamma_transform_v(img, gamma):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    illum = hsv[..., 2] / 255.
    illum = np.power(illum, gamma)
    v = illum * 255.
    v[v > 255] = 255
    v[v < 0] = 0
    hsv[..., 2] = v.astype(np.uint8)
    img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return img

def gamma_transform_sv(img, gamma1, gamma2):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    illum = hsv[..., 2] / 255.
    illum = np.power(illum, gamma1)
    v = illum * 255.
    v[v > 255] = 255
    v[v < 0] = 0
    hsv[..., 2] = v.astype(np.uint8)

    illum = hsv[..., 1] / 255.
    illum = np.power(illum, gamma2)
    v = illum * 255.
    v[v > 255] = 255
    v[v < 0] = 0
    hsv[..., 1] = v.astype(np.uint8)
    img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return img

def gamma_transform(img_dir, img_write_dir):

    img_names=os.listdir(img_dir)
    for img_name in img_names:
        img_path=os.path.join(img_dir,img_name)
        s_img_write_dir=os.path.join(img_write_dir,img_name[:-4]+'HSV_s'+'.jpg')
        v_img_write_dir=os.path.join(img_write_dir,img_name[:-4]+'HSV_v'+'.jpg')
        sv_img_write_dir=os.path.join(img_write_dir,img_name[:-4]+'HSV_sv'+'.jpg')

        img = cv2.imread(img_path)

        img1 = gamma_transform_s(img, 1)
        img2 = gamma_transform_v(img, 2)
        img3 = gamma_transform_sv(img, 0.6, 0.8)

        cv2.imwrite(s_img_write_dir, img1)
        cv2.imwrite(v_img_write_dir, img2)
        cv2.imwrite(sv_img_write_dir, img3)

gamma_transform(args.img_dir,args.img_write_dir)
