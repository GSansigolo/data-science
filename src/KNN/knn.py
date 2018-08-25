# Burn-Areas KNN

# Imports
import matplotlib.pyplot as plt
from osgeo import gdal
from osgeo import osr
import numpy as np
from math import sqrt
import matplotlib.pyplot as plt
import warnings
from collections import Counter
from matplotlib import style

# KNN
def k_nearest_neighbors(data, predict, k=3):
	if len(data) >= k:
		warnings.warn('K is set to a value less the total')
	distances = []
	for group in data:
		for features in data[group]:
			euclidean_distance = np.linalg.norm(np.array(features)-np.array(predict))
			distances.append([euclidean_distance, group])
	votes = [i[1] for i in sorted(distances) [:k]]
	votes_result = Counter(votes).most_common(1)[0][0]
	return votes_result

# Open tifs
try:
	RGB = gdal.Open("RGB.TIF")
	MASK = gdal.Open("MASK.TIF")
	print ("Arquivos aberto com sucesso")
except:
	print("Erro na abertura dos arquivo")
	exit()

# Read the tifs
NBR2 = RGB.GetRasterBand(1).ReadAsArray()
MIRB = RGB.GetRasterBand(2).ReadAsArray()
NDVI = RGB.GetRasterBand(3).ReadAsArray()

# Read the mask
MASK = MASK.GetRasterBand(1).ReadAsArray()

# Create output array
OUTPUT = np.array([])
TRAIN = {"queimada":[], "nao-queimada":[]}

# For loop to Train
for i in range(int(RGB.RasterXSize*0.025)):
	for j in range(int(RGB.RasterYSize*0.025)):
		last_i, last_j = i, j
		if MASK[i][j] == 2:
			TRAIN["queimada"].append([NBR2[i][j], MIRB[i][j], NDVI[i][j]])
		else:
			TRAIN["nao-queimada"].append([NBR2[i][j], MIRB[i][j], NDVI[i][j]])
					
# For loop to test Test
for i in range(int(RGB.RasterXSize*0.005)):
	for j in range(int(RGB.RasterYSize*0.005)):
		teste = NBR2[last_i+i][last_j+j], MIRB[last_i+i][last_j+j], NDVI[last_i+i][last_j+j]
		if MASK[i][j] == 2:
			print(k_nearest_neighbors(TRAIN, [teste], k=3)+' - '+'queimada')		
		else:		
			print(k_nearest_neighbors(TRAIN, [teste], k=3)+' - '+'nao-queimada')


