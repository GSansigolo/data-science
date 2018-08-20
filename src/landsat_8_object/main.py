from image_landsat_8 import image_landsat_8
import os, sys
import matplotlib.pyplot as plt
from osgeo import gdal, ogr
import cv2
import numpy as np


def save_image(data_set_path, spectral_index, directory):
    print("Salvando arquivo...")

    try:
        dataset = gdal.Open(data_set_path)
    except:
        print("Erro na abertura do arquivo dataset para salvar a imagem!")

    geotiff = gdal.GetDriverByName('GTiff')
    dataset_output = geotiff.Create(directory, np.size(spectral_index, 1), np.size(spectral_index, 0), 1,
                                    gdal.GDT_Float32)

    dataset_output.SetGeoTransform(dataset.GetGeoTransform())
    dataset_output.SetProjection(dataset.GetProjectionRef())
    dataset_output.GetRasterBand(1).WriteArray(spectral_index)
    dataset_output.FlushCache()

    dataset_output = None

def indice_calculate(indice, file_path_tar, file_path_grade, directory_out):

    print ("-----------------------")
    print ("Realizando o Calculo do INDICE " + indice)

    if not os.path.exists(directory_out + indice + "/"):
        os.mkdir( directory_out + indice + "/", 0755 )

    # Define o caminho dos arquivos de saida
    indice_path = directory_out +  indice + "/"+ indice

    file_path_out = indice_path +  "_data" + "_.TIF"

    file_path_out_cut = indice_path +  "data_CUT" + "_.TIF"

    # file_path_out_dif_ndvi = indice_path + "_diferenca.TIF"
    # file_path_out_dif_rel_ndvi = indice_path +   "_REL_diferenca.TIF"

    landsat_images = image_landsat_8(file_path_tar, file_path_grade)

    # ----------------- CALCULA INDICE ------------------------- #

    if indice == "NDVI":
        band = landsat_images.ndvi()
    elif indice == "MIRB":
        band = landsat_images.mirb()
    elif indice == "NBR2":
        band = landsat_images.nbr2()
    else:
        print ("Opcao de indice errado")
        exit()

    # ----------------- SALVA IMAGEM ------------------------- #

    save_image(landsat_images.get_directory_tmp() + "B6.TIF", band, file_path_out)

    print "Imagem salva!"

    # ----------------- CORTA IMAGEM ------------------------- #
    #
    landsat_images.cut(file_path_out, file_path_grade, file_path_out_cut)
    # landsat_images_after.cut(file_path_out_after, file_path_grade, file_path_out_after_cut)
    #
    band_cut = landsat_images.get_band(file_path_out_cut)
    # band_ndvi_after_cut = landsat_images_after.get_band(file_path_out_after_cut)
    #
    print("DEPOIS DE CORTAR")
    print(band_cut.shape)

    #
    # # ------------ CALCULA A DIFERENCA DAS BANDAS --------------- #
    #
    # print("Calculando a Diferenca.. e salvando a imagem .tif")
    #
    # dif_ndvi = (band_ndvi_after_cut - band_ndvi_before_cut)
    #
    # save_image(file_path_out_before_cut, dif_ndvi, file_path_out_dif_ndvi)
    #
    # # Calcula a diferenca relativa verificar
    # rel_ndvi = dif_ndvi / abs(band_ndvi_before_cut)
    #
    # save_image(file_path_out_before_cut, rel_ndvi, file_path_out_dif_rel_ndvi)

    print( "Calculo " + indice + " FINALIZADO !")
    return file_path_out_cut



"""
    FUNCAO PRINCIPAL DA APLICACAO
"""
def main():

    # ARRUMAS PARA PATRONIzAR as ENTRADAS para NAO FICAR REPETIDAS AS FUNCOES IGUaIS ESTAO
    file_path_grade = str(sys.argv[1])
    file_path_tar_before = str(sys.argv[2])
    file_path_tar_after = str(sys.argv[3])

    function = str(sys.argv[4])

    print("Diretorio de saida: \n " + os.path.dirname(os.path.realpath(__file__)) + "/build/" + "\n")

    directory_out = os.path.dirname(os.path.realpath(__file__)) + "/build/"
    if not os.path.exists(directory_out):
        os.mkdir(directory_out, 0755 )

    if sys.argv < 4:
         print('To few arguments')

    saida = indice_calculate(function, file_path_tar_before, file_path_grade, directory_out)
    # saida = indice_calculate(function, file_path_tar_after, file_path_grade, directory_out)

    print (saida)


if __name__ == '__main__':
    main()
