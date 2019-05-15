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

        return num_img[:,start:start+length]


    def removeBackground(self):
        resize_img = cv2.resize(self.img,(self.HEIGHT,self.WIDTH),0,0,cv2.INTER_NEAREST)
        gray_img = cv2.cvtColor(resize_img,cv2.COLOR_BGR2GRAY)
        blur_img = cv2.medianBlur(gray_img,9)
        x = cv2.Sobel(blur_img,cv2.CV_32F,1,0,3)
        y = cv2.Sobel(blur_img,cv2.CV_32F,0,1,3)
        absX = cv2.convertScaleAbs(x)
        absY = cv2.convertScaleAbs(y)
        sobel_img = cv2.addWeighted(absX,0.5,absY,0.5,0)
        thresh_img = cv2.adaptiveThreshold(sobel_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,3,0)
        _,cnts,_ = cv2.findContours(thresh_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
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


img = cv2.imread('2.jpeg',-1)
img = Image(img)
#print(img.W_start,img.H_start,img.W_end,img.H_end)

cv2.rectangle(img.remove_back_img,(img.W_start-5,img.H_start),(img.W_end+5,img.H_end),(0,0,255),3)
cv2.imshow('aaa',img.remove_back_img)

cv2.waitKey(0)


'''
def glass(img):
    img_H, img_W = img.shape
    dst = np.zeros((img_H, img_W), np.uint8)
    scope = 6
    for i in range(img_H-scope):
        for j in range(img_W-scope):
            rand_seed = np.random.randint(scope)
            dst[i, j] = img[i+rand_seed, j+rand_seed]
    return dst

def binary(img):
    H, W = img.shape
    dst = np.zeros((H, W), np.uint8)
    for i in range(H):
        for j in range(W):
            if abs(150 - img[i,j]) < 10:
                dst[i,j] = 0
            else:
                dst[i,j] = 255
    return dst

def embossment(img):
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


def horizontal(img):
    h,w = img.shape
    dst = np.zeros((h,w),np.uint8)
    a = np.zeros(h,np.int32)
    #a = [0,0,0,0,0,0,0,0,0,0,...,0,0]初始化一个长度为h的数组，用于记录每一行的黑点个数  
    for j in range(0,h):  
        for i in range(0,w):  
            if  img[j,i]== 0 : 
                a[j]+=1 
                dst[j,i] = 255 
            dst[j,i] = 255
    
    for j  in range(0,h):  
        for i in range(0,a[j]):   
            dst[j,i]= 0 #0
    return dst,a

def position(array):
    H = len(array)
    label_H = int(H / 10)
    min_ = sum(array)
    ans = 0
    for i in range(int(1/2 * H) - label_H):
        a = int(2/5 * H) + i
        b = int(2/5 * H) + i + label_H
        mean = array[a:b].mean()
        print(i,mean,label_H)
        if mean < min_:
            ans = a
            min_ = mean
        if a > 0.6 * H:
            return ans,ans+label_H


img = cv2.imread('1.jpeg',-1)
imgs = cv2.resize(img,(650,350),0,0,cv2.INTER_NEAREST)
img = cv2.cvtColor(imgs,cv2.COLOR_BGR2GRAY)
img = cv2.medianBlur(img,11)


x = cv2.Sobel(img,cv2.CV_32F,1,0,3)
y = cv2.Sobel(img,cv2.CV_32F,0,1,3)
absX = cv2.convertScaleAbs(x)
absY = cv2.convertScaleAbs(y)
imgSobel = cv2.addWeighted(absX,0.5,absY,0.5,0)


imgSobel = cv2.adaptiveThreshold(imgSobel,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,3,0)

tmp,cnts,w1 = cv2.findContours(imgSobel,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

temp = 0
W = 0
H = 0
X = 0
Y = 0

for i in range(0,len(cnts)):
    x,y,w,h = cv2.boundingRect(cnts[i])
    if(temp <x + y + w + h):
        temp = w+h
        W = w
        H = h
        X = x
        Y = y
    

image = cv2.rectangle(imgs,(X,Y),(X+W,Y+H),(0,0,255),3)
img = imgs[Y:Y+H,X:X+W]
#image = cv2.drawContours(imgs,cnts,-1,(0,0,255),3)


cv2.imshow('img',img)
cv2.imshow('imgSobel',imgSobel)
cv2.imshow('image',image)
cv2.waitKey(0)

'''


'''
kernel = np.ones((5,5),np.uint8)

#img = cv2.imread('1.jpeg', -1)
img = cv2.resize(img,(650,350),0,0,cv2.INTER_NEAREST)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#img = cv2.GaussianBlur(img,(9,9),0)
#img = cv2.medianBlur(img,11)
#img = cv2.equalizeHist(img)
#img = cv2.GaussianBlur(img,(9,9),0)
gray = cv2.dilate(gray,None,iterations=2)
gray = cv2.erode(gray,None,iterations=2)
#img = cv2.equalizeHist(img)

#img_glass = glass(img)
img_glass = embossment(gray)


x = cv2.Sobel(img_glass,cv2.CV_32F,1,0,3)
y = cv2.Sobel(img_glass,cv2.CV_32F,0,1,3)
absX = cv2.convertScaleAbs(x)
absY = cv2.convertScaleAbs(y)
img_glass = cv2.addWeighted(absX,0.5,absY,0.5,0)
#img_glass = cv2.GaussianBlur(img_glass,(9,9),0)
img_glass = cv2.medianBlur(img_glass,9)
img_glass = cv2.dilate(img_glass,None,iterations=2)


#img_glass = cv2.equalizeHist(img_glass)
#binary = binary(img_glass)
_,binary = cv2.threshold(img_glass,10,255,cv2.THRESH_BINARY)
#binary = cv2.adaptiveThreshold(img_glass,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,3,-1)
binary = cv2.GaussianBlur(binary,(9,9),0)


horizontalxz,a = horizontal(binary)
a,b = position(a)
print(a)
res = img[a:b,:]

cv2.imshow('img',img)
cv2.imshow('glass', img_glass)
cv2.imshow('gray', gray)
cv2.imshow('binary', binary)
cv2.imshow('horizontalxz',horizontalxz)
cv2.imshow('res',res)
cv2.waitKey(0)
'''


''' 垂直映射，水平映射
def Thresh(img):
        horizontalight = img.shape[0]
        width = img.shape[1]
        dst = np.zeros((horizontalight,width,1),np.uint8)
        for i in range(0,horizontalight-2):
                for j in range(0,width-2):
                        if img[i][j] < 30 or img[i][j] >150:
                                dst[i][j] = 255
        return dst


kernel = np.ones((5,5),np.uint8)
img=cv2.imread('3.jpeg')  #读取图片，装换为可运算的数组
GrayImage=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)   #将BGR图转为灰度图
GrayImage = cv2.equalizeHist(GrayImage)~

plt.imshow(GrayImage,cmap=plt.gray())
plt.show()

thresh1 = Thresh(GrayImage)
thresh2 = Thresh(GrayImage)

cv2.imshow('thresh1',thresh1)
cv2.imshow('thresh2',thresh2)
cv2.waitKey(0)  
# print(thresh1[0,0])#250  输出[0,0]这个点的像素值  				#返回值ret为阈值
# print(ret)#130
(h,w)=img.shape #返回高和宽
print(h,w)#s输出高和宽

 
a = [0 for z in range(0, h)] 

 
for j in range(0,h):  
    for i in range(0,w):  
        if  thresh2[j,i]==0: 
            a[j]+=1 
            thresh2[j,i]=255
         
for j  in range(0,h):  
    for i in range(0,a[j]):   
        thresh2[j,i]=0    

a = [0 for z in range(0, w)] 
 #a = [0,0,0,0,0,0,0,0,0,0,...,0,0]初始化一个长度为w的数组，用于记录每一列的黑点个数  
 
#记录每一列的波峰
for j in range(0,w): #遍历一列 
    for i in range(0,h):  #遍历一行
        if  thresh1[i,j]==0:  #如果改点为黑点
            a[j]+=1  		#该列的计数器加一计数
            thresh1[i,j]=255 #记录完后将其变为白色 
    # print (j)           
 
#            
for j  in range(0,w):  #遍历每一列
    for i in range((h-a[j]),h):  #从该列应该变黑的最顶部的点开始向最底部涂黑
        thresh1[i,j]=0   #涂黑


plt.imshow(thresh1,cmap=plt.gray())
plt.show()
plt.imshow(thresh2,cmap=plt.gray())
plt.show()

#此时的thresh1便是一张图像向垂直方向上投影的直方图
#如果要分割字符的话，其实并不需要把这张图给画出来，只需要的到a=[]即可得到想要的信息
 
 
# img2 =Image.open('0002.jpg')
# img2.convert('L')
# img_1 = np.array(img2)

#cv2.imshow('img',thresh1)  
#cv2.waitKey(0)  
#cv2.destroyAllWindows()  
'''
