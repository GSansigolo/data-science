from sklearn import preprocessing, cross_validation, neighbors, svm
from os import listdir
from os.path import isfile, join
import numpy as np
import geopandas as gpd
import pandas as pd
import requests
import io

print("")
falsospath = "/home/sansigolo/Documents/git/CAP-240-394/src/SVM/FALSOS_221_067-09-26/"

queimadaspath = "/home/sansigolo/Documents/git/CAP-240-394/src/SVM/QUEIMADAS_221_067-09-26/"

falsosfilenames = [y for y in listdir(falsospath) for ending in ['dbf', 'shp', 'prj', 'shx'] if y.endswith(ending)] 

queimadasfilenames = [y for y in listdir(queimadaspath) for ending in ['dbf', 'shp', 'prj', 'shx'] if y.endswith(ending)] 
   
print(falsosfilenames)
print("")
print(queimadasfilenames)

f_dbf, f_shp, f_prj,  f_shx = [falsosfilename for falsosfilename in falsosfilenames]

falsos = gpd.read_file(falsospath+f_shp)

print("\nFalsos Shape: {}".format(falsos.shape)+"\n")

q_dbf, q_shp, q_prj,  q_shx = [queimadasfilename for queimadasfilename in queimadasfilenames]

queimadas = gpd.read_file(queimadaspath+q_shp)

print("Queimadas Shape: {}".format(queimadas.shape)+"\n")

df = pd.concat([falsos, queimadas], ignore_index=True)

df.replace('?', -99999, inplace=True)

df.drop(['id','cod_sat','cena_id', 'nome_arq', 'data_pas', 'orb_pto', 'versao', 'n_arq_ant', 'medianb1', 'data_inser', 'fid_1', 'data_proc','maquina', 'proc_id','valida_web', 'user_id', 'data_valid', 'data_visua', 'visualizac', 'visualizad', 'geometry'], 1, inplace=True)

X = np.array(df.drop(['verifica'],1))
y = np.array(df['verifica'])

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X,y,test_size=0.2)

clf = svm.SVC()
clf.fit(X_train, y_train)

accuracy = clf.score(X_test, y_test)

print('Accuracy: ', accuracy)
