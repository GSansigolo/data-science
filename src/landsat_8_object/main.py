from image_landsat_8 import image_landsat_8
import os, sys
import matplotlib.pyplot as plt
from osgeo import gdal, ogr
import gdal, gdalconst
import cv2
from scipy.cluster.vq import *
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

    print ("Arquivo salvo")

def indice_calculate(indice, file_path_tar, file_path_grade, directory_out):

    print ("----------------------------------------")
    print ("Realizando o Calculo do INDICE " + indice)

    if not os.path.exists(directory_out + indice + "/"):
        os.mkdir( directory_out + indice + "/" )


    landsat_images = image_landsat_8(file_path_tar, file_path_grade)

    # Define o caminho dos arquivos de saida
    indice_path = directory_out +  indice + "/"+ indice

    file_path_out = indice_path +  "_" + landsat_images.get_time() + "_.TIF"

    file_path_out_cut = indice_path + "_" + landsat_images.get_time() + "_CUT_.TIF"


    # ----------------- CALCULA INDICE ------------------------- #

    if indice == "NDVI":
        band = landsat_images.ndvi()
    elif indice == "MIRBI":
        band = landsat_images.mirb()
    elif indice == "NBR2":
        band = landsat_images.nbr2()
    elif indice == "NBR":
        band = landsat_images.nbr()
    elif indice == "NDWI":
        band = landsat_images.ndwi()
    else:
        print ("Opcao de indice errado")
        exit()

    # ----------------- SALVA IMAGEM ------------------------- #

    save_image(landsat_images.get_directory_tmp() + "B6.TIF", band, file_path_out)

    print ("Imagem salva!")

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

    file_path_out_diferenca = indice_path + "_diferenca.TIF"
    file_path_out_diferenca_relativa = indice_path +   "_REL_diferenca.TIF"

    # ------------ CALCULA A DIFERENCA DAS BANDAS --------------- #
    print("--------------------------------------------")
    print("Calculando a Diferenca.. e salvando a imagem .tif")

    diferenca = (after - before)

    save_image(indice_path + "_" + landsat_images.get_time() + "_CUT_.TIF", diferenca, file_path_out_diferenca)

    # Calcula a diferenca relativa verificar
    diferenca_relativa = diferenca / abs(before)

    name = indice_path + "_" + landsat_images.get_time() + "_CUT_.TIF"

    save_image(name, diferenca_relativa, file_path_out_diferenca_relativa)

    return file_path_out_diferenca

def teste_kmeans(landsat_images, filename, indice, directory_out):

    print("----------------------------------------")

    data_set = gdal.Open(filename, gdalconst.GA_ReadOnly)
    data_array = data_set.ReadAsArray()

    flat_data_array = data_array.flatten()


    fig = plt.figure()
    fig.suptitle('K-Means Classification')

    # Adiciona a imagem Original no plot
    ax = plt.subplot(241)
    plt.axis('off')
    ax.set_title('Original Image')
    plt.imshow(data_array, cmap = 'gray')

    # realizar a classificacao no K estipulado
    for i in range(2):
        print ("Calculando k-means with " + str(i+2) + " cluster.")
        file_path_out =  directory_out + "cluster_"+ indice + str(i+2) + "_.TIF"
        print ("Salvando as imagens no Diretorio: " + file_path_out)
        centroids, variance = kmeans(flat_data_array, i+2)
        code, distance = vq(flat_data_array, centroids)


        image_final = code.reshape(data_array.shape[0], data_array.shape[1])

        print("Processo K-means Terminado!")

        # plota as imagens com k = i + 2
        ax = plt.subplot(2,4,i+2)
        plt.axis('off')
        xlabel = str(i+2) , ' Cluster'
        ax.set_title(xlabel)
        plt.imshow(image_final)

        save_image(filename, image_final, file_path_out)

    plt.show()


"""
    FUNCAO PRINCIPAL DA APLICACAO
"""
def main():

    # dados de entrada passados pelo usuario

    file_path_grade = str(sys.argv[1])
    file_path_tar_before = str(sys.argv[2])
    file_path_tar_after = str(sys.argv[3])
    indice_name = str(sys.argv[4])
    kmeans_option = str(sys.argv[5])

    directory_out = os.path.dirname(os.path.realpath(__file__)) + "/build/"

    print("Diretorio de saida: \n " + directory_out + "\n")

    if not os.path.exists(directory_out):
        os.mkdir(directory_out )

    if sys.argv < 5:
         print('Poucos argumentos, verificar como utilizar')

    indice_path, before, landsat_images  = indice_calculate(indice_name, file_path_tar_before, file_path_grade, directory_out)
    _, after, landsat_images_after  = indice_calculate(indice_name, file_path_tar_after, file_path_grade, directory_out)

    name =  calcula_diferenca(landsat_images, indice_path, before, after)

    print kmeans_option
    if kmeans_option == '1':
        print("Iniciando Aprendizado nao supervisionado ")
        teste_kmeans(landsat_images, name, indice_name, directory_out)


if __name__ == '__main__':
    main()
