# coding: utf8
'''
-------------------------------------------------------------------------------------------------------
CONVERTER GEODATABASE
-------------------------------------------------------------------------------------------------------
Michel Metran
Criado em Ago/2017

Script elaborado para converter arquivos do geodatabase para diversos outros formatos comumente utilizados,
com a correção dos datum para WGS84, sendo esse o padrão frequentemente utilizado.

'''

# -------------------------------------------------------------------------------------------------------
# Módulos e Codificação
import FeaturesToGPX as gpx
import os
import sys
import arcpy
import zipfile
import string
import glob
import shutil

reload(sys)
sys.setdefaultencoding('utf8')

# -------------------------------------------------------------------------------------------------------
# Variável de Input
geodatabase = r'Y:\SIG_IC_09-16\Geodata\Geo_IC-09-16.mdb'

# -------------------------------------------------------------------------------------------------------
# Functions


def zip(src, dst):
    zf = zipfile.ZipFile("%s.zip" % (dst), "w")
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            print 'zipping %s as %s' % (os.path.join(dirname, filename),
                                        arcname)
            zf.write(absname, arcname)
    zf.close()


# -------------------------------------------------------------------------------------------------------
# Variáveis de Ambiente do ArcGIS
arcpy.ResetEnvironments()
arcpy.env.workspace = geodatabase
arcpy.env.overwriteOutput = True

# -------------------------------------------------------------------------------------------------------
# Create directories
print '## Etapa 1: Cria a estrutura das pastas e "Geodatabase em WGS"'

directorys = ['geo', 'shp', 'shp//WGS84', 'kml', 'lyr', 'gpx', 'tabs']

for directory in directorys:
    try:
        shutil.rmtree(os.path.join(os.path.dirname(
            geodatabase), directory), ignore_errors=True)
        os.makedirs(os.path.join(os.path.dirname(geodatabase), directory))
    except OSError:
        if not os.path.isdir(os.path.join(os.path.dirname(geodatabase), directory)):
            raise

wgs = 'Geo_WGS84.mdb'
arcpy.CreatePersonalGDB_management(
    (os.path.join(os.path.dirname(geodatabase), 'geo')), wgs)

# -------------------------------------------------------------------------------------------------------
# Projeta para WGS no geodatabase
print '## Etapa 2: Projeta qualquer featureclass SAD69, Córrego Alegre ou Sirgas2000 em WGS84'

datasets = arcpy.ListDatasets(feature_type='feature')
for ds in datasets:
    arcpy.CreateFeatureDataset_management(os.path.join(os.path.dirname(geodatabase), 'geo', wgs),
                                          ds,
                                          arcpy.SpatialReference(4326))

datasets = [''] + datasets if datasets is not None else []
for ds in datasets:
    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        path = os.path.join(arcpy.env.workspace, ds, fc)
        sr = arcpy.Describe(path).spatialReference.Name
        print 'Convertendo FeatureClass: ' + fc

        if sr == 'Unknown':
            print('Feature Class sem Sistema de Coordenada Definido: ' +
                  fc + 'não projetado.')

        elif sr == 'GCS_South_American_1969' or \
                sr == 'SAD_1969_UTM_Zone_21S' or \
                sr == 'SAD_1969_UTM_Zone_22S' or \
                sr == 'SAD_1969_UTM_Zone_23S' or \
                sr == 'SAD_1969_UTM_Zone_24S' or \
                sr == 'SAD_1969_UTM_Zone_25S':
            out = os.path.join(os.path.dirname(
                geodatabase), 'geo', wgs, ds, fc)
            arcpy.Project_management(
                path, out, arcpy.SpatialReference(4326), 'SAD69_para_WGS84')

        elif sr == 'GCS_Corrego_Alegre' or \
                sr == 'Corrego_Alegre_UTM_Zone_21S' or \
                sr == 'Corrego_Alegre_UTM_Zone_22S' or \
                sr == 'Corrego_Alegre_UTM_Zone_23S' or \
                sr == 'Corrego_Alegre_UTM_Zone_24S' or \
                sr == 'Corrego_Alegre_UTM_Zone_25S':
            out = os.path.join(os.path.dirname(
                geodatabase), 'geo', wgs, ds, fc)
            arcpy.Project_management(path, out, arcpy.SpatialReference(
                4326), 'CórregoAlegre_para_WGS84')

        elif sr == 'GCS_SIRGAS_2000' or \
                sr == 'SIRGAS_2000_UTM_Zone_21S' or \
                sr == 'SIRGAS_2000_UTM_Zone_22S' or \
                sr == 'SIRGAS_2000_UTM_Zone_23S' or \
                sr == 'SIRGAS_2000_UTM_Zone_24S' or \
                sr == 'SIRGAS_2000_UTM_Zone_25S':
            out = os.path.join(os.path.dirname(
                geodatabase), 'geo', wgs, ds, fc)
            arcpy.Project_management(
                path, out, arcpy.SpatialReference(4326), 'SIRGAS2000_para_WGS84')

        elif sr == 'GCS_WGS_1984' or \
                sr == 'WGS_1984_UTM_Zone_21S' or \
                sr == 'WGS_1984_UTM_Zone_22S' or \
                sr == 'WGS_1984_UTM_Zone_23S' or \
                sr == 'WGS_1984_UTM_Zone_24S' or \
                sr == 'WGS_1984_UTM_Zone_25S':
            out = os.path.join(os.path.dirname(
                geodatabase), 'geo', wgs, ds, fc)
            arcpy.Project_management(path, out, arcpy.SpatialReference(4326))

        else:
            print fc

