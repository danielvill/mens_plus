from flask import Blueprint, render_template, request, flash, session, redirect, url_for, current_app
from controllers.database import Conexion as dbase
from werkzeug.utils import secure_filename
import os
from modules.marca import Marca
from pymongo import MongoClient
db = dbase()

marca = Blueprint('marca', __name__)


# Este codigo es para lo que es el ID
def get_next_sequence(name): 
    seq = db.seqs.find_one({'_id': name})
    if seq is None:
        # Inicializa 'productoId' en 220 si no existe
        db.seqs.insert_one({'_id': 'marcaId', 'seq': 0})
        seq = db.seqs.find_one({'_id': name})

    result = db.seqs.find_one_and_update(
        {'_id': name},
        {'$inc': {'seq': 1}},
        return_document=True
    )
    return result.get('seq')

# Ingresar con un id marca
@marca.route('/admin/in_marca',methods=['GET','POST'])
def in_marca():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('marca.index'))  # Redirige al usuario al inicio si no está en la sesión
    
    if request.method == 'POST':
        id_marca = str(get_next_sequence('marcaId')).zfill(3)
        marca = db["marca"]
        nombre = request.form['nombre']
        proveedor = request.form['proveedor']
        comentario = request.form['comentario']

        exist_nombre = marca.find_one({"nombre": nombre})

        if exist_nombre:
            flash("El nombre de la marca ya existe", "danger")
            return redirect(url_for('marca.in_marca'))
        
        else:
            mar = Marca(id_marca, nombre, proveedor, comentario)
            marca.insert_one(mar.MarcaDBCollection())
            flash("Marca enviada a la base de datos", "success")
            return redirect(url_for('marca.in_marca'))
    else:
        return render_template('admin/in_marca.html', message=request.args.get('message'))
    
@marca.route('/edit_marca/<string:edamarca>', methods=['GET', 'POST'])#
def edit_marca(edamarca):
    marca = db['marca']
    nombre = request.form["nombre"]
    proveedor = request.form["proveedor"]
    comentario = request.form["comentario"]
    
    if nombre and proveedor and comentario:
        marca.update_one({'id_marca' : edamarca}, {'$set' : {'nombre' : nombre, 'proveedor' : proveedor, 'comentario' : comentario}})
        flash("Marca  "+ nombre + " editada correctamente " , "success")
        return redirect(url_for('marca.v_marca'))
    else:
        flash("Error al editar la marca", "danger")
        return redirect(url_for('marca.v_marca'))

# Eliminar marca
@marca.route('/del_marca/<string:delmarca>', methods=['GET', 'POST'])
def del_marca(delmarca):
    marca = db['marca']
    marca.delete_one({'id_marca': delmarca})
    flash("Marca eliminada correctamente", "success")
    return redirect(url_for('marca.v_marca'))

# Mostrar marcas
@marca.route('/admin/marca', methods=['GET'])
def v_marca():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('marca.index'))
    marcas = db['marca'].find()
    return render_template('admin/marca.html', marcas=marcas)


# Mostrar marcas
@marca.route('/user/marca', methods=['GET'])
def u_marca():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('marca.index'))
    marcas = db['marca'].find()
    return render_template('user/marca.html', marcas=marcas)
