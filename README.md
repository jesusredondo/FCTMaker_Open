# FCTMaker

FCTmaker se puede lanzar con ssl o sin él. Para ejecutarlo de manera no segura, se emplea el siguiente comando:

```python .\manage.py runserver```

Para lanzar el servidor con ssl, teniendo en cuenta que los cetificados se encontrasen en la carpteta *certificados*: 
```python manage.py runserver_plus --cert-file certificados/cert.pem --key-file certificados/key.pem```

Para convertir fctMaker en un servicio [ESTA PREGUNTA (Primera respuesta, no olvidar chmod +x)](https://askubuntu.com/questions/1151080/how-do-i-run-a-script-as-sudo-at-boot-time-on-ubuntu-18-04-server).

## Instalación:

1. Instalación de python - https://www.python.org/ . Seleccionar la opción que nos permite añadir python al PATH. 
   Comprobamos la instalación desde cmd: ```python --version```
2. Descargamos e instalamos un entorno de desarrollo si vamos a realizar modificaciones. Se recomienda emplear Pycharm. Si no se van a realizar modificaciones, se puede ejecutar el proyecto directamente desde consola sin instalar ningún IDE.
3. Creamos el [entorno virutal](https://docs.python.org/3/library/venv.html) en la ruta Server ```venviorments```. Para ello ejecutar el siguiente comando:

```python -m venv ./venviorments/FCTMaker```


4. Ejecutamos el siguiente archivo para seleccionar el entorno virtual ```.\venviorments\FCTMaker\Scripts\activate```. Si tuviésemos problemas de permisos para ejecutar dicho comando en Windows, revisar [este enlace](https://tecadmin.net/powershell-running-scripts-is-disabled-system/) y correr el comando que aparece como superadministrador en PowerShell.

5. Actualizamos pip ```pip install --upgrade pip```
6. Instalamos los requerimientos ```pip install -r requerimientos.txt```. Es posible que haya errores durante la instalación de los requisitos en Windows, para solucionarlo sería necesario instalar algunos componentes para ejecutar C++ como aparece en la respuesta de [esta pregunta de Stackoverflow](https://stackoverflow.com/questions/64261546/python-cant-install-packages) (Descargar vs_buildtools y ejecutar el comando que aparece al final de la respuesta marcada como solución).

# Credenciales de acceso:
El acceso a la aplicación tiene las siguientes credenciales por defecto:

- **Usuario**: admin
- **Pass**: admin

**IMPORTANTE**: Es indispensable eliminar dichas credenciales en una versión en producción. Se puede eliminar un usuario desde la administración de FCTMaker.

Para crear un nuevo usuario administrador podemos hacer emplear la línea de comandos:

```python .\manage.py createsuperuser```

También se puede realizar la gestión desde la parte de administración de FCTMaker.


## Base de datos:
Por defecto se emplea sqlite, pero podría emplearse cualquier otra base de datos, como cualquier proyecto de Django.

Por defecto, se incluye una base de datos en **db.sqlite3**. Contiene información de prueba que habría que modificar o eliminar.


## Cambiar el modelo de la BD:
Si fuese necesario cambiar el modelo de la base de datos habra que realizar los suiguientes pasos:
Extraído directamente del [tutorial](https://docs.djangoproject.com/en/2.0/intro/tutorial02/)
 
1. ```python manage.py makemigrations```
2. ```python manage.py migrate```

**OJO** Si añadimos nuevos modelos hay que registrarlos en ```admin.py``` 

## Realizar consultas sobre los modelos, realizar pruebas o modificar datos en CLI:

Se ha extraido directamente del tutorial de Django

1. ```python manage.py shell```
2. ```from fct.models import Tutor_Centro, Datos_Instituto, Datos_Empresa, Ciclo_Formativo, Curso, Alumno, Historico_Alumno_Curso```  //Añadimos los modelos que necesitamos.
3. ```Alumno.objects.all/filter/delete...``` Escribimos las sentencias de consulta necesarias. Ojo con modificar los datos que se reflejan en la BD.

## Copias de seguridad de la BD:
Se deja el script de Bash denominado *copia.sh* para configurarlo y automatizar de manera simple las copias de seguridad.


## Plantillas para los DOCX Generados:
Para modificar las plantillas sobre la que se generan todos los anexos, simplemente hay que modificar las bases que se encuentran subidas en ```fct/templatesDOCX```

