from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from controllers.database import Conexion as dbase
from modules.user import User
from pymongo import MongoClient

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
            return redirect(url_for('user.aduser',message ="La cedula ya existe"))
        elif exist_use:
            return redirect(url_for('user.aduser',message ="El usuario ya existe"))
        elif exist_contraseña:
            return redirect(url_for('user.aduser',message ="La contraseña ya existe"))
        else:
            useri = User(use,cedula,contraseña)
            usere.insert_one(useri.UserDBCollection())
            return redirect(url_for('user.aduser', message="Enviado a la base de datos"))
    else:
        return render_template('admin/in_user.html',message=request.args.get('message'))
    
# Editar usuario
@user.route('/edit_us/<string:edaduser>', methods=['GET', 'POST'])#
def edit_user(edaduser):

    use = db["user"]
    user = request.form["user"]
    cedula = request.form["cedula"]
    contraseña = request.form["contraseña"]

    if user and cedula and contraseña:
        user.updateone({"user": user , "cedula":cedula, "contraseña":contraseña})
        flash("Usuario " + user + "con cedula " + cedula + "Actualizado correctamente")
        return redirect(url_for('user.aduser'))
    else:
        return render_template("admin/user.html")

# Eliminar usuario
@user.route('/delete_us/<string:eliaduser>')
def delete_user(eliaduser):
    user = db["user"]
    user.delete_one({"user":eliaduser})
    flash("Usuario " + eliaduser + " eliminado correctamente")
    return redirect(url_for('user.aduser'))

# Visualizar usuario
@user.route("/admin/user")
def v_user():
    if "username" not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('user.index'))
    user = db["user"].find()
    return render_template("admin/user.html", user=user)

    

