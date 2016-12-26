@echo off
REM @Creado por: Ing. Cristian Andres Murillo A. Esp. en SIG
REM @Drescripcion: Script para actualizacion de las tablas de
REM lados de manzana, predios y terrenos en el aplicativo SIG ESTRATIFICACION

SET PGPASSWORD=**
SET user=**
SET dbname=**
set es=E:\**.csv

"C:\Program Files\PostgreSQL\9.3\bin\psql.exe" -U %user% -d %dbname% -c "DROP VIEW IF EXISTS public.terreno_estrato;"
"C:\Program Files\PostgreSQL\9.3\bin\psql.exe" -U %user% -d %dbname% -c "select actualizar_lados('%es%',';');"
"C:\Program Files\PostgreSQL\9.3\bin\psql.exe" -U %user% -d %dbname% -c "select vista_estratos();"
echo "Actualizacion Terminada..."
@echo off
PAUSE
