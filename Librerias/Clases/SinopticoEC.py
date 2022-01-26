class SinopticoEC:
    #SinopticoEscalaCoor
    sinoptico_id = 0
    latitud_min = 0
    latitud_max = 0
    longitud_min = 0
    longitud_max = 0
    proporcion_lat = 0
    proporcion_long = 0
    size = 0

    def __init__(self):
    
        try:
            
            self.sinoptico_id = 0
            self.latitud_min = 0
            self.latitud_max = 0
            self.longitud_min = 0
            self.longitud_max = 0
            self.proporcion_lat = 0
            self.proporcion_long = 0
            self.size = 0

        except Exception as ex:
            print(str(ex))