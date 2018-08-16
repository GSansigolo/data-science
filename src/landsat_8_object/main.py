from image_landsat_8 import image_landsat_8
import os, sys
import matplotlib.pyplot as plt
from osgeo import gdal, ogr
import cv2
import numpy as np

def calcula_NDVI(file_path_grade,file_path_tar_before, file_path_tar_after):

    # Define o caminho dos arquivos de saida
    file_path_out_before = "../data/NDVI/NDVI_221067_20170910.TIF"
    file_path_out_after = "../data/NDVI/NDVI_221067_20170926.TIF"

    file_path_out_before_cut = "../data/NDVI/NDVI_CUT_221067_20170910.TIF"
    file_path_out_after_cut = "../data/NDVI/NDVI_NDVI_221067_20170926.TIF"

    file_path_out_dif_ndvi = "../data/NDVI/NDVI_diferenca.TIF"

    landsat_images_before = image_landsat_8(file_path_tar_before, file_path_grade)
    landsat_images_after = image_landsat_8(file_path_tar_after, file_path_grade)

    # ----------------- REALIZA A LEITURA DAS BANDAS ------------------------- #

    band_red_before = landsat_images_before.get_band_red()
    band_red_before = landsat_images_before.calculo_reflectancia(band_red_before, 58.79152871)
    band_nir_before = landsat_images_before.get_band_nir()
    band_nir_before = landsat_images_before.calculo_reflectancia(band_nir_before, 58.79152871)

    band_red_after = landsat_images_after.get_band_red()
    band_red_after = landsat_images_after.calculo_reflectancia(band_red_after, 62.61676121)
    band_nir_after = landsat_images_after.get_band_nir()
    band_nir_after = landsat_images_after.calculo_reflectancia(band_nir_after, 62.61676121)

    # ----------------- CALCULA NDVI ------------------------- #

    band_ndvi_before = landsat_images_before.ndvi(band_red_before, band_nir_before)
    band_ndvi_after = landsat_images_after.ndvi(band_red_after, band_nir_after)

    # ----------------- SALVA NDVI ------------------------- #

    dataset_before = gdal.Open(landsat_images_before.get_directory_tmp() + "B5.TIF")
    dataset_after = gdal.Open(landsat_images_after.get_directory_tmp() + "B5.TIF")

    landsat_images_before.to_img(band_ndvi_before, file_path_out_before, dataset_before.GetGeoTransform(), dataset_before.GetProjectionRef())
    landsat_images_after.to_img(band_ndvi_after, file_path_out_after, dataset_after.GetGeoTransform(), dataset_after.GetProjectionRef())

    # Corta a Imagem do NDVI
    landsat_images_before.cut(file_path_out_before, file_path_grade, file_path_out_before_cut)
    landsat_images_after.cut(file_path_out_after, file_path_grade, file_path_out_after_cut)

    band_ndvi_before_cut = landsat_images_before.get_band(file_path_out_before_cut)
    band_ndvi_after_cut = landsat_images_after.get_band(file_path_out_after_cut)

    print("DEPOIS DE CORTAR")
    print(band_ndvi_before_cut.shape)
    print(band_ndvi_after_cut.shape)

    # ------------ CALCULA A DIFERENCA DAS BANDAS --------------- #

    print("Calculando a Diferenca.. e salvando a imagem .tif")

    dataset = gdal.Open(file_path_out_before_cut)

    dif_ndvi = (band_ndvi_after_cut - band_ndvi_before_cut)
    landsat_images_after.to_img(dif_ndvi, file_path_out_dif_ndvi, dataset.GetGeoTransform(), dataset.GetProjectionRef())

    # ------ TESTE FILTROS ---- #

    # kernel = np.ones((5,5), np.float32) / 25
    # dst = cv2.filter2D(dif_ndvi, -1, kernel)
    #
    # blur_3 = cv2.blur(dif_ndvi, (3,3))
    # blur_5 = cv2.blur(dif_ndvi, (5,5))
    # median_blur_3 = cv2.medianBlur(dif_ndvi, 3)
    # median_blur_5 = cv2.medianBlur(dif_ndvi, 5)
    # gaussian_blur_3 = cv2.GaussianBlur(dif_ndvi,(3,3),0)
    # gaussian_blur_5 = cv2.GaussianBlur(dif_ndvi,(5,5),0)
    # blur_lateral = cv2.bilateralFilter(dif_ndvi, 9,75, 9,75)
    #
    # landsat_images_after.to_img(blur_3, "../data/filtros/blur_3.TIF", dataset.GetGeoTransform(), dataset.GetProjectionRef())
    # landsat_images_after.to_img(blur_5, "../data/filtros/blur_5.TIF", dataset.GetGeoTransform(), dataset.GetProjectionRef())
    # landsat_images_after.to_img(median_blur_5, "../data/filtros/median_blur_5.TIF", dataset.GetGeoTransform(), dataset.GetProjectionRef())
    # landsat_images_after.to_img(median_blur_3, "../data/filtros/median_blur_3.TIF", dataset.GetGeoTransform(), dataset.GetProjectionRef())
    # landsat_images_after.to_img(gaussian_blur_3, "../data/filtros/gaussian_blur_3.TIF", dataset.GetGeoTransform(), dataset.GetProjectionRef())
    # landsat_images_after.to_img(gaussian_blur_5, "../data/filtros/gaussian_blur_5.TIF", dataset.GetGeoTransform(), dataset.GetProjectionRef())
    # landsat_images_after.to_img(blur_lateral, "../data/filtros/blur_lateral.TIF", dataset.GetGeoTransform(), dataset.GetProjectionRef())
    # landsat_images_after.to_img(dst, "../data/filtros/dst.TIF", dataset.GetGeoTransform(), dataset.GetProjectionRef())

    # Calcula a diferenca relativa verificar
    rel_ndvi = dif_ndvi / abs(band_ndvi_before_cut)

    landsat_images_after.to_img(rel_ndvi, "../data/NDVI/NDVI_dif_relativa.TIF", dataset.GetGeoTransform(), dataset.GetProjectionRef())

