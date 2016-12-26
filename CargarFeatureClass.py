import arcpy,os

try:
	data = arcpy.GetParameterAsText(0)
	outFc = arcpy.GetParameterAsText(1)	
	outPath = r"E:\ESTRATIFICACION\Actualizacion Aplicativo\Terrenos\actualizacion.gdb"
	template = outPath + "\\terreno_template"
	arcpy.AddMessage(template)
	srs = arcpy.Describe(template).SpatialReference
	arcpy.AddMessage(str(srs))
	arcpy.CreateFeatureclass_management(outPath, outFc, "POLYGON", template,"DISABLED","DISABLED", srs)
	arcpy.AddMessage("Añadido")
	#iCur = arcpy.da.InsertCursor(outPath+"\\"+outFc,("SHAPE@JSON","cod_predio", "cod_act", "cod_manzan","lado_manz"))
	arcpy.AddMessage("Añadido")
	with arcpy.da.SearchCursor(data,("SHAPE@JSON","matriz","DIRECCION","ACTIVIDAD","SESEMANW","SESEMANLAD")) as cursor:
		with arcpy.da.InsertCursor(outPath+"\\"+outFc,("SHAPE@JSON","cod_predio", "cod_act", "cod_manzan","lado_manz")) as cursor2:
			for row in cursor:
				'''arcpy.AddMessage("0")
				cur = iCur.newRow()
				arcpy.AddMessage("1")
				#cur.shape = row[0]
				cur.setValue("SHAPE@JSON",row[0])
				arcpy.AddMessage("2")
				cur.setValue("cod_predio",row[1])
				arcpy.AddMessage("3")
				cur.setValue("direccion",row[2])
				arcpy.AddMessage("4")
				cur.setValue("cod_act",row[3])
				arcpy.AddMessage("5")
				cur.setValue("cod_manzan",row[4])
				arcpy.AddMessage("6")
				cur.setValue("lado_manz",row[5])
				arcpy.AddMessage("7")'''
				arcpy.AddMessage("1")
				cursor2.insertRow(row)
				arcpy.AddMessage("Añadido "+str(row[1])+" al feature class")
	arcpy.AddMessage("Añadido 2")
except:
	arcpy.GetMessages()
	
