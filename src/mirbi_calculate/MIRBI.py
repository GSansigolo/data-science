from osgeo import gdal
from osgeo import osr
from gdalconst import *
import os
import sys
import re
import tarfile
import numpy as np
import matplotlib.pyplot as plt
import math

#change to dinamic
dir = "/home/sansigolo/Documents/git/CAP-240-394/"

#tar = tarfile.open(dir+'LC08_L1TP_221067_20170926_20171013_01_T1.tar.gz', "r:gz")

try:
	B6 = gdal.Open(dir+'LC08_L1TP_221067_20170926_20171013_01_T1_B6.TIF')
	B7 = gdal.Open(dir+'LC08_L1TP_221067_20170926_20171013_01_T1_B7.TIF')
	print ("Arquivos aberto com sucesso!")
except:
	print("Erro na abertura dos arquivo!")
	exit()

# Read the raster band as separate variable
band_6 = B6.GetRasterBand(1)
band_7 = B7.GetRasterBand(1)

# Data type of the values
print ("Tipos de dados:")
print('B6: ', gdal.GetDataTypeName(band_6.DataType))
print('B7: ', gdal.GetDataTypeName(band_7.DataType))

# Transfoma em um array numpy
array_B6 = band_6.ReadAsArray()
array_B7 = band_7.ReadAsArray()

array_MIRBI = (10*array_B7)-(9.8*array_B6)+2

print(array_MIRBI.shape)

plt.imshow(array_MIRBI, cmap='RdYlGn')
plt.colorbar()
plt.show()
plt.show()
