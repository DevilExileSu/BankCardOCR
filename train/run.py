from data_generator import DataGenerator
from train import train_model
import keras
import numpy as np
import time
import vgg_blstm_ctc
import tensorflow as tf
import os

def main():


    # 各种路径 以及参数
    weight_save_path = "model/"
    # 数字训练路径

    train_txt_path = "train.txt"
    val_txt_path = "val.txt"
    img_size = (256, 32) # W*H
    # 各种训练时候的参数
    num_classes = 11 # 包含“blank”
    max_label_length = 26
    downsample_factor = 4
    epochs = 100



    model_for_train = vgg_blstm_ctc.model(is_training=True, img_size=img_size, num_classes=num_classes, max_label_length=max_label_length)
    
    # 训练模型
    train_model(model_for_train, train_txt_path, val_txt_path,
             weight_save_path, epochs=epochs, img_size=img_size, batch_size=64, 
             max_label_length=max_label_length,down_sample_factor=downsample_factor)



    return 0

if __name__=="__main__":
    main()
