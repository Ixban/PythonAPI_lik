class SinopticoResumen:
    
    Viajes_Programados = 0
    Autobus_Programdos_Sinoptico = 0
    Autobus_Reales_Sinoptico = 0
    Autobus_Retrasados_Sinoptico = 0
    Autobus_Puntual_Sinoptico = 0
    Frecuencia_Paso_Sinoptico = 0
    Frecuencia_Salida_Terminal = 0
    Frecuencia_Llegada_Terminal = 0
    Frecuencia_Salida_Sinoptico = 0
    Frecuencia_Llegada_Sinoptico = 0
    Frecuencia_Autobuses_En_Sinoptico = 0

    def __init__(self):

        try:
            
            self.Viajes_Programados = 0 #
            self.Autobus_Programdos_Sinoptico = 0 #
            self.Autobus_Reales_Sinoptico = 0 #
            self.Autobus_Retrasados_Sinoptico = 0 #
            self.Autobus_Puntual_Sinoptico = 0 #
            self.Frecuencia_Paso_Sinoptico = 0 #
            self.Frecuencia_Salida_Terminal = 0 #
            self.Frecuencia_Llegada_Terminal = 0
            self.Frecuencia_Salida_Sinoptico = 0
            self.Frecuencia_Llegada_Sinoptico = 0
            self.Frecuencia_Autobuses_En_Sinoptico = 0

        except Exception as ex:
            print(str(ex))
