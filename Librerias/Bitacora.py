# <editor-fold desc="Importaciones">
import _thread
import datetime
import requests
import json
import Librerias.Configuracion as Config

from datetime import datetime
# </editor-fold>

# <editor-fold desc="Varibles de Configuración">
#Objeto de Configuración
obj_Configuracion = Config.CONFIG()
# </editor-fold>

# <editor-fold desc="Variables Publicas">
# --> Constantes de bitacora
USUARIO_ID = 1
# </editor-fold>

# <editor-fold desc="Clases Auxiliares">
# Clase de Tipos de Bitcora
class Tipo:
    FUNCIONAL = 1
    TECNICO = 2
    LOGIN = 3
    ACCESO = 4
    EXCEPCION = 5
    LOGOUT = 6
    INSERT = 7
    UPDATE = 8
    DELETE = 9
    GENERICO = 10
    ROBOT = 11
# </editor-fold>

# <editor-fold desc="Metodos Publicos">
# Añadimos la bitacora
def add_bitacora(type, user, header, detail, application, controller, functions, query='', table_name='', id_table=0,
                 status=1):
    resultado = False

    try:
        # Convertimos los parametros  a JSON
        data = _convierte_bitacora_json(type, user, header, detail, application, controller, functions,
                                       query, table_name, id_table, status)

        # Verificamos si tenemos que enviar la bitacora o guardamos la información.
        if obj_Configuracion.BIT_bol_envio_bitacora:
            _thread.start_new_thread(_add_bitacora_hilo, ("Nada", data))
            resultado = True
        else:
            print(detail)
            resultado = True
    except Exception as ex:
        print("Metodo: add_bitacora: " + ex.__str__())

    # Regresamos el valor
    return resultado

# </editor-fold>

# <editor-fold desc="Metodos Privados">
#Convertimos una bitacora JSON
def _convierte_bitacora_json(type, user, header, detail, application,
                            controller, functions, query='',
                            table_name='', id_table=0, status=1):
    dato = {
        "BITACORA": [{
            "type": type, "user": user, "header": header,
            "detail": detail, "application": application,
            "controller": obj_Configuracion.MACHINE_Name + "-" + controller,
            "functions": functions, "query": query,
            "table_name": table_name, "id_table": id_table, "status": status
        }]
    }
    return dato

#Agregamos la bitacora a un hilo
def _add_bitacora_hilo(var_no_sirve, data):
    resultado = False

    try:
        now = datetime.now()
        str_now = now.strftime("%H:%M:%S")

        #Mostramos el Log
        print("LOG -  Hora : {} , Data: {} ".format(str_now, json.dumps(data)))

        # Enviamos la información.
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
        r = requests.post(obj_Configuracion.BIT_url_psicopompo_bitacora + obj_Configuracion.BIT_url_psicopompo_bitacora_version
                          + "/BITACORA/Add_Bitacora", json=data, headers=headers)

        # Verificamos si la información se mando correctamente
        if r._content:
            resultado = True
        else:
            resultado = False
    except Exception as ex:
        print("Metodo: add_bitacora_hilo: " + ex.__str__())

    # Regresamos el valor
    return resultado

# </editor-fold>