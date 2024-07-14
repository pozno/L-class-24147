
import mysql.connector


# Instalar con pip install Flask
from flask import Flask, request, jsonify
# Instalar con pip install flask-cors
from flask_cors import CORS
# Si es necesario, pip install Werkzeug
from werkzeug.utils import secure_filename
# No es necesario instalar, es parte del sistema standard de Python
import os
import time





app = Flask (__name__)
CORS(app)



class Catalogo:

     def __init__(self, host, user, password, database, port):
    
    
       self.conn = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            database= database,
            port = port
    )
       self.connector = self.conn.cursor(dictionary=True)
       self.connector.execute('''CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            edad INT NOT NULL,
            rango INT NOT NULL,
            imagen_url VARCHAR(255),
            pais VARCHAR(30)NOT NULL)''')
       self.conn.commit()
       
  
     def verificarconexion(self):
        if self.conn.is_connected():
          print("conexion establecida")
        else:
          print("no se establecio la conexion") 
      


     
     def añadir_usuarios(self, id, nombre, edad, rango, imagen_url, pais ):
      self.connector.execute(f"SELECT * FROM usuarios WHERE id = {id}")
      usuario_existente = self.connector.fetchone()
      if usuario_existente:
        print("ya existe este usuario")
        return False

      sql = f"INSERT INTO usuarios (id, nombre, edad, rango, imagen_url, pais)VALUES({id}, '{nombre}',{edad},{rango},'{imagen_url}','{pais}')"
      self.connector.execute(sql)
      self.conn.commit()
      print("nuevo usuario ha sido agendado")
      return True
      
    
     def consultar(self, id):
      self.connector.execute(f"SELECT * FROM usuarios WHERE id ={id}")
      print(self.connector.fetchone())
      return  self.connector.fetchone()
      
     def modificar_datos(self, id, nuevo_nombre, nueva_edad, nuevo_rango, nueva_imagen_url, nuevo_pais):
      sql = f"UPDATE usuarios SET  nombre = '{nuevo_nombre}',edad = '{nueva_edad}',rango ='{nuevo_rango}',imagen_url ='{nueva_imagen_url}', pais ='{nuevo_pais}'WHERE id = '{id}'"
      self.connector.execute(sql)
      self.conn.commit()
      return self.connector.rowcount > 0
     
     def lista_usuarios(self):
      self.connector.execute("SELECT * FROM  usuarios")
      usuarios = self.connector.fetchall()
      print(usuarios)
      return usuarios


      

     def eliminar_usuario(self, id):
      self.connector.execute(f"DELETE FROM usuarios WHERE id = {id}")
      self.conn.commit()
      return self.connector.rowcount > 0

     def mostrar_usuarios(self, id):
      mostrar = self.consultar(id)
      if mostrar:
        print("-" * 40)
        print(f"id:{mostrar['id']}")
        print(f"nombre:{mostrar['nombre']}")
        print(f"edad:{mostrar['edad']}")
        print(f"rango:{mostrar['rango']}")
        print(f"imagen_url:{u['imagen_url']}")
        print(f"pais:{mostrar['pais']}")
        print("-" * 40)
      else:
        print("Usuario no encontrado.")
      
      
      
      

    
     
     
      
  
     

        
    
   
   
   
   
 
mi_catalogo = Catalogo(host='127.0.0.1', user='root', password='luisillo', database='hunters', port='3306')


mi_catalogo.verificarconexion()




@app.route("/usuarios", methods=["GET"])
def lista_usuarios():
  usuarios = mi_catalogo.lista_usuarios()
  return jsonify(usuarios)


@app.route("/usuarios/<int:id>", methods=["GET"])
def consultar_usuarios():
  usuario = mi_catalogo.consultar(id)
  if usuario:
    return jsonify(usuario)
  else:
    return "Usuario no encontrado" , 404


@app.route("/usuarios", methods=["POST"])
def agregar_usuario():
  id = request.form['id']
  nombre = request.form['nombre']
  edad = request.form['edad']
  rango = request.form['rango']
  imagen_url = request.files['imagen_url']
  pais = request.form['pais']
  nombre_imagen=""

  nombre_imagen = secure_filename(imagen.filename)
  nombre_base,  extension = os.path.splitext(nombre_imagen)
  nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"

  nuevo_codigo = mi_catalogo.añadir_usuarios(nombre, edad, rango, imagen_url, pais )
  if nuevo_codigo:
     imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))

     return jsonify({"mensaje": "Usuario agregado correctamente.", "codigo": nuevo_codigo, "imagen": nueva_imagen}), 201
  else:
    return jsonify({"mensaje":"No se pudo agregar el usuario"}), 500




@app.route("/usuarios/<int:id>", methods=["PUT"])
def modificar_datos(codigo):


  nuevo_nombre = request.form.get("nombre")
  nueva_edad = request.form.get("edad")
  nuevo_rango = request.form.get("rango")
  nueva_imagen_url = request.form.get("imagen_url")
  nuevo_pais = request.form.get("pais")

  if 'imagen' in request.files:
      imagen = request.files['imagen']

      nombre_imagen = secure_filename(imagen.filename)
      nombre_base, extension = os.path.splitext(nombre_imagen)
      nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"

      imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))

      usuario = mi_catalogo.consultar(id)
      if usuario:
        imagen_vieja = usuario["imagen_url"]
        ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)

        if os.path.exists(ruta_imagen):
          os.remove(ruta_imagen)

  else:
    usuario = mi_catalogo.consulta(id)
    if usuario:
       nombre_imagen = usuario["imagen_url"]



  if mi_catalogo.modificar_datos(id, nuevo_nombre, nueva_edad, nuevo_rango, nueva_imagen_url, nuevo_pais):

    return jsonify({"mensaje": "Los datos han sido actualizados"}), 200
  else:
    return jsonify({"mensaje": "Usuario no encontrado"}), 403


@app.route("/productos/<int:id>", methods=["DELETE"])
def eliminar_usuario(id):
  usuario= mi_catalogo.eliminar_usuario(id)
  if usuario:
    ruta_imagen =os.path.join(RUTA_DESTINO, producto['imagen_url'])
    if os.path.exists(ruta_imagen):
      os.remove(ruta_imagen)
    if mi_catalogo.eliminar_usuario(id):
      return jsonify({"mensaje": "Usuario eliminado"}), 200
    else:
      return jsonify({"mensaje: ":"error al eliminar el usuario"}), 404






























if __name__ == "__main__":
  app.run(debug=True)









  
