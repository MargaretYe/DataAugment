import os
import cv2
import numpy as np
import random
import argparse

parser = argparse.ArgumentParser(description='Noise Data Augment')
parser.add_argument('--img_dir', type=str, default="E:/test/mirror", help='original images path')
parser.add_argument('--img_write_dir', type=str, default="E:/test/mosaic/result", help='processed images')
args = parser.parse_args()

def sp_noise(noise_img, proportion):
    '''
    添加椒盐噪声
    '''
    height, width = noise_img.shape[0], noise_img.shape[1]
    num = int(height * width * proportion) #一个准备加入多少噪声小点
    for i in range(num):
        w = random.randint(0, width - 1)
        h = random.randint(0, height - 1)
        if random.randint(0, 1) == 0:
            noise_img[h, w] = 0
        else:
            noise_img[h, w] = 255
    return noise_img

def gaussian_noise(img, mean, sigma):
    '''
    添加高斯噪声
        img   :  原图
        mean  :  均值
        sigma :  标准差
    '''
    # 将图片灰度标准化
    img = img / 255
    # 产生高斯 noise
    noise = np.random.normal(mean, sigma, img.shape)
    # 将噪声和图片叠加
    gaussian_out = img + noise
    # 将超过 1 的置 1，低于 0 的置 0
    gaussian_out = np.clip(gaussian_out, 0, 1)
    # 将图片灰度范围的恢复为 0-255
    gaussian_out = np.uint8(gaussian_out*255)
    # 将噪声范围搞为 0-255
    # noise = np.uint8(noise*255)
    return gaussian_out       # 这里也会返回噪声，注意返回值

def random_noise(image,noise_num):
    '''
    添加随机噪点（实际上就是随机在图像上将像素点的灰度值变为255即白色）
    param image: 需要加噪的图片
    param noise_num: 添加的噪音点数目
    '''
    # 参数image：，noise_num：
    img_noise = image
    # cv2.imshow("src", img)
    rows, cols, chn = img_noise.shape
    # 加噪声
    for i in range(noise_num):
        x = np.random.randint(0, rows)#随机生成指定范围的整数
        y = np.random.randint(0, cols)
        img_noise[x, y, :] = 255
    return img_noise

def convert(img_dir, img_write_dir):
    for filename in os.listdir(img_dir):
        path = img_dir + "/" + filename
        print("doing... ", path)
        noise_img = cv2.imread(path)#读取图片
        # img_noise = gaussian_noise(noise_img, 0, 0.12) # 高斯噪声
        img_noise = sp_noise(noise_img,0.025)# 椒盐噪声
        # img_noise  = random_noise(noise_img,500)# 随机噪声
        cv2.imwrite(img_write_dir+'/'+filename,img_noise )

if __name__ == '__main__':
    convert(args.img_dir, args.img_write_dir)
