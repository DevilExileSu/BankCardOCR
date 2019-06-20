import os
import numpy as np 
from os import getcwd
import cv2
import PIL.Image
import random
import copy
import multiprocessing


PATH = 'train_img/'


def rand(a=0, b=1):
    return np.random.rand()*(b-a) + a

def rand_resize(img,img_name,count,annotation,jitter=.3):
    # img = cv2.imread(PATH + img_name,-1)
    w,h,_ = img.shape
    new_ar = w/h * rand(1-jitter,1+jitter)/rand(1-jitter,1+jitter)
    scale = rand(.25,2)
    if new_ar < 1:
        nh = int(scale*h)
        nw = int(nh*new_ar)
    else:
        nw = int(scale*w)
        nh = int(nw/new_ar)
    new_name = img_name[:6] + str(count) + '.png'
    count = count+1
    annotation[PATH + new_name] = annotation[PATH + img_name]
    new_img = cv2.resize(img,(nh,nw),cv2.INTER_CUBIC)
    cv2.imwrite(PATH + new_name ,new_img)
    return count

def place_img(img,img_name,count,annotation):
    # img = cv2.imread(PATH + img_name,-1)
    H,W,C = img.shape
    offestH = int(rand(int(H*0.1),int(H*0.2)))
    offestW = int(rand(int(W*0.015),int(W*0.02)))
    dst = np.zeros((H,W,C),np.uint8)
    dst1 = np.zeros((H,W,C),np.uint8)
    dst2 = np.zeros((H,W,C),np.uint8)
    dst3 = np.zeros((H,W,C),np.uint8)
    
    for i in range(H - offestH):
        for j in range(W - offestW):
                dst[i + offestH,j + offestW] = img[i,j]
                dst1[i,j] = img[i + offestH,j + offestW]
                dst2[i + offestH,j] = img[i,j + offestW]
                dst3[i,j+offestW] = img[i+offestH,j]
    
    new_name = img_name[:6] + str(count) + '.png'
    count += 1
    new_name1 = img_name[:6] + str(count) + '.png'
    count += 1
    new_name2 = img_name[:6] + str(count) + '.png'
    count += 1
    new_name3 = img_name[:6] + str(count) + '.png'
    count += 1

    cv2.imwrite(PATH + new_name,dst)
    cv2.imwrite(PATH + new_name1,dst1)
    cv2.imwrite(PATH + new_name2,dst2)
    cv2.imwrite(PATH + new_name3,dst3)


    annotation[PATH + new_name] = annotation[PATH + img_name]
    annotation[PATH + new_name1] = annotation[PATH + img_name]
    annotation[PATH + new_name2] = annotation[PATH + img_name]
    annotation[PATH + new_name3] = annotation[PATH + img_name]
    return count


def colormap(img,img_name,count,annotation):
    rand_b = rand() + 1
    rand_g = rand() + 1
    rand_r = rand() + 1
    H,W,C = img.shape
    new_name = img_name[:6] + str(count) + '.png'
    count += 1
    dst = np.zeros((H,W,C),np.uint8)
    for i in range(H):
        for j in range(W):
            (b,g,r) = img[i,j]
            b = int(b * rand_b)
            g = int(g * rand_g)
            r = int(r * rand_r)
            if b > 255:
                b = 255
            if g > 255:
                g = 255
            if r > 255:
                r = 255
            dst[i][j] = (b,g,r)
    annotation[PATH + new_name] = annotation[PATH + img_name]
    cv2.imwrite(PATH + new_name,dst)
    return count

