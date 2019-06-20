from Image import Image
from vgg_blstm_ctc import model
import cv2
import os
import numpy as np
import keras


test_dir = 'test_images/'
res_dir = 'test_results/'

char2num_dict = {'0': 0, '1': 1, '2':2, '3': 3, 
                '4': 4, '5': 5, '6': 6, '7': 7, 
                '8': 8, '9': 9, '_': 10}
num2char_dict = {value : key for key, value in char2num_dict.items()}

def PredictLabels_by_filename(model_for_pre, test_data_dir, img_size, downsample_factor, batch_size=64, weight_path=None):
    img_w, img_h = img_size
    img_path_list = os.listdir(test_data_dir)
    num_images = len(img_path_list)
    counter = num_images
    if weight_path is not None: # 表明传入的是一个空壳，需要加载权重参数
        model_for_pre.load_weights(weight_path, by_name=True) # by_name = True 表示按名字，只取前面一部分的权重
    predicted_labels = {}
    print("Predicting Start!")
    # 将数据装入
    for idx in range(0, num_images, batch_size):
        img_path_batch = img_path_list[idx:idx+batch_size]
        l_ipb = len(img_path_batch)
        img_batch = np.zeros((l_ipb, img_h, img_w, 1))
        # 将一个batch的图片装入内存 并进行处理
        print("There are {} images left.".format(counter))
        for i, img_path in enumerate(img_path_batch):
            img = cv2.imread(os.path.join(test_data_dir, img_path))
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray_img = cv2.resize(gray_img, (img_w, img_h))
            gray_img = np.expand_dims(gray_img, axis=-1)
            gray_img = gray_img / 255.0 * 2.0 - 1.0 # 零中心化
            img_batch[i, :, :, :] = gray_img

        # 传输进base_net获得预测的softmax后验概率矩阵
        y_pred_probMatrix = model_for_pre.predict(img_batch)
        y_pred_length = np.full((l_ipb,), int(img_w//downsample_factor))

        # Decode 阶段 
        y_pred_labels_tensor_list, _ = keras.backend.ctc_decode(y_pred_probMatrix, y_pred_length, greedy=True) # 使用的是最简单的贪婪算法
        y_pred_labels_tensor = y_pred_labels_tensor_list[0]
        y_pred_labels = keras.backend.get_value(y_pred_labels_tensor) # 现在还是字符编码
        # 转换成字符串
        y_pred_text = ["" for _ in range(l_ipb)]
        for k in range(l_ipb):
            label = y_pred_labels[k]
            for num in label:
                if num == -1:break
                y_pred_text[k] += num2char_dict[num]
        for j in range(len(img_path_batch)):
            predicted_labels[img_path_batch[j]] = y_pred_text[j]
        counter -= batch_size

    print("Predict Finished!")
    return predicted_labels

def main():
    img_path_list = os.listdir(test_dir)
    img_path_list = sorted(img_path_list)
    for num,img_name in enumerate(img_path_list):
        img = Image(cv2.imread(test_dir+img_name))
        cv2.imwrite(res_dir + 'card_' + str(num + 1) + '.jpg',img.pos_img)
        print(img_name + '定位完成')

    pre_model = model(is_training=False, img_size=(256, 32), num_classes = 11, max_label_length=26)
    res = PredictLabels_by_filename(pre_model,res_dir,(256,32),downsample_factor=4,weight_path='model/train_weight.h5')
    res_key = sorted(res)
    f = open(res_dir + 'result.txt','w')
    for img_name in res_key:
        f.write(img_name[:-4] + ':' + res[img_name] + '\n')
    f.close()

main()
