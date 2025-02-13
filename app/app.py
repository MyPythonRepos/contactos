from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
import secrets

app = Flask(__name__)
#app.secret_key = 'TF"Rh~kc55?XWA{,B@'  # Necesario para usar flash messages
app.secret_key = secrets.token_urlsafe(16)

DATA_FILE = 'data.json'

def cargar_datos():
    if not os.path.exists(DATA_FILE):
        datos_iniciales = {"groups": {}}
        with open(DATA_FILE, 'w') as f:
            json.dump(datos_iniciales, f, indent=4)
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def guardar_datos(datos):
    with open(DATA_FILE, 'w') as f:
        json.dump(datos, f, indent=4)

@app.route('/')
def index():
    datos = cargar_datos()
    return render_template('index.html', groups=datos['groups'])

@app.route('/add_group', methods=['GET', 'POST'])
def add_group():
    if request.method == 'POST':
        group_name = request.form['group_name'].strip()
        if not group_name:
            flash('El nombre del grupo no puede estar vacío.', 'error')
            return redirect(url_for('add_group'))
        
        datos = cargar_datos()
        if group_name in datos['groups']:
            flash('El grupo ya existe.', 'error')
            return redirect(url_for('add_group'))
        
        datos['groups'][group_name] = []
        guardar_datos(datos)
        flash(f'Grupo "{group_name}" añadido exitosamente.', 'success')
        return redirect(url_for('index'))
    return render_template('add_group.html')

@app.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
    datos = cargar_datos()
    grupos = list(datos['groups'].keys())
    if request.method == 'POST':
        group = request.form['group']
        contact_name = request.form['contact_name'].strip()
        contact_email = request.form['contact_email'].strip()
        
        if not contact_name or not contact_email:
            flash('El nombre y el correo del contacto no pueden estar vacíos.', 'error')
            return redirect(url_for('add_contact'))
        
        nuevo_contacto = {
            "name": contact_name,
            "email": contact_email,
            "obsolete": False
        }
        datos['groups'][group].append(nuevo_contacto)
        guardar_datos(datos)
        flash(f'Contacto "{contact_name}" añadido al grupo "{group}".', 'success')
        return redirect(url_for('index'))
    return render_template('add_contact.html', groups=grupos)

@app.route('/mark_obsolete/<group>/<int:contact_index>', methods=['POST'])
def mark_obsolete(group, contact_index):
    datos = cargar_datos()
    try:
        datos['groups'][group][contact_index]['obsolete'] = True
        guardar_datos(datos)
        flash(f'Contacto marcado como obsoleto en el grupo "{group}".', 'success')
    except (IndexError, KeyError):
        flash('Contacto o grupo no encontrado.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
