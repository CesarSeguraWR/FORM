from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from flask_session import Session

app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'rooty'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'formulario'

mysql = MySQL(app)

# Configuración de la sesión
app.secret_key = 'mysecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Ruta de inicio
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para manejar el formulario de contacto
@app.route('/submit', methods=['POST'])
def submit():
    nombre = request.form['name']
    correo = request.form['email']

    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contactos (nombre, correo) VALUES (%s, %s)", (nombre, correo))
        mysql.connection.commit()
        cur.close()
        flash('¡Formulario enviado con éxito!', 'success')
    except Exception as e:
        flash(f"Error al guardar en la base de datos: {e}", 'error')
    
    return redirect(url_for('index'))

# Ruta "Nosotros"
@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

# Ruta de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form ['nombre']
        email = request.form ['email']
        password = request.form ['password']
        rol = '1'
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT email FROM signup WHERE email = %s', (email,))
        if cursor.fetchone():
            flash('⚠️ Este email ya está registrado')
            return redirect(url_for('signup'))
        cursor.execute('INSERT INTO signup (name, email, password) VALUES (%s, %s, %s)', (name, email, password))

        mysql.connection.commit()
        flash('✅ Cuenta creada satisfactoriamente')
    
    return render_template('login.html')

# Ruta protegida, accesible solo después de iniciar sesión
@app.route('/protegido')
def protegido():
    if 'user' in session:
        return f"Bienvenido, {session['user']}! Esta es una página protegida."
    else:
        return redirect(url_for('login'))

# Ruta para mostrar los usuarios (accesible solo para administradores)
@app.route('/usuarios')
def usuarios():
    if 'user' not in session or session.get('rol') != '1':  # '1' es el valor para el rol de Administrador
        flash('Acceso denegado: Necesitas ser Administrador para acceder a esta página.', 'error')
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT nombre, password FROM usuarios")
    data = cur.fetchall()
    cur.close()
    return render_template('usuarios.html', usuarios=data)

# Ruta para el registro de nuevos usuarios
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']
        rol = '1'
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO usuarios (nombre, password, rol) VALUES (%s, %s, %s)", (nombre, password, rol))
            mysql.connection.commit()
            cur.close()
            flash('¡Registro exitoso! Puedes iniciar sesión ahora.', 'success')
        except Exception as e:
            flash(f"Error al registrar el usuario: {e}", 'error')
        
        return redirect(url_for('login'))
    
    return render_template('registro.html')

# Ruta para la página de contacto
@app.route('/contactenos')
def contactenos():
    return render_template('contactenos.html')

# Ruta para el registro de administradores
@app.route('/registro_a', methods=['GET', 'POST'])
def registro_a():
    if request.method == 'POST':
        name = request.form ['nombre']
        password = request.form ['password']
        rol = request.form ['rol']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO signup (name, email, password, rol) VALUES (%s, %s, %s, %s)', (name, emai, password, rol))
        mysql.connection.commit()
        flash('✅ Cuenta creada satisfactoriamente')
        return redirect(url_for('login'))
    
    return render_template('registro_a.html')

# Ejecuta la aplicación
if __name__ == '__main__':
    app.run(debug=True)
