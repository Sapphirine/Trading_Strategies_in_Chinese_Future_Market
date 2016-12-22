# -*- coding: utf-8 -*-

import numpy as np


def load_data(prev=30):
    Hlcr = []
    Ret = []
    np.random.seed(1337)
    with open('data/IFB1_test.csv') as f:
        hlcr = f.readline()
        while hlcr != '':
            hlcr = f.readline()
            parts = hlcr.split(',')
            if hlcr == '':
                break
            if parts[6] == 'NA\n':
                continue
            else:
                tmp = float(parts[6])
                if tmp > 0:
                    Ret.append(0)
                elif tmp < 0:
                    Ret.append(1)
                else:
                    Ret.append(2)

                newfeature = [float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4]), float(parts[5])]
                Hlcr.append(newfeature)

    X = []
    Y = []
    for i in range(0, len(Hlcr) - prev):
        X.append(Hlcr[i:i + prev])
        Y.append(Ret[i + prev - 1])

    X = np.asarray(X)
    Y = np.asarray(Y)
    p = np.random.permutation(len(X))
    X = X[p]
    Y = Y[p]
    X_train = X[0:7500]
    Y_train = Y[0:7500]
    X_test = X[7500:]
    Y_test = Y[7500:]
    return (X_train, Y_train), (X_test, Y_test)


if __name__ == '__main__':
    (X_tra, Y_tra), (X_te, Y_te) = load_data(prev=6)
    print X_tra.shape
    print Y_tra.shape
    print X_te.shape
    print Y_te.shape


