class Viaje:
    
    Autobus: 0
    Puntualidad: 0
    Frecuencia_Atras: 0
    Frecuencia_Adelante: 0
    Velocidad: 0
    Kilometros_Recorridos: 0
    Clave_Conductor: 0
    Conductor: ""
    Ruta: ""
    Origen_Id: 0
    Origen_Desc: ""
    Destino_Id: 0
    Destino_Desc: ""
    Fecha_Salida_Programada: ""
    Fecha_Salida_Real: ""
    Fecha_Llegada_Programada: ""
    Fecha_Llegada_Real: ""
    Estatus: ""
    Estatus_Id: 0
    Fecha_Ultima_Actualizacion: ""
    Ultima_Alerta: ""
    Siguiente_Parada_Id: 0
    Siguiente_Parada_Desc: ""
    Fecha_Siguiente_Parada: ""
    Latitud: 0
    Longitud: 0
    Trecho_Porcentaje: 0
    Viaje_Porcentaje: 0
    Trecho_Id: 0
    Trazado_Id: 0

    def __init__(self):

        try:
            
            self.Autobus: 0
            self.Puntualidad: 0
            self.Frecuencia_Atras: 0
            self.Frecuencia_Adelante: 0
            self.Velocidad: 0
            self.Kilometros_Recorridos: 0
            self.Clave_Conductor: 0
            self.Conductor: ""
            self.Ruta: ""
            self.Origen_Id: 0
            self.Origen_Desc: ""
            self.Destino_Id: 0
            self.Destino_Desc: ""
            self.Fecha_Salida_Programada: ""
            self.Fecha_Salida_Real: ""
            self.Fecha_Llegada_Programada: ""
            self.Fecha_Llegada_Real: ""
            self.Estatus: ""
            self.Estatus_Id: 0
            self.Fecha_Ultima_Actualizacion: ""
            self.Ultima_Alerta: ""
            self.Siguiente_Parada_Id: 0
            self.Siguiente_Parada_Desc: ""
            self.Fecha_Siguiente_Parada: ""
            self.Latitud: 0
            self.Longitud: 0
            self.Trecho_Porcentaje: 0
            self.Viaje_Porcentaje: 0
            self.Trecho_Id: 0
            self.Trazado_Id: 0

        except Exception as ex:
            print(str(ex))
