class Autorizacion:
    def __init__(self,fecha, noFacturas, listaFacturas, error, noReceptores,noEmisores, noCorrectas):
        self.fecha=fecha
        self.noFacturas = noFacturas
        self.listaFacturas = listaFacturas
        self.error = error
        self.noReceptores = noReceptores
        self.noEmisores = noEmisores
        self.noCorrectas = noCorrectas
        self.codigo = int(self.getCodigo(str(fecha))) + int(noCorrectas)
        
        
    def getCodigo(self, fecha):
        cero = "00000000"
        lista = fecha.split("/")
        lista = reversed(lista)
        valor = ''.join(map(str, lista))
        codigo = str(valor) + cero
        return (codigo.replace(' ',''))


class Factura:
    
    def __init__(self, fecha, referencia, nit_emisor, nit_receptor, valor, iva, total, codigo):
        self.fecha = fecha
        self.referencia = referencia
        self.nit_receptor = nit_receptor
        self.nit_emisor = nit_emisor
        self.valor = valor
        self.iva = iva
        self.total = total
        self.codigo = codigo

class Errores:
    def __init__(self): 
        self.fecha = 0
        self.hora = 0
        self.referencia = 0
        self.nit_receptor = 0
        self.nit_emisor = 0
        self.valor = 0
        self.iva = 0
        self.total = 0
        self.duplicada = 0