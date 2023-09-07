

import numpy as np
import argparse
from scipy import io, spatial
import time
from random import shuffle
import random
from sklearn import preprocessing
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
 

res101 = io.loadmat('./AWA1/res101.mat')
att_splits=io.loadmat('./AWA1/att_splits.mat')
 
train_loc = 'train_loc'
val_loc = 'val_loc'
test_loc = 'test_unseen_loc'
 
feat = res101['features']
# Shape -> (dxN)
X_train = feat[:, np.squeeze(att_splits[train_loc]-1)]
X_val = feat[:, np.squeeze(att_splits[val_loc]-1)]
X_test = feat[:, np.squeeze(att_splits[test_loc]-1)]

labels = res101['labels']
labels_train = np.squeeze(labels[np.squeeze(att_splits[train_loc]-1)])
labels_val = np.squeeze(labels[np.squeeze(att_splits[val_loc]-1)])
labels_test = np.squeeze(labels[np.squeeze(att_splits[test_loc]-1)])
 
train_labels_seen = np.unique(labels_train)
val_labels_unseen = np.unique(labels_val)
test_labels_unseen = np.unique(labels_test)

train_labels_seen = np.array([x-1 for x in train_labels_seen])

val_labels_unseen= np.array([x-1 for x in val_labels_unseen])

test_labels_unseen = np.array([x-1 for x in test_labels_unseen])
 
i=0
for labels in train_labels_seen:
  labels_train[labels_train == labels] = i    
  i+=1
 
j=0
for labels in val_labels_unseen:
  labels_val[labels_val == labels] = j
  j+=1
 
k=0
for labels in test_labels_unseen:
  labels_test[labels_test == labels] = k
  k+=1
 
sig = att_splits['att']
  # Shape -> (Number of attributes, Number of Classes)
train_sig = sig[:, train_labels_seen]
val_sig = sig[:, val_labels_unseen]
test_sig = sig[:, test_labels_unseen]


sorted_ind =  np.concatenate([val_labels_unseen , train_labels_seen], axis=0)
sorted_ind=np.sort(sorted_ind)
train_sig_fin = sig[:, sorted_ind]

testClasses = test_labels_unseen
trainClasses =  np.concatenate([train_labels_seen , val_labels_unseen], axis=0)

sorted_ind_all =  np.concatenate([val_labels_unseen , train_labels_seen], axis=0)
sorted_ind_all =  np.concatenate([sorted_ind_all , test_labels_unseen], axis=0)
sorted_ind_all=np.sort(sorted_ind_all)



# Loads features
X = res101['features'].transpose()
Y_temp = res101['labels']
Y_temp=Y_temp.transpose()
Y_temp=Y_temp[0]
Y = np.array([x-1 for x in Y_temp])
Y =Y.astype(np.int32).transpose()
#Y1 =np.array(Y1.tolist())
ATTR =  att_splits['att']
att =  att_splits['att']
att=np.transpose(att)
noExs = X.shape[0]


trainDataX = []
trainDataLabels = []
trainDataAttrs = []

testDataX = []
testDataLabels = []
testDataAttrs = []



for ii in range(0,noExs):
    if(Y[ii] in trainClasses):
        trainDataX = trainDataX + [X[ii]]
        trainDataLabels = trainDataLabels + [Y[ii]]
        trainDataAttrs = trainDataAttrs + [att[Y[ii]]]
    elif(Y[ii] in testClasses):
        #print(str(Y[ii])  + "  is in   " + str(testClasses))
        testDataX = testDataX + [X[ii]]
        testDataLabels = testDataLabels + [Y[ii]]
        testDataAttrs = testDataAttrs + [att[Y[ii]]]
    else:
        print('Fatal Error... Please check code/data')
       
       
trainDataX = np.array(trainDataX)
trainDataLabels = np.array(trainDataLabels)
trainDataAttrs = np.array(trainDataAttrs)

testDataX = np.array(testDataX)
testDataLabels = np.array(testDataLabels)
testDataAttrs = np.array(testDataAttrs)

