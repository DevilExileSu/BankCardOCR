# -bankCardNumIdentify

# 基于tensorflow、keras实现对银行卡号识别
---
# 测试环境
---
```
Ubuntu 18.04
python 3.6.7 
numpy 1.16.4
tensorflow-gpu 1.13.1 或者是cpu版本
keras 2.2.4
opencv-python 4.1.0.25
PyQt5 5.12.2
CUDA 10.0.130
cuDNN 7.5 
```
### 环境搭建
```
pip3 install numpy==1.16.4
pip3 install tensorflow-gpu==1.13.1 #或者使用cpu版本
pip3 install keras==2.2.4
pip3 install opencv-python==4.1.0.25
pip3 install PyQt5==5.12.2
```
#### CUDA与cuDNN安装
[具体安装过程可以在NVIDIA官网查看](https://developer.nvidia.com/cuda-10.0-download-archive)

---
# 启动demo
执行demo.py打开银行卡号识别的GUI界面。batch_test.py用于对银行卡进行批量识别，将要识别的银行卡放在同目录下的test_images文件中。定位结果以及识别结果存放在test_results中。

# 训练模型
在train文件中首先执行datasets.py进行数据增强，并生成对应图片路径及标签文件，再执行run.py文件开始模型的训练，训练大概20个epoch后loss不再收敛可以停止。训练的模型被保存在train/model中。

# 测试模型
选取银行卡图片进行测试时，银行卡尽量充满图片，横向放置。
