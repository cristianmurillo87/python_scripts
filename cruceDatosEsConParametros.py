import arcpy, os, sys
from datetime import date
def actualizarTabla(predios, matrizPredios,ssmlPredios, ssmPredios, manzanaPredios, ladoPredios,terrenos, matrizTerrenos, ssmlTerrenos):
	try:

		terrenosAlias = "terrenos"
		prediosAlias = "predios"
		campo3 = "CONTROL"
		hoy = date.today().strftime("%d%m%Y")
		#crear layers temporales
		#arcpy.MakeFeatureLayer_management(terrenos,terrenosAlias)
		arcpy.AddMessage("Creando capa temporal...")
		arcpy.MakeTableView_management(predios, prediosAlias)
		arcpy.AddMessage("Capa temporal creada.")

		#crear el join
		arcpy.AddMessage("Creando join entre predios a terrenos...")
		arcpy.AddJoin_management(prediosAlias,matrizPredios,terrenos,matrizTerrenos,"KEEP_COMMON")
		arcpy.AddMessage("Join creado.")
		#actualizar lados de manzana con la field calculator

		expresion = "["+os.path.splitext(os.path.basename(terrenos))[0] + "."+ssmlTerrenos+"]"
		campo1= '"'+os.path.splitext(os.path.basename(predios))[0] + '.'+ssmlPredios+'"'
		campo2= '"'+os.path.splitext(os.path.basename(terrenos))[0] + '.'+ssmlTerrenos+'"'

		arcpy.AddMessage("Seleccionando elementos...")
		#arcpy.AddMessage("calculando campos entre "+campo1+" y "+campo2)
		arcpy.SelectLayerByAttribute_management(prediosAlias, "NEW_SELECTION", campo2 + " NOT IN (NULL, '', ' ')")

		arcpy.AddMessage("Actualizando lados de manzana...")
		arcpy.CalculateField_management(prediosAlias, ssmlPredios, expresion)
		arcpy.CalculateField_management(prediosAlias, campo3, "str(" + hoy + ")", "PYTHON")
		arcpy.AddMessage("Lados de manzana actualizados.")

		#actualizar codigo de manzana (8 y 3 caracteres) y de lado
		expresion2= "!" + os.path.splitext(os.path.basename(terrenos))[0] + "." + ssmlTerrenos + "!"
		arcpy.AddMessage("Actualizando codigos de manzana...")
		arcpy.CalculateField_management(prediosAlias, ssmPredios, expresion2 + "[0:8]" ,"PYTHON")
		arcpy.AddMessage("Codigos de manzana actualizados.")
		arcpy.AddMessage("Actualizando letra del lado de manzana...")
		arcpy.CalculateField_management(prediosAlias, ladoPredios, expresion2 + "[8:9]","PYTHON")
		arcpy.AddMessage("Letras de lados actualizadas.")
		arcpy.AddMessage("Actualizando numero de la manzana...")
		arcpy.CalculateField_management(prediosAlias, manzanaPredios, "int(" + expresion2 + "[4:8].strip())","PYTHON")
		arcpy.AddMessage("Numeros de manzana actualizados")
		#eliminar join
		arcpy.RemoveJoin_management(prediosAlias)
		arcpy.SelectLayerByAttribute_management(prediosAlias, "CLEAR_SELECTION")
		arcpy.AddMessage("Actualziacion terminada.")	
	except Exception, e:
		import traceback, sys
		tb = sys.exc_info()[2]
		arcpy.AddMessage("Line %i" % tb.tb_lineno)
		arcpy.AddMessage(e.message)


#Base predial catastral
#predios = r"E:\ESTRATIFICACION\Actualizacion Aplicativo\BASE PREDIAL\1_BASE_CATAS_MARZO_17.dbf"
predios = arcpy.GetParameterAsText(0)
#Terrenos catastrales
#terrenos = r"E:\ESTRATIFICACION\Actualizacion Aplicativo\Terrenos\MARZ-17\1PREDIOS_MARZ_17.shp"
terrenos = arcpy.GetParameterAsText(1)

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


#Codigo matriz de los terrenos
matrizTerrenos = "matriz"
#SESEMANLADO en los terrenos
sesemanladoTerrenos = "SESEMANLAD"

actualizarTabla(predios,matrizPredios,sesemanladoPredios,sesemanPredios,manzanaPredios,ladoPredios,terrenos,matrizTerrenos,sesemanladoTerrenos)

