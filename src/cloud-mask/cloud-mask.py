# Cloud-Mask
# Unsupervised machine learning to create a cloud-mask using images from Landsat 8 Satellite. 

# Imports
import matplotlib.pyplot as plt
from osgeo import gdal
from osgeo import osr
import numpy as np
import imageio
import cv2

# Get the Tifs
dir = "/home/sansigolo/Documents/git/CAP-240-394/"

try:
	B6 = gdal.Open(dir+'LC08_L1TP_221067_20170926_20171013_01_T1_B6.TIF')
	B3 = gdal.Open(dir+'LC08_L1TP_221067_20170113_20170311_01_T1_B3_C.TIF')
	B4 = gdal.Open(dir+'LC08_L1TP_221067_20170113_20170311_01_T1_B4_C.TIF')
	B5 = gdal.Open(dir+'LC08_L1TP_221067_20170113_20170311_01_T1_B5_C.TIF')
	print ("Arquivos aberto com sucesso!")
except:
	print("Erro na abertura dos arquivo!")
	exit()


# Read Raster Bands
band_3 = B3.GetRasterBand(1)
band_4 = B4.GetRasterBand(1)
band_5 = B5.GetRasterBand(1)

# Trasform in Numpy Array
array_B3 = band_3.ReadAsArray().astype(np.float32)
array_B4 = band_4.ReadAsArray().astype(np.float32)
array_B5 = band_5.ReadAsArray().astype(np.float32)

# Create Fake-Color Band
img = array_B3 + array_B4 + array_B5 
img = imageio.imwrite('outfile.jpg', img)
img = cv2.imread('outfile.jpg')
Z = img.reshape((-1,3))

# Convert to Float32
Z = np.float32(Z)

# Define and Apply KMeans()
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 4
ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

# Make the Image
center = np.uint8(center)
res = center[label.flatten()]
res2 = res.reshape((img.shape))

# Set Mask
lower_cloud = np.array([51,51,51])
upper_cloud = np.array([149,149,149])

# Cut
mask = cv2.inRange(res2, lower_cloud, upper_cloud)
img = imageio.imwrite('outfile.jpg', mask)

# Plot
plt.imshow(mask, cmap='gray')
plt.colorbar()
plt.show()

# set geotransform
image_size = mask.shape
print("image_size: "+str(image_size[0])+","+str(image_size[1]))
nx = image_size[0]
ny = image_size[1]
width = B3.RasterXSize
height = B3.RasterYSize
print("width, height: "+str(width)+", "+str(height))
gt = B3.GetGeoTransform()
print("gt: "+str(gt))
minx = gt[0]
miny = gt[3] + width*gt[4] + height*gt[5] 
maxx = gt[0] + width*gt[1] + height*gt[2]
maxy = gt[3] 
print("minx, miny, maxx, maxy: "+str(minx)+", "+str(miny)+", "+str(maxx)+", "+str(maxy))
xres = (maxx - minx) / float(nx)
yres = (maxy - miny) / float(ny)
geotransform = (minx, xres, 0, maxy, 0, -yres)

# create the 3-band raster file
dst_ds = gdal.GetDriverByName('GTiff').Create('cloud-mask.tif', ny, nx, 1, gdal.GDT_Byte)

dst_ds.SetGeoTransform(geotransform)    # specify coords
srs = osr.SpatialReference()            # establish encoding
srs.ImportFromEPSG(4326)                # WGS84 lat/long
dst_ds.SetProjection(srs.ExportToWkt()) # export coords to file
dst_ds.GetRasterBand(1).WriteArray(mask)   # write r-band to the raster
dst_ds.FlushCache()                     # write to disk
dst_ds = None


