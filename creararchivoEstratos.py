import sys
import psycopg2
import psycopg2.extras


def conectarBD():
	try:
		conn = psycopg2.connect("dbname='*******' user='*****' host='**.**.**.**' password='********'")
		conn.autocommit = True
	 	print("Conectado exitosamente a la base de datos")
	 	return conn
	except:
	 	print("No se pudo establecer conexion con la base de datos")


estratos = ['1','2','3','4','5','6']


archivo=open('E:\\ESTRATIFICACION\\TABLAS\\estratos.txt', 'w')
archivo.write("estrato;total\n")
archivo.close()

conn=conectarBD()

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
for estrato in estratos:
	try:
		cur.execute("select estrato, count(lado_manz) total from lados where estrato = %s group by estrato",(estrato,))

	except:
		print("error al ejecutar consulta para el estato "+str(estrato))

	print(cur.query)


	visitas=cur.fetchall()
	archivo=open('E:\\ESTRATIFICACION\\TABLAS\\estratos.txt', 'a')
	for visita in visitas:
		nueva_linea = str(visita['estrato'])+";"+str(visita['total'])+"\n"
		archivo.write(nueva_linea)
	archivo.close()

conn.close()
print("Conexion a la base de datos cerrada exitosamente")
