'''
Created on Jul 24, 2018
Author: @G_Sansigolo
'''
from osgeo import gdal
import matplotlib.pyplot as plt
import numpy as np
from numpy import *
import pandas as pd
from os import listdir

mypath = "/home/sansigolo/Documents/git/CAP-240-394/data-tif/"

filenames = [y for y in listdir(mypath) for ending in ['TIF','tif'] if y.endswith(ending)] 

df = pd.DataFrame(columns=['Filename','ReadAsArray'])

for filenames in filenames:

	try:
		tif = gdal.Open(mypath+filenames)
	except:
		print('The file does not exist.')

	array = tif.ReadAsArray()

	print('['+filenames+']')

	df = df.append({'Filename': filenames, 'ReadAsArray': array}, ignore_index=True)

print(df.tail())

