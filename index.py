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
    app.run(debug=True)