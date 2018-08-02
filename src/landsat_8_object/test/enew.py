# import geopandas as gpd
# import pandas as pd
# import requests
# import io
# from os import listdir
# from os.path import isfile, join
# from shapely import geometry
# import fiona
#
# def records(filename, usecols, **kwargs):
#     with fiona.open(filename, **kwargs) as source:
#         for feature in source:
#             f = {k: feature[k] for k in ['id', 'geometry']}
#             f['properties'] = {k: feature['properties'][k] for k in usecols}
#             yield f
#
#
# mypath = "/home/rafael/Desktop/dados_queimadas" \
#                      "/landsat_8/GradeTMAmericaSul/grade_tm_americasul.shp"
# #
#
# # gpd.GeoDataFrame.from_features(records(mypath, ['path_row']), ['path_row']).ix[437][0]
# #print(gpd.GeoDataFrame.from_features(records(mypath, ['path_row']), ['path_row']).ix[437][0])
# # for i in range(900):
# #     if (gpd.GeoDataFrame.from_features(records(mypath, ['path_row']), ['path_row']).ix[i][1] == '221_067'):
# #         print(i)
# #         print(gpd.GeoDataFrame.from_features(records(mypath, ['path_row']), ['path_row']).ix[i])
# #         print(gpd.GeoDataFrame.from_features(records(mypath, ['path_row']), ['path_row']).ix[i][0])
#
# #print(gpd.GeoDataFrame.from_features(records(mypath, ['path_row']), ['path_row']).ix[1][1])
# #
# # filenames = [y for y in listdir(mypath) for ending in ['dbf', 'shp', 'prj', 'shx'] if y.endswith(ending)]
# #
# # print(filenames)
# #
# # dbf, shp, prj, shx = [filename for filename in filenames]
# #
# # df = gpd.read_file(mypath + shp)
# #
# # print(gpd.GeoDataFrame.from_features(df,))
#
# #print("\nShape of the dataframe: {}".format(df.shape) + "\n")
#
# import ogr
#
#
# def write_shapefile(poly, out_shp):
#     """
#     https://gis.stackexchange.com/a/52708/8104
#     """
#     # Now convert it to a shapefile with OGR
#     driver = ogr.GetDriverByName('Esri Shapefile')
#     ds = driver.CreateDataSource(out_shp)
#     layer = ds.CreateLayer('', None, ogr.wkbPolygon)
#     # Add one attribute
#     layer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))
#     defn = layer.GetLayerDefn()
#
#     ## If there are multiple geometries, put the "for" loop here
#
#     # Create a new feature (attribute and geometry)
#     feat = ogr.Feature(defn)
#     feat.SetField('id', 123)
#
#     # Make a geometry, from Shapely object
#     geom = ogr.CreateGeometryFromWkt(poly.wkt)
#     feat.SetGeometry(geom)
#
#     layer.CreateFeature(feat)
#     feat = geom = None  # destroy these
#
#     # Save and close everything
#     ds = layer = feat = geom = None
#
# poly = gpd.GeoDataFrame.from_features(records(mypath, ['path_row']), ['path_row']).ix[437][0]
#
# print(poly.wkt)
# write_shapefile(poly, r'/home/rafael/out.shp')
#
#
#
import os

# def cut(grid_file, tiff_file, new_tiff_file):
#     os.system("gdalwarp -q -cutline "
#               + grid_file + " "
#                             "-tr 30.0 30.0 -of GTiff "
#               + tiff_file + " " + new_tiff_file)
#
#
path = "/home/rafael/teste/"
#
# grid_file = path+"out_grade/out_221_067_grade.shp"
# tiff_file = path+"LC08_L1TP_221067_20170926_20171013_01_T1_B4.TIF"
# new_t = path+"new.TIF"
#
#
# cut(grid_file,tiff_file,new_t)
import re


# for i in os.listdir(path):
#     regex = re.search("(.*).TIF$", i)
#     if(regex != None):
#         print(regex.group(1))
#
#

print(re.search("(.*?).((tar.gz)|(zip))", os.path.basename(path)))

#
# print()

# a = image_landsat_8("/home/rafael/Desktop/dados_queimadas" \
#                     "/landsat_8/LC08_L1TP_221067_" \
#                     "20170926_20171013_01_T1.tar.gz",
#                     "/home/rafael/Desktop/dados_queimadas/landsat_8/out_grade/out_221_067_grade.shp")

# Exemplo
# red = a.get_band_red()
# nir = a.get_band_nir()
#
# plt.imshow(a.ndvi(red, nir), cmap='RdYlGn')
# plt.colorbar()
# plt.show()