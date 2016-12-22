from __future__ import print_function
import numpy as np
np.random.seed(1337)  # for reproducibility
from genTrainTest_IFB1 import load_data
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD, Adam, RMSprop
from keras.utils import np_utils

def run_model(dropout=True, normalized = True):
    batch_size = 128
    nb_classes = 3
    nb_epoch = 1521

    # the data, shuffled and split between train and test sets
    prev = 40
    (X_train, y_train), (X_test, y_test) = load_data(prev = prev)


    X_train = X_train.reshape(X_train.shape[0], prev*5)
    X_test = X_test.reshape(X_test.shape[0], prev*5)
    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32')

    if normalized:
        train_mean = np.mean(X_train, axis=0)
        train_std = np.std(X_train, axis=0)
        epsilon = 0.000001
        X_train = (X_train - train_mean) / (train_std + epsilon)
        X_test = (X_test - train_mean) / (train_std + epsilon)


    # convert class vectors to binary class matrices
    Y_train = np_utils.to_categorical(y_train, nb_classes)
    Y_test = np_utils.to_categorical(y_test, nb_classes)

    if dropout:
        drop = 0.1
    else:
        drop = 0



    model = Sequential()
    model.add(Dense(256, input_shape=(prev*5,)))
    model.add(Activation('sigmoid'))
    model.add(Dropout(drop))
    model.add(Dense(512))
    model.add(Activation('sigmoid'))
    model.add(Dropout(drop))
    model.add(Dense(512))
    model.add(Activation('sigmoid'))
    model.add(Dropout(drop))
    model.add(Dense(512))
    model.add(Activation('sigmoid'))
    model.add(Dropout(drop))
    model.add(Dense(3))
    model.add(Activation('softmax'))

    model.summary()

    model.compile(loss='categorical_crossentropy',
                  optimizer=RMSprop(),
                  metrics=['accuracy'])

    history = model.fit(X_train, Y_train,
                        batch_size=batch_size, nb_epoch=nb_epoch,
                        verbose=1, validation_data=(X_test, Y_test),
                        )
    score = model.evaluate(X_test, Y_test, verbose=0)
    print('Test score:', score[0])
    print('Test accuracy:', score[1])

if __name__ == '__main__':
    run_model(dropout=True, normalized=True)
    # run_model(dropout=True, normalized=False)
    # run_model(dropout=False, normalized=True)
    # run_model(dropout=False, normalized=False)