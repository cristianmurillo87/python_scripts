import arcpy,os
from datetime import date
# data = "E:\ESTRATIFICACION\Actualizacion Aplicativo\Terrenos\MARZ-01\PREDIOS_MRZ_01.shp"
# outFc = "tererere"
# outPath = r"E:\ESTRATIFICACION\Actualizacion Aplicativo\Terrenos\actualizacion.gdb"
arcpy.env.overwriteOutput = True
#Capa de Terrenos
data = arcpy.GetParameterAsText(0)
#Nombre de la Capa de Salida
outFc = arcpy.GetParameterAsText(1)
outPath = r"E:\ESTRATIFICACION\Actualizacion Aplicativo\Terrenos\actualizacion.gdb"
template = outPath + "\\terreno_template"
hoy = date.today().strftime("%d%m%Y")
finalPath = r"E:\ESTRATIFICACION\Actualizacion Aplicativo"
try:
	arcpy.AddMessage(template)
	srs = arcpy.Describe(template).SpatialReference
	arcpy.CreateFeatureclass_management(outPath, outFc, "POLYGON", template,"DISABLED","DISABLED", srs)
	with arcpy.da.SearchCursor(data,["SHAPE@","matriz","DIRECCION","ACTIVIDAD","SESEMANW","SESEMANLAD"]) as cursor:
		with arcpy.da.InsertCursor(outPath+"\\"+outFc,["SHAPE@","cod_predio", "direccion","cod_act", "cod_manzan","lado_manz"]) as cursor2:
			for row in cursor:
				cursor2.insertRow(row)
	arcpy.FeatureClassToFeatureClass_conversion(outPath+'\\'+outFc, finalPath, "terrenos_"+hoy)
	arcpy.AddMessage("Ejecucion terminada")
except Exception, e:
	import traceback, sys
	tb = sys.exc_info()[2]
	arcpy.AddMessage("Linea %i" % tb.tb_lineno)
	arcpy.AddMessage(e.message)

	
