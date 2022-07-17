from clases import Classic, Gold, Black
from razones import RazonAltaChequera,RazonAltaTarjetaCredito,RazonCompraDolar,RazonRetiroEfectivo,RazonTransferenciaEnviada,RazonTransferenciaRecibida, razon
import json, datetime, webbrowser

def leerJSON():
    try:
        archivoJson = open("eventos\eventos_gold.json", "r", newline="")
    except FileNotFoundError:                              
        print("Error. El archivo especificado no existe.")
    else:
        datos_cliente = json.load(archivoJson)
        return datos_cliente
        
def crearCliente(datos_cliente):
    if datos_cliente["tipo"] == "CLASSIC":
        cliente = Classic(datos_cliente)
    elif datos_cliente["tipo"] == "GOLD":
        cliente = Gold(datos_cliente)
    elif datos_cliente["tipo"] == "BLACK":
        cliente = Black(datos_cliente)

    return cliente

def procesarTransacciones(transacciones, cliente):
    transacciones_procesadas = []   #Array de diccionario de cada transacción con los datos a usar
    razon = ""

    for transaccion in transacciones:
        if transaccion["estado"] == "RECHAZADA":
            if transaccion["tipo"] == "RETIRO_EFECTIVO_CAJERO_AUTOMATICO":
                razon = RazonRetiroEfectivo().resolver(cliente, transaccion)
            elif transaccion["tipo"] == "ALTA_TARJETA_CREDITO":
                razon = RazonAltaTarjetaCredito().resolver(cliente, transaccion)
            elif transaccion["tipo"] == "ALTA_CHEQUERA":
                razon = RazonAltaChequera().resolver(cliente, transaccion)
            elif transaccion["tipo"] == "COMPRA_DOLAR":
                razon = RazonCompraDolar().resolver(cliente, transaccion)
            elif transaccion["tipo"] == "TRANSFERENCIA_ENVIADA":
                razon = RazonTransferenciaEnviada().resolver(cliente, transaccion)
            elif transaccion["tipo"] == "TRANSFERENCIA_RECIBIDA":
                razon = RazonTransferenciaRecibida().resolver(cliente, transaccion)
        else:
            razon = ""

        transacciones_procesadas.append({"fecha": transaccion["fecha"], "tipo": transaccion["tipo"], "estado":transaccion["estado"], "monto": transaccion["monto"], "razon": razon})

    return transacciones_procesadas

def contenidoHtml(cliente, transacciones_procesadas):
    
    listado = ""
    for transaccion in transacciones_procesadas:
        listado += f"""
        <tr>
            <td>{transaccion["fecha"]}</td>
            <td>{transaccion["tipo"]}</td>
            <td>{transaccion["estado"]}</td>
            <td>{transaccion["monto"]}</td>
            <td>{transaccion["razon"]}</td>
        </tr>
        """
    return (f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <title>Listado de Transacciones</title>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" />
    </head>
    <body class="container align-items-center justify-content-center">
        <header class="col">
            <h1 class="row mt-3">Listado de Transacciones</h1>
        </header>
        <section  id="datosCliente">
            <div class="row">
                <hr>
                <p>Nombre: {cliente.nombre}</p>
                <hr>
                <p>Número de cliente: {cliente.numero}</p>
                <hr>
                <p>Documento: {cliente.dni}</p>
                <hr>
                <p>Dirección: {str(cliente.direccion)}</p>
                <hr>
            </div>
        </section>
        <section id="tabla">
            <table class="table">
                <thead>
                    <tr>
                        <th>Fecha</th>
                        <th>Tipo</th>
                        <th>Estado</th>
                        <th>Monto</th>
                        <th>Razón</th>
                    </tr>
                </thead> 
                <tbody>
                    {listado}
                </tbody>    
            </table>
        </section>
    </body>
    </html>
    """)

def generarHtml(cliente, transacciones_procesadas):
    contenido = contenidoHtml(cliente, transacciones_procesadas)
    timestamp = int(datetime.datetime.now().timestamp())
    documento_html = f"index-{timestamp}.html"
    ruta_html = f"{documento_html}"

    with open(ruta_html, "w", encoding="utf-8", newline="") as salida:   
        salida.write(contenido)

    try:
        webbrowser.open(ruta_html)
    except FileNotFoundError:
        print("No se ha podido generar la salida")

if __name__ == "__main__":
    datos_cliente = leerJSON()                  #Datos cliente = Diccionario leído del JSON
    cliente = crearCliente(datos_cliente)       #cliente = Objeto del cliente
    transacciones_procesadas = procesarTransacciones(datos_cliente["transacciones"], cliente)   #Array con las transacciones procesadas
    generarHtml(cliente, transacciones_procesadas)
    
