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
from datetime import datetime, timedelta
from routes.marca import marca
# * Un dato importante para descargar el pdf es que debe ser con el siguiente comando de node 
#  * npm i html2pdf.js
block_until = {} # Diccionario para almacenar las sesiones de los usuarios como cierre de caja


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
    # Verificar si el sistema está bloqueado por cierre de caja
    ip_address = request.remote_addr
    
    # Variable para controlar si se debe verificar el bloqueo (por defecto sí)
    check_block = True
    
    if request.method == 'POST':
        usuario = request.form['user']
        password = request.form['contraseña']
        
        # Verificar primero si es un administrador
        usuario_fo = db.admin.find_one({'user':usuario,'contraseña':password})
        
        # Si es un administrador, no verificar el bloqueo
        if usuario_fo:
            check_block = False
            session["username"] = usuario
            return redirect(url_for('transicion'))
        
        # Si no es administrador, verificar si es operador
        operador = db.user.find_one({'user':usuario,'contraseña':password})
        
        # Si es operador, verificamos el bloqueo antes de continuar
        if operador and check_block and ip_address in block_until:
            current_time = datetime.now()
            if current_time < block_until[ip_address]:
                # Calcular tiempo restante
                remaining = block_until[ip_address] - current_time
                
                # Convertir a horas, minutos y segundos para mostrar
                remaining_hours = int(remaining.total_seconds() // 3600)
                remaining_minutes = int((remaining.total_seconds() % 3600) // 60)
                remaining_seconds = int(remaining.total_seconds() % 60)
                
                # Mostrar mensaje de bloqueo
                flash(f"Sistema bloqueado por cierre de caja. Disponible en {remaining_hours}h {remaining_minutes}m {remaining_seconds}s.")
                return render_template('index.html', 
                                    remaining_hours=remaining_hours,
                                    remaining_minutes=remaining_minutes, 
                                    remaining_seconds=remaining_seconds,
                                    total_seconds=int(remaining.total_seconds()))
        
        # Si es operador y no hay bloqueo o ya pasó el tiempo, permitir acceso
        if operador:
            session["username"] = usuario
            return redirect(url_for('user.usventa'))
        
        # Si no es ni administrador ni operador, mostrar error
        flash("Contraseña incorrecta")
        return redirect(url_for('index'))
    else:
        # Para peticiones GET, verificar bloqueo solo si no es un administrador ya logueado
        admin_logged_in = "username" in session and db.admin.find_one({'user': session["username"]})
        
        # Si no hay un administrador logueado, verificar el bloqueo
        if not admin_logged_in and ip_address in block_until:
            current_time = datetime.now()
            if current_time < block_until[ip_address]:
                # Calcular tiempo restante
                remaining = block_until[ip_address] - current_time
                
                # Convertir a horas, minutos y segundos para mostrar
                remaining_hours = int(remaining.total_seconds() // 3600)
                remaining_minutes = int((remaining.total_seconds() % 3600) // 60)
                remaining_seconds = int(remaining.total_seconds() % 60)
                
                # Mostrar mensaje de bloqueo
                flash(f"Sistema bloqueado por cierre de caja . Disponible en {remaining_hours}h {remaining_minutes}m {remaining_seconds}s.")
                return render_template('index.html', 
                                    remaining_hours=remaining_hours,
                                    remaining_minutes=remaining_minutes, 
                                    remaining_seconds=remaining_seconds,
                                    total_seconds=int(remaining.total_seconds()))
            else:
                # Eliminar el bloqueo si ya pasó el tiempo
                del block_until[ip_address]   

    # Este codigo es para que funcione lo que ingresao de administrado y usuario
    
    if request.method == 'POST':
        usuario = request.form['user']
        password = request.form['contraseña']
        usuario_fo = db.admin.find_one({'user':usuario,'contraseña':password})
        operador = db.user.find_one({'user':usuario,'contraseña':password})
        if usuario_fo:
            session["username"]= usuario
            return redirect(url_for('transicion'))
        elif operador:
            session["username"]= usuario # Recuerda que para que pueda salir el nombre de usuario tiene que ser username como 
            # Aparece en el codigo de carpeta user de routes
            return redirect(url_for('user.usventa'))
        else:
            flash("Contraseña incorrecta")
            return redirect(url_for('index'))
    else:
        return render_template('index.html')


# Este es para cerrar caja solo para usuario
# Ruta para manejar el cierre de caja
@app.route('/cerrar_caja', methods=['POST'])
def cerrar_caja():
    # Verificar si hay una sesión activa
    if "username" not in session:
        flash("Debe iniciar sesión para realizar esta acción.")
        return redirect(url_for('index'))
    
    # Obtener el nombre de usuario actual
    current_user = session["username"]
    
    # Verificar si el usuario es un operador y no un administrador
    operador = db.user.find_one({'user': current_user})
    
    if not operador :
        # Si el usuario es un administrador o no es un operador, no permitir el cierre
        flash("Solo los operadores pueden cerrar caja.")
        return redirect(url_for('user.usventa'))
    
    # Obtener la dirección IP del usuario para el bloqueo
    ip_address = request.remote_addr
    
    # Establecer el tiempo de bloqueo (14 horas desde ahora)
    block_until[ip_address] = datetime.now() + timedelta(hours=14)
    
    # Cerrar la sesión actual
    session.pop("username", None)
    
    flash("Caja cerrada. El sistema estará bloqueado por 14 horas.")
    return redirect(url_for('index'))


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

# Codigo para marca
app.register_blueprint(marca)

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