import arcpy,os
from datetime import date
# data = "E:\ESTRATIFICACION\Actualizacion Aplicativo\Terrenos\MARZ-01\PREDIOS_MRZ_01.shp"
# outFc = "tererere"
# outPath = r"E:\ESTRATIFICACION\Actualizacion Aplicativo\Terrenos\actualizacion.gdb"
arcpy.env.overwriteOutput = True
#Tabla de Predios
data = arcpy.GetParameterAsText(0)
#Nombre de la Capa de Salida
outTable = "prov_predios"
outPath = r"E:\ESTRATIFICACION\Actualizacion Aplicativo\Terrenos\actualizacion.gdb"
template = outPath + "\\predios_template"
hoy = date.today().strftime("%d%m%Y")
finalPath = r"E:\ESTRATIFICACION\Actualizacion Aplicativo"
try:
	arcpy.CreateTable_management(outPath, outTable, template)
	with arcpy.da.SearchCursor(data,["NUMEROPRE","MATRIZ","ACTIVIDAD","NUMERONAL","DIRECCION"]) as cursor:
		with arcpy.da.InsertCursor(outPath+"\\"+outTable,["num_predia","cod_predio", "cod_act", "cod_pred_n","direccion"]) as cursor2:
			for row in cursor:
				cursor2.insertRow(row)
	arcpy.TableToTable_conversion(outPath+'\\'+outTable, finalPath, "predios_"+hoy+".dbf")
	arcpy.AddMessage("Ejecucion terminada")
except Exception, e:
	import traceback, sys
	tb = sys.exc_info()[2]
	arcpy.AddMessage("Linea %i" % tb.tb_lineno)
	arcpy.AddMessage(e.message)

	
