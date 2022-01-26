class ViajesTrecho:
    
    ID = 0
    VIAJE_ID = 0
    TRECHO_ID = 0
    TRECHO_TRAZADO_ID = 0
    FECHA_HORA_PROGRAMADA_LLEGADA ="None"
    FECHA_HORA_REAL_LLEGADA ="None"
    FECHA_HORA_PROGRAMADA_SALIDA = "None"
    FECHA_HORA_REAL_SALIDA = "None"

    def __init__(self):

        try:
            
            self.ID = 0
            self.VIAJE_ID = 0
            self.TRECHO_ID = 0
            self.TRECHO_TRAZADO_ID = 0
            self.FECHA_HORA_PROGRAMADA_LLEGADA ="None"
            self.FECHA_HORA_REAL_LLEGADA ="None"
            self.FECHA_HORA_PROGRAMADA_SALIDA = "None"
            self.FECHA_HORA_REAL_SALIDA = "None "

        except Exception as ex:
            print(str(ex))
