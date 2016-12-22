# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 16:41:18 2016

@author: yutingan
"""

from __future__ import print_function

from pyspark import SparkContext
# $example on$
import sys
from pyspark.mllib.tree import DecisionTree, DecisionTreeModel
from pyspark.mllib.util import MLUtils
from pyspark.mllib.regression import LabeledPoint
from time import time
import numpy as np

# $example off$

if __name__ == "__main__":

    sc = SparkContext(appName="PythonDecisionTreeClassificationExample")
    
    index_dict={'BSP': 6,'C': 2,'C-L': 9,'C-L_pct': 11,'C-diff1': 12,'C-diff1_pct': 15,'C-diff2': 13,'C-diff2_pct': 16,'C-diff3': 14,'C-diff3_pct': 17,'H': 3,'H-C': 8,'H-C_pct': 10,'L': 4,'O': 1,'amt': 0,'return': 5,'strategy': 7}
    
    
    tag=index_dict['strategy']
    #features=[index_dict['C-L'],index_dict['H-C']]

#features=[index_dict['C-L_pct'],index_dict['H-C_pct']]
#features=[index_dict['C-diff1'],index_dict['C-diff2'],index_dict['C-diff3']]
    features=[index_dict['C-diff1_pct'],index_dict['C-diff2_pct'],index_dict['C-diff3_pct']]

#features=[index_dict['BSP']]
    #features=[index_dict['C'],index_dict['H'],index_dict['O'],index_dict['L']]
    tagAndFeatures=[tag]+features
# $example on$

    # Load and parse the data file into an RDD of LabeledPoint.
    def parsePoint(line):
           values = line.strip('\n').split('\t')

           for i in tagAndFeatures:
                        values[i]=float(values[i])
           return LabeledPoint(values[tag], [values[features[0]],values[features[1]],values[features[2]]])

           

    #return LabeledPoint(values[index_dict['strategy']], [values[index_dict['H']],values[index_dict['L']],values[index_dict['O']],values[index_dict['C']],])
               #return LabeledPoint(values[index_dict['strategy']], [values[index_dict['H']],values[index_dict['L']],values[index_dict['O']],values[index_dict['C']],])
#return LabeledPoint(values[index_dict['strategy']], [values[index_dict['H-C']],values[index_dict['C-L']]])
#return LabeledPoint(values[index_dict['strategy']], [values[index_dict['H']],values[index_dict['L']],values[index_dict['O']],values[index_dict['C']],])
#return LabeledPoint(values[index_dict['strategy']], [values[index_dict['H']],values[index_dict['L']],values[index_dict['O']],values[index_dict['C']],])
#return LabeledPoint(values[index_dict['strategy']], [values[index_dict['H']],values[index_dict['L']],values[index_dict['O']],values[index_dict['C']],])
    train_data = sc.textFile(sys.argv[1],1)
    test_data=sc.textFile(sys.argv[2],1)

    train_parsedData = train_data.map(parsePoint)
    test_parsedData=test_data.map(parsePoint)
    

    # Train a DecisionTree model.
    #  Empty categoricalFeaturesInfo indicates all features are continuous.
    model = DecisionTree.trainClassifier(train_parsedData, numClasses=2, categoricalFeaturesInfo={},
                                         impurity='gini')

    # Evaluate model on test instances and compute test error
    predictions = model.predict(test_parsedData.map(lambda x: x.features))
    labelsAndPredictions = test_parsedData.map(lambda lp: lp.label).zip(predictions)
    t0=time()
    test_accuracy = labelsAndPredictions.filter(lambda (v, p): v == p).count() / float(test_parsedData.count())
    tt=time()-t0
    print("Prediction made in {} seconds. Test accuracy is {}".format(round(tt,3), round(test_accuracy,4)))
    print('Learned classification tree model:')
    print(model.toDebugString())

    # Save and load model
# model.save(sc, "/Users/angela/Desktop/columbia_life/big_data_analytics/project/myDecisionTreeClassificationModel")
#sameModel = DecisionTreeModel.load(sc, "/Users/angela/Desktop/columbia_life/big_data_analytics/project/myDecisionTreeClassificationModel")

#cd $SPARK_HOME

#./bin/spark-submit /Users/angela/Desktop/columbia_life/big_data_analytics/project/DecisionTree_classification.py  "/Users/angela/Desktop/columbia_life/big_data_analytics/project/train_data.txt" "/Users/angela/Desktop/columbia_life/big_data_analytics/project/test_data.txt"
