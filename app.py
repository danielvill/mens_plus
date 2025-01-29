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
# El siguiente es para usar lo que es pug 
from jinja2 import Environment, FileSystemLoader# pip install Flask Jinja2

# * Un dato importante para descargar el pdf es que debe ser con el siguiente comando de node 
#  * npm i html2pdf.js

db = dbase()
app = Flask(__name__)
app.secret_key = 'menplus105'
app.config['UPLOAD_FOLDER'] = 'D:/Sistema men_plus/static/assets/img'



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

# *Codigo de ingreso de venta
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