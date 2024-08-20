from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'bamby'

db_config = {
    'host': 'localhost',
    'user': 'rooty',
    'password': 'password',
    'database': 'formulario'
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

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE nombre=%s AND password=%s", (nombre, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            session['user'] = user['nombre']
            return redirect(url_for('protegido'))
        else:
            flash('Nombre o contraseña incorrectos')
    return render_template('login.html')

@app.route('/protegido')
def protegido():
    if 'user' in session:
        return f"Bienvenido, {session['user']}! Esta es una página protegida."
    else:
        return redirect(url_for('login'))

@app.route('/usuarios')
def usuarios():
    return render_template('usuarios.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/contactenos')
def contactenos():
    return render_template('contactenos.html')

if __name__ == '__main__':
    app.run(debug=True)
