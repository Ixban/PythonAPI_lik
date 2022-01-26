class Mensajes:
    
    AUTOBUS = 0
    MSJ = "NONE"
    ESTADO = 0
    ENVIADO = "NONE"
    ENTREGADO = "NONE"
    TRECHO_ACTUAL_ID = 0
    TO_AUTOBUS = 0

    def __init__(self):

        try:
            
            self.AUTOBUS = 0
            self.MSJ = ""
            self.ESTADO = 0
            self.ENVIADO = ""
            self.ENTREGADO = ""
            self.TRECHO_ACTUAL_ID = 0
            self.TO_AUTOBUS = 0

        except Exception as ex:
            print(str(ex))
