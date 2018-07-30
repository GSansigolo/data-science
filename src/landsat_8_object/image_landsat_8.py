import os
import tarfile
import numpy as np
from fiona._err import GDALError
from osgeo import gdal
import re
import shutil


class image_landsat_8:

    def __init__(self, filepath):
        self.file_directory = os.path.dirname(filepath)
        # self.compact_file_name = os.path.basename(filepath)
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



    def get_band_nir(self):
        return gdal.Open(self.pattern_path + "B5.TIFF").GetRasterBand(1)


    def get_band_red(self):
        return gdal.Open(self.pattern_path + "B3.TIFF").GetRasterBand(1)


    def get_band_6(self):
        return gdal.Open(self.pattern_path + "B6.TIFF").GetRasterBand(1)

    def get_band_7(self):
        return gdal.Open(self.pattern_path + "B7.TIFF").GetRasterBand(1)



    def get_raster_min_max(self, band):
        try:
            return band.ComputeRasterMinMax()
        except GDALError:
            raise ("BAND IS OBJECT GDAL?")


    def size_of_band(self, band):
        return "Size is {} x {} x {}".format(band.RasterXSize,
                                             band.RasterYSize, band.RasterCount)


    def ndvi(self, band_red = get_band_red(), band_nir = get_band_nir()):
        array_red = band_red.ReadAsArray().astype(np.float64)
        array_nir = band_nir.ReadAsArray().astype(np.float64)

        return (array_nir - array_red) / (array_nir + array_red)


    def ndvi_to_img(self, array_ndvi, directory, geotransform = get_band_nir().GetGeoTransform(),
                                                 projection = get_band_nir().GetProjectionRef()):

        self.__save_file__(array_ndvi.astype(np.float32), directory, geotransform, projection)



    def __save_file__(self, array_ndvi, directory, geotransform, projection):

        geotiff = gdal.GetDriverByName('GTiff')
        dataset_output = geotiff.Create(directory, np.size(array_ndvi,1),np.size(array_ndvi, 0), 1,
                                        gdal.GDT_Float32)

        dataset_output.SetGeoTransform(geotransform)
        dataset_output.SetProjection(projection)
        dataset_output.GetRasterBand(1).WriteArray(array_ndvi)
        dataset_output.FlushCache()



# a = image_landsat_8("/home/rafael/Desktop/dados_queimadas" \
#                     "/landsat_8/LC08_L1TP_221067_" \
#                     "20170926_20171013_01_T1.tar.gz")

# def reflectance_calculate(self, mascara):
#     refmcoefs = 0.00002
#     refacoefs = -0.1
#     elevation = get_sum_elevation()
#     # elevation = 58.75905587
#
#     # tem que ler o arquivo de metadados da imagem para pegar esse valor
#     # SUN_ELEVATION = 58.75905587
#
#     return (np.ma.masked_equal(mascara, 0) * refmcoefs + refacoefs) * (1 / math.sin(math.radians(elevation)))

# def reflectance_calculate(mascara):
#     refmcoefs = 0.00002
#     refacoefs = -0.1
#     elevation = get_sum_elevation()
#     # elevation = 58.75905587

# def get_band_5(self):
#    # dataset_nir = gdal.Open(self.archive.)
