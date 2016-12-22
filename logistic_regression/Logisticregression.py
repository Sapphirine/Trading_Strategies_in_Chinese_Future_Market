# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 21:03:13 2016

@author: yutingan
"""


import sys
from pyspark.mllib.classification import LogisticRegressionWithLBFGS, LogisticRegressionModel
from pyspark.mllib.regression import LabeledPoint
from pyspark import SparkContext
from time import time

if __name__=="__main__":
    if len(sys.argv) !=3:
        print >>sys.stderr,"Usage: train_model <file> <train_data> <test_data>"
        exit(-1)
    else:
        sc=SparkContext(appName="Logistic model")
        # Load and parse the data
        def parsePoint(line):
           values = line.split('\t')
           for i in range(5,13):
               if values[i]=='' or values[i]==' ':
                   values[i]=0
               else:
                   values[i]=float(values[i])
           return LabeledPoint(values[12], values[5:9])

        train_data = sc.textFile(sys.argv[1],1)
        test_data=sc.textFile(sys.argv[2],1)
        train_parsedData = train_data.map(parsePoint)
        test_parsedData=test_data.map(parsePoint)
        print train_parsedData

        # Build the model
        t0=time()
        model = LogisticRegressionWithLBFGS.train(train_parsedData)
        tt=time()-t0
        
        print "Classifier trained in {} seconds".format(round(tt,3))

        # Evaluating the model on training data
        labelsAndPreds = test_parsedData.map(lambda p: (p.label, model.predict(p.features)))
        t0=time()
        test_accuracy = labelsAndPreds.filter(lambda (v, p): v == p).count() / float(test_parsedData.count())
        tt=time()-t0
        print "Prediction made in {} seconds. Test accuracy is {}".format(round(tt,3), round(test_accuracy,4))
        print model

        # Save and load model
        model.save(sc, "target/tmp/pythonLogisticRegressionWithLBFGSModel")