# Cloud-Mask
# Unsupervised machine learning to create a cloud-mask using images from Landsat 8 Satellite. 

# Imports
import matplotlib.pyplot as plt
from osgeo import gdal
from osgeo import osr
import numpy as np

try:
	B1 = gdal.Open('cluster_NDVI3_.TIF')
	print ("Arquivos aberto com sucesso!")
except:
	print("Erro na abertura dos arquivo")
	exit()


# Read Raster Bands
band_1 = B1.GetRasterBand(1)

# Trasform in Numpy Array
array_B1 = band_1.ReadAsArray().astype(np.float32)
print ("Bandas Convertidas")

# Plot
plt.suptitle('array_B1')
plt.imshow(array_B1, cmap='gray')
plt.colorbar()
plt.show()

output = np.ones_like(array_B1)
data_masked = np.ma.MaskedArray(output, array_B1 == 0)

data_masked = np.select([data_masked != 1, data_masked == 3], [np.ones_like(data_masked), np.full_like(data_masked, 3, dtype=np.int8)])

mask = np.select([data_masked <= 0, data_masked>=1], [np.ones_like(data_masked), np.full_like(data_masked, 3, dtype=np.int8)])

# Plot
plt.suptitle('Mask')
plt.imshow(mask, cmap='gray')
plt.colorbar()
plt.show()

# Save
filename_output = "AREA_Q.TIF"
geotiff = gdal.GetDriverByName('GTiff')
dataset_output = geotiff.Create(filename_output, B1.RasterXSize, B1.RasterYSize, 1, gdal.GDT_Int16)
dataset_output.SetGeoTransform(B1.GetGeoTransform())
dataset_output.SetProjection(B1.GetProjectionRef())
dataset_output.GetRasterBand(1).WriteArray(mask)
dataset_output.FlushCache()
dataset_output = None
print ("Arquivos salvo com sucesso")



