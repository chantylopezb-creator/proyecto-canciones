import os
import json
from flask import Flask, render_template, request, redirect

directorio_base = os.path.dirname(os.path.abspath(__file__))
ruta_templates = os.path.join(directorio_base, 'templates')
# Archivo JSON donde se guardan las canciones
ruta_json = os.path.join(directorio_base, 'canciones.json')

app = Flask(__name__, template_folder=ruta_templates)

# funciones para leer y guardar datos en el archivo JSON
def leer_datos():
    """Lee el archivo JSON. Si no existe, lo crea con una lista vacía."""
    if not os.path.exists(ruta_json):
        guardar_datos([])
        return []
    with open(ruta_json, 'r', encoding='utf-8') as archivo:
        return json.load(archivo)

def guardar_datos(datos):
    """Guarda la lista de canciones en el archivo JSON."""
    with open(ruta_json, 'w', encoding='utf-8') as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


#rutas

# PÁGINA 1: Inicio (Leer), tabla con las canciones
@app.route('/')
def inicio():
    canciones = leer_datos()
    return render_template('index.html', canciones=canciones)

# PÁGINA 2: Registro, formulario para agregar
@app.route('/registro')
def registro():
    return render_template('registro.html')

# Crear una canción
@app.route('/agregar', methods=['POST'])
def agregar_cancion():
    nombre = request.form.get('nombre')
    artista = request.form.get('artista')
    album = request.form.get('album')
    genero = request.form.get('genero')

    if nombre and artista and album and genero:
        canciones = leer_datos()
        canciones.append({"nombre": nombre, "artista": artista, "album": album, "genero": genero})
        guardar_datos(canciones)

    return redirect('/')

# PÁGINA 3: Edición, formulario con los datos actuales
@app.route('/editar/<int:id_cancion>')
def editar_cancion(id_cancion):
    canciones = leer_datos()
    if 0 <= id_cancion < len(canciones):
        return render_template('editar.html', cancion=canciones[id_cancion], id=id_cancion)
    return redirect('/')

# Actualizar una canción
@app.route('/actualizar/<int:id_cancion>', methods=['POST'])
def actualizar_cancion(id_cancion):
    canciones = leer_datos()
    if 0 <= id_cancion < len(canciones):
        nombre = request.form.get('nombre')
        artista = request.form.get('artista')
        album = request.form.get('album')
        genero = request.form.get('genero')

        if nombre and artista and album and genero:
            canciones[id_cancion]['nombre'] = nombre
            canciones[id_cancion]['artista'] = artista
            canciones[id_cancion]['album'] = album
            canciones[id_cancion]['genero'] = genero
            guardar_datos(canciones)

    return redirect('/')

# Eliminar una canción
@app.route('/eliminar/<int:id_cancion>')
def eliminar_cancion(id_cancion):
    canciones = leer_datos()
    if 0 <= id_cancion < len(canciones):
        canciones.pop(id_cancion)
        guardar_datos(canciones)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
