import xml.etree.ElementTree as ET
from facturas import Factura, Errores, Autorizacion
import re

class Functions:
    
    def __init__(self):
        pass

    def analizarEntrada(self, xml, listaAutorizaciones):
        string = xml
        if string == "":
            return
        
        tree = ET.ElementTree(ET.fromstring(string))
        root = tree.getroot()
        valid = True
        
        for dte in  root.findall("DTE"):
            tiempo = dte.find("TIEMPO").text
            referencia = str(dte.find("REFERENCIA").text).strip()
            emisor = dte.find("NIT_EMISOR").text
            receptor = dte.find("NIT_RECEPTOR").text
            valor = dte.find("VALOR").text
            iva = dte.find("IVA").text
            total = dte.find("TOTAL").text
            
            tiempo_parseado = self.parseTiempo(tiempo)

            fecha = tiempo_parseado[0][0]
            hora = tiempo_parseado[1][0]
            print(fecha)
            index = self.getAutorizacion(listaAutorizaciones,fecha)
            
            codigo = int(listaAutorizaciones[index].codigo) + 1
            
            valor_parseado = self.checkValor(valor)
            iva_parseado = self.checkValor(iva)
            total_parseado = self.checkValor(total)
            
           
            
            if not fecha:
                valid = False
                listaAutorizaciones[index].error.fecha += 1
            if not hora:
                valid = False
                listaAutorizaciones[index].error.hora += 1
            if self.checkReferencia(referencia, listaAutorizaciones):
                valid = False
                listaAutorizaciones[index].error.duplicada += 1
            if self.comprobarNIT(emisor) is False:
                valid = False
                listaAutorizaciones[index].error.nit_emisor += 1
            if self.comprobarNIT(receptor) is False:
                valid = False
                listaAutorizaciones[index].error.nit_receptor += 1
            if valor_parseado[1] is False:
                valid = False
                listaAutorizaciones[index].error.valor += 1
            if iva_parseado[1] is False or self.checkIva(valor, iva) is False:
                valid = False
                listaAutorizaciones[index].error.iva += 1
            if total_parseado[1] is False or self.checkTotal(valor, iva, total) is False:
                valid = False
                listaAutorizaciones[index].error.total += 1
                
            if valid:
                print("Valid!")
                
                receptor_repetido = False
                for factura in listaAutorizaciones[index].listaFacturas:
                        
                    if str(factura.nit_receptor) == str(receptor):
                        receptor_repetido = True
                if receptor_repetido is False:
                    listaAutorizaciones[index].noReceptores += 1
                        
                emisor_repetido = False
                for factura in listaAutorizaciones[index].listaFacturas:
                        
                    if str(factura.nit_emisor) == str(emisor):
                        emisor_repetido = True
                if emisor_repetido is False:
                    listaAutorizaciones[index].noEmisores += 1

                
                listaAutorizaciones[index].listaFacturas.append(Factura(fecha,referencia,emisor,receptor,valor,iva,total, codigo))
                listaAutorizaciones[index].noFacturas += 1
                listaAutorizaciones[index].noCorrectas += 1
                listaAutorizaciones[index].codigo += 1
                
                print("here")
                
                
                    
            else:
                # del listaAutorizaciones[-1]
                print("Invalid")
            
        return (listaAutorizaciones)
            
    def leerSalida(self):
        pass
    
    def parseTiempo(self, tiempo):
        fecha = "noFecha"
        hora = "noHora"
        
        fecha = re.findall(r'[0-9]{2}/[0-9]{2}/[0-9]{4}', tiempo)
        hora = re.findall(r'[0-9]{1,2}:[0-9]{1,2}', tiempo)
        
        if fecha:
            aux = fecha[0].split("/")
            if not 0<int(aux[0])<32:
                fecha = []
            if not 0<int(aux[1])<13:
                fecha = []
            # if not 0<int(aux[2]):
            #     fecha = []
        
        if hora:
            aux2 = hora[0].split(":")
            if not 0<int(aux2[0])<25:
                hora = []
            if not 0<int(aux2[1])<61:
                hora = []      
              
        # print(fecha, hora)
        return(fecha,hora)
        
    def checkReferencia(self, referencia, listaAutorizaciones):
        for autorizacion in listaAutorizaciones:
            for factura in autorizacion.listaFacturas:
                if str(factura.referencia).strip() == str(referencia):
                    print("Referencia Repetida")
                    return True
        return False
                
    
    def comprobarNIT(self, nit):
        return True
    
    def checkValor(self, tiempo):
        valor_res = "noValor"
        valor_res = re.findall(r'[0-9]+\.[0-9]{2}', tiempo)
        res = 0
        found = False
        print(valor_res)
        if valor_res:
            found = True
            res = float(valor_res[0])
        
        print(res, found)
        return(res, found)
    
    def checkIva(self, valor, iva):
        total = round(float(valor)*0.12, 2)
        print(total, iva)
        if float(total) == float(iva):
            return True
        print("IVA no valido")
        return False
    
    def checkTotal(self, valor, iva, total):
        aux = float(valor) + float(iva)
        
        if float(aux) == float(total):
            return True
        print("Total no valido")
        return False
    
    def getAutorizacion(self, listaAutorizacion, fecha):
        index = 0
        for autorizacion in listaAutorizacion:
            if autorizacion.fecha.strip() == fecha.strip():
                return index
            index += 1
        error = Errores()
        listaAutorizacion.append(Autorizacion(fecha,0,[],error,0,0,0))
        return index
 
    def tablaIva(self, nit, desde , hasta, listaAutorizaciones):
        import time
        from datetime import datetime
        from time import mktime

        lista = []
        
        desde = desde.strip()
        hasta = hasta.strip()
        
        fecha_desde = time.strptime(desde, "%d/%m/%Y")
        fecha_hasta = time.strptime(hasta, "%d/%m/%Y")
        
        check_valid = False
        
        if fecha_desde < fecha_hasta:
            print("Valid")
            check_valid = True
        else:
            print("No")
            
        if check_valid:
            for autorizacion in listaAutorizaciones:
                lista_aux = []
                
                fecha = autorizacion.fecha.strip()
                fecha_actual = time.strptime(fecha, "%d/%m/%Y")
                
                if fecha_desde <= fecha_actual <= fecha_hasta:
                    lista_aux.append(fecha_actual)
                    
                    dt = datetime.fromtimestamp(mktime(fecha_actual))
                    
                    fecha_str = dt.strftime("%d/%m/%Y")
                    
                    total_emitido = 0
                    total_recibido = 0
                    
                    for factura in autorizacion.listaFacturas:

                        if str(factura.nit_emisor).strip() == str(nit).strip():
                            iva = float(str(factura.iva).strip())
                            total_emitido += iva

                        print(nit, factura.nit_receptor)  
                        if str(factura.nit_receptor).strip() == str(nit).strip():
                            iva = float(str(factura.iva).strip())
                            total_recibido += iva
                    
                    lista_aux.append(total_emitido)
                    lista_aux.append(total_recibido)
                    
                lista.append(lista_aux)

            lista.sort()
            
            lista_fechas_aux = []
            lista_emisores_aux = []
            lista_receptores_aux = []
            
            for elemento in lista:
                dt = datetime.fromtimestamp(mktime(elemento[0]))
                fecha_str = dt.strftime("%d/%m/%Y")
                
                lista_fechas_aux.append(fecha_str)
                lista_emisores_aux.append(elemento[1])
                lista_receptores_aux.append(elemento[2])

            return (lista_fechas_aux, lista_emisores_aux, lista_receptores_aux )
        return(None)
              
    def tablaFecha(self, iva, desde , hasta, listaAutorizaciones):
        import time
        from datetime import datetime
        from time import mktime
        
        lista = []
        
        desde = desde.strip()
        hasta = hasta.strip()
        
        fecha_desde = time.strptime(desde, "%d/%m/%Y")
        fecha_hasta = time.strptime(hasta, "%d/%m/%Y")
        
        check_valid = False
        
        if fecha_desde < fecha_hasta:
            print("Valid")
            check_valid = True
        else:
            print("No")
            
        if check_valid:
            for autorizacion in listaAutorizaciones:
                lista_aux = []
                
                fecha = autorizacion.fecha.strip()
                fecha_actual = time.strptime(fecha, "%d/%m/%Y")
                
                if fecha_desde <= fecha_actual <= fecha_hasta:
                    lista_aux.append(fecha_actual)
                    
                    dt = datetime.fromtimestamp(mktime(fecha_actual))
                    fecha_str = dt.strftime("%d/%m/%Y")
                    
                    total = 0
                    for factura in autorizacion.listaFacturas:
                        if iva:
                            total += float(factura.total)
                        else:
                            total += float(factura.valor)
    
                    lista_aux.append(total)
                    
                lista.append(lista_aux)

            lista.sort()
            
            lista_fechas_aux = []
            lista_total_aux = []
            
            for elemento in lista:
                dt = datetime.fromtimestamp(mktime(elemento[0]))
                fecha_str = dt.strftime("%d/%m/%Y")
                
                lista_fechas_aux.append(fecha_str)
                lista_total_aux.append(elemento[1])
                
            return (lista_fechas_aux, lista_total_aux)
        return(None)       
            
            