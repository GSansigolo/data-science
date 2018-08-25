import numpy as np
from sklearn.neural_network import MLPClassifier
from osgeo import gdal, ogr

path_default = "/home/sansigolo/Downloads/"

print ("Abrindo arquivos..")
try:
	B7 = gdal.Open(path_default + "testete2.tif")
except:
	print("Erro na abertura do arquivo dataset para salvar a imagem!")

matriz_entrada = B7.GetRasterBand(1).ReadAsArray()

matriz_entrada = np.select([matriz_entrada <= 0, matriz_entrada>=1], [np.ones_like(matriz_entrada), np.full_like(matriz_entrada, 3, dtype=np.int8)])

print (matriz_entrada.shape)

# Save
filename_output = "matriz_entrada.TIF"

geotiff = gdal.GetDriverByName('GTiff')
dataset_output = geotiff.Create(filename_output, B7.RasterXSize, B7.RasterYSize, 1, gdal.GDT_Int16)
dataset_output.SetGeoTransform(B7.GetGeoTransform())
dataset_output.SetProjection(B7.GetProjectionRef())
dataset_output.GetRasterBand(1).WriteArray(matriz_entrada)
dataset_output.FlushCache()
dataset_output = None

print ("Arquivos salvo com sucesso")

