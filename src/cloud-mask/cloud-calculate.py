from osgeo import gdal
import numpy as np

try:
	nuvem1 = gdal.Open("data/LC08_L1TP_221067_20170926_20171013_01_T1_CLD.TIF")
	nuvem2 = gdal.Open("data/221_067_2017-01-13_nuvem.tif")
	print ("Arquivos aberto com sucesso!")
except:
	print("Erro na abertura dos arquivo!")
	exit()

mascara1 = nuvem1.GetRasterBand(1).ReadAsArray().astype(np.int8)
mascara2 = nuvem2.GetRasterBand(1).ReadAsArray().astype(np.int8)

nuvem2 = np.sum(mascara2==1)
limpa1 = np.sum(mascara1==1)

tamanho_imagem1 = mascara1.shape[0] * mascara1.shape[1]
tamanho_imagem2 = mascara2.shape[0] * mascara2.shape[1]

cloud_mask = (limpa1 * 100) / tamanho_imagem1
nuvem = (100-(nuvem2 * 100) / tamanho_imagem2)

print("")

print("Porcentagem Nuvem (Mascara): %.2f" %(100-cloud_mask) )
print("Porcentagem Nuvem (Exemplo): %.2f" %(100-nuvem) )

print("")

print("Porcentagem Não-Nuvem (Mascara): %.2f" %cloud_mask)
print("Porcentagem Não-Nuvem (Exemplo): %.2f" %nuvem)

print("")

print("Porcentagem de Acerto: %.2f" %(100-((cloud_mask-nuvem)/cloud_mask)*100) )

