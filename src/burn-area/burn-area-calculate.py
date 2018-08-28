from osgeo import gdal
import numpy as np

try:
	nuvem1 = gdal.Open("AREA_Q.TIF")
	print ("Arquivos aberto com sucesso!")
except:
	print("Erro na abertura dos arquivo!")
	exit()

mascara1 = nuvem1.GetRasterBand(1).ReadAsArray().astype(np.int8)

abc = np.sum(mascara1==1)

tamanho_imagem1 = mascara1.shape[0] * mascara1.shape[1]

cloud_mask = (abc * 100) / tamanho_imagem1

print("")

print("Porcentagem Queimada (Mascara): %.2f" %(100-cloud_mask) )

print("")

print("Porcentagem Não-Queimada (Mascara): %.2f" %cloud_mask)

print("")

