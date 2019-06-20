import cv2
import numpy as np

class Image:
    HEIGHT = 550
    WIDTH = 350
    img = 0
    remove_back_img = 0
    number_area = 0
    def __init__(self,img):
        self.img = img
        H,W,_ = img.shape
        if H/W > 0.6 and H/W < 0.69:
            self.remove_back_img = cv2.resize(self.img,(self.HEIGHT,self.WIDTH))
        else:
            self.remove_back_img = self.removeBackground()

        self.number_area = self.position(self.remove_back_img)

        self.pos_img = self.getNumberArea()
        
    def getNumberArea(self):
        num_img = self.number_area
        h,w,_ = num_img.shape
        gray_img = cv2.cvtColor(num_img,cv2.COLOR_BGR2GRAY)
        dilate_img= self.embossment(gray_img)
        embo_img = cv2.medianBlur(dilate_img,3)
        _,thresh_img= cv2.threshold(embo_img,155,255,cv2.THRESH_BINARY)

        
        thresh_img = cv2.medianBlur(thresh_img,3)
        thresh_img = cv2.GaussianBlur(thresh_img,(3,3),0)
        thresh_img = cv2.dilate(thresh_img,None,iterations=10)

        _,thresh_img= cv2.threshold(thresh_img,220,255,cv2.THRESH_BINARY)
        a = np.zeros(w,np.uint8)
        for j in range(0,w): #计算水平方向上的黑色像素点数目，
            for i in range(0,h):
                if  thresh_img[i,j] == 0: 
                    a[j] += 1
        
        a = a[::-1]
        length = int(0.75 * w)
        min_ = sum(a)
        start = 0
        for i in range(len(a)):
            if a[i] < 15:
                a[i] = 0
            else:
                a[i] = 35
        for i in range(w - length):
            end = i + length 
            mean_ = a[i:end].mean()
            if(min_ > mean_ and i < 50):
                min_ = mean_
                start = i
        end = w - start 
        a = a[::-1]
        min_ = sum(a)
        start = 0
        for i in range(130):
            mean_ = a[i:end].mean()
            if min_ > mean_:
                min_ = mean_
                start = i
        # print(start,end)
        self.W_end = end + 20
        self.W_start = start + 25
        # cv2.imshow('aaa',num_img[:,start:end+10])
        return num_img[:,start+5:end]

    def removeBackground(self):
        resize_img = cv2.resize(self.img,(self.HEIGHT,self.WIDTH),0,0,cv2.INTER_NEAREST) #调整图片大小
        self.img = resize_img 
        gray_img = cv2.cvtColor(resize_img,cv2.COLOR_BGR2GRAY) #灰度处理
        blur_img = cv2.medianBlur(gray_img,9) #中值滤波去除噪声
        x = cv2.Sobel(blur_img,cv2.CV_32F,1,0,3) #Sobel边缘检测
        y = cv2.Sobel(blur_img,cv2.CV_32F,0,1,3)
        absX = cv2.convertScaleAbs(x)
        absY = cv2.convertScaleAbs(y)
        sobel_img = cv2.addWeighted(absX,0.5,absY,0.5,0)
        thresh_img = cv2.adaptiveThreshold(sobel_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,3,0) #自适应二值化
        cnts,_ = cv2.findContours(thresh_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #找到最大连通区域
        temp = 0
        W = 0
        H = 0
        X = 0
        Y = 0
        for i in range(0,len(cnts)):
            x,y,w,h = cv2.boundingRect(cnts[i])
            if(temp <w + h):    
                temp = w+h
                W = w
                H = h
                X = x
                Y = y  
        remove_back_img = resize_img[Y:Y+H,X:X+W]
        return cv2.resize(remove_back_img,(self.HEIGHT,self.WIDTH),cv2.INTER_NEAREST)


    def embossment(self,img):
        H,W = img.shape
        dst = np.zeros((H,W),np.uint8)
        for i in range(0,H):
            for j in range(0,W-1):
                grayP0 = int(img[i,j])
                grayP1 = int(img[i,j+1])
                newP = grayP0 - grayP1 + 150
                if newP > 255:
                    newP = 255
                if newP < 0:
                    newP = 0
                dst[i,j] = newP
        return dst

    def horizontal(self,img):
        H,W = img.shape
        # test_img = np.ones((H,W)) * 255
        hor_array = np.zeros(H,np.int32)
        for j in range(0,H):  
            for i in range(0,W):  
                if  img[j,i]== 0 : 
                    hor_array[j]+=1 
                    # test_img[j,i] = 255
        # for j in range(0,H):
            # for i in range(0,hor_array[j]):
                # test_img[j,i]=0
        return hor_array
        # return hor_array,test_img
    

    def getArea(self,array):

        H = len(array)
        label_H = int(H / 10)
        min_ = sum(array)
        ans = 0
        for i in range(int(1/2 * H) - label_H): #从图像高2/5位置处开始进行平均值计算。
            a = int(2/5 * H) + i
            b = int(2/5 * H) + i + label_H
            mean = array[a:b].mean()
            if mean < min_:
                ans = a
                min_ = mean
            if a > 0.6 * H:
                return ans,ans+label_H

    def position(self,img):
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_img = cv2.dilate(gray_img,None,iterations=2)
        gray_img = cv2.erode(gray_img,None,iterations=2)

        emboss_img = self.embossment(gray_img)
        sobel_x = cv2.Sobel(emboss_img,cv2.CV_32F,1,0,3) #边缘检测
        sobel_y = cv2.Sobel(emboss_img,cv2.CV_32F,0,1,3)
        absX = cv2.convertScaleAbs(sobel_x)
        absY = cv2.convertScaleAbs(sobel_y)
        sobel_img = cv2.addWeighted(absX,0.5,absY,0.5,0)
        sobel_img = cv2.medianBlur(sobel_img,11)  #中值模糊
        sobel_img = cv2.dilate(sobel_img,None,iterations=2) #膨胀

        _,threshold = cv2.threshold(sobel_img,10,255,cv2.THRESH_BINARY) #二值化
        threshold = cv2.GaussianBlur(threshold,(9,9),0) #高斯模糊

        # pixel_array,test_img = self.horizontal(threshold)
        pixel_array = self.horizontal(threshold) #对图形黑色像素进行竖直投影

        start,end = self.getArea(pixel_array)

        self.H_start = start
        self.H_end = end

        res = img[start:end,20:]
        return res
