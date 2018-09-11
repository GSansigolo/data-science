from sklearn import preprocessing, neighbors, svm
from sklearn.model_selection import train_test_split
from os import listdir
from os.path import isfile, join
import numpy as np
import geopandas as gpd
import pandas as pd
import requests
import io

print("")
falsospath = "/home/sansigolo/Documents/git/CAP-240-394/src/SVM/AQM_L8_221_067_2017/FALSOS_221_067-2017/"

queimadaspath = "/home/sansigolo/Documents/git/CAP-240-394/src/SVM/AQM_L8_221_067_2017/QUEIMADAS_221_067-2017/"

falsosfilenames = [y for y in listdir(falsospath) for ending in ['dbf', 'shp', 'prj', 'shx'] if y.endswith(ending)] 

queimadasfilenames = [y for y in listdir(queimadaspath) for ending in ['dbf', 'shp', 'prj', 'shx'] if y.endswith(ending)] 

print(falsosfilenames)
print("")
print(queimadasfilenames)

f_dbf, f_prj, f_shp, f_shx = [falsosfilename for falsosfilename in falsosfilenames]

falsos = gpd.read_file(falsospath+f_shp)

print("\nFalsos Shape: {}".format(falsos.shape)+"\n")

q_dbf, q_prj, q_shp, q_shx = [queimadasfilename for queimadasfilename in queimadasfilenames]

queimadas = gpd.read_file(queimadaspath+q_shp)

print("Queimadas Shape: {}".format(queimadas.shape)+"\n")

df = pd.concat([falsos, queimadas], ignore_index=True)

df.replace('?', -99999, inplace=True)

df['ndwi'] = (df['medianb5'] - df['medianb6']) / (df['medianb5'] + df['medianb6'])

df['bai'] = 1 / (((df['medianb5'] - 0.06) ** 2) + ((df['medianb4'] - 0.1) ** 2))

df['nbr'] = (df['medianb5'] - df['medianb7']) / (df['medianb5'] + df['medianb7'])

df.drop(['id','cod_sat','cena_id', 'area_ha', 'dif_dnbrl', 'medianb6', 'medianb7', 'nome_arq', 'orb_pto', 'n_arq_ant', 'medianb1', 'proc_id','data_atual', 'data_anter', 'geometry', 'focos', 'ndvi', 'perim'], 1, inplace=True)

print(df.tail())

X = np.array(df.drop(['verifica'],1))

y = np.array(df['verifica'])

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2)

clf = svm.SVC()
clf.fit(X_train, y_train)

accuracy = clf.score(X_test, y_test)

print('\nAccuracy: ', accuracy)
