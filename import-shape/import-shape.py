'''
Created on Jul 20, 2018
Author: @G_Sansigolo
'''
import geopandas as gpd
import pandas as pd
import requests
import io
from os import listdir
from os.path import isfile, join

paths = ['2017-05-05', '2017-06-22', '2017-07-24', '2017-08-09', '2017-09-10', '2017-09-26']

df = pd.DataFrame(columns=['id', 'nome_arq', 'data_pas', 'orb_pto', 'area_ha', 'perim', 'versao', 'n_arq_ant', 'fid', 'proc_id', 'maquina', 'NDVI', 'NBRL', 'DIF_NDVI', 'DIF_DNBRL', 'medianb2', 'medianb3', 'medianb4', 'medianb5', 'medianb6', 'medianb7', 'cena_id', 'cod_sat', 'ano', 'lim_ndvi', 'lim_nbrl', 'data_proc', 'geometry'])

for paths in paths:
    mypath = "/home/sansigolo/Documents/git/CAP-240-394/data-shp/"+paths+"/"

    filenames = [y for y in listdir(mypath) for ending in ['dbf', 'shp', 'prj', 'shx'] if y.endswith(ending)] 
   
    print(filenames)

    dbf, shp, prj,  shx = [filename for filename in filenames]

    df  = df.append(gpd.read_file(mypath+shp))

    print("\nShape of the dataframe: {}".format(df.shape)+"\n")

print(df.tail())

nome_arq = df.drop_duplicates(subset='nome_arq', keep='first', inplace=False)

print(nome_arq['nome_arq'])
