# Burn-Areas-Mask

# Imports
import matplotlib.pyplot as plt
from osgeo import gdal
from osgeo import osr
import numpy as np
import imageio
import cv2

# Open TIF
try:
	RGB = gdal.Open("RGB.TIF")
	print ("Arquivos abertos com sucesso")
except:
	print("Erro na abertura dos arquivos")
	exit()

# Read Raster Bands
NDWI_T2 = RGB.GetRasterBand(1).ReadAsArray().astype(np.float32)
NDVI_DIF = RGB.GetRasterBand(2).ReadAsArray().astype(np.float32)
BAI_T2 = RGB.GetRasterBand(3).ReadAsArray().astype(np.float32)
print ("Bandas Convertidas")

rgb = NDVI_DIF*0.6 + NDWI_T2*0.3 + BAI_T2*0.3 
rgb = np.divide(rgb, 1.32817e-18)

# Plot
plt.suptitle('rgb')
plt.imshow(rgb)
plt.colorbar()
plt.show()

# Cut
output = np.full_like(NDVI_DIF, 3, dtype=np.int8)
data_masked = np.ma.MaskedArray(output, rgb <= -0.59e17)

data_masked = np.select([data_masked != 3, data_masked == 3], [np.ones_like(data_masked), np.full_like(data_masked, 3, dtype=np.int8)])

# Plot
plt.suptitle('Mask')
plt.imshow(data_masked, cmap='gray')
plt.colorbar()
plt.show()

# Save
filename_output = "AREA_Q.TIF"
geotiff = gdal.GetDriverByName('GTiff')
dataset_output = geotiff.Create(filename_output, RGB.RasterXSize, RGB.RasterYSize, 1, gdal.GDT_Int16)
dataset_output.SetGeoTransform(RGB.GetGeoTransform())
dataset_output.SetProjection(RGB.GetProjectionRef())
dataset_output.GetRasterBand(1).WriteArray(data_masked)
dataset_output.FlushCache()
dataset_output = None
print ("Arquivos salvo com sucesso")



