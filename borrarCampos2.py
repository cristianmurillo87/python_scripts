import arcpy

mxd = arcpy.mapping.MapDocument("CURRENT")

tables = arcpy.mapping.ListTableViews(mxd,"RESPUESTA")


for table in tables:
	for field in arcpy.ListFields(table):
		if field.name not in ["OID","NUMEPRED","ID_PREDI_1","DIRECCION","NUMERO_PRE","CODIGO","ESTRATO_1"]:
			print "Se eliminara el campo {0}".format(field.name)
			arcpy.DeleteField_management(table, field.name)
			