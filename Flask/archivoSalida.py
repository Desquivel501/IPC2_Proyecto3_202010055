from facturas import Factura, Errores, Autorizacion
import xml.etree.ElementTree as ET
from lxml import etree 

class Salida:
    
    def __init__(self):
        pass
    
    def leerSalida(self):
        listaAutorizaciones = []
        filename = "Flask/autorizaciones.xml"
        archivo = open(filename,"r")
        contenido = archivo.read()
        
        if contenido is not "":

            parser = ET.XMLParser(encoding="utf-8")
            tree = ET.parse(filename,parser =parser)
            root = tree.getroot()
            
            for autorizacion in root.findall("AUTORIZACION"):
                fecha = autorizacion.find("FECHA").text
                noFacturas = int(autorizacion.find("FACTURAS_RECIBIDAS").text)
                
                listaErrores = Errores()
                errores = autorizacion.find("ERRORES")
                listaErrores.duplicada = int(errores.find("REFERENCIA_DUPLICADA").text)
                if listaErrores.duplicada is None:
                    listaErrores.duplicada = 0
                    
                listaErrores.nit_receptor = int(errores.find("NIT_RECEPTOR").text)
                if listaErrores.nit_receptor is None:
                    listaErrores.nit_receptor = 0
                    
                listaErrores.nit_emisor = int(errores.find("NIT_EMISOR").text)
                if listaErrores.nit_emisor is None:
                    listaErrores.nit_emisor = 0
                    
                listaErrores.iva = int(errores.find("IVA").text)
                if listaErrores.iva is None:
                    listaErrores.iva = 0
                    
                listaErrores.total = int(errores.find("TOTAL").text) 
                if listaErrores.total is None:
                    listaErrores.total = 0
                
                noCorrectas = int(autorizacion.find("FACTURAS_CORRECTAS").text)
                noReceptores = int(autorizacion.find("CANTIDAD_RECEPTORES").text)
                noEmisores = int(autorizacion.find("CANTIDAD_EMISORES").text)
                
                listaFacturas = []
                listado_autorizacion = autorizacion.find("LISTADO_AUTORIZACIONES")
                
                for factura in listado_autorizacion.findall("APROBACION"):
                    nit_emisor = factura.find("NIT_EMISOR").text
                    referencia = factura.find("NIT_EMISOR").attrib["ref"]
                    codigo_aprobacion = factura.find("CODIGO_APROBACION").text
                    total = factura.find("TOTAL").text
                    valor = round(float(total)/1.12, 2)
                    iva = float(total) - float(valor)

                    listaFacturas.append(Factura(fecha,referencia,nit_emisor,None,valor,round(iva,2),total,codigo_aprobacion))   
                
                listaAutorizaciones.append(Autorizacion(fecha,int(noFacturas),listaFacturas,listaErrores,noReceptores,noEmisores,noCorrectas))
        

            
        return listaAutorizaciones
    
    
    def generarSalida(self, listaAutorizaciones):
        root = etree.Element('LISTAAUTORIZACIONES')
        tree = etree.ElementTree(root)
        
        for autorizacion in listaAutorizaciones:
            
            autorizacion_tag = etree.Element('AUTORIZACION')
            root.append(autorizacion_tag)
            
            fecha = etree.Element('FECHA')
            fecha.text = str(autorizacion.fecha)
            autorizacion_tag.append(fecha)
            
            recibidas = etree.Element('FACTURAS_RECIBIDAS')
            recibidas.text = str(autorizacion.noFacturas)
            autorizacion_tag.append(recibidas)
            
            errores = etree.Element('ERRORES')
            autorizacion_tag.append(errores)
            
            error_emisor = etree.Element('NIT_EMISOR')
            error_emisor.text = str(autorizacion.error.nit_emisor)
            errores.append(error_emisor)
            
            error_receptor = etree.Element('NIT_RECEPTOR')
            error_receptor.text = str(autorizacion.error.nit_receptor)
            errores.append(error_receptor)
            
            error_duplicada = etree.Element('REFERENCIA_DUPLICADA')
            error_duplicada.text = str(autorizacion.error.duplicada)
            errores.append(error_duplicada)
            
            error_valor = etree.Element('VALOR')
            error_valor.text = str(autorizacion.error.valor)
            errores.append(error_valor)
            
            error_iva = etree.Element('IVA')
            error_iva.text = str(autorizacion.error.iva)
            errores.append(error_iva)
            
            error_total = etree.Element('TOTAL')
            error_total.text = str(autorizacion.error.total)
            errores.append(error_total)
            
            noCorrectas = etree.Element('FACTURAS_CORRECTAS')
            noCorrectas.text = str(autorizacion.noCorrectas)
            autorizacion_tag.append(noCorrectas)
            
            noEmisores = etree.Element('CANTIDAD_EMISORES')
            noEmisores.text = str(autorizacion.noEmisores)
            autorizacion_tag.append(noEmisores)
            
            noReceptores = etree.Element('CANTIDAD_RECEPTORES')
            noReceptores.text = str(autorizacion.noReceptores)
            autorizacion_tag.append(noReceptores)
            
            listado = etree.Element('LISTADO_AUTORIZACIONES')
            autorizacion_tag.append(listado)
            
            noAprobaciones = 0
            for factura in autorizacion.listaFacturas:
                aprobacion = etree.Element('APROBACION')
                listado.append(aprobacion)
                
                nit_emisor = etree.Element('NIT_EMISOR')
                nit_emisor.text = str(factura.nit_emisor)
                nit_emisor.set('ref', str(factura.referencia))
                aprobacion.append(nit_emisor)
                
                codigo = etree.Element('CODIGO_APROBACION')
                codigo.text = str(factura.codigo)
                aprobacion.append(codigo)
                
                total = etree.Element('TOTAL')
                total.text = str(factura.total)
                aprobacion.append(total)
                
                noAprobaciones+=1
            
            total_aprobaciones = etree.Element('TOTAL_APROBACIONES')
            total_aprobaciones.text = str(noAprobaciones)
            listado.append(total_aprobaciones)
            
            try:
                filename = "Flask/autorizaciones.xml"
                tree.write(filename, pretty_print=True)
            except Exception as e:
                print("ERROR: ",e)
                
                
                
            
            
            
            
            
            
            
            
            
            