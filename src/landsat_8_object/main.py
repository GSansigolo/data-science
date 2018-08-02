from image_landsat_8 import image_landsat_8
from osgeo import gdal


landsat_images_before = image_landsat_8("../data/LC08_L1TP_221067_20170910_20170927_01_T1.tar.gz",
                                        "../data/grade_221_067/221_067_grade.shp")

landsat_images_after = image_landsat_8("../data/LC08_L1TP_221067_20170926_20171013_01_T1.tar.gz",
                                        "../data/grade_221_067/221_067_grade.shp")

band_red_before = landsat_images_before.get_band_red()
band_nir_before = landsat_images_before.get_band_nir()

band_red_after = landsat_images_after.get_band_red()
band_nir_after = landsat_images_after.get_band_nir()

print("Antes do NDVI")
print("BEFORE")
print(band_red_before.shape)
print(band_nir_before.shape)
print("AFTER")
print(band_red_after.shape)
print(band_nir_after.shape)

# ----------------- CALCULATE NDVI IMAGE ------------------------- #

band_ndvi_before = landsat_images_before.ndvi(band_red_before, band_nir_before)
band_ndvi_after = landsat_images_after.ndvi(band_red_after, band_nir_after)

print("Depois do NDVI")
print("BEFORE")
print(band_ndvi_before.shape)
print("AFTER")
print(band_ndvi_after.shape)

# TO DO
# dif_band = (band_ndvi_after - band_ndvi_before)
# dif_band2 = (band_ndvi_before - band_ndvi_after)

file_path_out = "../data/OUT_NDVI_BEFORE32.TIF"
dataset = gdal.Open(landsat_images_before.get_directory_tmp() + "B5.TIF")

landsat_images_before.to_img(band_ndvi_before, file_path_out, dataset.GetGeoTransform(),
                dataset.GetProjectionRef())

file_path_out = "../data/OUT_NDVI_AFTER32.TIF"

landsat_images_after.to_img(band_ndvi_after, file_path_out, dataset.GetGeoTransform(),
                dataset.GetProjectionRef())

landsat_images_before.cut(file_path_out, "../data/grade_221_067/221_067_grade.shp", "../data/OUT_NDVI_AFTER_CUT32.TIF")

landsat_images_after.cut(file_path_out, "../data/grade_221_067/221_067_grade.shp", "../data/OUT_NDVI_AFTER_CUT32.TIF")

#
# landsat_images_after.plot_image(dif_band)
# landsat_images_after.plot_image(dif_band2)
