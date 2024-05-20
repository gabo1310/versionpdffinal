# Primer uso
## SE DEBE USAR PYTHON 3.11 EN ADELANTE, TENER INSTALADO TODO LO NECESARIO PARA CREAR ENTORNOS VIRTUALES .VENV Y PIPENV
## Preparacion entorno virtual (en la carpeta de trabajo)

```
# Crear el entorno virtual
python -m venv .venv

# Activacion (aparecera un .venv a la izquierda)
.\.venv\Scripts\activate

# Instalar dependencias (puede tardar un rato)
pip install -r requirements.txt

# Inicializar database
flask --app app.web init-db
```

### Hacer funcionar el server python(en caso de ya preparar el entorno, no es necesario el .\.venv\Scripts\activate, si se enciende por segunda vez, si se debe activar, aparecera a la izquierda de los comandos un (.venv) que muestra que esta listo):

.\.venv\Scripts\activate
```
```
ejecutar: 
inv dev

posibles errores: el problema de langchain es que 
tiene problemas de incopatibilidad entre algunas versiones de sus  librerias
para solucionarlo (ocupo windows 10 por si acaso ya que puede dar otros problemas en windows 11 segun los foros):
No module named 'pwd': instalar esta version: langchain-community==0.0.19 o alguna similar que no de problemas, revisar las de langchain en particular 

problemas con anthropic o langchain-anthropic, instalar la ultima version, sino buscar alguna anterior que sea compatible y que no de problemas entre las otras

en el requeriments.txt estan todas las versiones, puede aparecer el mensaje de warning, se puede ignorar ya que por el momento ya no daria errores

```

### hacer funcionar el redis

en una nueva terminal crear un nuevo entorno virtual en caso de no haberlo creado inicialmente:
```
python -m venv .venv

activar entorno virtual, recordar el .venv para ver que esta activado:

.\.venv\Scripts\activate

y luego: 

inv devworker
```



### hacer funcionar el "database " para mostrar los pdf:
se debe ejecutar esto en la carpeta de local-do-filepdf

pipenv shell

pipenv install

(en caso de ya instalarlo por primera vez, utilizar solo pipenv shell en adelante)

# Instalar dependencias (puede tardar un rato)
pip install -r requirements.txt

ejecutar: 
python app.py


-----------------------
#modificaciones:
## si se quieren hacer modificaciones al front, se debe primero se debe construir las dependencias npm:
npm install --save-dev vite
y luego: 
npm run build

esto es debido a que utiliza de manera estatica las creacione de las paginas, por lo que con npm se debe ir a cada instante construir esta instancia
#   p d f i a r e v i s i o n  
 #   p d f i a r e v i s i o n  
 #   p d f i a r e v i s i o n  
 #   p d f i a r e v i s i o n  
 #   p d f i a r e v i s i o n  
 #   p d f i a  
 #   v e r s i o n p d f f i n a l  
 