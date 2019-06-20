import os
import cv2
import numpy as np
from keras import backend as K
from dicts import char2num_dict, num2char_dict
import random

def ctc_loss_layer(args):
    '''
    输入：args = (y_true, y_pred, pred_length, label_length)
    y_true, y_pred分别是预测的标签和真实的标签
    shape分别是（batch_size，max_label_length)和(batch_size, time_steps, num_categories)
    perd_length, label_length分别是保存了每一个样本所对应的预测标签长度和真实标签长度
    shape分别是（batch_size, 1)和(batch_size, 1)
    输出：
    batch_cost 每一个样本所对应的loss
    shape是（batch_size, 1)
    '''
    y_true, y_pred, pred_length, label_length = args
    # y_pred = y_pred[:, 2:, :]
    batch_cost = K.ctc_batch_cost(y_true, y_pred, pred_length, label_length)
    return batch_cost


def fake_ctc_loss(y_true, y_pred):
    '''
    这个函数是为了符合keras comepile的要求入口参数只能有y_true和y_pred
    之后在结合我们的ctc_loss_layer一起工作
    '''
    return y_pred