# -------------------------------------------------------------------------------------------------------
# Converte feature class em shapefiles no datum original
print '## Etapa 3: Converte feature class em shapefiles no datum original'

arcpy.env.workspace = geodatabase
datasets = arcpy.ListDatasets(feature_type='feature')
datasets = [''] + datasets if datasets is not None else []

for ds in datasets:
    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        # Make dir
        path_shp = os.path.join(os.path.dirname(geodatabase), 'shp')
        path_temp = os.path.join(path_shp, 'temp')
        os.makedirs(path_temp)

        # Copy files
        path_in = os.path.join(arcpy.env.workspace, ds, fc)
        path_out = os.path.join(path_temp, fc + '.shp')
        arcpy.CopyFeatures_management(path_in, path_out)

        # Zip files
        zip(path_temp, os.path.join(os.path.dirname(geodatabase), 'shp', fc))

        # Move files
        files = os.path.join(path_temp, '*.*')
        for file in glob.glob(files):
            shutil.move(file, os.path.join(path_shp, os.path.basename(file)))

        # Delete dir
        shutil.rmtree(path_temp, ignore_errors=True)

# -------------------------------------------------------------------------------------------------------
# Converte feature class em shapefiles no datum WGS84
print '## Etapa 4: Converte feature class em shapefiles no datum WGS84'

arcpy.env.workspace = os.path.join(os.path.dirname(geodatabase), 'geo', wgs)
datasets = arcpy.ListDatasets(feature_type='feature')
datasets = [''] + datasets if datasets is not None else []

for ds in datasets:
    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        # Make dir
        path_shp = os.path.join(os.path.dirname(geodatabase), 'shp//WGS84')
        path_temp = os.path.join(path_shp, 'temp')
        os.makedirs(path_temp)

        # Copy files
        path_in = os.path.join(arcpy.env.workspace, ds, fc)
        path_out = os.path.join(path_temp, fc + '.shp')
        arcpy.CopyFeatures_management(path_in, path_out)

        # Zip files
        zip(path_temp, os.path.join(os.path.dirname(geodatabase), 'shp//WGS84', fc))

        # Move files
        files = os.path.join(path_temp, '*.*')
        for file in glob.glob(files):
            shutil.move(file, os.path.join(path_shp, os.path.basename(file)))

        # Delete dir
        shutil.rmtree(path_temp, ignore_errors=True)

# -------------------------------------------------------------------------------------------------------
# Converte feature class em LYR
print '## Etapa 5: Converte feature class em LYR'

arcpy.env.workspace = geodatabase
datasets = arcpy.ListDatasets(feature_type='feature')
datasets = [''] + datasets if datasets is not None else []

for ds in datasets:
    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        layer = os.path.basename(fc)
        print layer

        path_out = os.path.join(os.path.dirname(
            geodatabase), 'lyr', fc + '.lyr')

        arcpy.MakeFeatureLayer_management(fc, layer)
        arcpy.SaveToLayerFile_management(
            layer, path_out, is_relative_path="RELATIVE", version="CURRENT")

# -------------------------------------------------------------------------------------------------------
# Converte feature class em KML
print '## Etapa 6: Converte feature class em KML'

arcpy.env.workspace = os.path.join(os.path.dirname(geodatabase), 'shp//WGS84')
datasets = arcpy.ListDatasets(feature_type='feature')
datasets = [''] + datasets if datasets is not None else []

for ds in datasets:
    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        print fc

        NomeCompleto = os.path.splitext(fc)
        Nome, Completo = NomeCompleto

        path_out = os.path.join(os.path.dirname(
            geodatabase), 'kml', Nome + '.kmz')
        arcpy.MakeFeatureLayer_management(fc, Nome)
        arcpy.LayerToKML_conversion(Nome, path_out)

# -------------------------------------------------------------------------------------------------------
# Converte feature class em XLS
print '## Etapa 7: Converte feature class em XLS'

arcpy.env.workspace = geodatabase
datasets = arcpy.ListDatasets(feature_type='feature')
datasets = [''] + datasets if datasets is not None else []

for ds in datasets:
    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        path_out = os.path.join(os.path.dirname(
            geodatabase), 'tabs', fc + '.xls')
        arcpy.TableToExcel_conversion(fc, path_out)

# -------------------------------------------------------------------------------------------------------
# Converte feature class em GPX
print '## Etapa 8: Converte feature class em GPX'

# https://github.com/arcpy/sample-gp-tools/tree/master/FeaturesToGPX

arcpy.env.workspace = os.path.join(os.path.dirname(geodatabase), 'geo', wgs)
datasets = arcpy.ListDatasets(feature_type='feature')
datasets = [''] + datasets if datasets is not None else []

fctypes = ['Point', 'Polyline']
for fctype in fctypes:
    for ds in datasets:
        for fc in arcpy.ListFeatureClasses(feature_type=fctype, feature_dataset=ds):
            path_out = os.path.join(os.path.dirname(
                geodatabase), 'gpx', fc + '.gpx')
            gpx.featuresToGPX(fc, path_out, 'false', '')


# -------------------------------------------------------------------------------------------------------
# Finalizando
arcpy.ResetEnvironments()
print '# ' + '-' * 100
print '# End'
