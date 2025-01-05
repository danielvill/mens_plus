from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from controllers.database import Conexion as dbase
from modules.venta import Venta
from pymongo import MongoClient
from bson import ObjectId
db = dbase()

venta = Blueprint('venta', __name__)


# Este codigo es para lo que es el ID
def get_next_sequence(name): 
    seq = db.seqs.find_one({'_id': name})
    if seq is None:
        # Inicializa 'productoId' en 220 si no existe
        db.seqs.insert_one({'_id': 'ventaId', 'seq': 0})
        seq = db.seqs.find_one({'_id': name})

    result = db.seqs.find_one_and_update(
        {'_id': name},
        {'$inc': {'seq': 1}},
        return_document=True
    )
    return result.get('seq')


@venta.route("/admin/in_venta",methods=['GET','POST'])
def adventa():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('cliente.index'))
    # Este es el apartado para visualizar a los clientes y los productos 
    cliente = db["cliente"].find()
    producto = db["producto"].find()


    if request.method == 'POST':
        id_venta = str(get_next_sequence('ventaId')).zfill(1)
        venta = db["venta"]
        n_cliente = request.form["n_cliente"]
        n_apellido = request.form["n_apellido"]
        direccion = request.form["direccion"]
        cedula = request.form["cedula"]
        fecha = request.form["fecha"]
        
        # Recoger los productos

        n_productos = request.form.getlist("n_productos")
        colores = request.form.getlist("color")
        cantidades = request.form.getlist("cantidad")
        precios = request.form.getlist("precio")
        resultados = request.form.getlist("resultado")
        totales = request.form.getlist("total")
        
        # Debugging
        print("Productos:", n_productos)
        print("Colores:", colores)
        print("Cantidades:", cantidades)
        print("Precios:", precios)
        print("Resultados:", resultados)
        print("Totales:", totales)

        productos = []
        for i in range(len(n_productos)):
            producto = {
                "n_producto": n_productos[i] if i < len(n_productos) else '',
                "color": colores[i] if i < len(colores) else '',
                "cantidad": cantidades[i] if i < len(cantidades) else '',
                "precio": precios[i] if i < len(precios) else '',
                "resultado": resultados[i] if i < len(resultados) else '',
                "total": totales[i] if i < len(totales) else ''
            }
            productos.append(producto)

        # Crear el documento de venta
        venta_documento = {
            "id_venta": id_venta,
            "n_cliente": n_cliente,
            "n_apellido": n_apellido,
            "direccion": direccion,
            "cedula": cedula,
            "fecha": fecha,
            "productos": productos
        }
        
        # Insertar el documento en la colección de ventas
        venta.insert_one(venta_documento)
        print("Documento de Venta:", venta_documento)

        flash("Venta registrada con éxito")
        return redirect(url_for('venta.adventa'))

    else:
        return render_template("admin/in_venta.html",cliente=cliente,producto=producto)
    



# Visualizar venta
@venta.route("/admin/venta")
def v_cli():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('venta.index'))
    venta = db['venta'].find()
    return render_template("admin/venta.html", venta=venta)



# Visualizar detalles del cliente por ID y que se pueda revisar 
@venta.route("/admin/venta/<id>")
def v_cliente(id):
    if 'username' not in session:
        flash("Inicia sesión con tu usuario y contraseña")
        return redirect(url_for('venta.index'))
    cliente = db['venta'].find_one({"_id": ObjectId(id)})
    return render_template("admin/v_cliente.html", cliente=cliente)
