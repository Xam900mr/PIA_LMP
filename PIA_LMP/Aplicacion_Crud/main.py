from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import os
from wtforms import Form, BooleanField, StringField, PasswordField, validators, DateField, IntegerField

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
    remember = BooleanField('Recordarme')

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

    user_id = session.get('user_id')
    user_type = session.get('user_type')

    return render_template('index.html', Libros=Libros, session=session, user_id=user_id, user_type=user_type)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        cursor = db.cursor()
        query = "SELECT Nombre, Contrasena, tipo FROM usuarios WHERE Correo = %s"
        cursor.execute(query, (form.Correo.data,))
        user = cursor.fetchone()
        cursor.close()
        
        if user and check_password_hash(user[1], form.Contrasena.data):
            session['user_id'] = user[0]
            session['user_type'] = user[2]  
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
def add_book():     
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
        flash('Libro agregado exitosamiente', 'success') 
        return redirect(url_for('index')) 
    return render_template('Agregar.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)  
    flash("Has cerrado sesión exitosamente")
    return redirect(url_for('index'))

if __name__=='__main__':
    app.run(debug=True)