import sys
import psycopg2
import psycopg2.extras


def conectarBD():
	try:
		conn = psycopg2.connect("dbname='bd_estratificacion' user='postgres' host='172.18.10.127' password='adminestra10A'")
		conn.autocommit = True
	 	print("Conectado exitosamente a la base de datos")
	 	return conn
	except:
	 	print("No se pudo establecer conexion con la base de datos")


comunas = ['01','17','18','19','20']
for comuna in comunas:
	archivo=open('E:\\ESTRATIFICACION\\TABLAS\\2016\\visitas\\com_'+str(comuna)+'.txt', 'w')
	archivo.write("com;barr;manz;lado;nom_barr;direccion\n")
	archivo.close()

conn=conectarBD()

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
for comuna in comunas:
	try:
		cur.execute("select com, barr, manz, lado, nom_barr, direccion from casos.visita where com = %s order by com, barr, manz",(comuna,))

	except:
		print("error al ejecutar consulta en comuna "+str(comuna))

	print(cur.query)
	
	
	visitas=cur.fetchall()
	archivo=open('E:\\ESTRATIFICACION\\TABLAS\\2016\\visitas\\com_'+str(comuna)+'.txt', 'a')
	for visita in visitas:
		nueva_linea = str(visita['com'])+";"+str(visita['barr'])+";"+str(visita['manz'])+";"+str(visita['lado'])+";"+str(visita['nom_barr'])+";"+str(visita['direccion'])+"\n"
		archivo.write(nueva_linea)
	archivo.close()
	
conn.close()
print("Conexion a la base de datos cerrada exitosamente")