def blur(img,img_name,count,annotation):
    img_GaussianBlur = cv2.GaussianBlur(img,(5,5),0)
    img_Mean = cv2.blur(img,(5,5))
    img_Median = cv2.medianBlur(img,3)
    img_Bilater = cv2.bilateralFilter(img,5,100,100)    

    new_name = img_name[:6] + str(count) + '.png'
    count += 1
    new_name1 = img_name[:6] + str(count) + '.png'
    count += 1
    new_name2 = img_name[:6] + str(count) + '.png'
    count += 1
    new_name3 = img_name[:6] + str(count) + '.png'
    count += 1

    annotation[PATH + new_name] = annotation[PATH + img_name]
    annotation[PATH + new_name1] = annotation[PATH + img_name]
    annotation[PATH + new_name2] = annotation[PATH + img_name]
    annotation[PATH + new_name3] = annotation[PATH + img_name]    

    cv2.imwrite(PATH + new_name,img_GaussianBlur)
    cv2.imwrite(PATH + new_name1,img_Mean)
    cv2.imwrite(PATH + new_name2,img_Median)
    cv2.imwrite(PATH + new_name3,img_Bilater)
    return count

def noise(img,img_name,count,annotation):
    H,W,C= img.shape
    noise_img = np.zeros((H,W,C),np.uint8)

    for i in range(H):
        for j in range(W):
            noise_img[i,j] = img[i,j]

    for i in range(500):
        x = np.random.randint(H)
        y = np.random.randint(W)
        noise_img[x,y,:] = 255

    new_name = img_name[:6] + str(count) + '.png'
    count += 1
    annotation[PATH + new_name] = annotation[PATH + img_name]
    cv2.imwrite(PATH + new_name,noise_img)
    return count
  
def concat(img,img_name,count,annotation,img_list):
    # img = cv2.imread(PATH+img_name)
    H,W,C = img.shape
    num = int(rand(4,6))
    imgs = random.sample(img_list,num)
    dst = np.zeros((H,W*(num+1),C),np.uint8)
    for h in range(H):
        for w in range(W):
            dst[h,w] = img[h,w]

    new_name = img_name[:6] + str(count) + '.png'
    count += 1
    
    boxes = copy.copy(annotation[PATH + img_name])

    for i,image_name in enumerate(imgs):
        image = cv2.imread(PATH + image_name)
        for h in range(H):
            for w in range(W):
                dst[h,W*(i+1)+w] = image[h,w]
        for label in annotation[PATH + image_name]:
            boxes.append(label)
    
    cv2.imwrite(PATH + new_name,dst)
    annotation[PATH + new_name] = boxes


    count = noise(dst,new_name,count,annotation) #1
    count = noise(dst,new_name,count,annotation)
    for i in range(4):
        count = rand_resize(dst,new_name,count,annotation) #4
    count = colormap(dst,new_name,count,annotation) #1
    count = blur(dst,new_name,count,annotation) #4
    count = place_img(dst,new_name,count,annotation) #4

    return count


def main(img,img_name,annotation):
    count = 1
    for i in range(5):
        count = concat(img,img_name,count,annotation,img_list) #1
        
    print(img_name + "增强完成")


if __name__ == '__main__':
    trainval_percent = 0.2
    train_percent = 0.8
    # annotation = {}
    img_list = os.listdir(PATH)

    manager = multiprocessing.Manager()
    annotation = manager.dict()
    
    for img_name in img_list:
        boxes = []
        a = np.linspace(0,120,5,dtype=np.int)
        for i in range(len(a)-1):
            if img_name[i] == '_':
                continue
            boxes.append(img_name[i])
        annotation[PATH + img_name] = boxes

    pool = multiprocessing.Pool(10)
    for img_name in img_list:
        img = cv2.imread(PATH + img_name ,-1)
        pool.apply_async(main,(img,img_name,annotation,))
        

    pool.close()
    pool.join()
    
    train_file = open('train.txt','w')
    val_file = open('val.txt','w')
    val_split = 0.1
    rand_index = list(range(len(annotation)))
    random.shuffle(rand_index) 
    val_index = rand_index[0 : int(0.1 * len(annotation))]

    for i,names in enumerate(annotation.keys()):
        if i in val_index:
            val_file.write(names)
            for label in annotation[names]:
                val_file.write(" " + str(label))
            val_file.write('\n')
        else:
            train_file.write(names)
            for label in annotation[names]:
                train_file.write(" " + str(label))
            train_file.write('\n')

    train_file.close() 
    val_file.close()
