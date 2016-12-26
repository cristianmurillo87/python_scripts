import arcpy, os

tabla = arcpy.GetParameterAsText(0)
campos = arcpy.GetParameterAsText(1)

try:
	arcpy.DeleteField_management(tabla,campos.name)
except:
	print arcpy.GetMessages()
finally:
	print "Ejecucion finalizada"
	
	
