from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from controllers.database import Conexion as dbase
from modules.producto import Producto
from pymongo import MongoClient
db = dbase()

producto = Blueprint('producto', __name__)

@producto.route('/admin/in_producto', methods=['GET', 'POST'])
def adpro():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('user.index'))  # Redirige al usuario al inicio si no está en la sesión
    
    if request.method == 'POST':
        producto = db["producto"]
        nombre = request.form['nombre'] # Este debe contener completo el nombre
        precio = request.form['precio']
        color = request.form['color']
        img = request.form['img']
        cantidad = request.form['cantidad']

        exist_nombre = producto.find_one({"nombre": nombre})

        if exist_nombre:
            flash("El nombre del producto ya existe")
            return redirect(url_for('producto.adpro'))
        else:
            produc = Producto(nombre, precio, color, img, cantidad)
            producto.insert_one(produc.ProductoDBCollection())
            flash("Producto agregado correctamente")
            return redirect(url_for('producto.adpro'))

    else:
        return render_template('admin/in_producto.html')
        
            

