class Ruta:
    
    ID = 0
    NAME = "" 
    ACTIVE = 0
    COLOR_ID = ""
    PARADA_INI = 0
    PARADA_FIN = 0
    DISTANCIA = 0
    TIEMPO = 0
    ENTRENADO = 0

    def __init__(self):

        try:
            
            self.ID = 0
            self.NAME = "" 
            self.ACTIVE = 0
            self.COLOR_ID = ""
            self.PARADA_INI = 0
            self.PARADA_FIN = 0
            self.DISTANCIA = 0
            self.TIEMPO = 0
            self.ENTRENADO = 0

        except Exception as ex:
            print(str(ex))
