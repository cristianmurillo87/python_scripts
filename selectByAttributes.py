import arcpy

def select(layer, field, code):
	mxd = arcpy.mapping.MapDocument("CURRENT")
	df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
	lyr= arcpy.mapping.ListLayers(mxd, layer, df)[0]
	query = str( field + "=" +  "'"+ code +"'")
	print query
	arcpy.SelectLayerByAttribute_management(lyr, "NEW_SELECTION", query)
	df.extent = lyr.getSelectedExtent()

def cod (field, code):
	print str( '"' + field + "=" + "'"+ code +"'" + '"')
	
