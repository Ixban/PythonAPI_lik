import datetime
import Librerias.Bitacora as Bit

# <editor-fold desc="Metodos de Fechas">
def convert_datetime_datetime(fecha):
    try:
        str_fecha = fecha.strftime("%Y-%m-%d %H:%M:%S")
        return datetime.datetime.strptime(str_fecha, '%Y-%m-%d %H:%M:%S')
    except Exception as ex:
        Bit.add_bitacora(Bit.Tipo.EXCEPCION, Bit.USUARIO_ID, "ERROR EN convert_datetime_datetime.",
                         "Error: " + ex.__str__(), "UTILERIAS", "convert_datetime_datetime", "", "", "", 1, 1)

    return None

def convert_string_datetime(fecha):
    try:
        return datetime.datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
    except Exception as ex:
        Bit.add_bitacora(Bit.Tipo.EXCEPCION, Bit.USUARIO_ID, "ERROR EN convert_string_datetime.",
                         "Error: " + ex.__str__(), "UTILERIAS", "convert_string_datetime", "", "", "", 1, 1)

    return None

def convert_datetime_string(fecha):
    try:
        return fecha.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as ex:
        Bit.add_bitacora(Bit.Tipo.EXCEPCION, Bit.USUARIO_ID, "ERROR EN convert_datetime_string.",
                         "Error: " + ex.__str__(), "UTILERIAS", "convert_datetime_string", "", "", "", 1, 1)

    return None
# </editor-fold>