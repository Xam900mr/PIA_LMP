from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import os
from wtforms import Form, BooleanField, StringField, PasswordField, validators, ValidationError

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


cursor=db.cursor()

app = Flask (__name__, template_folder='./Templates')
app.secret_key = os.urandom(24)

@app.route('/', methods=['GET'])
def index():
    cursor.execute("select * from Libros")
    Libros = cursor.fetchall()

    return render_template('index.html', Libros=Libros)

@app.route('/login', methods=['GET', 'POST'])
def login():     
    form = LoginForm(request.form)   
    if request.method == 'POST' and form.validate():        
        query = "SELECT ID, Contrasena FROM usuarios WHERE Correo = %s"        
        cursor.execute(query, (form.Correo.data,))       
        user = cursor.fetchone()               
        if user and check_password_hash(user[1], form.Contrasena.data):                        
            session['user_id'] = user[0]            
            flash('Inicio de sesión exitoso') 
            return redirect(url_for('dashboard')) 
        else:
            flash('Correo o contraseña incorrectos') 
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():     
    form = FormUsuarios(request.form)   
    if request.method == 'POST' and form.validate():         
        hashed_password = generate_password_hash(form.Contrasena.data)        
        query = """         
        INSERT INTO usuarios (Nombre, Correo, Contrasena)         
        VALUES (%s, %s, %s)         
        """        
        values = (form.Usuario.data, form.Correo.data, hashed_password)                
        cursor.execute(query, values)         
        db.commit()         
        flash('Gracias por registrarte') 
        return redirect(url_for('login')) 
    return render_template('register.html', form=form)

if __name__=='__main__':
    app.run(debug=True)