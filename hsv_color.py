import os
import cv2
import codecs
import time
import numpy as np

ori_gt_lists = ['D:/MOT17-Det/train/MOT17-02/gt/gt.txt',
                'D:/MOT17-Det/train/MOT17-04/gt/gt.txt',
                'D:/MOT17-Det/train/MOT17-05/gt/gt.txt',
                'D:/MOT17-Det/train/MOT17-09/gt/gt.txt',
                'D:/MOT17-Det/train/MOT17-10/gt/gt.txt',
                'D:/MOT17-Det/train/MOT17-11/gt/gt.txt',
                'D:/MOT17-Det/train/MOT17-13/gt/gt.txt']

img_dir = 'D:/MOT17-Det/voc/JPEGImages/'
annotation_dir = 'D:/MOT17-Det/voc/Annotations/'
root = 'D:/MOT17-Det/voc/ImageSets/Main/'

fp_trainlist = open(root + 'train_list.txt', 'w')


def replace_char(string, char, index):
    string = list(string)
    string[index] = char
    return ''.join(string)


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


for each_dir in ori_gt_lists:

    start_time = time.time()

    fp = open(each_dir, 'r')
    userlines = fp.readlines()
    fp.close()

    # 寻找gt中的对应的最大frame
    # max_indx = 0
    # for line in userlines:
    #     e_fram = int(line.split(',')[0])
    #     if e_fram > max_index:
    #         max_index = e_fram
    # print(max_index)

    fram_list = []
    for line in userlines:
        e_fram = int(line.split(',')[0])
        fram_list.append(e_fram)
    max_index = max(fram_list)
    print(each_dir + 'max_index：', max_index)

    for i in range(1, max_index):
        clear_name = each_dir[-12:-10] + format(str(i), '0>6s')
        format_name = clear_name + '.jpg'
        detail_dir = img_dir + format_name
        img = cv2.imread(detail_dir)
        shape_img = img.shape
        height = shape_img[0]
        width = shape_img[1]
        depth = shape_img[2]

        gamma1 = np.random.uniform(0.5, 1.5)
        gamma2 = np.random.uniform(0.5, 1.5)
        gamma3 = np.random.uniform(0.5, 1.5)
        gamma4 = np.random.uniform(0.5, 1.5)
        img1 = gamma_transform_s(img, gamma1)
        img2 = gamma_transform_v(img, gamma2)
        img3 = gamma_transform_sv(img, gamma3, gamma4)

        format_name1 = replace_char(format_name, '1', 2)
        format_name2 = replace_char(format_name, '2', 2)
        format_name3 = replace_char(format_name, '3', 2)

        cv2.imwrite(img_dir + format_name1, img1)
        cv2.imwrite(img_dir + format_name2, img2)
        cv2.imwrite(img_dir + format_name3, img3)

        txt_name = format_name[:-4]
        txt_name1 = format_name1[:-4]
        txt_name2 = format_name2[:-4]
        txt_name3 = format_name3[:-4]

        # fp.writelines(txt_name + 'n')
        # fp.writelines(txt_name1 + 'n')
        # fp.writelines(txt_name2 + 'n')
        # fp.writelines(txt_name3 + 'n')

        xml_list = [txt_name, txt_name1, txt_name2, txt_name3]

        each_index = [num for num, x in enumerate(fram_list) if x == (i)]

        for xml_name in xml_list:
            fp_trainlist.writelines(xml_name + 'n')

            with codecs.open(annotation_dir + xml_name + '.xml', 'w') as xml:
                xml.write('<?xml version="1.0" encoding="UTF-8"?>n')
                xml.write('<annotation>n')
                xml.write('t<folder>' + 'voc' + '</folder>n')
                xml.write('t<filename>' + xml_name + '.jpg' + '</filename>n')
                # xml.write('t<path>' + path + "/" + info1 + '</path>n')
                xml.write('t<source>n')
                xml.write('tt<database> The MOT17-Det </database>n')
                xml.write('t</source>n')
                xml.write('t<size>n')
                xml.write('tt<width>' + str(width) + '</width>n')
                xml.write('tt<height>' + str(height) + '</height>n')
                xml.write('tt<depth>' + str(depth) + '</depth>n')
                xml.write('t</size>n')
                xml.write('tt<segmented>0</segmented>n')
                for j in range(len(each_index)):
                    num = each_index[j]

                    x1 = int(userlines[num].split(',')[2])
                    y1 = int(userlines[num].split(',')[3])
                    x2 = int(userlines[num].split(',')[4])
                    y2 = int(userlines[num].split(',')[5])

                    xml.write('t<object>n')
                    xml.write('tt<name>person</name>n')
                    xml.write('tt<pose>Unspecified</pose>n')
                    xml.write('tt<truncated>0</truncated>n')
                    xml.write('tt<difficult>0</difficult>n')
                    xml.write('tt<bndbox>n')
                    xml.write('ttt<xmin>' + str(x1) + '</xmin>n')
                    xml.write('ttt<ymin>' + str(y1) + '</ymin>n')
                    xml.write('ttt<xmax>' + str(x1 + x2) + '</xmax>n')
                    xml.write('ttt<ymax>' + str(y1 + y2) + '</ymax>n')
                    xml.write('tt</bndbox>n')
                    xml.write('t</object>n')

                xml.write('</annotation>')

    end_time = time.time()
    print('process {} cost time:{}s'.format(each_dir, (end_time - start_time)))
fp_trainlist.close()
print('succeed in processing all gt files')