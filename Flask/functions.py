from os import path
import xml.etree.ElementTree as ET
from facturas import Factura, Errores, Autorizacion
import re

class Functions:
    
    def __init__(self):
        pass

    def analizarEntrada(self, xml, listaAutorizaciones):
        string = xml
        if string == "":
            return(listaAutorizaciones)
        
        try:
            tree = ET.ElementTree(ET.fromstring(string))
        except:
            print("Exit")
            return(listaAutorizaciones)
        
        root = tree.getroot()
        
        for dte in  root.findall("DTE"):
            valid = True
            tiempo = str(dte.find("TIEMPO").text).strip()
            referencia = str(dte.find("REFERENCIA").text).strip()
            emisor = str(dte.find("NIT_EMISOR").text).strip()
            receptor = str(dte.find("NIT_RECEPTOR").text).strip()
            valor = str(dte.find("VALOR").text).strip()
            iva = str(dte.find("IVA").text).strip()
            total = str(dte.find("TOTAL").text).strip()
            
            tiempo_parseado = self.parseTiempo(tiempo)

            fecha = tiempo_parseado[0]
            hora = tiempo_parseado[1]
            
            if fecha[1]:
                index = self.getAutorizacion(listaAutorizaciones,fecha[0])
                listaAutorizaciones[index].noFacturas += 1
            else:
                print("Exit")
                return(listaAutorizaciones)
            
            codigo = int(listaAutorizaciones[index].codigo) + 1
            
            valor_parseado = self.checkValor(valor)
            iva_parseado = self.checkValor(iva)
            total_parseado = self.checkValor(total)
            

            if fecha[1] is False:
                valid = False
                listaAutorizaciones[index].error.fecha += 1
                print("Error Fecha")
            if hora[1] is False:
                listaAutorizaciones[index].error.hora += 1
                print("Error Hora")
            if self.checkReferencia(referencia, listaAutorizaciones):
                valid = False
                print("Error Referencia")
                listaAutorizaciones[index].error.duplicada += 1
                
            comprobarEmisor = self.comprobarNIT(emisor)
            if comprobarEmisor[0] is False:
                valid = False
                print("Error Nit Emisor")
                listaAutorizaciones[index].error.nit_emisor += 1
            emisor = comprobarEmisor[1]
            
            comprobarReceptor = self.comprobarNIT(receptor)
            if comprobarReceptor[0] is False:
                valid = False
                print("Error Nit Receptor")
                listaAutorizaciones[index].error.nit_receptor += 1
            receptor = comprobarReceptor[1]
                
            if valor_parseado[1] is False:
                valid = False
                print("Error Valor")
                listaAutorizaciones[index].error.valor += 1
                
            if iva_parseado[1] is False or self.checkIva(valor_parseado[0], iva_parseado[0]) is False:
                valid = False
                print("Error Iva")
                listaAutorizaciones[index].error.iva += 1
                
            if total_parseado[1] is False or self.checkTotal(valor_parseado[0], iva_parseado[0], total_parseado[0]) is False:
                valid = False
                print("Error Total")
                listaAutorizaciones[index].error.total += 1
                
            if valid:
                print("Valid!")
                
                receptor_repetido = False
                for factura in listaAutorizaciones[index].listaFacturas:       
                    if str(factura.nit_receptor).strip() == str(receptor).strip():
                        receptor_repetido = True
                if receptor_repetido is False:
                    listaAutorizaciones[index].noReceptores += 1
                        
                emisor_repetido = False
                for factura in listaAutorizaciones[index].listaFacturas:
                    if str(factura.nit_emisor).strip() == str(emisor).strip():
                        emisor_repetido = True
                if emisor_repetido is False:
                    listaAutorizaciones[index].noEmisores += 1

                
                listaAutorizaciones[index].listaFacturas.append(Factura(fecha[0],referencia, str(emisor).strip(), str(receptor).strip(), valor,iva,total, codigo))
                
                listaAutorizaciones[index].noCorrectas += 1
                listaAutorizaciones[index].codigo += 1
                 
            else:
                print("Invalid")
            
        return (listaAutorizaciones)
            
    def leerSalida(self):
        pass
    
    def parseTiempo(self, tiempo):
        fecha = "noFecha"
        hora = "noHora"
        
        fecha = re.findall(r'[0-9]{2}/[0-9]{2}/[0-9]{4}', tiempo)
        hora = re.findall(r'[0-9]{1,2}:[0-9]{1,2}', tiempo)
        
        fecha_list = [None,False]
        if fecha:
            print("Found Fecha:", fecha)
            fecha_list = [fecha[0],True]
            aux = fecha[0].split("/")
            if not 0<int(aux[0])<32:
                fecha_list = [None,False]
            if not 0<int(aux[1])<13:
                fecha_list = [None,False]
        
        hora_list = [None,False]
        if hora:
            print("Found Hora", hora)
            hora_list = [hora[0],True]
            aux2 = hora[0].split(":")
            if not 0<int(aux2[0])<25:
                hora_list = [None,False]
            if not 0<=int(aux2[1])<61:
                hora_list = [None,False]
              
        return(fecha_list, hora_list)
        
    def checkReferencia(self, referencia, listaAutorizaciones):
        for autorizacion in listaAutorizaciones:
            for factura in autorizacion.listaFacturas:
                if str(factura.referencia).strip() == str(referencia):
                    print("Referencia Repetida")
                    return True
        return False
                
    def comprobarNIT(self, nit):
        valor = str(nit).strip()     
        try:
            int(valor)
        except ValueError:
            return (False, None)
 
        if len(valor) > 20:
            return (False, None)
        
        digit_map = map(int, valor)
        nit_list = list(digit_map)
        
        nit_list.pop()

        nit_list = list(reversed(nit_list))
        
        total = 0
        aux = 1
        for num in nit_list:
            total += aux*num
            aux+=1
        

        total = total % 11
        total = 11 - total 
        total = total % 11
        
        if total == 10:
            nit = str(nit).strip()
            nit += "K"

        return (True, nit)
    
    def checkValor(self, valor):
        valor_res = re.findall(r'\b[0-9]+\.[0-9]{2}(?!\S)\b', valor)
        is_match = bool(valor_res)
        
        if is_match:
            res = float(valor_res[0])
            return(res, True)
        else:
            return (0, False)
        
    
    def checkIva(self, valor, iva):
        total = round(float(valor)*0.12, 2)
        if (float(iva)-1) <= float(total) <= (float(iva)+1):
            return True
        return False
    
    def checkTotal(self, valor, iva, total):
        aux = float(valor) + float(iva)
        
        if (float(total)-1) <= float(aux) <= (float(total)+1):
            return True
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
 
    def tablaIva(self, fecha, listaAutorizaciones):
        titulos = []
        lista_emitido = []
        lista_recibido = []
        lista_nits = self.getNits(listaAutorizaciones)
        
        fecha = fecha.strip()
        
        for autorizacion in listaAutorizaciones:

            fecha_actual = autorizacion.fecha.strip()
                
            if fecha == fecha_actual:
                
                for nit_actual in lista_nits:  
                    total_emitido = 0
                    total_recibido = 0
                    titulos.append(nit_actual)
                
                    for factura in autorizacion.listaFacturas:
            
                        if str(factura.nit_emisor).strip() == str(nit_actual).strip():
                            iva = float(str(factura.iva).strip())
                            total_emitido += iva
    
                        if str(factura.nit_receptor).strip() == str(nit_actual).strip():
                            iva = float(str(factura.iva).strip())
                            total_recibido += iva
                            
                    if total_emitido == 0 and total_recibido == 0:
                        titulos.pop()
                    else:
                        lista_emitido.append(float(round(float(total_emitido), 2)))
                        lista_recibido.append(float(round(float(total_recibido), 2)))
                    
                return (titulos, lista_emitido, lista_recibido)
        
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
            
            
        if lista_fechas_aux and lista_total_aux:
            return (lista_fechas_aux, lista_total_aux)
        else:
            return(None)       
            
    def tablaIva2(self, nit, fecha , listaAutorizaciones):

        valores = []
        titulos = ["Emitido", "Recibido"]
        
        fecha = fecha.strip()
        
        for autorizacion in listaAutorizaciones:

            fecha_actual = autorizacion.fecha.strip()
                
            if fecha == fecha_actual:
                total_emitido = 0
                total_recibido = 0
                
                for factura in autorizacion.listaFacturas:
                    
                    if str(factura.nit_emisor).strip() == str(nit).strip():
                        iva = float(str(factura.iva).strip())
                        total_emitido += iva
  
                    if str(factura.nit_receptor).strip() == str(nit).strip():
                        iva = float(str(factura.iva).strip())
                        total_recibido += iva
                
                valores.append(float(total_emitido))
                valores.append(float(total_recibido))

                return (valores, titulos)
        
        return(None)
    
    
    def getNits(sef, listaAutorizaciones):
        lista_nits = []
        
        for autorizacion in listaAutorizaciones:
            for factura in autorizacion.listaFacturas:
                
                if str(factura.nit_emisor).strip() not in lista_nits:
                    if factura.nit_emisor is not None:
                        lista_nits.append(str(factura.nit_emisor).strip())
                    
                if str(factura.nit_receptor).strip() not in lista_nits:
                    if factura.nit_receptor is not None:
                        lista_nits.append(str(factura.nit_receptor).strip())
                    
        return lista_nits