def calcula_MIRB(file_path_grade,file_path_tar_before, file_path_tar_after):

    print("Calculo do MIRB...")

    # Define o caminho dos arquivos de saida
    file_path_out_before = "../data/MIRB/MIRB_221067_20170910.TIF"
    file_path_out_after = "../data/MIRB/MIRB_221067_20170926.TIF"

    file_path_out_before_cut = "../data/MIRB/MIRB_CUT_221067_20170910.TIF"
    file_path_out_after_cut = "../data/MIRB/MIRB_CUT_221067_20170926.TIF"

    file_path_out_dif = "../data/MIRB/MIRB_diferenca.TIF"

    landsat_images_before = image_landsat_8(file_path_tar_before, file_path_grade)
    landsat_images_after = image_landsat_8(file_path_tar_after, file_path_grade)

    # ----------------- REALIZA A LEITURA DAS BANDAS ------------------------- #

    band_swir_1_before = landsat_images_before.get_band_swir_1()
    band_swir_1_before = landsat_images_before.calculo_reflectancia(band_swir_1_before, 58.79152871)
    band_swir_2_before = landsat_images_before.get_band_swir_2()
    band_swir_2_before = landsat_images_before.calculo_reflectancia(band_swir_2_before, 58.79152871)

    band_swir_1_after = landsat_images_after.get_band_swir_1()
    band_swir_1_after = landsat_images_after.calculo_reflectancia(band_swir_1_after, 62.61676121)
    band_swir_2_after = landsat_images_after.get_band_swir_2()
    band_swir_2_after = landsat_images_after.calculo_reflectancia(band_swir_2_after, 62.61676121)

    # ----------------- CALCULA MIRB ------------------------- #

    band_mirb_before = landsat_images_before.mirb(band_swir_1_before,  band_swir_2_before)
    band_mirb_after = landsat_images_after.mirb(band_swir_1_after,  band_swir_2_after)

    # ----------------- SALVA MIRB ------------------------- #

    dataset_before = gdal.Open(landsat_images_before.get_directory_tmp() + "B5.TIF")
    dataset_after = gdal.Open(landsat_images_after.get_directory_tmp() + "B5.TIF")

    landsat_images_before.to_img(band_mirb_before, file_path_out_before, dataset_before.GetGeoTransform(), dataset_before.GetProjectionRef())
    landsat_images_after.to_img(band_mirb_after, file_path_out_after, dataset_after.GetGeoTransform(), dataset_after.GetProjectionRef())

    # Corta a Imagem do MIRB
    landsat_images_before.cut(file_path_out_before, file_path_grade, file_path_out_before_cut)
    landsat_images_after.cut(file_path_out_after, file_path_grade, file_path_out_after_cut)

    band_mirb_before_cut = landsat_images_before.get_band(file_path_out_before_cut)
    band_mirb_after_cut = landsat_images_after.get_band(file_path_out_after_cut)

    print("DEPOIS DE CORTAR")
    print(band_mirb_before_cut.shape)
    print(band_mirb_after_cut.shape)

    # ------------ CALCULA A DIFERENCA DAS BANDAS --------------- #

    print("Calculando a Diferenca.. e salvando a imagem .tif")

    dataset = gdal.Open(file_path_out_before_cut)

    dif_mirb = (band_mirb_after_cut - band_mirb_before_cut)
    landsat_images_after.to_img(dif_mirb, file_path_out_dif, dataset.GetGeoTransform(), dataset.GetProjectionRef())

    # Calcula a diferenca relativa verificar
    rel_ndvi = dif_mirb / abs(band_mirb_before_cut)

    landsat_images_after.to_img(rel_ndvi, "../data/MIRB/MIRB_dif_relativa.TIF", dataset.GetGeoTransform(), dataset.GetProjectionRef())



