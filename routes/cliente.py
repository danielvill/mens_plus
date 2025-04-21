from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from controllers.database import Conexion as dbase
from modules.cliente import Cliente
from pymongo import MongoClient
db = dbase()

cliente = Blueprint('cliente', __name__)


# Ingreso con un Id unico
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

        exist_cedula = cliente.find_one({"cedula": cedula})
        exist_telefono = cliente.find_one({"telefono": telefono})
        exist_correo = cliente.find_one({"correo": correo})

        if exist_cedula:
            flash("La cedula ya existe" , "danger")
            return redirect(url_for('cliente.adcli'))
        elif exist_telefono:
            flash("El celular ya existe" ,"danger")
            return redirect(url_for('cliente.adcli'))
        elif exist_correo:
            flash("El correo ya existe" , "danger")
            return redirect(url_for('cliente.adcli'))
        else:
            client = Cliente( nombre, apellido, cedula, direccion, telefono, correo)
            cliente.insert_one(client.ClienteDBCollection())
            flash("Enviado a la base de datos" , "success")
            return redirect(url_for('cliente.adcli'))
    else:
        return render_template('admin/in_cliente.html',message=request.args.get('message'))
        
@cliente.route('/edit_cli/<string:edacli>', methods=['GET', 'POST'])#
def edit_cli(edacli):
    cliente = db['cliente']
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    cedula = request.form['cedula']
    direccion = request.form["direccion"]
    telefono = request.form["telefono"]
    correo = request.form['correo']
    
    if nombre and apellido  and cedula and direccion and telefono and correo:
        cliente.update_one({'cedula' : edacli}, {'$set' : {'nombre' : nombre, 'apellido' : apellido, 'cedula' : cedula ,"direccion" :direccion , "telefono" : telefono , "correo" : correo}})
        flash("Cliente  "+ nombre + " con  cedula " + cedula + " editado correctamente " , "success")
        return redirect(url_for('cliente.v_cli'))
    else:
        return render_template('admin/cliente.html')

# * Eliminar cliente
@cliente.route('/delete_cli/<string:eliacli>')
def delete_cli(eliacli):
    cliente = db["cliente"]
    documento =  cliente.find_one({"cedula":eliacli})
    nombre = documento["nombre"]
    apellido = documento["apellido"]
    cedula = documento["cedula"]
    cliente.delete_one({"cedula":eliacli})
    flash("Cliente  "+ nombre +" "+ apellido +" con cedula " + cedula  + " eliminado correctamente" , "success") 
    return redirect(url_for('cliente.v_cli'))

# Visualizar cliente
@cliente.route("/admin/cliente")
def v_cli():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('cliente.index'))
    cliente = db['cliente'].find()
    return render_template("admin/cliente.html", cliente=cliente)


