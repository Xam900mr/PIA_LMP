from flask import Flask, render_template, request
import mysql.connector

db = mysql.connector.connect(
    user="root",
    password="ramm160799",
    host="localhost",
    database="adtareas"
)

app = Flask (__name__, template_folder='./Templates')

@app.route('/', methods=['GET'])
def index():
    cursor=db.cursor()
    cursor.execute("select * from Libros")
    Libros = cursor.fetchall()

    return render_template('index.html', Libros=Libros)



if __name__=='__main__':
    app.run(debug=True)