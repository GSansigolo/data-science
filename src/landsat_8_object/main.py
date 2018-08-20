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


    landsat_images = image_landsat_8(file_path_tar, file_path_grade)

    # Define o caminho dos arquivos de saida
    indice_path = directory_out +  indice + "/"+ indice

    file_path_out = indice_path +  "_" + landsat_images.get_time() + "_.TIF"

    file_path_out_cut = indice_path + "_" + landsat_images.get_time() + "_CUT_.TIF"


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

    print( "Calculo " + indice + " FINALIZADO !")
    return indice_path, band_cut, landsat_images

def calcula_diferenca(landsat_images, indice_path, before, after):

    # print ("Teste passagem")
    # print(before.shape)
    # print(before.shape)

    file_path_out_diferenca = indice_path + "_diferenca.TIF"
    file_path_out_diferenca_relativa = indice_path +   "_REL_diferenca.TIF"

    # ------------ CALCULA A DIFERENCA DAS BANDAS --------------- #

    print("Calculando a Diferenca.. e salvando a imagem .tif")

    diferenca = (after - before)

    save_image(indice_path + "_" + landsat_images.get_time() + "_CUT_.TIF", diferenca, file_path_out_diferenca)

    # Calcula a diferenca relativa verificar
    diferenca_relativa = diferenca / abs(before)

    save_image(indice_path + "_" + landsat_images.get_time() + "_CUT_.TIF", diferenca_relativa, file_path_out_diferenca_relativa)


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

    indice_path, before, landsat_images  = indice_calculate(function, file_path_tar_before, file_path_grade, directory_out)
    _, after, landsat_images_after  = indice_calculate(function, file_path_tar_after, file_path_grade, directory_out)

    calcula_diferenca(landsat_images, indice_path, before, after)


if __name__ == '__main__':
    main()
