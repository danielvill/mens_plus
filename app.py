from flask import flash, Flask, json, send_file,session, render_template, request,Response ,jsonify, redirect, url_for
from bson import json_util
from controllers.database import Conexion as dbase
from datetime import datetime,timedelta #* Importacion de manejo de tiempo
from flask import jsonify
from reportlab.pdfgen import canvas # *pip install reportlab este es para imprimir reportes
from reportlab.lib.pagesizes import letter #* pip install reportlab 
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle, Spacer ,Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet ,ParagraphStyle
from routes.cliente import cliente
from routes.producto import producto
from routes.venta import venta
from routes.user import user
from flask import Flask
from mail_config import mail
# El siguiente es para usar lo que es pug 
from jinja2 import Environment, FileSystemLoader# pip install Flask Jinja2
import os
# * Un dato importante para descargar el pdf es que debe ser con el siguiente comando de node 
#  * npm i html2pdf.js



db = dbase()
app = Flask(__name__)
app.secret_key = 'menplus105'
app.config['UPLOAD_FOLDER'] = 'D:/Sistema men_plus/static/assets/img'

# Configuración de email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = ''  # Tu dirección de Gmail
app.config['MAIL_PASSWORD'] = ''  # Tu contraseña de Gmail
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# Inicializar mail
mail.init_app(app)
# * Crear Backup de la base de datos 
@app.route('/crear_backup', methods=['POST'])
def crear_backup():
    # Obtén los datos de las colecciones 'producto', 'stock' y 'usuarios'
    producto_data = db.producto.find({}, {'_id': 0})  # Excluye el campo '_id'
    cliente_data = db.cliente.find({}, {'_id': 0})
    venta_data = db.venta.find({}, {'_id': 0})

    # Crea una carpeta para los respaldos (si no existe)
    backup_folder = 'backups'
    os.makedirs(backup_folder, exist_ok=True)

    # Genera nombres de archivo con la fecha actual
    fecha_actual = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    producto_filename = f'{backup_folder}/producto_{fecha_actual}.json'
    cliente_filename = f'{backup_folder}/cliente_{fecha_actual}.json'
    venta_filename = f'{backup_folder}/venta_{fecha_actual}.json'

    # Guarda los datos en archivos JSON
    with open(producto_filename, 'w') as producto_file:
        for empleado in producto_data:
            json.dump(empleado, producto_file)
            producto_file.write('\n')

    with open(cliente_filename, 'w') as cliente_file:
        for herramienta in cliente_data:
            json.dump(herramienta, cliente_file)
            cliente_file.write('\n')

    with open(venta_filename, 'w') as venta_file:
        for venta in venta_data:
            json.dump(venta, venta_file)
            venta_file.write('\n')
    return redirect(url_for('completo'))

# todo : Tengo que terminar bien la animacion para el respaldo a la base de datos 

# Transiciones
@app.route('/completo')
def completo():
    return render_template('/admin/completo.html')

@app.route('/admin/completo')
def adcomp():
    return redirect(url_for('user.aduser'))


# * Vista de Ingreso al sistema 
@app.route('/',methods=['GET','POST'])
def run():
    return render_template('index.html')


#* Este es para cerrar la sesion 
@app.route('/logout')
def logout():
    # Elimina el usuario de la sesión si está presente
    session.pop('username', None)
    return redirect(url_for('index'))


#* Vista Ingreso de admin y usuarios
@app.route('/index',methods=['GET','POST'])
def index():

    if request.method == 'POST':
        usuario = request.form['user']
        password = request.form['contraseña']
        usuario_fo = db.admin.find_one({'user':usuario,'contraseña':password})
        if usuario_fo:
            session["username"]= usuario
            return redirect(url_for('transicion'))
        else:
            flash("Contraseña incorrecta")
            return redirect(url_for('index'))
    else:
        return render_template('index.html')

# Transiciones
@app.route('/transicion')
def transicion():
    return render_template('transition.html')

@app.route('/user/aduser')
def aduser():
    return redirect(url_for('user.aduser'))




# *Codigo de ingreso de usuarios
app.register_blueprint(user)

# *Codigo de ingreso de clientes
app.register_blueprint(cliente)

# *Codigo de ingreso de producto
app.register_blueprint(producto)

# Importar y registrar venta después de inicializar mail
# Importar y registrar Blueprint después de inicializar mail
from routes.venta import venta, init_mail
init_mail(mail)
app.register_blueprint(venta)

@app.errorhandler(404)
def notFound(error=None):
    message = {
        'message': 'No encontrado ' + request.url,
        'status': '404 Not Found'
    }
    return render_template('404.html', message=message), 404


if __name__ == '__main__':
    app.run(debug=True, port=4000)