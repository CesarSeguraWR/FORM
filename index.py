# app.py
from flask import Flask, request, render_template

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'syntax'
app.config['MYSQL_PASSWORD'] = 'syntax'
app.config['MYSQL_DB'] = 'bei'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        # Aquí puedes agregar la lógica para procesar los datos del formulario
        # Por ejemplo, puedes enviar un correo electrónico con los datos del formulario
        print(f"Nombre: {name}, Correo electrónico: {email}")
        return "Formulario enviado con éxito!"
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configuración de la conexión a la base de datos
db_config = {
    'host': 'localhost',
    'user': 'tu_usuario',  # Cambia esto por tu usuario de MySQL
    'password': 'tu_contraseña',  # Cambia esto por tu contraseña de MySQL
    'database': 'formulario_db'
}

def connect_db():
    conn = mysql.connector.connect(**db_config)
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    nombre = request.form['name']
    correo = request.form['email']
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contactos (nombre, correo) VALUES (%s, %s)", (nombre, correo))
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