# def calcula_nbr2(file_path_grade,file_path_tar_before, file_path_tar_after):
#
#     print("Calculo do NBR2...")
#
#     # Define o caminho dos arquivos de saida
#     file_path_out_before = "../data/NBR2/NBR2_221067_20170910.TIF"
#     file_path_out_after = "../data/NBR2/NBR2_221067_20170926.TIF"
#
#     file_path_out_before_cut = "../data/NBR2/NBR2_CUT_221067_20170910.TIF"
#     file_path_out_after_cut = "../data/NBR2/NBR2_CUT_221067_20170926.TIF"
#
#     file_path_out_dif = "../data/NBR2/NBR2_diferenca.TIF"
#
#     landsat_images_before = image_landsat_8(file_path_tar_before, file_path_grade)
#     landsat_images_after = image_landsat_8(file_path_tar_after, file_path_grade)
#
#     # ----------------- REALIZA A LEITURA DAS BANDAS ------------------------- #
#
#     band_swir_1_before = landsat_images_before.get_band_swir_1()
#     band_swir_1_before = landsat_images_before.calculo_reflectancia(band_swir_1_before, 58.79152871)
#     band_swir_2_before = landsat_images_before.get_band_swir_2()
#     band_swir_2_before = landsat_images_before.calculo_reflectancia(band_swir_2_before, 58.79152871)
#
#     band_swir_1_after = landsat_images_after.get_band_swir_1()
#     band_swir_1_after = landsat_images_after.calculo_reflectancia(band_swir_1_after, 62.61676121)
#     band_swir_2_after = landsat_images_after.get_band_swir_2()
#     band_swir_2_after = landsat_images_after.calculo_reflectancia(band_swir_2_after, 62.61676121)


"""
    FUNCAO PRINCIPAL DA APLICACAO
"""
def main():

    # ARRUMAS PARA PATRONIzAR as ENTRADAS para NAO FICAR REPETIDAS AS FUNCOES IGUaIS ESTAO
    # file_path_grade = str(sys.argv[1])
    # file_path_tar_before = str(sys.argv[2])
    # file_path_tar_after = str(sys.argv[3])
    #
    # function = str(sys.argv[4])
    #
    # swith(function)
    # {
    #     case
    # }



    # Define o caminho dos arquivos de entrada
    file_path_grade = "../data/grade_221_067/221_067_grade.shp"
    file_path_tar_before = "../data/LC08_L1TP_221067_20170910_20170927_01_T1.tar.gz"
    file_path_tar_after = "../data/LC08_L1TP_221067_20170926_20171013_01_T1.tar.gz"

    calcula_NDVI(file_path_grade,file_path_tar_before, file_path_tar_after)
    calcula_MIRB(file_path_grade,file_path_tar_before, file_path_tar_after)


if __name__ == '__main__':
    main()
