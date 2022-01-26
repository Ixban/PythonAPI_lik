from Librerias.Clases.Trechos import Trechos


class Trazados():

    Trazado_Id = 0
    Trazado_Color = ""
    Trazado_Version = 0
    Trazado_Desc = ""
    Trazado_Origen_Id = 0
    Trazado_Origen_Desc = ""
    Trazado_Destino_id = 0
    Trazado_Destino_Desc = ""
    #Coordenadas = ""
    #def __init__(self,Trechos):
    def __init__(self):

        try:

            #Trechos.__init__(self.Trazado_Id, self.Trazado_Color, self.Trazado_Version, self.Trazado_Desc, self.Trazado_Origen_Id, self.Trazado_Origen_Desc, self.Trazado_Destino_id, self.Trazado_Destino_Desc)
            #Trechos.__init__(self,Trechos.Trecho_Id, Trechos.Trecho_Desc, Trechos.Trecho_Origen_Id, Trechos.Trecho_Origen_Desc, Trechos.Trecho_Destino_id, Trechos.Trecho_Destino_Desc, Trechos.Trecho_Puntualidad, Trechos.Trecho_Frecuencia, self.Trazado_Id, self.Trazado_Color, self.Trazado_Version, self.Trazado_Desc, self.Trazado_Origen_Id, self.Trazado_Origen_Desc, self.Trazado_Destino_id, self.Trazado_Destino_Desc)

            self.Trazado_Id = 0
            self.Trazado_Color = ""
            self.Trazado_Version = 0
            self.Trazado_Desc = ""
            self.Trazado_Origen_Id = 0
            self.Trazado_Origen_Desc = ""
            self.Trazado_Destino_id = 0
            self.Trazado_Destino_Desc = ""
            #self.Coordenadas = ""
        except Exception as ex:
            print(str(ex))