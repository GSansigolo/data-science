from image_landsat_8 import image_landsat_8
import os, sys
import matplotlib.pyplot as plt
from osgeo import gdal, ogr
import cv2
import numpy as np


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

    dataset_before = gdal.Open(landsat_images_before.get_directory_tmp() + "B6.TIF")
    dataset_after = gdal.Open(landsat_images_after.get_directory_tmp() + "B7.TIF")

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

def save_image(data_set_path, spectral_index, directory):
    print("Salvando arquivos...")
    print data_set_path

    try:
        dataset = gdal.Open(data_set_path)
        print ("Arquivo aberto com sucesso!")
    except:
        print("Erro na abertura do arquivo!")


    geotiff = gdal.GetDriverByName('GTiff')
    dataset_output = geotiff.Create(directory, np.size(spectral_index, 1), np.size(spectral_index, 0), 1,
                                    gdal.GDT_Float32)

    dataset_output.SetGeoTransform(dataset.GetGeoTransform())
    dataset_output.SetProjection(dataset.GetProjectionRef())
    dataset_output.GetRasterBand(1).WriteArray(spectral_index)
    dataset_output.FlushCache()

    dataset_output = None

def ndvi(file_path_tar_before, file_path_tar_after, file_path_grade, directory_out):

    print ("-----------------------")
    print ("Realizando o Calculo do NDVI...")

    if not os.path.exists(directory_out + "NDVI/"):
        os.mkdir( directory_out + "NDVI/", 0755 )

    # Define o caminho dos arquivos de saida
    file_path_out_before = directory_out + "NDVI/NDVI_before.TIF"
    file_path_out_after = directory_out + "NDVI/NDVI_after.TIF"

    file_path_out_before_cut = directory_out + "NDVI/NDVI_CUT_before.TIF"
    file_path_out_after_cut = directory_out + "NDVI/NDVI_NDVI_after.TIF"

    file_path_out_dif_ndvi = directory_out + "NDVI/NDVI_diferenca.TIF"
    file_path_out_dif_rel_ndvi = directory_out + "NDVI/REL_NDVI_diferenca.TIF"

    landsat_images_before = image_landsat_8(file_path_tar_before, file_path_grade)
    landsat_images_after = image_landsat_8(file_path_tar_after, file_path_grade)

    # ----------------- REALIZA A LEITURA DAS BANDAS ------------------------- #

    band_red_before = landsat_images_before.get_band_red()
    band_nir_before = landsat_images_before.get_band_nir()

    band_red_after = landsat_images_after.get_band_red()
    band_nir_after = landsat_images_after.get_band_nir()

    # ----------------- CALCULA NDVI ------------------------- #

    band_ndvi_before = landsat_images_before.ndvi(band_red_before, band_nir_before)
    band_ndvi_after = landsat_images_after.ndvi(band_red_after, band_nir_after)

    # ----------------- SALVA NDVI ------------------------- #

    save_image(landsat_images_before.get_directory_tmp() + "B6.TIF", band_ndvi_before, file_path_out_before)
    save_image(landsat_images_after.get_directory_tmp() + "B7.TIF", band_ndvi_after, file_path_out_after)

    print "Imagens salvas!"

    # ----------------- CORTA NDVI ------------------------- #

    landsat_images_before.cut(file_path_out_before, file_path_grade, file_path_out_before_cut)
    landsat_images_after.cut(file_path_out_after, file_path_grade, file_path_out_after_cut)

    band_ndvi_before_cut = landsat_images_before.get_band(file_path_out_before_cut)
    band_ndvi_after_cut = landsat_images_after.get_band(file_path_out_after_cut)

    print("DEPOIS DE CORTAR")
    print(band_ndvi_before_cut.shape)
    print(band_ndvi_after_cut.shape)

    # ------------ CALCULA A DIFERENCA DAS BANDAS --------------- #

    print("Calculando a Diferenca.. e salvando a imagem .tif")

    dif_ndvi = (band_ndvi_after_cut - band_ndvi_before_cut)

    save_image(file_path_out_before_cut, dif_ndvi, file_path_out_dif_ndvi)

    # Calcula a diferenca relativa verificar
    rel_ndvi = dif_ndvi / abs(band_ndvi_before_cut)

    save_image(file_path_out_before_cut, rel_ndvi, file_path_out_dif_rel_ndvi)

    return "Calculo NDVI FINALIZADO"

def nbr2(file_path_tar_before, file_path_tar_after, file_path_grade, directory_out):

    return "Calculo NBR2 FINALIZADO"

def mirb(file_path_tar_before, file_path_tar_after, file_path_grade, directory_out):
    return "Calculo NBR2 FINALIZADO"


def funtios_main(argument, file_path_grade, file_path_tar_before, file_path_tar_after, directory_out):

    switcher = {
        "ndvi": ndvi,
        "nbr2": nbr2,
        "mirb": mirb,
         3: lambda: "Error",
    }
    # pega as opcoes
    func = switcher.get(argument, lambda: "nothing")
    # executa a funcao
    return func(file_path_tar_before, file_path_tar_after, file_path_grade, directory_out)

"""
    FUNCAO PRINCIPAL DA APLICACAO
"""
def main():

    # ARRUMAS PARA PATRONIzAR as ENTRADAS para NAO FICAR REPETIDAS AS FUNCOES IGUaIS ESTAO
    file_path_grade = str(sys.argv[1])
    file_path_tar_before = str(sys.argv[2])
    file_path_tar_after = str(sys.argv[3])

    function = str(sys.argv[4])

    print(os.path.dirname(os.path.realpath(__file__)) + "/build/")

    directory_out = os.path.dirname(os.path.realpath(__file__)) + "/build/"
    if not os.path.exists(directory_out):
        os.mkdir(directory_out, 0755 )

    if sys.argv < 4:
         print('To few arguments')

    saida = funtios_main("ndvi", file_path_grade, file_path_tar_before, file_path_tar_after, directory_out)

    print (saida)



    # Define o caminho dos arquivos de entrada
    # file_path_grade = "../data/grade_221_067/221_067_grade.shp"
    # file_path_tar_before = "../data/LC08_L1TP_221067_20170910_20170927_01_T1.tar.gz"
    # file_path_tar_after = "../data/LC08_L1TP_221067_20170926_20171013_01_T1.tar.gz"
    #
    # calcula_NDVI(file_path_grade,file_path_tar_before, file_path_tar_after)
    # calcula_MIRB(file_path_grade,file_path_tar_before, file_path_tar_after)


if __name__ == '__main__':
    main()
