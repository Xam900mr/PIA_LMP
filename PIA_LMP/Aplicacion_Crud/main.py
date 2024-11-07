from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import os
from wtforms import Form, BooleanField, StringField, PasswordField, validators, DateField, IntegerField
from datetime import datetime, timedelta

db = mysql.connector.connect(
    user="root",
    password="ramm160799",
    host="localhost",
    database="adtareas"
)

class FormUsuarios(Form):
    Usuario = StringField('Username', [validators.Length(min=8, max=60)])
    Correo = StringField('Email Address', [validators.Length(min=8, max=60)])
    Contrasena = PasswordField('New Password', [validators.DataRequired(), validators.EqualTo('confirm', message='La contrasena debe de ser igual')])
    confirm = PasswordField('Repeat Password')

class LoginForm(Form):
    Correo = StringField('Correo', [validators.DataRequired(), validators.Email()])
    Contrasena = PasswordField('Contraseña', [validators.DataRequired()])

class BookForm(Form):     
    Nombre = StringField('Nombre', [validators.DataRequired()])     
    Autor = StringField('Autor', [validators.DataRequired()])     
    isbn = StringField('ISBN', [validators.DataRequired()])     
    edicion = IntegerField('Edición', [validators.DataRequired()])     
    fecha_pub = DateField('Fecha de Publicación', [validators.DataRequired()], format='%Y-%m-%d')     
    categoria = StringField('Categoría', [validators.DataRequired()]) 
    cantidad = IntegerField('Cantidad', [validators.DataRequired()]) 
    disponibilidad = IntegerField('Disponibilidad', [validators.DataRequired()]) 
    editorial = StringField('Editorial', [validators.DataRequired()]) 



app = Flask (__name__, template_folder='./Templates')
app.secret_key = os.urandom(24)

