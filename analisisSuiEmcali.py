#busqueda y asignacion de codigos unicos nacionales a los clientes emcali
import psycopg2
import psycopg2.extras

def conectarBD():
	try:
		conn = psycopg2.connect("dbname='*********' user='*******' host='***.**.**.***' password='***********'")
		conn.autocommit = True
	 	print("Conectado exitosamente a la base de datos")
	 	return conn
	except:
	 	print("No se pudo establecer conexion con la base de datos")

def asignarIds():

	conn=conectarBD()

	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

	try:
		cur.execute("select matriz from resumen_npn_matriz_2014")
	except:
		print("Error al ejecutar la consulta")

	rows = cur.fetchall()

	for row in rows:
		matriz = row['matriz']
		#print ("matriz: "+str(matriz))
		try:
			cur.execute("select gid from listado_matriz_npns_2014 where matriz = %s",(str(matriz),))
		except:
			print("Error al ejecutar la consulta")
		#print(cur.query)
		#total = cur.rowcount 
		#print("Se encontraron "+str(total)+" elementos con el matriz "+str(matriz))
		gids = cur.fetchall()

		id = 1
		for gid in gids:
			cur.execute("update listado_matriz_npns_2014 set id2=%s where gid=%s",(id, gid['gid']))
			#print(cur.query)
			print("creando id "+str(id))
			id=id+1 

	 	
	conn.close()
	print("Conexion a la base de datos cerrada exitosamente")

def asignarNpns():

	conn=conectarBD()
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

	try:
		cur.execute("select * from resumen_npn_matriz_2014 where disponibles > 1")
		print("Se encontraron "+str(cur.rowcount)+" registros.")
	except:
		print("Error al ejecutar la consulta")

	matrices = cur.fetchall()

	for matriz in matrices:
		limite = 1
		if matriz['clientes'] > matriz['disponibles']:
			limite = matriz['disponibles']
		elif matriz['clientes'] < matriz['disponibles']:
			limite = matriz['clientes']
		
		try:
			cur.execute("select gid from sin_numeronal where cod_unico = %s and nuevo_cod_unico is null limit %s",(matriz['cod_unico'],limite))
			#print("Se encontraron "+str(cur.rowcount)+" registros con el codigo "+ matriz['cod_unico']+".")
		except:
			print("Error al buscar registros")

		gids = cur.fetchall()

		id = 1
		for gid in gids:
			try:
				cur.execute("update sin_numeronal set nuevo_cod_unico = (select numeronal from listado_matriz_npns_2014 where matriz = %s and id2= %s) where gid = %s",(matriz['matriz'],id,gid['gid']))
				print("se asigno NPN al registro con ID "+str(gid['gid']))
			except:
				print("Error en la asignacion de codigos")
			id=id+1

asignarNpns()
#asignarIds()
