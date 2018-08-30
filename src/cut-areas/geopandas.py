import geopandas as gpd
import pandas as pd
import requests
import io
from os import listdir
from os.path import isfile, join

mypath = "/home/sansigolo/Documents/git/CAP-240-394/src/cut-areas"

filenames = [y for y in listdir(mypath) for ending in ['dbf', 'shp', 'prj', 'shx'] if y.endswith(ending)] 
   
print(filenames)

dbf, shp, prj,  shx = [filename for filename in filenames]

df  = gpd.read_file(mypath+shp)

print("\nShape of the dataframe: {}".format(df.shape)+"\n")

print(df.geometry.tail())

df['geometry'] = df['geometry'].buffer(0.002)

df.to_file(mypath+"new_shape_221_067-09-26")

#gdalwarp -dstnodata 0 -cutline new_shape_221_067-09-26.shp -crop_to_cutline -of GTiff 221_067_2017-09-26_RGB.TIF 221_067_2017-09-26_RGB.TIF
