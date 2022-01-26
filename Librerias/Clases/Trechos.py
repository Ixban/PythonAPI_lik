class Trechos:

    Trecho_Id = 0
    Trecho_Desc = ""
    Trecho_Origen_Id = 0
    Trecho_Origen_Desc =  ""
    Trecho_Destino_id = 0
    Trecho_Destino_Desc = ""
    Trecho_Puntualidad = 0
    Trecho_Frecuencia = 0
    Trecho_Sinoptico = 0
    #Trazados = ""

    def __init__(self):

        try:

            self.Trecho_Id = 0
            self.Trecho_Desc = ""
            self.Trecho_Origen_Id = 0
            self.Trecho_Origen_Desc = ""
            self.Trecho_Destino_id = 0
            self.Trecho_Destino_Desc = ""
            self.Trecho_Puntualidad = 0
            self.Trecho_Frecuencia = 0
            self.Trecho_Sinoptico = 0
            
        except Exception as ex:
            print(str(ex))



