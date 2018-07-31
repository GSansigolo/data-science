from image_landsat_8 import image_landsat_8
from osgeo import gdal


landsat_images_before = image_landsat_8("../data/LC08_L1TP_221067_20170910_20170927_01_T1.tar.gz")
landsat_images_after = image_landsat_8("../data/LC08_L1TP_221067_20170926_20171013_01_T1.tar.gz")

band_red_before = landsat_images_before.get_band_red()
band_nir_before = landsat_images_before.get_band_nir()

band_red_after = landsat_images_after.get_band_red()
band_nir_after = landsat_images_after.get_band_nir()

# ----------------- CALCULATE NDVI IMAGE ------------------------- #

band_ndvi_before = landsat_images_before.ndvi(band_red_before, band_nir_before)
band_ndvi_after = landsat_images_after.ndvi(band_red_after, band_nir_after)

print(band_ndvi_before.shape)
print(band_ndvi_after.shape)

# TO DO
# dif_band = (band_ndvi_after - band_ndvi_before)
# dif_band2 = (band_ndvi_before - band_ndvi_after)

# file_path_out = "../data/OUT_NDVI.TIF"
# dataset_nir = gdal.Open(landsat_images.get_directory_tmp() + "B5.TIF")
#
# landsat_images.ndvi_to_img(band_ndvi, file_path_out, dataset_nir.GetGeoTransform(),
#                 dataset_nir.GetProjectionRef())

#
# landsat_images_after.plot_image(dif_band)
# landsat_images_after.plot_image(dif_band2)
