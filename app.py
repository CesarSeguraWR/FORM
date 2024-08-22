from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'bamby'  # Clave secreta para sesiones

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'rooty',
    'password': 'password',
    'database': 'formulario'
}

# Función para conectar a la base de datos
def connect_db():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error al conectar con la base de datos: {err}")
        return None

# Ruta de inicio
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para manejar el formulario de contacto
@app.route('/submit', methods=['POST'])
def submit():
    nombre = request.form['name']
    correo = request.form['email']

    conn = connect_db()
    if conn is None:
        flash('Error al conectar con la base de datos', 'error')
        return redirect(url_for('index'))
    
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contactos (nombre, correo) VALUES (%s, %s)", (nombre, correo))
        conn.commit()
        flash('¡Formulario enviado con éxito!', 'success')
    except mysql.connector.Error as err:
        flash(f"Error al guardar en la base de datos: {err}", 'error')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('index'))

# Ruta "Nosotros"
@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

# Ruta de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']
        
        conn = connect_db()
        if conn is None:
            flash('Error al conectar con la base de datos', 'error')
            return redirect(url_for('login'))

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE nombre=%s AND password=%s", (nombre, password))
            user = cursor.fetchone()
            if user:
                session['user'] = user['nombre']
                return redirect(url_for('protegido'))
            else:
                flash('Nombre o contraseña incorrectos', 'error')
        except mysql.connector.Error as err:
            flash(f"Error en la consulta a la base de datos: {err}", 'error')
        finally:
            cursor.close()
            conn.close()
    
    return render_template('login.html')

# Ruta protegida, accesible solo después de iniciar sesión
@app.route('/protegido')
def protegido():
    if 'user' in session:
        return f"Bienvenido, {session['user']}! Esta es una página protegida."
    else:
        return redirect(url_for('login'))

# Ruta para mostrar los usuarios (puedes personalizar esta página)
@app.route('/usuarios')
def usuarios():
    return render_template('usuarios.html')

# Ruta para el registro de nuevos usuarios
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']

        conn = connect_db()
        if conn is None:
            flash('Error al conectar con la base de datos', 'error')
            return redirect(url_for('registro'))

        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (nombre, password) VALUES (%s, %s)", (nombre, password))
            conn.commit()
            flash('¡Registro exitoso! Puedes iniciar sesión ahora.', 'success')
        except mysql.connector.Error as err:
            flash(f"Error al registrar el usuario: {err}", 'error')
        finally:
            cursor.close()
            conn.close()
        
        return redirect(url_for('login'))
    
    return render_template('registro.html')

# Ruta para la página de contacto
@app.route('/contactenos')
def contactenos():
    return render_template('contactenos.html')

# Ejecuta la aplicación
if __name__ == '__main__':
    app.run(debug=True)
