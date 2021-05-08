import cv2
import math
import numpy as np
import os
import glob
import json
import shutil
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree, Element

def getColorImg(alpha,beta,img_path,img_write_path):
    img = cv2.imread(img_path)
    colored_img = np.uint8(np.clip((alpha * img + beta), 0, 255))
    cv2.imwrite(img_write_path,colored_img)

# def getColorAnno(anno_path,anno_write_path):
#     tree = ET.parse(anno_path)
#     tree.write(anno_write_path)  # 保存修改后的XML文件

def color(alpha,beta,img_dir,img_write_dir,anno_write_dir):
    if not os.path.exists(img_write_dir):
        os.makedirs(img_write_dir)

    if not os.path.exists(anno_write_dir):
        os.makedirs(anno_write_dir)
    img_names=os.listdir(img_dir)
    for img_name in img_names:
        img_path=os.path.join(img_dir,img_name)
        img_write_path=os.path.join(img_write_dir,img_name[:-4]+'color'+str(int(alpha*10))+'.jpg')
        #
        # anno_path=os.path.join(anno_dir,img_name[:-4]+'.xml')
        # anno_write_path = os.path.join(anno_write_dir, img_name[:-4]+'color'+str(int(alpha*10))+'.xml')
        #
        getColorImg(alpha,beta,img_path,img_write_path)
        # getColorAnno(anno_path,anno_write_path)

alphas=[1.1,1.0]
beta=10
img_dir='E:\\test\\mirror'
anno_dir='Color'
img_write_dir='E:\\test\\color'
anno_write_dir='Color/color_Annotations'
for alpha in alphas:
    color(alpha,beta,img_dir,img_write_dir,anno_write_dir)