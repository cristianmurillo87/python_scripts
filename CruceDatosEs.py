import arcpy, os, sys
def borrarCapas():
	mxd = arcpy.mapping.MapDocument('CURRENT')
	for df in arcpy.mapping.ListDataFrames(mxd):
		for lyr in arcpy.mapping.ListLayers(mxd,"",df):
			arcpy.mapping.RemoveLayer(df, lyr)

def actualizarTabla(predios, matrizPredios,ssmlPredios, ssmPredios, manzanaPredios, ladoPredios,terrenos, matrizTerrenos, ssmlTerrenos):
	try:

		terrenosAlias = "terrenos"
		prediosAlias = "predios"

		#crear layers temporales
		#arcpy.MakeFeatureLayer_management(terrenos,terrenosAlias)
		print "Creando capa temporal...\n"
		arcpy.MakeTableView_management(predios, prediosAlias)
		print "Capa temporal creada\n"

		#crear el join
		print "Creando join entre predios a terrenos...\n"
		arcpy.AddJoin_management(prediosAlias,matrizPredios,terrenos,matrizTerrenos,"KEEP_COMMON")
		print "Join creado\n"
		#actualizar lados de manzana con la field calculator

		expresion = "["+os.path.splitext(os.path.basename(terrenos))[0] + "."+ssmlTerrenos+"]"
		query= '"'+os.path.splitext(os.path.basename(predios))[0] + '.'+ssmlPredios+'"'

		print "Seleccionando elementos...\n"
		arcpy.SelectLayerByAttribute_management(prediosAlias, "NEW_SELECTION", query + " NOT IN ('', ' ' ,NULL )")

		print "Actualizando lados de manzana...\n"
		arcpy.CalculateField_management(prediosAlias, ssmlPredios, expresion)
		print "Lados de manzana actualizados\n"

		#actualizar codigo de manzana (8 y 3 caracteres) y de lado
		expresion2= "!" + os.path.splitext(os.path.basename(terrenos))[0] + "." + ssmlTerrenos + "!"
		print "Actualizando codigos de manzana...\n"
		arcpy.CalculateField_management(prediosAlias, ssmPredios, expresion2 + "[0:8]" ,"PYTHON")
		print "Codigos de manzana actualizados\n"
		print "Actualizando letra del lado de manzana...\n"
		arcpy.CalculateField_management(prediosAlias, ladoPredios, expresion2 + "[8:9]","PYTHON")
		print "Letras de lados actualizadas\n"
		print "Actualizando numero de la manzana...\n"
		arcpy.CalculateField_management(prediosAlias, manzanaPredios, "int(" + expresion2 + "[4:8].strip())","PYTHON")
		print "Numeros de manzana actualizados\n"
		#eliminar join
		arcpy.RemoveJoin_management(prediosAlias)
		arcpy.SelectLayerByAttribute_management(prediosAlias, "CLEAR_SELECTION")
		print "Actualziacion terminada.\n"
	except Exception, e:
		import traceback, sys
		tb = sys.exc_info()[2]
		print "Line %i" % tb.tb_lineno
		print e.message


#Base predial catastral
predios = r"E:\ESTRATIFICACION\Actualizacion Aplicativo\BASE PREDIAL\2MARZ_10.dbf"
#Codigo Matriz de los predios
matrizPredios ="MATRIZ"
#SESEMANLADO en los predios
sesemanladoPredios = "SESEMANLAD"
#SESEMAN en los predios
sesemanPredios = "SESEMAN"
#Manzana en los predios
manzanaPredios = "MANZANA"
#LADO en los predios
ladoPredios = "LADO"

#Terrenos catastrales
terrenos = r"E:\ESTRATIFICACION\Actualizacion Aplicativo\Terrenos\MARZ-10\PREDIOS_MARZ_10.shp"
#Codigo matriz de los terrenos
matrizTerrenos = "matriz"
#SESEMANLADO en los terrenos
sesemanladoTerrenos = "SESEMANLAD"


borrarCapas()
actualizarTabla(predios,matrizPredios,sesemanladoPredios,sesemanPredios,manzanaPredios,ladoPredios,terrenos,matrizTerrenos,sesemanladoTerrenos)

