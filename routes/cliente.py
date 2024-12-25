from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from controllers.database import Conexion as dbase
from modules.cliente import Cliente
from pymongo import MongoClient
db = dbase()

cliente = Blueprint('cliente', __name__)

@cliente.route('/admin/in_cliente',methods=['GET','POST'])
def adcli():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('cliente.index'))  # Redirige al usuario al inicio si no está en la sesión
    

    if request.method == 'POST':
        cliente = db["cliente"]
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        cedula = request.form['cedula']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        correo = request.form['correo']

        exist_nombre = cliente.find_one({"nombre": nombre})
        exist_apellido = cliente.find_one({"apellido":apellido})
        exist_cedula = cliente.find_one({"cedula": cedula})
        exist_direccion = cliente.find_one({"direccion": direccion})
        exist_telefono = cliente.find_one({"telefono": telefono})
        exist_correo = cliente.find_one({"correo": correo})

        if exist_nombre:
            return redirect(url_for('cliente.adcli',message ="El nombre ya existe"))
        elif exist_apellido:
            return redirect(url_for('cliente.adcli',message ="El apellido ya existe"))
        elif exist_cedula:
            return redirect(url_for('cliente.adcli',message ="La cedula ya existe"))
        elif exist_direccion:
            return redirect(url_for('cliente.adcli',message ="La dirección ya existe"))
        elif exist_telefono:
            return redirect(url_for('cliente.adcli',message ="El telefono ya existe"))
        elif exist_correo:
            return redirect(url_for('cliente.adcli',message ="El correo ya existe"))
        else:
            client = Cliente(None, nombre, apellido, cedula, direccion, telefono, correo)
            cliente.insert_one(client.ClienteDBCollection())
            return redirect(url_for('cliente.adcli', message="Enviado a la base de datos"))
    else:
        return render_template('admin/in_cliente.html',message=request.args.get('message'))
        






        
