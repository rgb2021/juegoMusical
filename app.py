import os
import secrets
import psycopg2

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

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

@app.route('/insert')
def insertBd():
    contra = os.environ.get('CONTRA')
    try:
        cnx = psycopg2.connect(user="wundvabjfd", password=contra, host="juegogustosmusicales"
                                                                        "-server.postgres.database"
                                                                        ".azure.com", port=5432,
                               database="juegogustosmusicales-database")
        cursor = cnx.cursor()
        insert_table_query = ("INSERT INTO usuarios (nombre, url, token) VALUES ('Juan Pérez', 'https://ejemplo.com', 'abc123');")
        cursor.execute(insert_table_query)
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

    return "registro insertado correctamente."

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
        elementos = cursor.fetchall()
    except Exception as e:
        # En caso de error, imprimir el mensaje de error
        elementos = []
        mensaje_error = f'Error al obtener elementos: {str(e)}'
        return render_template('lista_elementos.html', elementos=elementos, mensaje_error=mensaje_error)

@app.route('/')
def index():
    print('Request for index page received')
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/hello', methods=['POST'])
def hello():
    longitud = 32
    name = request.form.get('name')
    url = request.form.get('url')
    token = secrets.token_hex(longitud // 2)

    if name:
        print('Request for hello page received with name=%s' % name)
        return render_template('hello.html', name=name, url=url, token=token)
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
