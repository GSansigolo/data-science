
import os
import numpy as np
import cv2

dir_path = "teste/"
dir_out = "casos_teste/"
max = 9


for number in range(max):
    # name_in = dir_path + "queimadas_" + str(number)
    # name_in = dir_path + "falsos_" + str(number)
    name_in = dir_path + "teste_" + str(number)
    name_out = dir_out + str(number) + "_.TIF"

    band_6 = name_in + "_B6_.TIF"
    band_5 = name_in + "_B5_.TIF"
    band_4 = name_in + "_B4_.TIF"

    # print("Name_in {}".format(band_6))
    # print("Name_out {}".format(band_6))

    command = "gdal_merge.py -separate -of GTiff -o " + name_out + " " + band_6 + " " + band_5 + " " + band_4

    os.system(command)
