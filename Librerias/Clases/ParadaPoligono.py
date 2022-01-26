class Parada_Poligono:
        
    ID = 0
    PARADA_ID = 0
    SEQUENCE   = 0
    ACTIVE = 0
    LATITUD = 0
    LONGITUD = 0

    def __init__(self):

        try:
            
            self.ID = 0
            self.PARADA_ID = 0
            self.SEQUENCE   = 0
            self.ACTIVE = 0
            self.LATITUD = 0
            self.LONGITUD = 0

        except Exception as ex:
            print(str(ex))
