import cv2
import numpy as np

class Image:
    HEIGHT = 650
    WIDTH = 350
    img = 0
    remove_back_img = 0
    number_area = 0
    def __init__(self,img):
        self.img = img
        self.remove_back_img = self.removeBackground()
        self.number_area = self.position(self.remove_back_img)
        self.pos_img = self.getNumberArea()
        
    def getNumberArea(self):
        num_img = self.number_area
        h,w,_ = num_img.shape
        gray_img = cv2.cvtColor(num_img,cv2.COLOR_BGR2GRAY)
        dilate_img = cv2.dilate(gray_img,None,iterations=2)
        embo_img = self.embossment(dilate_img)
        thresh_img = cv2.adaptiveThreshold(embo_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,3,-1)
        thresh_img = cv2.medianBlur(thresh_img,3)
        thresh_img = cv2.dilate(thresh_img,None,iterations=2)
        thresh_img = cv2.erode(thresh_img,None,iterations=2)
        thresh_img = cv2.dilate(thresh_img,None,iterations=10)
        a = np.zeros(w,np.uint8)
        for j in range(0,w): 
            for i in range(0,h):
                if  thresh_img[i,j] == 0: 
                    a[j] += 1  		
        length = int(0.85 * w)
        min_ = sum(a)
        start = 0
        for i in range(w - length):
            end = i + length 
            mean_ = a[i:end].mean()
        
            if(min_ > mean_):
                min_ = mean_
                start = i

        self.W_start = start
        self.W_end = start+length

        #cv2.rectangle(self.remove_back_img,(self.W_start,self.H_start),(self.W_end,self.H_end),(0,0,255),3)
        return num_img[:,start:start+length]


    def removeBackground(self):
        resize_img = cv2.resize(self.img,(self.HEIGHT,self.WIDTH),0,0,cv2.INTER_NEAREST)
        self.img = resize_img
        gray_img = cv2.cvtColor(resize_img,cv2.COLOR_BGR2GRAY)
        blur_img = cv2.medianBlur(gray_img,9)
        x = cv2.Sobel(blur_img,cv2.CV_32F,1,0,3)
        y = cv2.Sobel(blur_img,cv2.CV_32F,0,1,3)
        absX = cv2.convertScaleAbs(x)
        absY = cv2.convertScaleAbs(y)
        sobel_img = cv2.addWeighted(absX,0.5,absY,0.5,0)
        thresh_img = cv2.adaptiveThreshold(sobel_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,3,0)
        cnts,_ = cv2.findContours(thresh_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
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
        hor_array = np.zeros(H,np.int32)
        for j in range(0,H):  
            for i in range(0,W):  
                if  img[j,i]== 0 : 
                    hor_array[j]+=1 
        return hor_array

    def getArea(self,array):
        H = len(array)
        label_H = int(H / 10)
        min_ = sum(array)
        ans = 0
        for i in range(int(1/2 * H) - label_H):
            a = int(2/5 * H) + i
            b = int(2/5 * H) + i + label_H
            mean = array[a:b].mean()
            if mean < min_:
                ans = a
                min_ = mean
            if a > 0.6 * H:
                return ans,ans+label_H

    def position(self,img):
        #img = cv2.resize(img,(self.HEIGHT,self.WIDTH),0,0,cv2.INTER_NEAREST)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_img = cv2.dilate(gray_img,None,iterations=2)
        gray_img = cv2.erode(gray_img,None,iterations=2)
        emboss_img = self.embossment(gray_img)
        sobel_x = cv2.Sobel(emboss_img,cv2.CV_32F,1,0,3)
        sobel_y = cv2.Sobel(emboss_img,cv2.CV_32F,0,1,3)
        absX = cv2.convertScaleAbs(sobel_x)
        absY = cv2.convertScaleAbs(sobel_y)
        sobel_img = cv2.addWeighted(absX,0.5,absY,0.5,0)
        sobel_img = cv2.medianBlur(sobel_img,11)
        sobel_img = cv2.dilate(sobel_img,None,iterations=2)

        _,threshold = cv2.threshold(sobel_img,10,255,cv2.THRESH_BINARY)
        threshold = cv2.GaussianBlur(threshold,(9,9),0)
        pixel_array = self.horizontal(threshold)
        start,end = self.getArea(pixel_array)

        self.H_start = start
        self.H_end = end
        res = img[start:end,:]
        return res

#img = cv2.imread('test_images/9.jpeg')
#test = Image(img)
#cv2.imshow('test',test.pos_img)
#cv2.waitKey(0)
