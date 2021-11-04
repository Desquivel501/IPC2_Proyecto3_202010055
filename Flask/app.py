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
    objeto = {
        "xml":contenido
    }

    return jsonify(objeto)


@app.route("/getTablaIva", methods=["POST"])
def getTablaIva():
    global listaAutorizaciones
    
    tabla = Functions()

    fecha = request.json['fecha']
    
    datos = tabla.tablaIva(fecha,listaAutorizaciones)
    
    objeto={"mensaje":"ERROR"}
    
    if datos is not None:

        objeto = {
            "titulos":datos[0],
            "emitido":datos[1],
            "recibido":datos[2],
            "mensaje":"Correcto",
            "titulo":str("IVA emitido y recibido el " + fecha),
        }
    return jsonify(objeto)


@app.route("/getTablaIva2", methods=["POST"])
def getTablaIva2():
    global listaAutorizaciones
    
    tabla = Functions()

    nit = request.json['nit']
    fecha = request.json['fecha']
    
    datos = tabla.tablaIva2(nit,fecha,listaAutorizaciones)
    
    objeto={"mensaje":"ERROR"}
    
    if datos is not None:

        objeto = {
            "xValues":datos[1],
            "yValues":datos[0],
            "titulo":str("IVA emitido y recibido el " + fecha),
            "mensaje":"Correcto"
        }
    return jsonify(objeto)


@app.route("/getTablaFecha", methods=["POST"])
def getTablaFecha():
    global listaAutorizaciones
    
    tabla = Functions()

    iva = request.json['iva']
    desde = request.json['desde']
    hasta = request.json['hasta']
    
    datos = tabla.tablaFecha(iva,desde,hasta,listaAutorizaciones)
    
    objeto={"mensaje":"ERROR"}
    
    if datos is not None:
        
        objeto = {
            "xValues":datos[0],
            "total":datos[1],
            "mensaje":"Correcto"
        }

    return jsonify(objeto)


@app.route("/", methods=["GET"])
def getHome():
   
    objeto = {
        "Index":"Hola"
    }

    return jsonify(objeto)


@app.route("/reset", methods=["GET"])
def reset():
    global listaAutorizaciones
    listaAutorizaciones = []
    
    filename = "Flask/autorizaciones.xml"
    archivo = open(filename, "w+")
    archivo.write("")
    archivo.close()
    
    objeto = {"Mensaje":"Borrado"}
    
    return jsonify(objeto)


@app.route("/getNits", methods=["GET"])
def getNits():
    global listaAutorizaciones
    function = Functions()
    lista_nits = function.getNits(listaAutorizaciones)
    
    objeto = {"Lista":lista_nits}
    
    return jsonify(objeto)


@app.route("/salidaPDF", methods=["GET"])
def salidaPDF():
    import base64
    import os
    from reportlab.pdfgen import canvas
    
    filenamePDF = "Flask/IPC2_Proyecto3_202010055_Documentacion.pdf"
    
    with open(filenamePDF, "rb") as pdf_file:
        encoded_string = base64.b64encode(pdf_file.read())
        
    print("salida")
    objeto = {
        "archivo":str(encoded_string)
    }

    return jsonify(objeto)








if __name__ == "__main__":
    app.run(threaded=True, debug=True)