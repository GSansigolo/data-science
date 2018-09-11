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
