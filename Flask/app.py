from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
import json
from facturas import Factura, Errores, Autorizacion
from functions import Functions
from archivoSalida import Salida

app = Flask(__name__)
CORS(app)

listaAutorizaciones = []

@app.before_first_request
def leerArchivoSalida():
    salida = Salida()
    global listaAutorizaciones
    listaAutorizaciones = salida.leerSalida()

@app.after_request
def actualizarArchivoSalida(response):
    salida = Salida()
    salida.generarSalida(listaAutorizaciones)
    return response

@app.route("/entrada",methods=["POST"])
def leerEntrada():
    funcion = Functions()
    texto = request.json['archivo']
    # print(texto)
    global listaAutorizaciones
    listaAutorizaciones = funcion.analizarEntrada(texto, listaAutorizaciones)
    return jsonify({
        "Mensaje":"Se ha leido el archivo"
    }) 
    
@app.route("/getSalida", methods=["GET"])
def getSalidaStr():
    filename = "Flask/autorizaciones.xml"
    archivo = open(filename, "r")
    contenido = archivo.read()
    print("salida")
    print(contenido)
    objeto = {
        "xml":contenido
    }
    
    return jsonify(objeto)

if __name__ == "__main__":
    app.run(threaded=True, debug=True)