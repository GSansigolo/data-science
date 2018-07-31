from image_landsat_8 import image_landsat_8
from osgeo import gdal
import matplotlib.pyplot as plt


landsat_images = image_landsat_8("../data/LC08_L1TP_221067_20170926_20171013_01_T1.tar.gz")

band_red = landsat_images.get_band_red()
band_nir = landsat_images.get_band_nir()

file_path_out = "../data/OUT_NDVI.TIF"
dataset_nir = gdal.Open(landsat_images.get_directory_tmp() + "B5.TIF")

landsat_images.ndvi_to_img(landsat_images.ndvi(band_red, band_nir), file_path_out, dataset_nir.GetGeoTransform(),
                dataset_nir.GetProjectionRef())


# plt.imshow(landsat_images.ndvi(band_red, band_nir), cmap='RdYlGn')
# plt.colorbar()
# plt.show()
