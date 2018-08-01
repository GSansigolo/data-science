## Cloud-Mask
# Unsupervised machine learning approach to create a cloud-mask using images from Landsat 8 Satellite. 

# Imports
import matplotlib.pyplot as plt
from osgeo import gdal
import numpy as np
import imageio
import cv2

# Get the Tifs
dir = "/home/sansigolo/Documents/git/CAP-240-394/"

try:
	B3 = gdal.Open(dir+'LC08_L1TP_221067_20170113_20170311_01_T1_B3_C.TIF')
	B4 = gdal.Open(dir+'LC08_L1TP_221067_20170113_20170311_01_T1_B4_C.TIF')
	B5 = gdal.Open(dir+'LC08_L1TP_221067_20170113_20170311_01_T1_B5_C.TIF')
	print ("Arquivos aberto com sucesso!")
except:
	print("Erro na abertura dos arquivo!")
	exit()

# Read the raster band as separate variable
band_3 = B3.GetRasterBand(1)
band_4 = B4.GetRasterBand(1)
band_5 = B5.GetRasterBand(1)

# Trasform in numpy array
array_B3 = band_3.ReadAsArray().astype(np.float32)
array_B4 = band_4.ReadAsArray().astype(np.float32)
array_B5 = band_5.ReadAsArray().astype(np.float32)


# Create a fake-color band
img = array_B3 + array_B4 + array_B5
warnings.filterwarnings(action='once')
img = imageio.imwrite('outfile.jpg', img)
img = cv2.imread('outfile.jpg')
Z = img.reshape((-1,3))


# Convert to np.float32
Z = np.float32(Z)

# Define criteria, number of clusters(K) and apply kmeans()
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 4
ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

# Now convert back into uint8, and make original image
center = np.uint8(center)
res = center[label.flatten()]
res2 = res.reshape((img.shape))

# Set the mask lower and upper
lower_cloud = np.array([51,51,51])
upper_cloud = np.array([149,149,149])

# Cut the image with mask
mask = cv2.inRange(res2, lower_cloud, upper_cloud)

# Plot
plt.imshow(mask, cmap='RdYlGn')
plt.colorbar()
plt.show()

