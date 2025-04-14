from flask import Blueprint, make_response,send_file, render_template, request, flash, session, redirect, url_for
from controllers.database import Conexion as dbase
from modules.venta import Venta
from pymongo import MongoClient
from flask import jsonify
from bson import ObjectId
from reportlab.pdfgen import canvas # *pip install reportlab este es para imprimir reportes
from reportlab.lib.pagesizes import letter #* pip install reportlab 
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle, Spacer ,Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet ,ParagraphStyle
import io
from flask import Flask
db = dbase()
from mail_config import mail
from flask_mail import Message
# Importar mail después de definir el Blueprint



venta = Blueprint('venta', __name__)

mail = None

# Función para inicializar mail
def init_mail(mail_instance):
    global mail
    mail = mail_instance

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

@venta.route("/admin/in_venta", methods=['GET', 'POST'])
def adventa():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('cliente.index'))
    
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
        return redirect(url_for('venta.adventa'))

    else:
        return render_template("admin/in_venta.html", cliente=cliente, producto=producto)




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

# Visualizar venta usuarios
@venta.route("/user/venta")
def u_cli():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('venta.index'))
    venta = db['venta'].find({"usuario": session['username']})
    return render_template("user/venta.html", venta=venta)

    

# Nueva ruta para generar el PDF
@venta.route("/admin/venta/<id>/pdf")
def generar_pdf(id):
    if 'username' not in session:
        flash("Inicia sesión con tu usuario y contraseña")
        return redirect(url_for('venta.index'))
    
    cliente = db['venta'].find_one({"_id": ObjectId(id)})
    
    if not cliente:
        flash("Cliente no encontrado")
        return redirect(url_for('venta.index'))
    
    # Crear el PDF en memoria
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Título
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2.0, height - 50, "MODAMENSPLUS")
    
    # Detalles del cliente
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"FACTURA: {cliente['id_venta']}")
    c.drawString(50, height - 120, f"Nombre: {cliente['n_cliente']}")
    c.drawString(50, height - 140, f"Apellido: {cliente['n_apellido']}")
    c.drawString(50, height - 160, f"Direccion: {cliente['direccion']}")
    c.drawString(50, height - 180, f"Cedula: {cliente['cedula']}")
    c.drawString(50, height - 200, f"Fecha: {cliente['fecha']}")
    
    # Tabla de productos
    c.drawString(50, height - 240, "Nombre de los productos")
    c.drawString(200, height - 240, "Color")
    c.drawString(300, height - 240, "Cantidad")
    c.drawString(400, height - 240, "Precio $")
    c.drawString(500, height - 240, "Total")
    
    y = height - 260
    for producto in cliente['productos']:
        c.drawString(50, y, producto['n_producto'])
        c.drawString(200, y, producto['color'])
        c.drawString(300, y, str(producto['cantidad']))
        c.drawString(400, y, str(producto['precio']))
        c.drawString(500, y, str(producto['resultado']))
        y -= 20
    
    # Total
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y - 40, f"Total: {cliente['productos'][0]['total']}")
    
    c.showPage()
    c.save()
    
    buffer.seek(0)
    
    return send_file(buffer, as_attachment=True, download_name=f'factura_{cliente["id_venta"]}.pdf', mimetype='application/pdf')



# Función para obtener el correo del cliente
def obtener_correo_cliente(cedula):
    cliente = db['cliente'].find_one({"cedula": cedula})
    if cliente:
        return cliente.get('correo')
    return None

# Función para generar el PDF
def generar_pdf_cliente(cliente):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Título
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2.0, height - 50, "MODAMENSPLUS")
    
    # Detalles del cliente
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"FACTURA: {cliente['id_venta']}")
    c.drawString(50, height - 120, f"Nombre: {cliente['n_cliente']}")
    c.drawString(50, height - 140, f"Apellido: {cliente['n_apellido']}")
    c.drawString(50, height - 160, f"Direccion: {cliente['direccion']}")
    c.drawString(50, height - 180, f"Cedula: {cliente['cedula']}")
    c.drawString(50, height - 200, f"Fecha: {cliente['fecha']}")
    
    # Tabla de productos
    c.drawString(50, height - 240, "Nombre de los productos")
    c.drawString(200, height - 240, "Color")
    c.drawString(300, height - 240, "Cantidad")
    c.drawString(400, height - 240, "Precio $")
    c.drawString(500, height - 240, "Total")
    
    y = height - 260
    for producto in cliente['productos']:
        c.drawString(50, y, producto['n_producto'])
        c.drawString(200, y, producto['color'])
        c.drawString(300, y, str(producto['cantidad']))
        c.drawString(400, y, str(producto['precio']))
        c.drawString(500, y, str(producto['resultado']))
        y -= 20
    
    # Total
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y - 40, f"Total: {cliente['productos'][0]['total']}")
    
    c.showPage()
    c.save()
    
    buffer.seek(0)
    return buffer

# Función para enviar el correo con el PDF adjunto
def enviar_correo_cliente(correo, pdf_buffer, nombre_cliente):
    try:
        msg = Message(
            subject="Gracias por tu compra",
            sender="tu_correo@example.com",  # Remitente
            recipients=[correo],  # Destinatario
            body=f"Hola {nombre_cliente},\n\nGracias por tu compra. Adjuntamos tu factura en PDF.\n\nSaludos,\nMODAMENSPLUS"
        )
        
        # Adjuntar el PDF
        msg.attach(
            filename=f"factura_{nombre_cliente}.pdf",
            content_type="application/pdf",
            data=pdf_buffer.getvalue()
        )
        
        # Enviar el correo
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error al enviar el correo: {str(e)}")
        return False

# Ruta para enviar el PDF por correo
@venta.route("/admin/venta/<id>/enviar_correo")
def enviar_factura_correo(id):
    if 'username' not in session:
        flash("Inicia sesión con tu usuario y contraseña")
        return redirect(url_for('venta.index'))
    
    # Obtener los datos del cliente desde la colección venta
    cliente = db['venta'].find_one({"_id": ObjectId(id)})
    if not cliente:
        flash("Cliente no encontrado")
        return redirect(url_for('venta.index'))
    
    # Obtener el correo del cliente desde la colección cliente
    correo_cliente = obtener_correo_cliente(cliente['cedula'])
    if not correo_cliente:
        flash("No se encontró el correo del cliente")
        return redirect(url_for('venta.v_cliente', id=id))
    
    # Generar el PDF
    pdf_buffer = generar_pdf_cliente(cliente)
    
    # Enviar el correo con el PDF adjunto
    if enviar_correo_cliente(correo_cliente, pdf_buffer, cliente['n_cliente']):
        flash("Correo enviado correctamente","success")
    else:                                
        flash("Error al enviar el correo","alert")
    
    return redirect(url_for('venta.v_cliente', id=id))
