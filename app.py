import json
import os
import secrets
import urllib

import psycopg2

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for, jsonify)

app = Flask(__name__)


@app.route('/create')
def createBd():
    contra = os.environ.get('CONTRA')
    try:
        cnx = psycopg2.connect(user="wundvabjfd", password=contra, host="juegogustosmusicales"
                                                                        "-server.postgres.database"
                                                                        ".azure.com", port=5432,
                               database="juegogustosmusicales-database")
        cursor = cnx.cursor()
        create_table_query = ("CREATE TABLE IF NOT EXISTS usuarios (id SERIAL PRIMARY KEY,nombre VARCHAR(255),"
                              "url VARCHAR(255),token VARCHAR(255));")
        cursor.execute(create_table_query)
        cnx.commit()

        create_table_query = (
            "CREATE TABLE IF NOT EXISTS votaciones (id SERIAL PRIMARY KEY,token VARCHAR(255), nombre VARCHAR(255),valoracion INTEGER);")
        cursor.execute(create_table_query)
        cnx.commit()

    except Exception as e:
        # Si se produce un error, imprímelo
        return str(e)
    # finally:
    # Cierra el cursor y la conexión
    # if cursor:
    #     cursor.close()
    # if cnx:
    #     cnx.close()

    return "La tabla fue creada correctamente."


