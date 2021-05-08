import cv2
import os
import random
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Mixup Data Augment')
parser.add_argument('--img_path', type=str, default="E:/test/mirror/", help='original images path')
parser.add_argument('--save_path', type=str, default="E:/test/mixup2/", help='mixup augmented images')
args = parser.parse_args()

img_names = os.listdir(args.img_path)
img_num = len(img_names)
print('img_num:', img_num)

for imgname in img_names:
    imgpath = args.img_path + imgname
    if not imgpath.endswith('jpg'):
        continue
    img = cv2.imread(imgpath)
    img_h, img_w = img.shape[0], img.shape[1]
    print(img_h,img_w)

    i = random.randint(0, img_num - 1)
    print('i:', i)
    add_path = args.img_path + img_names[i]
    addimg = cv2.imread(add_path)
    add_h, add_w = addimg.shape[0], addimg.shape[1]
    if add_h != img_h or add_w != img_w:
        print('resize!')
        addimg = cv2.resize(addimg, (img_w, img_h), interpolation=cv2.INTER_LINEAR)
    scale_h, scale_w = img_h / add_h, img_w / add_w

    lam = np.random.beta(1.0, 1.0)
    print(lam)
    mixed_img = lam * img + (1 - lam) * addimg
    save_img = args.save_path + imgname[:-4] + '_3.jpg'
    cv2.imwrite(save_img, mixed_img)
    print(save_img)

    print(imgname, img_names[i])
