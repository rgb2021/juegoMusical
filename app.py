import os
import secrets
import psycopg2

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)


@app.route('/createbd')
def createBd():
#    try:
#        cnx = psycopg2.connect(user="wundvabjfd", password=os.environ.get('CONTRA'), host="juegogustosmusicales"
#                                                                                          "-server.postgres.database"
#                                                                                          ".azure.com", port=5432,
#                               database="juegogustosmusicales-database")
#        cursor = cnx.cursor()
#        create_table_query = ("CREATE TABLE IF NOT EXISTS usuarios (id SERIAL PRIMARY KEY,nombre VARCHAR(255),"
#                              "url VARCHAR(255),token VARCHAR(255));")
#        cursor.execute(create_table_query)
#        cnx.commit()
#        print("La tabla fue creada correctamente.")
#    except Exception as e:
#        # Si se produce un error, imprímelo
#        print("Error:", e)
#    finally:
#        # Cierra el cursor y la conexión
#        if cursor:
#            cursor.close()
#        if cnx:
#            cnx.close()

    password = os.environ.get('CONTRA')
    return password
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
   longitud=32
   name = request.form.get('name')
   url = request.form.get('url')
   token = secrets.token_hex(longitud // 2)

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name , url = url , token = token)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.run()
