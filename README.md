# Introduccion
Esto es un pequeño proyecto casero para crear un juego en el que un grupo de usuarios selecciona un video musical de youtube. 
Cuando todos los usuarios han seleccionado el suyo. Se genera una lista con todos los videos y todos los usuarios votan para dar una puntuacion a la cancion y para intentar adivinar quien selecciono cada cancion.

Se ha creado una pequeña API para gestionar el juego
# Metodos API
## /
Este metodo renderiza la pagina para pedir los datos al usuario y los envia al metodo /insert
## /create
Este metodo crea las tablas usuarios y votaciones en la base de datos
## /insert
Este metodo genera un token y lo inserta en la tabla de usuarios junto con el nombre y la url del video seleccionado
## /list
Este metodo imprime todos los usuarios y las votaciones registrados hasta ahora
## /count
Este metodo muestra el numero de usuarios
## /clear
Este metodo elimina la tabla de usuarios y las votaciones
## /vote
Este metodo genera el formulario de votacion
## /ratings
Este metodo procesa las votaciones 
