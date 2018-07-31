import os
import tarfile
import numpy as np
# from fiona._err import GDALError
from osgeo import gdal
import re
import shutil
import matplotlib.pyplot as plt

class image_landsat_8:

    def __init__(self, filepath):
        np.seterr(divide='ignore', invalid='ignore')
        self.file_directory = os.path.dirname(filepath)
        self.compact_file_name = os.path.basename(filepath)
        regex = re.search("(.*?).((tar.gz)|(zip))", os.path.basename(filepath))
        self.compressed_file_name = regex.group(1)
        self.compressed_type = regex.group(2)

        try:
            file_tmp = self.file_directory + "/tmp_" + self.compressed_file_name
            os.makedirs(file_tmp)
            self.directory_tmp = file_tmp
        except OSError:
            raise

        self.__zip_descomp__(filepath, self.directory_tmp, self.compressed_type)
        self.pattern_path = self.directory_tmp + "/" + self.compressed_file_name + "_"


    def __del__(self):
        shutil.rmtree(self.directory_tmp)

    def __zip_descomp__(self, compressed_path, tmp_dir, compressed_type):

        # if(compressed_type == "tar.gz")
        tar = tarfile.open(compressed_path)
        tar.extractall(tmp_dir)
        tar.close()

    def get_directory_tmp(self):
        return self.pattern_path

    def get_band_nir(self):
        obj_gdal = gdal.Open(self.pattern_path + "B5.TIF")
        return obj_gdal.GetRasterBand(1).ReadAsArray()

    def get_band_red(self):
        obj_gdal = gdal.Open(self.pattern_path + "B4.TIF")
        return obj_gdal.GetRasterBand(1).ReadAsArray()

    def get_band_6(self):
        return gdal.Open(self.pattern_path + "B6.TIF").GetRasterBand(1)

    def get_band_7(self):
        return gdal.Open(self.pattern_path + "B7.TIF").GetRasterBand(1)

    def get_raster_min_max(self, band):
        return band.ComputeRasterMinMax()
        # try:
        #     return band.ComputeRasterMinMax()
        # except GDALError:
        #     raise ("BAND IS OBJECT GDAL?")

    def size_of_band(self, band):
        return "Size is {} x {} x {}".format(band.RasterXSize,
                                             band.RasterYSize, band.RasterCount)

    def ndvi(self, band_red, band_nir):

        band_red = band_red.astype(np.float64)
        band_nir = band_nir.astype(np.float64)

        return ((band_nir - band_red) / (band_nir + band_red)).astype(np.float32)


    def ndvi_to_img(self, array_ndvi, directory, geotransform,
                    projection):


        self.__save_file__(array_ndvi, directory, geotransform, projection)


    def __save_file__(self, array_ndvi, directory, geotransform, projection):

        geotiff = gdal.GetDriverByName('GTiff')
        dataset_output = geotiff.Create(directory, np.size(array_ndvi, 1), np.size(array_ndvi, 0), 1,
                                        gdal.GDT_Float32)

        dataset_output.SetGeoTransform(geotransform)
        dataset_output.SetProjection(projection)
        dataset_output.GetRasterBand(1).WriteArray(array_ndvi)
        dataset_output.FlushCache()

        dataset_output = None

    def plot_image(self, band):

        plt.imshow(band, cmap='RdYlGn')
        plt.colorbar()
        plt.show()
