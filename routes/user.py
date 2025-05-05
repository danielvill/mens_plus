from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from controllers.database import Conexion as dbase
from modules.user import User
from pymongo import MongoClient
from modules.cliente import Cliente
db = dbase()
user = Blueprint('user', __name__)


@user.route('/admin/in_user',methods=['GET','POST'])
def aduser():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('user.index'))  # Redirige al usuario al inicio si no está en la sesión
    
    if request.method == 'POST':
        usere = db["user"]
        use = request.form['user']
        cedula = request.form['cedula']
        contraseña = request.form['contraseña']
        
    
        exist_cedula = usere.find_one ({"cedula":cedula})
        exist_use = usere.find_one ({"user":use})
        exist_contraseña = usere.find_one ({"contraseña":contraseña})

        if exist_cedula:
            flash("La cedula ya existe" ,"danger")
            return redirect(url_for('user.aduser'))
        elif exist_use:
            flash("El usuario ya existe"  ,"danger")
            return redirect(url_for('user.aduser'))
        elif exist_contraseña:
            flash("La contraseña ya existe","danger")
            return redirect(url_for('user.aduser'))
        else:
            useri = User(use,cedula,contraseña)
            usere.insert_one(useri.UserDBCollection())
            flash("Enviado a la base de datos","success")
            return redirect(url_for('user.aduser'))
    else:
        return render_template('admin/in_user.html')
    
# Editar usuario
@user.route('/edit_us/<string:edaduser>', methods=['GET', 'POST'])#
def edit_user(edaduser):

    use = db["user"]
    user = request.form["user"]
    cedula = request.form["cedula"]
    contraseña = request.form["contraseña"]

    if user and cedula and contraseña:
        use.update_one ({'cedula' : edaduser},{"$set" :{"user": user , "cedula":cedula, "contraseña":contraseña}})
        flash("Usuario " + user + " con cedula " + cedula + " Actualizado correctamente")
        return redirect(url_for('user.v_user'))
    else:
        return render_template("admin/user.html")

# Eliminar usuario
@user.route('/delete_user/<string:eliaduser>')
def delete_user(eliaduser):
    user = db["user"]
    user.delete_one({"cedula":eliaduser})
    flash("Usuario eliminado correctamente " )
    return redirect(url_for('user.v_user'))

# Visualizar usuario
@user.route("/admin/user")
def v_user():
    if "username" not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('user.index'))
    user = db["user"].find()
    return render_template("admin/user.html", user=user)

# Crear para usuario lo de ingreso de ventas 


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

@user.route("/user/in_venta", methods=['GET', 'POST'])
def usventa():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    
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
        hora = request.form["hora"]
        usi = request.form["usuario"]
        # Recoger los productos
        id_productos = request.form.getlist("id_producto")
        n_productos = request.form.getlist("n_productos")
        talla = request.form.getlist("talla")
        colores = request.form.getlist("color")
        cantidades = request.form.getlist("cantidad")
        precios = request.form.getlist("precio")
        resultados = request.form.getlist("resultado")
        totales = request.form.getlist("total")
         
       

        productos = []
        for i in range(len(n_productos)):
            producto = {
                "id_producto": id_productos[i] if i < len(id_productos) else '',
                "n_producto": n_productos[i] if i < len(n_productos) else '',
                "talla": talla[i] if i < len(talla) else '',
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
            "hora": hora,
            "productos": productos,
            "usuario":usi
        }
        
        # Insertar el documento en la colección de ventas
        venta.insert_one(venta_documento)
        print("Documento de Venta:", venta_documento)

        # Actualizar las cantidades de los productos
        for i in range(len(id_productos)):
            id_producto = id_productos[i]
            cantidad_vendida = cantidades[i]
            
            if cantidad_vendida:
                cantidad_vendida = int(cantidad_vendida)
            
                # Obtener el producto de la base de datos
                producto_db = db["producto"].find_one({"id_producto": id_producto})
                if producto_db:
                    nueva_cantidad = int(producto_db["cantidad"]) - cantidad_vendida
                    # Actualizar la cantidad del producto en la base de datos
                    db["producto"].update_one({"id_producto": id_producto}, {"$set": {"cantidad": str(nueva_cantidad)}})
                    print(f"Producto {id_producto} actualizado. Nueva cantidad: {nueva_cantidad}")
            else:
                print(f"Cantidad no válida para el producto {id_producto}")

        flash("Venta registrada con éxito y cantidades actualizadas","success")
        return redirect(url_for('user.usventa'))

    else:
        return render_template("user/in_venta.html", cliente=cliente, producto=producto,usuario=session['username'])


# Este apartado es para visualizar al cliente
@user.route("/user/cliente")
def u_cli():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('user.index'))
    cliente = db['cliente'].find()
    return render_template("user/cliente.html", cliente=cliente)

# Este es para visualizar los productos en user
@user.route("/user/producto")
def u_product():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('user.index'))
    producto = db["producto"].find()
    return render_template('user/producto.html', producto=producto)


# Ingreso con un Id unico
@user.route('/user/in_cliente',methods=['GET','POST'])
def usercli():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('user.index'))  # Redirige al usuario al inicio si no está en la sesión
    

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
            return redirect(url_for('user.u_cli'))
        elif exist_telefono:
            flash("El celular ya existe" ,"danger")
            return redirect(url_for('user.u_cli'))
        elif exist_correo:
            flash("El correo ya existe" , "danger")
            return redirect(url_for('user.u_cli'))
        else:
            client = Cliente( nombre, apellido, cedula, direccion, telefono, correo)
            cliente.insert_one(client.ClienteDBCollection())
            flash("Enviado a la base de datos" , "success")
            return redirect(url_for('user.u_cli'))
    else:
        return render_template('/user/in_cliente.html',message=request.args.get('message'))