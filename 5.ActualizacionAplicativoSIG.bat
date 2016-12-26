@echo off
REM @Creado por: Ing. Cristian Andres Murillo A. Esp. en SIG
REM @Drescripcion: Script para actualizacion de las tablas de
REM lados de manzana, predios y terrenos en el aplicativo SIG ESTRATIFICACION

SET PGPASSWORD=**
SET user=**
SET dbname=**
SET terrenos=**.shp
SET predios=**.dbf
set es=E:\**.csv
echo on

"C:\Program Files\PostgreSQL\9.3\bin\psql.exe" -U %user% -d %dbname% -c "DROP VIEW IF EXISTS public.terreno_estrato;"
"C:\Program Files\PostgreSQL\9.3\bin\shp2pgsql.exe" -I -s 97664 -g the_geom -d %terrenos% terrenos | "C:\Program Files\PostgreSQL\9.3\bin\psql.exe" -U %user% -d %dbname%
"C:\Program Files\PostgreSQL\9.3\bin\shp2pgsql.exe" -n -d %predios% predios | "C:\Program Files\PostgreSQL\9.3\bin\psql.exe" -U %user% -d %dbname%
"C:\Program Files\PostgreSQL\9.3\bin\psql.exe" -U %user% -d %dbname% -c "select actualizar_lados('%es%',';');"
"C:\Program Files\PostgreSQL\9.3\bin\psql.exe" -U %user% -d %dbname% -c "select vista_estratos();"
"C:\Program Files\PostgreSQL\9.3\bin\psql.exe" -U %user% -d %dbname% -c "DROP VIEW IF EXISTS public.terreno_lados;"
"C:\Program Files\PostgreSQL\9.3\bin\psql.exe" -U %user% -d %dbname% -c "create table terreno_lados as select lado_manz, st_union(the_geom) as the_geom from terrenos  group by lado_manz;"
"C:\Program Files\PostgreSQL\9.3\bin\psql.exe" -U %user% -d %dbname% -c "alter table terreno_lados add column id serial;"
"C:\Program Files\PostgreSQL\9.3\bin\psql.exe" -U %user% -d %dbname% -c "alter table terreno_lados add primary key (id);"
SET /P "Actualizacion Terminada..."
PAUSE
