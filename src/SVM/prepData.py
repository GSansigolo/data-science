import geopandas as gpd
import pandas as pd
import requests
import io
from os import listdir
from os.path import isfile, join
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