@app.route('/', methods=['GET'])
def index():
    
    cursor=db.cursor()
    cursor.execute("select * from Libros")
    Libros = cursor.fetchall()

    user_type = session.get('user_type')

    return render_template('index.html', Libros=Libros, session=session, user_type=user_type)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        cursor = db.cursor()
        query = "SELECT ID, Nombre, Contrasena, tipo FROM usuarios WHERE Correo = %s"
        cursor.execute(query, (form.Correo.data,))
        user = cursor.fetchone()
        cursor.close()
        
        if user and check_password_hash(user[2], form.Contrasena.data):
            session['user_id'] = user[0]
            session['user_name']= user[1]
            session['user_type'] = user[3]  
            flash('Inicio de sesión exitoso', 'success')  
            return redirect(url_for('index'))
        else:
            flash('Correo o contraseña incorrectos', 'danger') 
            return redirect(url_for('login'))
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():     
    form = FormUsuarios(request.form)   
    if request.method == 'POST' and form.validate():         
        hashed_password = generate_password_hash(form.Contrasena.data)        
        query = """         
        INSERT INTO usuarios (Nombre, Correo, Contrasena, tipo)         
        VALUES (%s, %s, %s, "u")         
        """        
        values = (form.Usuario.data, form.Correo.data, hashed_password)       
        cursor=db.cursor()         
        cursor.execute(query, values)         
        db.commit()         
        flash('Gracias por registrarte') 
        return redirect(url_for('login')) 
    return render_template('register.html', form=form)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():     
    form = BookForm(request.form)    
    if request.method == 'POST' and form.validate():    
        query = """         
        INSERT INTO libros (Nombre, Autor, ISBN, Edicion, Fecha_Pub, Categoria, Cantidad, Disponibilidad, editorial)         
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)         
        """             
        values = (form.Nombre.data, form.Autor.data, form.isbn.data, form.edicion.data, form.fecha_pub.data, form.categoria.data, form.cantidad.data, form.disponibilidad.data, form.editorial.data)
        cursor=db.cursor()
        cursor.execute(query, values)
        db.commit()
        cursor.close

        flash('Libro agregado exitosamiente', 'success') 
        return redirect(url_for('index')) 
    return render_template('Agregar.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)  
    flash("Has cerrado sesión exitosamente")
    return redirect(url_for('index'))


@app.route('/eliminar_libro/<int:libro_id>', methods=['POST'])
def eliminar_libro(libro_id):
    cursor = db.cursor()
    
    query_rentado = "SELECT Devuelto FROM rentas WHERE ID_Libro = %s AND Devuelto = 0"
    cursor.execute(query_rentado, (libro_id,))
    rentas_pendientes = cursor.fetchone() 

    if rentas_pendientes:
        flash('No se puede eliminar el libro porque aún hay rentas pendientes', 'error')
        cursor.close()
        return redirect(url_for('index'))
    else:
        rentas_query ="DELETE from rentas WHERE ID_Libro = %s"
    
        query = "DELETE FROM libros WHERE ID = %s"

        
        cursor.execute(rentas_query, (libro_id,))
        cursor.execute(query, (libro_id,))
        db.commit()
        cursor.close()
        
        flash('Libro eliminado exitosamente', 'success')

    return redirect(url_for('index'))



@app.route('/editar_libro/<int:libro_id>', methods=['GET', 'POST'])
def editar_libro(libro_id):
    form = BookForm(request.form)
    
    if request.method == 'POST' and form.validate():
        query = """
            UPDATE libros
            SET Nombre = %s, Autor = %s, ISBN = %s, Edicion = %s, Fecha_Pub = %s,
                Categoria = %s, Cantidad = %s, Disponibilidad = %s, editorial = %s
            WHERE ID = %s
        """
        values = (
            form.Nombre.data, form.Autor.data, form.isbn.data, form.edicion.data,
            form.fecha_pub.data, form.categoria.data, form.cantidad.data,
            form.disponibilidad.data, form.editorial.data, libro_id
        )
        cursor = db.cursor()
        cursor.execute(query, values)
        db.commit()
        cursor.close()
        
        flash('Libro actualizado exitosamente', 'success')
        return redirect(url_for('index'))
    
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM libros WHERE ID = %s", (libro_id,))
    libro = cursor.fetchone()
    cursor.close()
    
    if libro:
        form.Nombre.data = libro['Nombre']
        form.Autor.data = libro['Autor']
        form.isbn.data = libro['ISBN']
        form.edicion.data = libro['Edicion']
        form.fecha_pub.data = libro['Fecha_Pub']
        form.categoria.data = libro['Categoria']
        form.cantidad.data = libro['Cantidad']
        form.disponibilidad.data = libro['Disponibilidad']
        form.editorial.data = libro['editorial']
    
    return render_template('editar_libro.html', form=form, libro_id=libro_id)

@app.route('/procesar_renta/<int:libro_id>', methods=['POST'])
def procesar_renta(libro_id):
    fecha_renta = datetime.today().date()
    fecha_dev = fecha_renta + timedelta(days=30)
   
    cursor = db.cursor()
    
    insert_query = """
    INSERT INTO rentas (ID_Libro, ID_US, Fecha_Renta, Fecha_Dev, Devuelto)
    VALUES (%s, %s, %s, %s, 0)
    """
    cursor.execute(insert_query, (libro_id, session['user_id'], fecha_renta, fecha_dev,))
    
    update_query = """
    UPDATE libros
    SET Disponibilidad = Disponibilidad - 1
    WHERE ID = %s AND Disponibilidad > 0
    """
    cursor.execute(update_query, (libro_id,))
    
    db.commit()
    cursor.close()

    flash('Renta de libro exitosa. Fecha de devolución: %s' % fecha_dev, 'success')

    return redirect(url_for('index'))



@app.route('/Mis_Rentas', methods=['GET'])
def Mis_Rentas():
    query = """
    SELECT l.Nombre, r.ID_US, r.Fecha_Renta, r.Fecha_Dev, r.ID, l.ID
    FROM rentas r
    JOIN libros l ON r.ID_Libro = l.ID
    WHERE r.Devuelto = 0 AND r.ID_US = %s
    """
    cursor = db.cursor()
    cursor.execute(query, (session['user_id'],))

    rentas = cursor.fetchall()
    cursor.close()

    return render_template('rentas.html', rentas=rentas)

@app.route('/devolver_libro/<int:renta_id>/<int:libro_id>', methods=['POST'])
def devolver_libro(renta_id, libro_id):
    cursor = db.cursor()

    update_renta_query = """
    UPDATE rentas
    SET Devuelto = 1
    WHERE ID = %s
    """
    cursor.execute(update_renta_query, (renta_id,))

    update_libro_query = """
    UPDATE libros
    SET Disponibilidad = Disponibilidad + 1
    WHERE ID = %s
    """
    cursor.execute(update_libro_query, (libro_id,))

    db.commit()
    cursor.close()

    flash('Libro devuelto exitosamente', 'success')
    return redirect(url_for('Mis_Rentas'))



if __name__=='__main__':
    app.run(debug=True)