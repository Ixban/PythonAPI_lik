from Librerias.Clases.Trazados import Trazados

class Coordenadas():

    Trecho_Trazado_ID = 0
    Secuencia = 0
    SEQUENCE = 0
    Eje_X = 0
    Eje_Y = 0
    Latitud = 0
    Longitud = 0
    DistanciaAcumulada = 0

    def __init__(self):

        try:
            self.TRECHO_TRAZADO_ID = 0
            self.Secuencia = 0
            self.Eje_X = 0
            self.Eje_Y = 0
            self.SEQUENCE = 0
            self.LATITUD = 0
            self.LONGITUD = 0
            self.DistanciaAcumulada = 0
            
        except Exception as ex:
            print(str(ex))
