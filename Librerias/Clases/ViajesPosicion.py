class ViajesPosicion:
    
    VIAJE_ID = 0
    SEQUENCE = 0
    FECHA_HORA_PROCESAMIENTO = "None"
    FECHA_HORA_GPS = ""
    VELOCIDAD = 0
    DISTANCIA = 0
    PORCENTAJE_AVANCE_RUTA = 0
    PORCENTAJE_AVANCE_TRECHO = 0
    LATITUD = 0
    LONGITUD = 0
    TRECHO_ANTERIOR_ID = 0
    TRECHO_ACTUAL_ID = 0
    TRECHO_SIGUIENTE_ID = 0
    PARADA_ANTERIOR_ID = 0
    PARADA_SIGUIENTE_ID = 0
    FECHA_HORA_SIGUIENTE_PARADA_ESTIMADA = "None"
    ULTIMO_EVENTO_ID = 0
    PUNTUALIDAD = 0
    PUNTUALIDAD_PROGRAMADA = "None"
    FRECUENCIA_ATRAS = 0
    FRECUENCIA_ADELANTE = 0
    DISTANCIA_ATRAS = 0
    DISTANCIA_ADELANTE = 0
    VIAJE_ATRAS_ID = 0
    VIAJE_ADELANTE_ID = 0
    CLIMA_TIPO_ID = 0
    COLOR_PUNTUALIDAD = "N"
    COLOR_FRECUENCIA_ADELANTE = "N"
    COLOR_FRECUENCIA_ATRAS = "N"
    COLOR_STATUS = "N"
    VIAJE_STATUS_RECORRIDO_ID = 0

    def __init__(self):

        try:
            
            self.VIAJE_ID = 0
            self.SEQUENCE = 0
            self.FECHA_HORA_PROCESAMIENTO = "None"
            self.FECHA_HORA_GPS = "None"
            self.VELOCIDAD = 0
            self.DISTANCIA = 0
            self.PORCENTAJE_AVANCE_RUTA = 0
            self.PORCENTAJE_AVANCE_TRECHO = 0
            self.LATITUD = 0
            self.LONGITUD = 0
            self.TRECHO_ANTERIOR_ID = 0
            self.TRECHO_ACTUAL_ID = 0
            self.TRECHO_SIGUIENTE_ID = 0
            self.PARADA_ANTERIOR_ID = 0
            self.PARADA_SIGUIENTE_ID = 0
            self.FECHA_HORA_SIGUIENTE_PARADA_ESTIMADA = "None"
            self.ULTIMO_EVENTO_ID = 0
            self.PUNTUALIDAD = 0
            self.PUNTUALIDAD_PROGRAMADA = 0
            self.FRECUENCIA_ATRAS = 0
            self.FRECUENCIA_ADELANTE = 0
            self.DISTANCIA_ATRAS = 0
            self.DISTANCIA_ADELANTE = 0
            self.VIAJE_ATRAS_ID = 0
            self.VIAJE_ADELANTE_ID = 0
            self.CLIMA_TIPO_ID = 0
            self.COLOR_PUNTUALIDAD = "N"
            self.COLOR_FRECUENCIA_ADELANTE = "N"
            self.COLOR_FRECUENCIA_ATRAS = "N"
            self.COLOR_STATUS = "N"
            self.VIAJE_STATUS_RECORRIDO_ID = 0

        except Exception as ex:
            print(str(ex))
