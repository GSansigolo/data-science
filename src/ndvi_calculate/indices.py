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

def salva_arquivo(array_ndvi, dataset_nir):

    filename_output = "LC08_L1TP_223067_20180303_20180319_01_T1_NDVI.TIF"
    geotiff = gdal.GetDriverByName('GTiff')
    dataset_output = geotiff.Create(filename_output, dataset_nir.RasterXSize, dataset_nir.RasterYSize, 1, gdal.GDT_Float32)
    dataset_output.SetGeoTransform(dataset_nir.GetGeoTransform())
    dataset_output.SetProjection(dataset_nir.GetProjectionRef())
    dataset_output.GetRasterBand(1).WriteArray(array_ndvi)
    dataset_output.FlushCache()

    dataset_output = None

def ndvi_calculate(array_nir, array_red):
    # Realiza o calculo do NDVI
    array_ndvi = (array_nir - array_red) / (array_nir + array_red)
    print(array_ndvi.shape)

    return array_ndvi

def reflectance_calculate(mascara):
    refmcoefs = 0.00002
    refacoefs = -0.1
    elevation = 58.75905587

    # tem que ler o arquivo de metadados da imagem para pegar esse valor
    # SUN_ELEVATION = 58.75905587

    return (np.ma.masked_equal(mascara, 0) * refmcoefs + refacoefs) * (1 / math.sin(math.radians(elevation)) )

path = "/home/rafael/Desktop/dados_queimadas/landsat_8/tmp_LC08_L1TP_221067_20170926_20171013_01_T1/"

filename_nir =path+"LC08_L1TP_221067_20170926_20171013_01_T1_B5.TIF"
filename_red = path+"LC08_L1TP_221067_20170926_20171013_01_T1_B3.TIF"



try:
    dataset_nir = gdal.Open(filename_nir)
    dataset_red = gdal.Open(filename_red)
    print ("Arquivos aberto com sucesso!")
except:
    print("Erro na abertura dos arquivo!")
    exit()


# Realiza a leitura das bandas
band_nir = dataset_nir.GetRasterBand(1)
band_red = dataset_red.GetRasterBand(1)


# Mostra os tipos de dados




# Transfoma em um array numpy para realizar as operacoes

array_red = band_red.ReadAsArray().astype(np.float64)
array_nir = band_nir.ReadAsArray().astype(np.float64)

# realiza o calcula da reflectancia. algumas imagens ja possuem a reflectancia calculada
# array_red_ref = reflectance_calculate(array_red)
# array_nir_ref = reflectance_calculate(array_nir)

# permite a divisao por zero
np.seterr(divide='ignore', invalid='ignore')

array_ndvi = ndvi_calculate(array_red, array_nir)
array_ndvi = array_ndvi.astype(np.float32)


# salva_arquivo(array_ndvi, dataset_nir)
#
plt.imshow(array_ndvi, cmap='RdYlGn')
plt.colorbar()
plt.show()
