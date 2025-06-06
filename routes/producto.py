from flask import Blueprint, render_template, request, flash, session, redirect, url_for, current_app
from controllers.database import Conexion as dbase
from werkzeug.utils import secure_filename
import os
from modules.producto import Producto
from pymongo import MongoClient
db = dbase()

producto = Blueprint('producto', __name__)

# Este es para lo que es las imagenes
@producto.route('/alguna_ruta')
def alguna_funcion():
    UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
    
# codigo de verificacion de productos con las imagenes
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Este codigo es para las  imagenes
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Este codigo es para lo que es el ID
def get_next_sequence(name): 
    seq = db.seqs.find_one({'_id': name})
    if seq is None:
        # Inicializa 'productoId' en 220 si no existe
        db.seqs.insert_one({'_id': 'productoId', 'seq': 0})
        seq = db.seqs.find_one({'_id': name})

    result = db.seqs.find_one_and_update(
        {'_id': name},
        {'$inc': {'seq': 1}},
        return_document=True
    )
    return result.get('seq')

@producto.route('/admin/in_producto', methods=['GET', 'POST'])
def adpro():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('user.index'))
    marcas = db['marca'].find()

    if request.method == 'POST':
        id_producto = str(get_next_sequence('productoId')).zfill(3)
        producto = db["producto"]
        nombre = request.form['nombre']
        talla = request.form['talla']
        precio = request.form['precio']
        color = request.form['color']
        marca  = request.form['marca']
        cantidad = request.form['cantidad']
        
        exist_nombre_color = producto.find_one({"nombre": nombre, "color": color})

        if exist_nombre_color:
            flash("El nombre del producto y el color ya existen", "danger")
            return redirect(url_for('producto.adpro'))

        else:
            if 'imagen' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['imagen']
            if file.filename == '':
                flash('Selecciona una imagen')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                imagen_filename = filename
            
            produc = Producto(id_producto, nombre, talla,precio, color, imagen_filename, marca,cantidad)
            producto.insert_one(produc.ProductoDBCollection())
            flash("Producto agregado correctamente" , "success")
            return redirect(url_for('producto.adpro'))

    else:
        return render_template('admin/in_producto.html',marcas=marcas)

# Editar Producto
@producto.route('/edit_pro/<string:edipro>', methods=['GET', 'POST'])
def edit_pro(edipro):
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('producto.index'))
    producto = db['producto']
    producto_existente = producto.find_one({"id_producto": edipro})
    marca = db['marca'].find()
    if request.method == 'POST':
        id_producto = request.form["id_producto"]
        nombre = request.form["nombre"]
        precio = request.form["precio"]
        color = request.form["color"]
        cantidad = request.form["cantidad"]

        if "imagen" in request.files and request.files['imagen'].filename != '':
            file = request.files['imagen']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                imagen_filename = os.path.join('img', filename)
        else:
            imagen_filename = producto_existente['imagen']

        campos = [id_producto, nombre, precio, color, cantidad]

        try:
            if all(campos):
                producto.update_one({"id_producto": edipro}, {"$set": {
                    "id_producto": id_producto,
                    "nombre": nombre,
                    "precio": precio,
                    "color": color,
                    "cantidad": cantidad,
                    "imagen": imagen_filename
                }})
                flash("Producto " + nombre + " actualizado correctamente" ,"success")
                return redirect(url_for('producto.v_product'))
            else:
                flash("Todos los campos son obligatorios")
                return redirect(url_for('producto.edit_pro', edipro=edipro))
        except Exception as e:
            print(e)
            flash("Ha ocurrido un error" , "danger")
            return redirect(url_for('producto.edit_pro', edipro=edipro))

    return render_template('admin/edit_pro.html', producto=producto_existente,marca=marca)

# Eliminar Producto
@producto.route('/delete_pr/<string:eliadpro>')
def delete_pr(eliadpro):
    producto = db["producto"]
    documento = producto.find_one({"id_producto": eliadpro})
    if documento:
        nombre = documento["nombre"]
        producto.delete_one({"id_producto": eliadpro})
        flash("Producto " + nombre + " eliminado correctamente" , "success")
    else:
        flash("Producto no encontrado" , "danger")
    return redirect(url_for('producto.v_product'))

# Visualizar producto
@producto.route("/admin/producto")
def v_product():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('producto.index'))
    producto = db["producto"].find()
    return render_template('admin/producto.html', producto=producto)


# Este es para agregar el resumen de los productos 
@producto.route("/admin/resumen")
def resumen():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('producto.index'))
    
    # Contar registros en cada coleccion
    total_clientes = db['cliente'].count_documents({})
    total_productos = db['producto'].count_documents({})
    
    # Obtener la fecha actual en formato YYYY-MM-DD
    from datetime import datetime
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    
    # Filtrar ventas por la fecha actual
    ventas_del_dia = list(db['venta'].find({"fecha": fecha_actual}))
    
    # Calcular el total de ventas del día
    total_ventas_diarias = 0
    
    for venta in ventas_del_dia:
        # Verificar si existe el array "productos" y tiene al menos un elemento con "total"
        if "productos" in venta and venta["productos"] and len(venta["productos"]) > 0:
            if "total" in venta["productos"][0] and venta["productos"][0]["total"]:
                try:
                    total_ventas_diarias += float(venta["productos"][0]["total"])
                except (ValueError, TypeError):
                    # Registrar el error para diagnóstico
                    print(f"Error al convertir total en venta {venta.get('id_venta', 'unknown')}")
    
    # Para diagnóstico: imprimir el total y las ventas encontradas
    print(f"Fecha actual: {fecha_actual}")
    print(f"Ventas encontradas hoy: {len(ventas_del_dia)}")
    print(f"Total calculado: {total_ventas_diarias}")
    
    # Reiniciar cursores para la plantilla
    producto = db["producto"].find()
    venta = db["venta"].find()
    venta2 = db["venta"].find()
    
    # Contar el número total de ventas (para referencia)
    total_ventas = db['venta'].count_documents({})
    
    # También vamos a agregar un conteo de ventas del día
    conteo_ventas_dia = len(ventas_del_dia)
    
    return render_template('admin/resumen.html', 
                        total_clientes=total_clientes,
                        total_productos=total_productos,
                        total_ventas=total_ventas,
                        total_ventas_diarias=total_ventas_diarias,
                        conteo_ventas_dia=conteo_ventas_dia,
                        producto=producto,
                        venta=venta,
                        venta2=venta2,
                        fecha_actual=fecha_actual)