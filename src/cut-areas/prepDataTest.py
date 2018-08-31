import io
import os
import requests
import numpy as np
import pandas as pd
from osgeo import osr
from osgeo import gdal
from os import listdir
import geopandas as gpd
from os.path import isfile, join

tiff_path = "/home/sansigolo/Documents/git/CAP-240-394/src/cut-areas/LC08_L1TP_221067_20170926_20171013_01_T1/"

shape_path = "/home/sansigolo/Documents/git/CAP-240-394/src/cut-areas/221_067_2017-09-26_AQ30M_02_05.3/"

filenames = [y for y in listdir(shape_path) for ending in ['dbf', 'shp', 'prj', 'shx'] if y.endswith(ending)] 
   
print("\nFilenames: ",filenames)

dbf, shp, prj,  shx = [filename for filename in filenames]

df  = gpd.read_file(shape_path+shp)

print("\nShape of the dataframe: {}".format(df.shape)+"\n")

print("\nDataframe tail:\n", df.tail())

df['geometry'] = df['geometry'].buffer(0.002)

for i in range(2): #len(df)
	gp = df[df['geometry'] == df['geometry'][i]]
	gp.to_file(shape_path+"new_shape_221_067_09-26_"+str(i))
	shapefile = shape_path+"new_shape_221_067_09-26_"+str(i)+"/new_shape_221_067_09-26_"+str(i)+".shp"
	for j in range(1,12):
		new_tiff_file = "output/queimada_"+str(i)+"_B"+str(j)+"_.TIF"
		os.system("gdalwarp -overwrite -q -cutline " +shapefile+ " -crop_to_cutline -tr 30.0 30.0 " +tiff_path+'LC08_L1TP_221067_20170926_20171013_01_T1_B'+str(j)+'.TIF'+ " " +new_tiff_file)