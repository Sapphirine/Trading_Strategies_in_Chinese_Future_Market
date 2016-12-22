import numpy as np
def load_data(prev = 5):
    Hlcr = []
    Ret = []
    np.random.seed(1337)
    with open('data/HLCR.csv') as f, open('data/return.csv') as g:
        hlcr = f.readline()
        ret = g.readline()
        while ret != '':
            hlcr = f.readline()
            ret = g.readline()
            if ret == '':
                break
            retparts = ret.split(',')
            if retparts[1] == 'NA':
                continue
            else:
                tmp = float(retparts[1])
                if tmp>0:
                    Ret.append(0)
                elif tmp <0:
                    Ret.append(1)
                else:
                    Ret.append(2)

                hlcrparts = hlcr.split(',')
                Hlcr.append([int(hlcrparts[3]), int(hlcrparts[4]), int(hlcrparts[5]), int(hlcrparts[6]), int(hlcrparts[7])])


    X = []
    Y = []
    for i in range(0, len(Hlcr)-prev):
        X.append(Hlcr[i:i+prev])
        Y.append(Ret[i+prev-1])

    X = np.asarray(X)
    Y = np.asarray(Y)
    p = np.random.permutation(len(X))
    X = X[p]
    Y = Y[p]
    X_train = X[0:2500]
    Y_train = Y[0:2500]
    X_test = X[2500:]
    Y_test = Y[2500:]
    return (X_train, Y_train), (X_test, Y_test)
