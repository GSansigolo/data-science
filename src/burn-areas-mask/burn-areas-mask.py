# Burn-Areas-Mask

# Imports
import matplotlib.pyplot as plt
from osgeo import gdal
from osgeo import osr
import numpy as np
import imageio
import cv2

try:
	B1 = gdal.Open("data-in/diferenca_NDVI.TIF")
	print ("Arquivos aberto com sucesso")
except:
	print("Erro na abertura dos arquivo")
	exit()

# Read Raster Bands
band_1 = B1.GetRasterBand(1)

# Trasform in Numpy Array
array_B1 = band_1.ReadAsArray().astype(np.float32)
print ("Bandas Convertidas")

# Plot
plt.imshow(array_B1, cmap='RdYlGn')
plt.colorbar()
plt.show()

# Convert to Float32
img = imageio.imwrite('outfile.jpg', array_B1)
img = cv2.imread('outfile.jpg')
Z = img.reshape((-1,3))
Z = np.float32(Z)

print ("Iniciado o Machine Learning")

# Define and Apply KMeans()
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 5
ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

print ("Terminado o Machine Learning")

# Make the Image
center = np.uint8(center)
res = center[label.flatten()]
res2 = res.reshape((img.shape))

# Plot
plt.imshow(res2, cmap='gray')
plt.colorbar()
plt.show()

# Mask
lower_cloud = np.array([55,55,55])
upper_cloud = np.array([63,63,63])

# Cut
mask = cv2.inRange(res2, lower_cloud, upper_cloud)
img = imageio.imwrite('outfile.jpg', mask)

# Plot
plt.imshow(mask, cmap='gray')
plt.colorbar()
plt.show()

# Fix
mask = np.select([mask <= 0, mask>=1], [np.ones_like(mask), np.full_like(mask, 3, dtype=np.int8)])

# Save
filename_output = "data-out/NDVI_Q.TIF"
geotiff = gdal.GetDriverByName('GTiff')
dataset_output = geotiff.Create(filename_output, B1.RasterXSize, B1.RasterYSize, 1, gdal.GDT_Int16)
dataset_output.SetGeoTransform(B1.GetGeoTransform())
dataset_output.SetProjection(B1.GetProjectionRef())
dataset_output.GetRasterBand(1).WriteArray(mask)
dataset_output.FlushCache()
dataset_output = None
print ("Arquivos salvo com sucesso")
