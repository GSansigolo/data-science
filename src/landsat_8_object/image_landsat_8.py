import os
import tarfile
import numpy as np
# from fiona._err import GDALError
from osgeo import gdal
import re
import matplotlib.pyplot as plt
import shutil
import math


class image_landsat_8:

    def __init__(self, filepath, grid_file=None):
        np.seterr(divide='ignore', invalid='ignore')
        self.file_directory = os.path.dirname(filepath)
        self.compact_file_name = os.path.basename(filepath)
        regex = re.search("(.*?).((tar.gz)|(zip))", os.path.basename(filepath))
        self.compressed_file_name = regex.group(1)
        self.compressed_type = regex.group(2)


        try:
            file_tmp = self.file_directory + "/tmp_" + self.compressed_file_name
            # os.makedirs(file_tmp)
            self.directory_tmp = file_tmp + "/"
        except OSError:
            raise

        # self.__zip_descomp__(filepath, self.directory_tmp, self.compressed_type)
        self.pattern_path = self.directory_tmp + self.compressed_file_name + "_"
        # if(grid_file != None):
            # self.__cut__(self.directory_tmp, grid_file)

    # def __del__(self):
    #     shutil.rmtree(self.directory_tmp)

    def __cut__(self, directory, grid_file):
        print("Cortando os arquivos..")
        for file in os.listdir(directory):
            regex = re.search("(.*).TIF$", file)
            if (regex != None):
                self.__cut_gdal__(grid_file, directory + file, directory + regex.group(1) + "_CUT.TIF")

    def __cut_gdal__(self, grid_file, tiff_file, new_tiff_file):
       os.system("gdalwarp -overwrite -q -cutline " + grid_file
                  + " -crop_to_cutline -tr 30.0 30.0 " + tiff_file + " " + new_tiff_file)

    def cut(self, banda, grid_file, new_tiff_file):
        self.__cut_gdal__(grid_file, banda, new_tiff_file)

    def __zip_descomp__(self, compressed_path, tmp_dir, compressed_type):

        # if(compressed_type == "tar.gz")
        print("Descompactando...")
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

    def get_band_swir_1(self):
        obj_gdal = gdal.Open(self.pattern_path + "B6.TIF")
        return obj_gdal.GetRasterBand(1).ReadAsArray()

    def get_band_swir_2(self):
        obj_gdal = gdal.Open(self.pattern_path + "B7.TIF")
        return obj_gdal.GetRasterBand(1).ReadAsArray()

    def get_band(self, path):
        obj_gdal = gdal.Open(path)
        return obj_gdal.GetRasterBand(1).ReadAsArray()

    def get_raster_min_max(self, band):
        return band.ComputeRasterMinMax()
        # try:
        #     return band.ComputeRasterMinMax()
        # except GDALError:
        #     raise ("BAND IS OBJECT GDAL?")

    def size_of_band(self, band):
        return "Size is {} x {} x {}".format(band.RasterXSize,
                                             band.RasterYSize, band.RasterCount)

    # def mirb(self):
    #     return ((10 * self.get_band_swir_2()) -\
    #            (9.8 * self.get_band_swir_1()) + 2)

    def mirb(self, band_swir_1, band_swir_2):
        return (10 * band_swir_2) - (9.8 * band_swir_1) + 2

    # def ndvi(self):
    #     band_red = self.get_band_red().astype(np.float64)
    #     band_nir = self.get_band_nir().astype(np.float64)
    #
    #     return ((band_nir - band_red) / (band_nir + band_red)).astype(np.float32)

    def ndvi(self, band_red, band_nir):

        band_red = band_red.astype(np.float32)
        band_nir = band_nir.astype(np.float32)

        # return ((band_nir - band_red) / (band_nir + band_red))
        # return ((band_nir - band_red) / (band_nir + band_red)).astype(np.uint32)

        return np.ma.divide((band_nir - band_red), (band_nir + band_red)  )

    def to_img(self, spectral_index, directory, geotransform, projection):

        self.__save_file__(spectral_index, directory ,geotransform, projection)


    def __save_file__(self, spectral_index, directory, geotransform, projection):

        print("Salvando arquivos...")


        geotiff = gdal.GetDriverByName('GTiff')
        dataset_output = geotiff.Create(directory, np.size(spectral_index, 1), np.size(spectral_index, 0), 1,
                                        gdal.GDT_Float32)



        dataset_output.SetGeoTransform(geotransform)
        dataset_output.SetProjection(projection)
        dataset_output.GetRasterBand(1).WriteArray(spectral_index)
        dataset_output.FlushCache()

        dataset_output = None

    def plot_image(self, band):

        plt.imshow(band, cmap='RdYlGn')
        plt.colorbar()
        plt.show()

    def calculo_reflectancia(self, mascara, elevation):
        refmcoefs = 0.00002
        refacoefs = -0.1

        return (
               np.ma.masked_equal(
                   mascara, 0
               ) * refmcoefs + refacoefs
           ) * (
               1 / math.sin(math.radians(elevation))
           )