@app.route('/insert', methods=['POST'])
def insertBd():
    contra = os.environ.get('CONTRA')
    name = request.form.get('name')
    url = request.form.get('url')
    longitud = 32
    token = secrets.token_hex(longitud // 2)
    try:
        cnx = psycopg2.connect(user="wundvabjfd", password=contra, host="juegogustosmusicales"
                                                                        "-server.postgres.database"
                                                                        ".azure.com", port=5432,
                               database="juegogustosmusicales-database")
        cursor = cnx.cursor()
        insert_table_query = ("INSERT INTO usuarios (nombre, url, token) VALUES (%s , %s ,%s)")
        cursor.execute(insert_table_query, (name, url, token))
        cnx.commit()
    except Exception as e:
        # Si se produce un error, imprímelo
        return str(e)
    # finally:
    # Cierra el cursor y la conexión
    # if cursor:
    #     cursor.close()
    # if cnx:
    #     cnx.close()

    return render_template('hello.html', name=name, url=url, token=token)


@app.route('/list')
def listBd():
    contra = os.environ.get('CONTRA')
    try:
        cnx = psycopg2.connect(user="wundvabjfd", password=contra, host="juegogustosmusicales"
                                                                        "-server.postgres.database"
                                                                        ".azure.com", port=5432,
                               database="juegogustosmusicales-database")
        cursor = cnx.cursor()
        select_query = "SELECT * FROM usuarios;"
        cursor.execute(select_query)
        # Obtener todos los resultados
        listaUsuarios = cursor.fetchall()

        cursor = cnx.cursor()
        select_query = "SELECT * FROM votaciones;"
        cursor.execute(select_query)
        # Obtener todos los resultados
        listaVotaciones = cursor.fetchall()

        # numero_filas = cursor.fetchone()[0]
    except Exception as e:
        # En caso de error, imprimir el mensaje de error
        # elementos = []
        # mensaje_error = f'Error al obtener elementos: {str(e)}'
        numero_filas = 0
        return str(e)

    return render_template('lista_elementos.html', listaUsuarios=listaUsuarios, listaVotaciones=listaVotaciones)
    # return str(numero_filas)


@app.route('/count')
def countBd():
    contra = os.environ.get('CONTRA')
    try:
        cnx = psycopg2.connect(user="wundvabjfd", password=contra, host="juegogustosmusicales"
                                                                        "-server.postgres.database"
                                                                        ".azure.com", port=5432,
                               database="juegogustosmusicales-database")
        cursor = cnx.cursor()
        select_query = "SELECT COUNT(*) FROM usuarios;"
        cursor.execute(select_query)
        # Obtener todos los resultados
        # elementos = cursor.fetchall()
        numero_filas = cursor.fetchone()[0]
    except Exception as e:
        # En caso de error, imprimir el mensaje de error
        # elementos = []
        # mensaje_error = f'Error al obtener elementos: {str(e)}'
        numero_filas = 0
        return "petando voy"

    # return render_template('lista_elementos.html', elementos=elementos, mensaje_error=mensaje_error)
    return str(numero_filas)


@app.route('/')
def index():
    print('Request for index page received')
    return render_template('index.html')


@app.route('/clear')
def clear():
    contra = os.environ.get('CONTRA')
    try:
        # Establecer la conexión a la base de datos
        cnx = psycopg2.connect(user="wundvabjfd", password=contra,
                               host="juegogustosmusicales-server.postgres.database.azure.com", port=5432,
                               database="juegogustosmusicales-database")
        cursor = cnx.cursor()
        # Construir la sentencia SQL DELETE
        delete_query = "DELETE FROM usuarios;"
        # Ejecutar la sentencia DELETE
        cursor.execute(delete_query)
        # Confirmar los cambios en la base de datos
        cnx.commit()

        delete_query = "DELETE FROM votaciones;"
        # Ejecutar la sentencia DELETE
        cursor.execute(delete_query)
        # Confirmar los cambios en la base de datos
        cnx.commit()

    except Exception as e:
        # En caso de error, imprimir el mensaje de error
        return str(e)
    # finally:
    # Cerrar el cursor y la conexión
    # cursor.close()
    # conn.close()
    return "La tabla usuarios y votaciones han sido vaciadas exitosamente."


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


def generar_json(conn):
    # Crear un cursor
    cur = conn.cursor()

    # Ejecutar la consulta
    cur.execute("SELECT nombre, url, token FROM usuarios")

    # Obtener todos los registros
    registros = cur.fetchall()

    # Datos para el JSON
    datos = [
        {
            "url": registro[1],
            "nombres": [registro[0] for registro in registros],
            "valoracion": 0,
            "token": registro[2]
        } for registro in registros
    ]

    # Convertir los datos a JSON
    json_datos = json.dumps(datos)

    return json_datos
@app.route('/vote')
def votar():
    contra = os.environ.get('CONTRA')
    try:
        cnx = psycopg2.connect(user="wundvabjfd", password=contra,
                               host="juegogustosmusicales-server.postgres.database.azure.com", port=5432,
                               database="juegogustosmusicales-database")
        res = generar_json(cnx)

    except Exception as e:
        # Si hay algún error, realiza un rollback
        cnx.rollback()
        return jsonify({"error": str(e)})

    return render_template('votacion.html', datos=str(res))


@app.route('/ratings')
def recibir_valoraciones():
    contra = os.environ.get('CONTRA')
    parametros_url = request.args.get('datos')  # Obtén el parámetro de la URL
    datos_recibidos = json.loads(urllib.parse.unquote(parametros_url))

    # Procesa los datos según tus necesidades
    print("Datos recibidos:", datos_recibidos)
    # return jsonify({"mensaje": "Datos recibidos correctamente"},{"datos":datos_recibidos})

    try:
        cnx = psycopg2.connect(user="wundvabjfd", password=contra,
                               host="juegogustosmusicales-server.postgres.database.azure.com", port=5432,
                               database="juegogustosmusicales-database")
        cursor = cnx.cursor()
        # Recorre el JSON y realiza una inserción por cada fila en la base de datos

        elementos = []
        for key, value in datos_recibidos.items():
            nombre = value.get('nombre')
            valoracion = value.get('valoracion')

            elementos.append({key, nombre, valoracion})
            # Realiza la inserción en la base de datos
            cursor.execute("INSERT INTO votaciones (token , nombre, valoracion) VALUES (%s, %s, %s)",
                           (key, nombre, valoracion))

            # Confirma la transacción
            cnx.commit()

    except Exception as e:
        # Si hay algún error, realiza un rollback
        cnx.rollback()
        return jsonify({"error": str(e)})

    return render_template('votado.html', datos=datos_recibidos.items())


@app.route('/hello', methods=['POST'])
def hello():
    longitud = 32
    name = request.form.get('name')
    url = request.form.get('url')
    token = secrets.token_hex(longitud // 2)

    if name:
        print('Request for hello page received with name=%s' % name)

    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
