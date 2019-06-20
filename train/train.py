from utils import fake_ctc_loss
import keras
import os
import cv2
import time
from data_generator import DataGenerator
import keras.backend.tensorflow_backend as KTF
import tensorflow as tf
import os


def train_model(model,  train_txt, val_txt, weight_save_path, img_size=(256,32), batch_size=64, max_label_length=26, down_sample_factor=4, epochs=100):
    print("Training start!")

    try:
        model.load_weights(weight_save_path+"ep011-loss2.812-val_loss2.837.h5")
        print("restore model successful....")
    except:
        print("Create new model...")
        pass 

    #callbacks  
    checkpoint = keras.callbacks.ModelCheckpoint(weight_save_path + "ep{epoch:03d}-loss{loss:.3f}-val_loss{val_loss:.3f}.h5",
        monitor='val_loss', save_weights_only=True, save_best_only=True, period=1)
    # early_stop_cbk = keras.callbacks.EarlyStopping(patience=3)
    reduce_lr_cbk = keras.callbacks.ReduceLROnPlateau(patience=3)
    logging = keras.callbacks.TensorBoard(log_dir=weight_save_path)
    # compile
    model.compile(optimizer='adam', loss={'ctc_loss_output': fake_ctc_loss})
    # fit_generator
    train_gen = DataGenerator(train_txt, img_size, down_sample_factor, batch_size, max_label_length)
    val_gen = DataGenerator(val_txt, img_size, down_sample_factor, batch_size, max_label_length)
    model.fit_generator(generator=train_gen.get_data(),
                        steps_per_epoch=train_gen.img_number//batch_size,
                        validation_data=val_gen.get_data(),
                        validation_steps=val_gen.img_number//batch_size,
                        callbacks=[checkpoint, reduce_lr_cbk,logging], 
                        epochs = epochs,
                        # initial_epoch=38,
                        )
    print("Training finished!")
    return 0

