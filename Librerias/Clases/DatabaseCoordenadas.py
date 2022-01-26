from Almacenamiento import init_db, end_db, db_session, Ejecutor
from Almacenamiento import Tablas

import Librerias.Clases.ViajesPosicion as ViajesPos
import Librerias.Clases.ViajeTrecho as ViajesTre
import Librerias.Clases.Ruta as RutaC
import Librerias.Clases.MultiRuta_Ruta as MultiRutaRuta
import Librerias.Clases.ParadaPoligono as Parada_Poligono_C
import Librerias.Clases.SinopticoEC as SinocticoEC
import Librerias.Clases.Proporcion as Proporcion
import Librerias.Clases.Mensajes as msj
import Librerias.Clases.SinopticoResumen as SP
import Librerias.Clases.Trechos as Trechos_Class

import Librerias.Clases.Coordenadas as CoordenadasClass

from sqlalchemy import text
from datetime import date, timedelta, datetime
import datetime 
import traceback
from statistics import mode

import pytz

def coordenadas_example():
    #init_db()
    misParadas= Tablas.Parada.query_all({})
    for parada in misParadas:
        print(parada)
        misVertices = Tablas.Parada_Poligono.query_all({"PARADA_ID": parada.ID})

        for vertice in misVertices:
            print(vertice)

    #end_db()

#Func
def getSinopticossql():
    
    Sinoptics = []
    sql = ''
    try:
        
        Sinoptics = db_session.query(Tablas.Multiruta.ID,
                                    Tablas.Multiruta.NAME,
                                    Tablas.Multiruta.ACTIVE,
                                    Tablas.Multiruta.COLOR_ID
	    				        ).\
								filter(Tablas.Multiruta.ACTIVE == 1).all()
  
        # sql  = text("SELECT ID, NAME, ACTIVE, COLOR_ID FROM MULTIRUTA WHERE ACTIVE = 1")
        # Sinoptics = Ejecutor.execute(sql)
        
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return Sinoptics

#GetSinopticos

def getSinopticos():
    
    Sinoptics = []
    sql = ''
    try:
        
        Sinoptics = db_session.query(Tablas.Multiruta.ID,
                                    Tablas.Multiruta.NAME,
                                    Tablas.Multiruta.ACTIVE,
                                    Tablas.Multiruta.COLOR_ID
	    				        ).\
								filter(Tablas.Multiruta.ACTIVE == 1).all()

    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return Sinoptics

#GetSinopticos

#GetSinopticos_MC

def getSinopticos_MC(ID):

    SinopticsM = []

    try:
        
        SinopticsM = db_session.query(Tablas.MultiRuta_Trecho.ID,
                                       Tablas.MultiRuta_Trecho.MULTIRUTA_ID,
                                       Tablas.MultiRuta_Trecho.TRECHO_ID
                                       ).\
                                       filter(Tablas.MultiRuta_Trecho.MULTIRUTA_ID == ID).all()

    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return SinopticsM

#GetSinopticos_MC

#GetRutas

def getRutas():
        
    Rutas = ""

    try:
        
        Rutas = db_session.query(Tablas.Ruta.ID,
                                     Tablas.Ruta.NAME,
                                     Tablas.Ruta.ACTIVE,
                                     Tablas.Ruta.COLOR_ID,
                                     Tablas.Ruta.PARADA_INI,
                                     Tablas.Ruta.PARADA_FIN,
                                     Tablas.Ruta.DISTANCIA,
                                     Tablas.Ruta.TIEMPO,
                                     Tablas.Ruta.ENTRENADO,
						        ).\
								filter(Tablas.Ruta.ACTIVE == 1).all()

    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return Rutas

#GetRutas

#GetTrechos

def getTrechos(ID):
        
    Trechos = ""

    try:

        Trechos = db_session.query(Tablas.Ruta_Trecho.ID,
                                     Tablas.Ruta_Trecho.RUTA_ID,
                                     Tablas.Ruta_Trecho.TRECHO_ID,
                                     Tablas.Ruta_Trecho.SEQUENCE
						        ).\
								filter(Tablas.Ruta_Trecho.RUTA_ID == ID).all()

    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return Trechos

#GetTrechos

#getSinopticos_ID_LIST

def getSinopticos_ID_LIST(ID):
        
    Sinoptics = ""

    try:
        sql = text(" SELECT DISTINCT MULTIRUTA_ID FROM RUTA_TRECHO AS A " +
                         " INNER JOIN MULTIRUTA_TRECHO AS B ON B.TRECHO_ID = A.TRECHO_ID " +
                         " WHERE A.RUTA_ID = " + str(ID) + " ")
        
        Sinoptics = Ejecutor.execute(sql)

    except Exception as ex:
        print("getSinopticos_ID" + str(ex))

    return Sinoptics

#getSinopticos_ID_LIST

#GetParadas

def GetParadas():
        
    parada = ""

    try:

        parada = db_session.query(Tablas.Parada.ID,
                                  Tablas.Parada.NAME,
                                  Tablas.Parada.ACTIVE,
                                  Tablas.Parada.COLOR_ID,
                                  Tablas.Parada.PARADA_TIPO_ID,
                                  Tablas.Parada.ZONA_HORARIA_ID,
                                  Tablas.Parada.CLAVE
						        ).\
								filter(Tablas.Parada.ACTIVE == 1).all()
        #active = 1
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return parada

#GetParadas

#GetParadasSingle

def GetParadasSingle(Sinoptico):
        
    parada = ""

    try:

        sql = text(" SELECT DISTINCT A.ID, A.NAME, A.ACTIVE, A.COLOR_ID, A.PARADA_TIPO_ID, A.ZONA_HORARIA_ID, A.CLAVE, E.MULTIRUTA_ID FROM PARADA AS A " +
                   " INNER JOIN RUTA_PARADA AS B ON B.PARADA_ID = A.ID " +
                   " INNER JOIN TRECHO AS C ON C.PARADA_INI = A.ID " +
                   " INNER JOIN TRECHO AS D ON D.PARADA_FIN = A.ID " +
                   " INNER JOIN MULTIRUTA_TRECHO AS E ON E.TRECHO_ID = C.ID " +
                   " WHERE E.MULTIRUTA_ID = "+ str(Sinoptico) + " ORDER BY A.ID ")
        
        parada = Ejecutor.execute(sql)
        #active = 1
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return parada

#GetParadasSingle


#GetParadaCoordenada

def GetParadacoordenada(ID):
        
    parada = ""

    try:

        parada = db_session.query(Tablas.Parada_Poligono.ID,
                                  Tablas.Parada_Poligono.PARADA_ID,
                                  Tablas.Parada_Poligono.SEQUENCE,
                                  Tablas.Parada_Poligono.ACTIVE,
                                  Tablas.Parada_Poligono.LATITUD,
                                  Tablas.Parada_Poligono.LONGITUD).\
								  filter(Tablas.Parada_Poligono.PARADA_ID == ID).\
                                  limit(1).all()
                                  
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return parada

#GetParadaCoordenada

#getRutasParada

def getRutasParada(ID):
    
    data = {}
    data["Rutas"] = []
    data["Trechos"] = []
    data['Sinopticos'] = []
    Query_In = ""

    try:

        try:
            lista = []
            sql = text('SELECT DISTINCT RUTA_ID FROM RUTA_PARADA WHERE PARADA_ID = ' + str(ID) + ' ')
            Rutas = Ejecutor.execute(sql)
            if Rutas != None:
                for r in Rutas:
                    lista.append(str(Rutas[r]['RUTA_ID']))
        
                #lista = list(dict.fromkeys(lista))

                for l in lista:
                    data["Rutas"].append(
                        {
                            'Ruta_Id': int(l)
                        }
                    )
        
                #Query_In = ','.join(map(str,lista))

        except Exception as ex:
            print(traceback.format_exc())
            print(str(ex))
        
        try:
            lista = []
            sql = text('SELECT DISTINCT ID FROM TRECHO WHERE  PARADA_INI = ' + str(ID) + ' OR PARADA_FIN = ' + str(ID) + ' ')
            Trechos = Ejecutor.execute(sql)

            if Trechos != None:
                for t in Trechos:
                    lista.append(Trechos[t]['ID'])
        
                lista = list(dict.fromkeys(lista))

                for l in lista:
                    data["Trechos"].append(
                        {
                            "Trecho_Id": int(l)
                        }
                    )
                    
                    Query_In = ','.join(map(str,lista))
                    
        except Exception as ex:
            print(traceback.format_exc())
            print(str(ex))

        try:
            lista = []
            if Query_In != '':
                #sql = text('SELECT DISTINCT MULTIRUTA_ID FROM MULTIRUTA_RUTA WHERE RUTA_ID IN (' + str(Query_In) +')')
                
                sql = text(' SELECT DISTINCT MULTIRUTA_TRECHO.MULTIRUTA_ID FROM MULTIRUTA_TRECHO ' +
                           ' WHERE MULTIRUTA_TRECHO.TRECHO_ID IN (' + str(Query_In) +')')
                
                Sinopticos = Ejecutor.execute(sql)
                if Sinopticos != None:
                    for s in Sinopticos:
                        lista.append(str(Sinopticos[s]['MULTIRUTA_ID']))

                    lista = list(dict.fromkeys(lista))

                    for l in lista:
                        data["Sinopticos"].append(
                            {
                                "Sinoptico_Id": int(l)
                            }
                        )
                        
        except Exception as ex:
            print(traceback.format_exc())
            print(str(ex))

    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))   

    return [data["Rutas"], data["Trechos"], data["Sinopticos"]]

#getRutasParada

#getCoordenadasSinoptico
def getCoordenadasSinopticoList():
    
    ParadasList = []
    Coordenadas = []
    sql = ""
    try:
        
        sql = text("SELECT DISTINCT PARADA_ID, ID, SEQUENCE, ACTIVE, LATITUD, LONGITUD FROM PARADA_POLIGONO WHERE SEQUENCE = 1")
        Coordenadas =  Ejecutor.execute(sql)
        
        if Coordenadas != None:
            for t in Coordenadas:
                objParada_Poligono = Parada_Poligono_C.Parada_Poligono()
                objParada_Poligono.ID =  Coordenadas[t]['ID']
                objParada_Poligono.PARADA_ID = Coordenadas[t]['PARADA_ID']
                objParada_Poligono.SEQUENCE =  Coordenadas[t]['SEQUENCE']
                objParada_Poligono.ACTIVE =  Coordenadas[t]['ACTIVE']
                objParada_Poligono.LATITUD =  Coordenadas[t]['LATITUD']
                objParada_Poligono.LONGITUD = Coordenadas[t]['LONGITUD']
                ParadasList.append(objParada_Poligono)
        
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return ParadasList 

#getCoordenadasSinoptico

#getCoordenadasSinoptico

def getCoordenadasSinoptico(ID):
    
    objParada_Poligono = Parada_Poligono_C.Parada_Poligono()

    Trechos = ""
    
    try:

        Trechos = db_session.query(Tablas.Parada_Poligono.ID,
                                  Tablas.Parada_Poligono.PARADA_ID,
                                  Tablas.Parada_Poligono.SEQUENCE,
                                  Tablas.Parada_Poligono.ACTIVE,
                                  Tablas.Parada_Poligono.LATITUD,
                                  Tablas.Parada_Poligono.LONGITUD).\
								  filter(Tablas.Parada_Poligono.PARADA_ID == ID).\
                                  limit(1).all()
        if Trechos != None:
            for t in Trechos:
                objParada_Poligono.ID = t.ID
                objParada_Poligono.PARADA_ID = t.PARADA_ID
                objParada_Poligono.SEQUENCE = t.SEQUENCE
                objParada_Poligono.ACTIVE = t.ACTIVE
                objParada_Poligono.LATITUD = t.LATITUD
                objParada_Poligono.LONGITUD = t.LONGITUD
                    
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return objParada_Poligono

#getCoordenadasSinoptico

#

def getCoordenadasSinopticoM(CoordenadaLIST, ID):
    
    objParada_Poligono = Parada_Poligono_C.Parada_Poligono()
    lista = []
    try:
        
        for t in CoordenadaLIST:
            if (t.PARADA_ID == ID):
                objParada_Poligono.PARADA_ID = t.PARADA_ID
                objParada_Poligono.SEQUENCE = t.SEQUENCE
                objParada_Poligono.ACTIVE = t.ACTIVE
                objParada_Poligono.LATITUD = t.LATITUD
                objParada_Poligono.LONGITUD = t.LONGITUD
                lista.append(objParada_Poligono)

    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return lista

def getCoordenadasSinopticoU(CoordenadaLIST, ID):
    
    objParada_Poligono = Parada_Poligono_C.Parada_Poligono()
    lista = []
    try:
        
        for t in CoordenadaLIST:
            if (t.PARADA_ID == ID):
                
                objParada_Poligono.ID = t.ID
                objParada_Poligono.PARADA_ID = t.PARADA_ID
                objParada_Poligono.SEQUENCE = t.SEQUENCE
                objParada_Poligono.ACTIVE = t.ACTIVE
                objParada_Poligono.LATITUD = t.LATITUD
                objParada_Poligono.LONGITUD = t.LONGITUD
                lista.append(objParada_Poligono)
                break

    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return objParada_Poligono

#

#GetDate

def GetDate():
        
    date_time = datetime.datetime.now()  - timedelta(hours= 5) 
    date_time_s = date_time.strftime("%m/%d/%Y, %H:%M:%S")

    return date_time_s

#GetDate

#GetMensajes

def GetMensajes():
    
    today = convertlocaldate(datetime.datetime.now() )
    Fecha = datetime.datetime.strptime(today, "%Y-%m-%d %H:%M:%S" )
    Fecha = Fecha.strftime("%Y/%m/%d")
    Fecha_I = str(Fecha) + " 00:00:00"
    Fecha_F = str(Fecha) + " 23:59:59"
    FechaIni = datetime.datetime.strptime(str(Fecha_I), '%Y/%m/%d %H:%M:%S')
    FechaFin = datetime.datetime.strptime(str(Fecha_F), '%Y/%m/%d %H:%M:%S')

    Bus = ""
    try:

        Bus = db_session.query(
            Tablas.Sae_Mensajes_Txt.PK_ID,
            Tablas.Sae_Mensajes_Txt.MSJ,
            Tablas.Sae_Mensajes_Txt.SENDER,
            Tablas.Sae_Mensajes_Txt.AUTOBUS,
            Tablas.Sae_Mensajes_Txt.ENVIADO,
            Tablas.Sae_Mensajes_Txt.ENTREGADO,
            Tablas.Sae_Mensajes_Txt.ESTADO,
            Tablas.Sae_Mensajes_Txt.TO_AUTOBUS,
            Tablas.Sae_Mensajes_Txt.ID_SUPLY).\
            filter(Tablas.Sae_Mensajes_Txt.ENVIADO > FechaIni,
				   Tablas.Sae_Mensajes_Txt.ENVIADO < FechaFin).all()

    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))


    return Bus

#GetMensajes

#GetSinoptico_Autobus

def GetSinoptico_Autobus(ID):
    
    Sinoptico = 1

    today = convertlocaldate(datetime.datetime.now() )
    Fecha = datetime.datetime.strptime(today, "%Y-%m-%d %H:%M:%S" )
    Fecha = Fecha.strftime("%Y/%m/%d")
    Fecha_I = str(Fecha) + " 00:00:00"
    Fecha_F = str(Fecha) + " 23:59:59"
    FechaIni = datetime.datetime.strptime(str(Fecha_I), '%Y/%m/%d %H:%M:%S')
    FechaFin = datetime.datetime.strptime(str(Fecha_F), '%Y/%m/%d %H:%M:%S')

    Viaje = ""

    try:
        Viaje = db_session.query(Tablas.Viaje.ID,
						        Tablas.Viaje.AUTOBUS_ID,
                                Tablas.Viaje.VIAJE_STATUS_ID,
                                Tablas.Viaje.ULTIMO_VIAJE_POSICION_ID).\
								filter(Tablas.Viaje.FECHA_HORA_PROGRAMADA_SALIDA > FechaIni,
								Tablas.Viaje.FECHA_HORA_PROGRAMADA_SALIDA < FechaFin,
                                Tablas.Viaje.VIAJE_STATUS_ID == 2,
                                Tablas.Viaje.AUTOBUS_ID == ID).\
                                limit(1).all()
                    #Tablas.Viaje.VIAJE_STATUS_ID == 2
                    #Tablas.Viaje.VIAJE_STATUS_ID == 2,
        Viaje_pos = ""

        Viaje_pos = db_session.query(Tablas.Viaje_Posicion.VIAJE_ID,
                                 Tablas.Viaje_Posicion.TRECHO_ACTUAL_ID,                                 
                                 Tablas.Viaje_Posicion.ULTIMO_EVENTO_ID).\
                                 filter(Tablas.Viaje_Posicion.ID == Viaje.ULTIMO_VIAJE_POSICION_ID).\
                                 limit(1).all()

        Sinoptico = getSinopticoTrechov2(Viaje_pos.TRECHO_ACTUAL_ID)

    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return Sinoptico

#GetSinoptico_Autobus

#GetParametros

def GetParametros():

    Parametros = ""

    try:

        sql = text('SELECT RTRIM(LLAVE) AS LLAVE, RTRIM(VALOR) AS VALOR, RTRIM(ACTIVE) AS ACTIVE' +
                   ' FROM SAE_PARAMETRO ' +
                   ' WHERE LLAVE LIKE ' + str("'gen%'") + ' AND ACTIVE = 1' )

        Parametros = Ejecutor.execute(sql)

    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return Parametros

#GetParametros

#getPlaneCEv2 

def getPlaneCEv2(X, Y):
    
    resolucion_X = int(X)
    resolucion_Y = int(Y)

    sinopticos = ""
    latitud = []
    longitud = []
    ListObject = []
    value = 0
    try:
        sql = text(' SELECT DISTINCT MULTIRUTA.ID  FROM MULTIRUTA  WHERE MULTIRUTA.ACTIVE = 1 ')

        sinopticos = Ejecutor.execute(sql)

        for tt in sinopticos:
            
            try:
            
                sql_trech = text('   SELECT DISTINCT TRECHO_TRAZADO.TRECHO_ID, TRAZADO.LATITUD, TRAZADO.LONGITUD ' +
                                 '   FROM TRECHO_TRAZADO ' +

                                 '   INNER JOIN TRAZADO on TRAZADO.TRECHO_TRAZADO_ID = TRECHO_TRAZADO.ID ' +
                                 '   INNER JOIN TRECHO ON TRECHO.ID = TRECHO_TRAZADO.TRECHO_ID ' +
                                 '   INNER JOIN MULTIRUTA_TRECHO ON MULTIRUTA_TRECHO.TRECHO_ID = TRECHO.ID ' +
                                 '   INNER JOIN MULTIRUTA ON MULTIRUTA.ID = MULTIRUTA_TRECHO.MULTIRUTA_ID ' +
                             
                                '   WHERE MULTIRUTA.ID = ' + str(sinopticos[tt]['ID']) + ' ')

                #print(str(sinopticos[tt]['ID']))
            
                coordenadas_fil = Ejecutor.execute(sql_trech)

                latitud = []
                longitud = []
                ##########
                if len(coordenadas_fil) > 0:
                    
                    for i in coordenadas_fil:
                
                        latitud.append( float(coordenadas_fil[i]['LATITUD']) )
                        longitud.append( float(coordenadas_fil[i]['LONGITUD']) )

                    latitud.sort()
                    longitud.sort()

                    latitud_min = float(latitud[0])
                    latitud_max = float(latitud[len(latitud) -1 ])

                    longitud_min = float(longitud[0])
                    longitud_max = float(longitud[len(longitud) -1])
                    
                else:
                    latitud_min = 0.1
                    latitud_max = 0.2

                    longitud_min = 0.1
                    longitud_max = 0.2
                    
                #############
                tam_lien_lat = latitud_max - latitud_min
                tam_lien_long = longitud_max - longitud_min

                proporcion_lat =  tam_lien_lat / resolucion_X
                proporcion_long = tam_lien_long / resolucion_Y

                if proporcion_long < 0.00016:
                    value = 1
                    
                obj_SEC = SinocticoEC.SinopticoEC()
                obj_SEC.sinoptico_id = int(sinopticos[tt]['ID'])
                obj_SEC.latitud_min = latitud_min
                obj_SEC.latitud_max = latitud_max
                obj_SEC.longitud_min = longitud_min
                obj_SEC.longitud_max = longitud_max
                obj_SEC.proporcion_lat = proporcion_lat
                obj_SEC.proporcion_long = proporcion_long
                obj_SEC.size = value
                ListObject.append(obj_SEC)
                
            except Exception as ex:
                print(traceback.format_exc())
                print(str(ex))

    except Exception as ex:
        print(str(ex))
        print(traceback.format_exc())
        

    return ListObject

#getPlaneCEv2 

#getViajesOpt

def getViajesOpt():
    
    # today = convertlocaldate(datetime.datetime.now() )
    # Fecha = datetime.datetime.strptime(today, "%Y-%m-%d %H:%M:%S" )
    # Fecha = Fecha.strftime("%Y/%m/%d")
    # Fecha_I = str(Fecha) + " 00:00:00"
    # Fecha_F = str(Fecha) + " 23:59:59"
    # FechaIni = datetime.datetime.strptime(str(Fecha_I), '%Y/%m/%d %H:%M:%S')
    # FechaFin = datetime.datetime.strptime(str(Fecha_F), '%Y/%m/%d %H:%M:%S')

    Viaje = []

    try:
        # Viaje = db_session.query(Tablas.Viaje.ID,
		# 				        Tablas.Viaje.RUTA_ID,
		# 				        Tablas.Viaje.AUTOBUS_ID,
		# 				        Tablas.Viaje.CONDUCTOR_ID,
		# 				        Tablas.Viaje.FECHA_HORA_PROGRAMADA_SALIDA,
		# 				        Tablas.Viaje.FECHA_HORA_REAL_SALIDA,
        #                         Tablas.Viaje.FECHA_HORA_PROGRAMADA_LLEGADA,
		# 				        Tablas.Viaje.FECHA_HORA_REAL_LLEGADA,
        #                         Tablas.Viaje.ERPCO_CORRIDA_ID,
        #                         Tablas.Viaje.VIAJE_STATUS_ID,
        #                         Tablas.Viaje.FECHA_ACTUALIZACION,
        #                         Tablas.Viaje.ULTIMO_VIAJE_POSICION_ID).\
		# 						filter(Tablas.Viaje.FECHA_HORA_PROGRAMADA_SALIDA > FechaIni,
		# 						Tablas.Viaje.FECHA_HORA_PROGRAMADA_SALIDA < FechaFin,
        #                         Tablas.Viaje.ULTIMO_VIAJE_POSICION_ID > 0,
        #                         Tablas.Viaje.VIAJE_STATUS_ID == 2).all()
        
        sql = text(" SELECT A.ID, A.RUTA_ID,  A.AUTOBUS_ID, A.CONDUCTOR_ID,  A.FECHA_HORA_PROGRAMADA_SALIDA,  A.FECHA_HORA_REAL_SALIDA, " +
                   " A.FECHA_HORA_PROGRAMADA_LLEGADA, A.FECHA_HORA_REAL_LLEGADA, A.ERPCO_CORRIDA_ID, A.VIAJE_STATUS_ID, A.FECHA_ACTUALIZACION, A.ULTIMO_VIAJE_POSICION_ID " +
                   
                   #" C.TRECHO_ACTUAL_ID, C.LATITUD, c.LONGITUD, C.PUNTUALIDAD, C.FRECUENCIA_ATRAS, C.FRECUENCIA_ADELANTE, C.VELOCIDAD, C.DISTANCIA, C.COLOR_PUNTUALIDAD, " +
                   #" C.COLOR_FRECUENCIA_ADELANTE, C.COLOR_FRECUENCIA_ATRAS, C.COLOR_STATUS, C.FECHA_HORA_GPS,C.PARADA_SIGUIENTE_ID,C.FECHA_HORA_SIGUIENTE_PARADA_ESTIMADA, " +
                   #" C.PORCENTAJE_AVANCE_TRECHO, C.PORCENTAJE_AVANCE_RUTA"
                   
                   " FROM VIAJE AS A " +
                   #" INNER JOIN RUTA AS B ON A.RUTA_ID = B.ID " +
	               #" LEFT JOIN VIAJE_POSICION AS C ON A.ULTIMO_VIAJE_POSICION_ID = C.ID " +
	               #" LEFT JOIN TRECHO AS D ON C.TRECHO_ACTUAL_ID = D.ID " +
	               " WHERE A.VIAJE_STATUS_ID = 2 " +
                   #" ORDER BY C.FECHA_HORA_GPS DESC , FECHA_HORA_PROGRAMADA_SALIDA DESC "
                   "" )
                   #" FROM VIAJE WHERE VIAJE.VIAJE_STATUS_ID = 2 AND VIAJE.FECHA_HORA_PROGRAMADA_SALIDA >= Convert(varchar, convert(varchar, getdate(), 23) + ' 00:00:00') AND FECHA_HORA_PROGRAMADA_SALIDA < Convert(varchar, convert(varchar, getdate(), 23) + ' 23:59:59') AND ULTIMO_VIAJE_POSICION_ID > 0" )
        
        Viaje = Ejecutor.execute(sql)
                    #,
                    #Tablas.Viaje.VIAJE_STATUS_ID == 2
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return Viaje

#getViajesOpt

#getViajesOpt

def getViajesOptSinoptico(Sinoptico):
    
    Viaje = []

    try:
        
        sql = text(" SELECT A.ID, A.RUTA_ID,  A.AUTOBUS_ID, A.CONDUCTOR_ID,  A.FECHA_HORA_PROGRAMADA_SALIDA,  A.FECHA_HORA_REAL_SALIDA, " +
                   " A.FECHA_HORA_PROGRAMADA_LLEGADA, A.FECHA_HORA_REAL_LLEGADA, A.ERPCO_CORRIDA_ID, A.VIAJE_STATUS_ID, A.FECHA_ACTUALIZACION, A.ULTIMO_VIAJE_POSICION_ID, " +
                   " B.VIAJE_ID,B.SEQUENCE, B.FECHA_HORA_PROCESAMIENTO, B.FECHA_HORA_GPS, B.VELOCIDAD, B.DISTANCIA, B.PORCENTAJE_AVANCE_RUTA, B.PORCENTAJE_AVANCE_TRECHO, " +
                   " B.LATITUD, B.LONGITUD, B.TRECHO_ANTERIOR_ID, B.TRECHO_ACTUAL_ID, B.TRECHO_SIGUIENTE_ID, B.PARADA_ANTERIOR_ID, B.PARADA_SIGUIENTE_ID, B.FECHA_HORA_SIGUIENTE_PARADA_ESTIMADA, B.ULTIMO_EVENTO_ID, " +
                   " B.PUNTUALIDAD, ISNULL(B.FRECUENCIA_ATRAS, 0) AS FRECUENCIA_ATRAS , ISNULL(B.FRECUENCIA_ADELANTE, 0) AS FRECUENCIA_ADELANTE , B.DISTANCIA_ATRAS, B.DISTANCIA_ADELANTE, B.VIAJE_ATRAS_ID, B.VIAJE_ADELANTE_ID, B.CLIMA_TIPO_ID, B.COLOR_PUNTUALIDAD," +
                   " B.COLOR_FRECUENCIA_ADELANTE, B.COLOR_FRECUENCIA_ATRAS, B.COLOR_STATUS, B.VIAJE_STATUS_RECORRIDO_ID, C.MULTIRUTA_ID" +                                     
                   " FROM VIAJE AS A " +
                   " INNER JOIN VIAJE_POSICION AS b ON B.ID = A.ULTIMO_VIAJE_POSICION_ID " +
                   " INNER JOIN MULTIRUTA_TRECHO AS C ON C.TRECHO_ID = B.TRECHO_ACTUAL_ID " +
                   " WHERE A.VIAJE_STATUS_ID = 2  AND C.MULTIRUTA_ID = " + str(Sinoptico) + " ORDER BY A.ID" +
                   "" )
                   
        Viaje = Ejecutor.execute(sql)
          
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return Viaje

#getViajesOptSingleSinoptico


#getViajePos

def getViajePos(ID):
    
    obj_ViajePos = ViajesPos.ViajesPosicion()

    try:
        ViajeC = db_session.query(Tablas.Viaje_Posicion.VIAJE_ID,
                                 Tablas.Viaje_Posicion.SEQUENCE,
                                 Tablas.Viaje_Posicion.FECHA_HORA_PROCESAMIENTO,
                                 Tablas.Viaje_Posicion.FECHA_HORA_GPS,
                                 Tablas.Viaje_Posicion.VELOCIDAD,
                                 Tablas.Viaje_Posicion.DISTANCIA,
                                 Tablas.Viaje_Posicion.PORCENTAJE_AVANCE_RUTA,
                                 Tablas.Viaje_Posicion.PORCENTAJE_AVANCE_TRECHO,
                                 Tablas.Viaje_Posicion.LATITUD,
                                 Tablas.Viaje_Posicion.LONGITUD,
                                 Tablas.Viaje_Posicion.TRECHO_ANTERIOR_ID,
                                 Tablas.Viaje_Posicion.TRECHO_ACTUAL_ID,
                                 Tablas.Viaje_Posicion.TRECHO_SIGUIENTE_ID,                                 
                                 Tablas.Viaje_Posicion.PARADA_ANTERIOR_ID,                                 
                                 Tablas.Viaje_Posicion.PARADA_SIGUIENTE_ID,                                 
                                 Tablas.Viaje_Posicion.FECHA_HORA_SIGUIENTE_PARADA_ESTIMADA,                                 
                                 Tablas.Viaje_Posicion.ULTIMO_EVENTO_ID,
                                 Tablas.Viaje_Posicion.PUNTUALIDAD,
                                 Tablas.Viaje_Posicion.FRECUENCIA_ATRAS,
                                 Tablas.Viaje_Posicion.FRECUENCIA_ADELANTE,
                                 Tablas.Viaje_Posicion.DISTANCIA_ATRAS,
                                 Tablas.Viaje_Posicion.DISTANCIA_ADELANTE,
                                 Tablas.Viaje_Posicion.VIAJE_ATRAS_ID,
                                 Tablas.Viaje_Posicion.VIAJE_ADELANTE_ID,
                                 Tablas.Viaje_Posicion.CLIMA_TIPO_ID,
                                 Tablas.Viaje_Posicion.COLOR_PUNTUALIDAD,
                                 Tablas.Viaje_Posicion.COLOR_FRECUENCIA_ADELANTE, 
                                 Tablas.Viaje_Posicion.COLOR_FRECUENCIA_ATRAS,
                                 Tablas.Viaje_Posicion.COLOR_STATUS,
                                 Tablas.Viaje_Posicion.VIAJE_STATUS_RECORRIDO_ID).\
                                 filter(Tablas.Viaje_Posicion.ID == ID).\
                                 limit(1).all()

        #Viaje = Tablas.Viaje_Posicion.query_one({"VIAJE_ID": str(ID)})
        #order_by(Tablas.Viaje_Posicion.FECHA_HORA_PROCESAMIENTO.desc()).\
        
        if ViajeC != None:
            for Viaje in ViajeC:
                if Viaje.VIAJE_ID != None:
                    obj_ViajePos.VIAJE_ID = Viaje.VIAJE_ID
            
                if Viaje.SEQUENCE != None:
                    obj_ViajePos.SEQUENCE = Viaje.SEQUENCE
            
                if Viaje.FECHA_HORA_PROCESAMIENTO != None:
                    obj_ViajePos.FECHA_HORA_PROCESAMIENTO = Viaje.FECHA_HORA_PROCESAMIENTO
            
                if Viaje.FECHA_HORA_GPS != None:
                    obj_ViajePos.FECHA_HORA_GPS = Viaje.FECHA_HORA_GPS
            
                if Viaje.VELOCIDAD != None:
                    obj_ViajePos.VELOCIDAD = Viaje.VELOCIDAD
            
                if Viaje.DISTANCIA != None:
                    obj_ViajePos.DISTANCIA = Viaje.DISTANCIA

                if Viaje.PORCENTAJE_AVANCE_RUTA != None:
                    obj_ViajePos.PORCENTAJE_AVANCE_RUTA = Viaje.PORCENTAJE_AVANCE_RUTA
            
                if Viaje.PORCENTAJE_AVANCE_TRECHO != None:
                    obj_ViajePos.PORCENTAJE_AVANCE_TRECHO = Viaje.PORCENTAJE_AVANCE_TRECHO
            
                if Viaje.LATITUD != None:
                    obj_ViajePos.LATITUD = Viaje.LATITUD
            
                if Viaje.LONGITUD != None:
                    obj_ViajePos.LONGITUD = Viaje.LONGITUD
            
                if Viaje.TRECHO_ANTERIOR_ID != None:
                    obj_ViajePos.TRECHO_ANTERIOR_ID = Viaje.TRECHO_ANTERIOR_ID

                if Viaje.TRECHO_ACTUAL_ID != None:
                    obj_ViajePos.TRECHO_ACTUAL_ID = Viaje.TRECHO_ACTUAL_ID
                    #print("Set Viaje.TRECHO_ACTUAL_ID:" + str(Viaje.TRECHO_ACTUAL_ID))
            
                if Viaje.TRECHO_SIGUIENTE_ID != None:
                    obj_ViajePos.TRECHO_SIGUIENTE_ID = Viaje.TRECHO_SIGUIENTE_ID
            
                if Viaje.PARADA_ANTERIOR_ID != None:
                    obj_ViajePos.PARADA_ANTERIOR_ID = Viaje.PARADA_ANTERIOR_ID
            
                if Viaje.PARADA_SIGUIENTE_ID != None:
                    obj_ViajePos.PARADA_SIGUIENTE_ID = Viaje.PARADA_SIGUIENTE_ID

                if Viaje.FECHA_HORA_SIGUIENTE_PARADA_ESTIMADA != None:
                    obj_ViajePos.FECHA_HORA_SIGUIENTE_PARADA_ESTIMADA = Viaje.FECHA_HORA_SIGUIENTE_PARADA_ESTIMADA
            
                if Viaje.ULTIMO_EVENTO_ID != None:
                    obj_ViajePos.ULTIMO_EVENTO_ID = Viaje.ULTIMO_EVENTO_ID
            
                if Viaje.PUNTUALIDAD != None:
                    obj_ViajePos.PUNTUALIDAD = Viaje.PUNTUALIDAD

                if Viaje.FRECUENCIA_ATRAS != None:
                    obj_ViajePos.FRECUENCIA_ATRAS = Viaje.FRECUENCIA_ATRAS
            
                if Viaje.FRECUENCIA_ADELANTE != None:
                    obj_ViajePos.FRECUENCIA_ADELANTE = Viaje.FRECUENCIA_ADELANTE
            
                if Viaje.DISTANCIA_ATRAS != None:
                    obj_ViajePos.DISTANCIA_ATRAS = Viaje.DISTANCIA_ATRAS
            
                if Viaje.DISTANCIA_ADELANTE != None:
                    obj_ViajePos.DISTANCIA_ADELANTE = Viaje.DISTANCIA_ADELANTE
            
                if Viaje.VIAJE_ATRAS_ID != None:
                    obj_ViajePos.VIAJE_ATRAS_ID = Viaje.VIAJE_ATRAS_ID
            
                if Viaje.VIAJE_ADELANTE_ID != None:
                    obj_ViajePos.VIAJE_ADELANTE_ID = Viaje.VIAJE_ADELANTE_ID
            
                if Viaje.CLIMA_TIPO_ID != None:
                    obj_ViajePos.CLIMA_TIPO_ID = Viaje.CLIMA_TIPO_ID

                if Viaje.COLOR_PUNTUALIDAD != None:
                    obj_ViajePos.COLOR_PUNTUALIDAD = Viaje.COLOR_PUNTUALIDAD

                if Viaje.COLOR_FRECUENCIA_ADELANTE != None:
                    obj_ViajePos.COLOR_FRECUENCIA_ADELANTE = Viaje.COLOR_FRECUENCIA_ADELANTE

                if Viaje.COLOR_FRECUENCIA_ATRAS != None:
                    obj_ViajePos.COLOR_FRECUENCIA_ATRAS = Viaje.COLOR_FRECUENCIA_ATRAS

                if Viaje.COLOR_STATUS != None:
                    obj_ViajePos.COLOR_STATUS = Viaje.COLOR_STATUS

                if Viaje.VIAJE_STATUS_RECORRIDO_ID != None:
                    obj_ViajePos.VIAJE_STATUS_RECORRIDO_ID = Viaje.VIAJE_STATUS_RECORRIDO_ID

            #if Viaje.PUNTUALIDAD_PROGRAMADA != None:
            #    obj_ViajePos.PUNTUALIDAD_PROGRAMADA = Viaje.PUNTUALIDAD_PROGRAMADA
            
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))  

    return obj_ViajePos

#getViajePos

#getMensajesSQL

def getMensajesSQL():
    
    today = convertlocaldate(datetime.datetime.now() )
    Fecha = datetime.datetime.strptime(today, "%Y-%m-%d %H:%M:%S" )
    Fecha = Fecha.strftime("%Y-%m-%d")
    Fecha_I = str(Fecha) + "T00:00:00"
    Fecha_F = str(Fecha) + "T23:59:59"
    #FechaIni = datetime.datetime.strptime(str(Fecha_I), '%Y-%m-%d %H:%M:%S')
    #FechaFin = datetime.datetime.strptime(str(Fecha_F), '%Y-%m-%d %H:%M:%S')
    lista = []
    
    Mensaje = ""

    try:
        
        #sql = text(" SELECT SAE_MENSAJES_TXT.AUTOBUS,SAE_MENSAJES_TXT.TO_AUTOBUS, SAE_MENSAJES_TXT.MSJ, SAE_MENSAJES_TXT.ESTADO, SAE_MENSAJES_TXT.ENVIADO, " +

        #           " SAE_MENSAJES_TXT.ENTREGADO, VIAJE_POSICION.TRECHO_ACTUAL_ID FROM VIAJE " + 
        #           " INNER JOIN SAE_MENSAJES_TXT ON SAE_MENSAJES_TXT.AUTOBUS = VIAJE.AUTOBUS_ID " + 
        #           " INNER JOIN VIAJE_POSICION ON VIAJE_POSICION.ID = VIAJE.ULTIMO_VIAJE_POSICION_ID " +
        #           " WHERE SAE_MENSAJES_TXT.ENVIADO BETWEEN '" + str(Fecha_I) + "' AND '" + str(Fecha_F) + "' " + 
        #           " AND VIAJE.FECHA_HORA_PROGRAMADA_SALIDA BETWEEN '" + str(Fecha_I) + "' AND '" + str(Fecha_F) + "' "+
        #           " AND VIAJE.VIAJE_STATUS_ID = 2 ORDER BY SAE_MENSAJES_TXT.AUTOBUS" )
        

        #           " SAE_MENSAJES_TXT.ENTREGADO, VIAJE_POSICION.TRECHO_ACTUAL_ID FROM VIAJE " +
        #           " INNER JOIN SAE_MENSAJES_TXT ON SAE_MENSAJES_TXT.AUTOBUS = VIAJE.AUTOBUS_ID " +
        #           " INNER JOIN VIAJE_POSICION ON VIAJE_POSICION.ID = VIAJE.ULTIMO_VIAJE_POSICION_ID " +
        #           " WHERE SAE_MENSAJES_TXT.ENVIADO BETWEEN '" + str(Fecha_I) + "' AND '" + str(Fecha_F) + "' " +
        #           " AND VIAJE.FECHA_HORA_PROGRAMADA_SALIDA BETWEEN '" + str(Fecha_I) + "' AND '" + str(Fecha_F) + "' "+
        #           " AND VIAJE.VIAJE_STATUS_ID = 2 ORDER BY SAE_MENSAJES_TXT.AUTOBUS" )

        sql = text("select * from dbo.[FUN_MENSAJES]()")
        Mensaje = Ejecutor.execute(sql)

        if len(Mensaje) > 0:
            for MensajeItem in Mensaje:
                objMensaje = msj.Mensajes()
                objMensaje.AUTOBUS =  int(Mensaje[MensajeItem]['AUTOBUS'])
                objMensaje.MSJ =  str(Mensaje[MensajeItem]['MSJ'])
                objMensaje.ESTADO =  int(Mensaje[MensajeItem]['ESTADO'])
                objMensaje.ENVIADO =  str(Mensaje[MensajeItem]['ENVIADO'])
                objMensaje.ENTREGADO =  str(Mensaje[MensajeItem]['ENTREGADO'])
                objMensaje.TRECHO_ACTUAL_ID =  int(Mensaje[MensajeItem]['TRECHO_ACTUAL_ID'])
                objMensaje.TO_AUTOBUS = int(Mensaje[MensajeItem]['TO_AUTOBUS'])
                lista.append(objMensaje)    

    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    
    return lista

#getMensajesSQL

#getColorTrecho

def getColorTrecho(ID):

    Color_Trecho = "#000000"
    today = convertlocaldate(datetime.datetime.now() )
    Fecha = datetime.datetime.strptime(today, "%Y-%m-%d %H:%M:%S" )
    Fecha = Fecha.strftime("%Y/%m/%d")
    Fecha_I = str(Fecha) + " 00:00:00"
    Fecha_F = str(Fecha) + " 23:59:59"
    FechaIni = datetime.datetime.strptime(str(Fecha_I), '%Y/%m/%d %H:%M:%S')
    FechaFin = datetime.datetime.strptime(str(Fecha_F), '%Y/%m/%d %H:%M:%S')

    Viaje = ""
    List = []
    try:

        sql = text(" select D.ID AS TRECHO_ID,D.NAME ,C.COLOR_FRECUENCIA_ADELANTE ,COUNT(*) AS TOTAL_REGISTROS " +
                   " FROM VIAJE AS A " +
	        
                   " INNER JOIN RUTA AS B ON A.RUTA_ID = B.ID " +
	               " INNER JOIN VIAJE_POSICION AS C ON A.ULTIMO_VIAJE_POSICION_ID = C.ID " +
	               " INNER join TRECHO AS D ON C.TRECHO_ACTUAL_ID = D.ID	 " +
    
                   " WHERE A.VIAJE_STATUS_ID =2  " +
	               " AND C.COLOR_FRECUENCIA_ADELANTE IS NOT NULL " +
	               " AND D.ID= " + str(ID) + "   " +
                   " GROUP BY " + 
	               " D.ID  " +
	               " ,D.NAME " +
	               " ,C.COLOR_FRECUENCIA_ADELANTE " +
                   " order by D.ID, TOTAL_REGISTROS desc ")
        #
        Viaje = Ejecutor.execute(sql)

        if len(Viaje) > 0:
            #Color_Trecho = GetSelectColor(str(Viaje['row1']['COLOR_FRECUENCIA_ADELANTE']).rstrip())
            Color_Trecho = "#000000"
        else:
            Color_Trecho = "#000000"
        
    except Exception as ex:
        Color_Trecho = "#000000"
        print(traceback.format_exc())
        print(str(ex))

    return Color_Trecho

#getColorTrecho

#getColorsList

def getColorsList():

    Color_Trecho = "#000000"
    today = convertlocaldate(datetime.datetime.now() )
    Fecha = datetime.datetime.strptime(today, "%Y-%m-%d %H:%M:%S" )
    Fecha = Fecha.strftime("%Y/%m/%d")
    Fecha_I = str(Fecha) + " 00:00:00"
    Fecha_F = str(Fecha) + " 23:59:59"
    FechaIni = datetime.datetime.strptime(str(Fecha_I), '%Y/%m/%d %H:%M:%S')
    FechaFin = datetime.datetime.strptime(str(Fecha_F), '%Y/%m/%d %H:%M:%S')

    Viaje = ""
    List = []
    try:

        sql = text(" select D.ID AS TRECHO_ID,D.NAME ,C.COLOR_FRECUENCIA_ADELANTE ,COUNT(*) AS TOTAL_REGISTROS " +
                   " FROM VIAJE AS A " +
	        
                   " INNER JOIN RUTA AS B ON A.RUTA_ID = B.ID " +
	               " INNER JOIN VIAJE_POSICION AS C ON A.ULTIMO_VIAJE_POSICION_ID = C.ID " +
	               " INNER join TRECHO AS D ON C.TRECHO_ACTUAL_ID = D.ID	 " +
    
                   " WHERE A.VIAJE_STATUS_ID =2  " +
	               " AND C.COLOR_FRECUENCIA_ADELANTE IS NOT NULL " +
                   " GROUP BY " + 
	               " D.ID  " +
	               " ,D.NAME " +
	               " ,C.COLOR_FRECUENCIA_ADELANTE " +
                   " order by D.ID, TOTAL_REGISTROS desc ")
        
        Color_Trecho = Ejecutor.execute(sql)
        
    except Exception as ex:
        Color_Trecho = []
        print(traceback.format_exc())
        print(str(ex))

    return Color_Trecho

#getColorsList

#getColorsList

def getColorTrechoList(List, ID):

    Color_Trecho = ""
    
    try:

        for i in List:
            if(List[i]["TRECHO_ID"] == ID):
                #Color_Trecho =  GetSelectColor(str(List[i]["COLOR_FRECUENCIA_ADELANTE"]))
                Color_Trecho = "#000000"

            
        if len(Color_Trecho) == 0:
            Color_Trecho = "#000000"
        
    except Exception as ex:
        Color_Trecho = "#000000"
        print(traceback.format_exc())
        print(str(ex))

    return Color_Trecho

#getColorTrechoList

#GetSelectColor

def GetSelectColor(color):

    if color == "V":
        return "#3AA935"

    if color == "R":
        return "#FF0000"

    if color == "A":
        return "#DFD220"

    if color == "N":
        return "#000000"

    if color == None:
        return "#000000"

    if color == "":
        return "#000000"   

#GetSelectColor

#getRuta

def getRuta(ID):
    
    obj_Ruta = RutaC.Ruta()
    r = "None"

    try:
        #Ruta = Tablas.Ruta.query_one({"ID": ID})
        r = db_session.query(Tablas.Ruta.ID,
                                 Tablas.Ruta.NAME,
                                 #Tablas.Ruta.ACTIVE,
                                 #Tablas.Ruta.COLOR_ID,
                                 #Tablas.Ruta.ACTIVE,
                                 Tablas.Ruta.PARADA_INI,
                                 Tablas.Ruta.PARADA_FIN,
                                 #Tablas.Ruta.DISTANCIA,
                                 #Tablas.Ruta.TIEMPO,
                                 #Tablas.Ruta.ENTRENADO
                                 ).\
                                 filter(Tablas.Ruta.ID == ID).\
                                 limit(1).all()
        if r != None:
            for Ruta in r:
                obj_Ruta.ID = Ruta.ID
                obj_Ruta.NAME = Ruta.NAME
                #obj_Ruta.ACTIVE = Ruta.ACTIVE
                #obj_Ruta.COLOR_ID = Ruta.COLOR_ID
                obj_Ruta.PARADA_INI = Ruta.PARADA_INI
                obj_Ruta.PARADA_FIN = Ruta.PARADA_FIN
                #obj_Ruta.DISTANCIA = Ruta.DISTANCIA
                #obj_Ruta.TIEMPO = Ruta.TIEMPO
                #obj_Ruta.ENTRENADO = Ruta.ENTRENADO

    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return obj_Ruta

#getRutaList

def getRutaList(List, ID):
    
    obj_Ruta = RutaC.Ruta()

    try:
        for r in List:
            if r.ID == ID:
                obj_Ruta.ID = r.ID
                obj_Ruta.NAME = r.NAME
                obj_Ruta.PARADA_INI = r.PARADA_INI
                obj_Ruta.PARADA_FIN = r.PARADA_FIN
                break

    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return obj_Ruta

#getRutaList

#getRuta

def GetRutaName(ID):
    
    obj_Ruta = RutaC.Ruta()
    r = "None"
    Name = "None"
    try:
        #Ruta = Tablas.Ruta.query_one({"ID": ID})
        r = db_session.query(Tablas.Ruta.NAME).\
                                 filter(Tablas.Ruta.ID == ID).\
                                 limit(1).all()
        if r != None:
            for Ruta in r:
                 Name = str(Ruta.NAME)
                

    except Exception as ex:
        Name = "None"
        print(traceback.format_exc())
        print(str(ex))

    return Name

#getRuta

#getTrecho

def getTrecho(ID):
    
    obj_ViajePos = ViajesTre.ViajesTrecho()

    Trecho = ""

    try:
        #Trecho = Tablas.Viaje_Trecho.query_one({"VIAJE_ID": ID})
        t = db_session.query(Tablas.Viaje_Trecho.ID,
                                 Tablas.Viaje_Trecho.VIAJE_ID,
                                 Tablas.Viaje_Trecho.TRECHO_ID,
                                 #Tablas.Viaje_Trecho.TRECHO_TRAZADO_ID,
                                 #Tablas.Viaje_Trecho.FECHA_HORA_PROGRAMADA_LLEGADA,
                                 #Tablas.Viaje_Trecho.FECHA_HORA_REAL_LLEGADA,
                                 #Tablas.Viaje_Trecho.FECHA_HORA_PROGRAMADA_SALIDA,
                                 #Tablas.Viaje_Trecho.FECHA_HORA_REAL_SALIDA
                                 ).\
                                 filter(Tablas.Viaje_Trecho.VIAJE_ID == ID).\
                                 limit(1).all()

        if t != None:
            for Trecho in t:
                if Trecho.VIAJE_ID != None:
                    obj_ViajePos.VIAJE_ID = Trecho.VIAJE_ID

                if Trecho.TRECHO_ID != None:
                    obj_ViajePos.TRECHO_ID = Trecho.TRECHO_ID

                #if Trecho.TRECHO_TRAZADO_ID != None:
                #    obj_ViajePos.TRECHO_TRAZADO_ID = Trecho.TRECHO_TRAZADO_ID

                #if Trecho.FECHA_HORA_PROGRAMADA_LLEGADA != None:
                #    obj_ViajePos.FECHA_HORA_PROGRAMADA_LLEGADA = Trecho.FECHA_HORA_PROGRAMADA_LLEGADA

                #if Trecho.FECHA_HORA_REAL_LLEGADA != None:
                #    obj_ViajePos.FECHA_HORA_REAL_LLEGADA = Trecho.FECHA_HORA_REAL_LLEGADA

                #if Trecho.FECHA_HORA_PROGRAMADA_SALIDA != None:
                #    obj_ViajePos.FECHA_HORA_PROGRAMADA_SALIDA = Trecho.FECHA_HORA_PROGRAMADA_SALIDA
                
                #if Trecho.FECHA_HORA_REAL_SALIDA != None:
                #    obj_ViajePos.FECHA_HORA_REAL_SALIDA = Trecho.FECHA_HORA_REAL_SALIDA

    except Exception as ex:
        print(str(ex))
        print(traceback.format_exc())
        obj_ViajePos = ViajesPos.ViajesPosicion()

    return obj_ViajePos

#getTrecho


#getTrecho

#getTrechoTrazado

def getTrazado_Trecho_Actual(ID):
    
    Trazado = []
    a = 0
    b = 0
    try:
        
        sql = text(' SELECT A.ID AS TRECHO_TRAZADO_ID, A.TRECHO_ID FROM TRECHO_TRAZADO AS A WHERE A.TRECHO_ID = ' + str(ID) + ' ')


        Trazado = Ejecutor.execute(sql)
        
        if len(Trazado) > 0:
            a = int(Trazado['row1']['TRECHO_TRAZADO_ID'])
            b = int(Trazado['row1']['TRECHO_ID'])


    except Exception as ex:
        
        InsertLog("Error: ",str(ex) + "1209")
        print("getSinopticoTrazado" + str(ex))

    #end_db()

    return [a,b]

#getSinopticoTrechov2


#getTrecho

#getSinopticoTrechov2

def getSinopticoTrechov2(ID):
    
    Sinoptico = []
    #init_db()
    try:
        
        sql = text(' SELECT DISTINCT TRECHO_TRAZADO.TRECHO_ID, MULTIRUTA_TRECHO.MULTIRUTA_ID AS ID ' +
                   ' FROM TRECHO_TRAZADO ' +
                   ' INNER JOIN TRECHO ON TRECHO.ID = TRECHO_TRAZADO.TRECHO_ID ' +
                   ' INNER JOIN RUTA_TRECHO ON RUTA_TRECHO.TRECHO_ID = TRECHO.ID ' +
                   ' INNER JOIN MULTIRUTA_TRECHO ON MULTIRUTA_TRECHO.TRECHO_ID = RUTA_TRECHO.TRECHO_ID ' +
                   ' INNER JOIN MULTIRUTA ON MULTIRUTA.ID = MULTIRUTA_TRECHO.MULTIRUTA_ID ' +
                   ' WHERE TRECHO.ID = ' + str(ID) + ' AND MULTIRUTA.ACTIVE = 1 ')


        sinopticos = Ejecutor.execute(sql)
        
        if len(sinopticos) > 0:
            #Sinoptico = int(sinopticos['row1']['ID'])
            for sip in sinopticos:
                
                num = int(sinopticos[sip]['ID'])
                
                if num not in Sinoptico:
                    Sinoptico.append(num)
        else:
            Sinoptico.append(int(1))

        if Sinoptico == "":
           #Sinoptico = 1
           Sinoptico.append(int(1))

    except Exception as ex:
        
        InsertLog("Error: ",str(ex) + "920")
        print("getSinopticoTrazado" + str(ex))

    #end_db()

    return Sinoptico

#getSinopticoTrechov2

#getSinopticoTrechoSingleActive

def getSinopticoTrechoSingleActive(ID):
    
    Sinoptico = []
    #init_db()
    try:
        
        sql = text(' SELECT DISTINCT MULTIRUTA_TRECHO.MULTIRUTA_ID AS ID ' +
                   ' FROM TRECHO_TRAZADO ' +
                   ' INNER JOIN TRECHO ON TRECHO.ID = TRECHO_TRAZADO.TRECHO_ID ' +
                   ' INNER JOIN MULTIRUTA_TRECHO ON MULTIRUTA_TRECHO.TRECHO_ID =  TRECHO.ID ' +
                   ' INNER JOIN MULTIRUTA ON MULTIRUTA.ID = MULTIRUTA_TRECHO.MULTIRUTA_ID ' +
				   ' WHERE MULTIRUTA.ACTIVE = 1 ' +
                   ' AND TRECHO.ID = ' + str(ID) + ' ')

        sinopticos = Ejecutor.execute(sql)
        
        if len(sinopticos) > 0:
            #Sinoptico = int(sinopticos['row1']['ID'])
            for sip in sinopticos:
                
                num = int(sinopticos[sip]['ID'])
                
                if num not in Sinoptico:
                    Sinoptico.append(num)

        else:
            Sinoptico.append(int(1))
            #Sinoptico = 1

        if Sinoptico == "":
           #Sinoptico = 1
           Sinoptico.append(int(1))

    except Exception as ex:
        
        InsertLog("Error: ",str(ex) + "920")
        print("getSinopticoTrazado" + str(ex))

    #end_db()

    return Sinoptico

#getSinopticoTrechoSingleActive


#getSinopticoTrechoSingle

def getSinopticoTrechoSingle(ID):
    
    Sinoptico = []
    #init_db()
    try:
        
        sql = text(' SELECT DISTINCT MULTIRUTA_TRECHO.MULTIRUTA_ID AS ID ' +
                   ' FROM TRECHO_TRAZADO ' +
                   ' INNER JOIN TRECHO ON TRECHO.ID = TRECHO_TRAZADO.TRECHO_ID ' +
                   ' INNER JOIN MULTIRUTA_TRECHO ON MULTIRUTA_TRECHO.TRECHO_ID =  TRECHO.ID ' +
                   ' WHERE TRECHO.ID = ' + str(ID) + ' ')

        sinopticos = Ejecutor.execute(sql)
        
        if len(sinopticos) > 0:
            #Sinoptico = int(sinopticos['row1']['ID'])
            for sip in sinopticos:
                Sinoptico.append(int(sinopticos[sip]['ID']))

        else:
            Sinoptico.append(int(1))
            #Sinoptico = 1

        if Sinoptico == "":
           #Sinoptico = 1
           Sinoptico.append(int(1))

    except Exception as ex:
        
        InsertLog("Error: ",str(ex) + "920")
        print("getSinopticoTrazado" + str(ex))

    #end_db()

    return Sinoptico

#getSinopticoTrechoSingle


#getSinopticoTrechoSingle

def getSinopticoTrechoSingleList(List,ID):
    
    Sinoptico = []
    #init_db()
    try:
        
        for i in List:
            if i.Trecho_Id == ID:
                Sinoptico.append(int(i.Trecho_Sinoptico))

    except Exception as ex:
        
        InsertLog("Error: ",str(ex) + "920")
        print("getSinopticoTrazado" + str(ex))

    #end_db()

    return Sinoptico

#getSinopticoTrechoSingle

#getCondutor

def getCondutor(ID):
    
    Conductor = ""
    NUMEMPLEADO = 00000

    try:
        #ConductorName = Tablas.Conductor.query_one({"NUMEMPLEADO": ID})
        ConductorName = db_session.query(Tablas.Conductor.ID,
                                 Tablas.Conductor.NAME,
                                 Tablas.Conductor.ACTIVE,
                                 Tablas.Conductor.NUMEMPLEADO).\
                                 filter(Tablas.Conductor.ID == ID).\
                                 limit(1).all()

        if ConductorName != None  or  len(ConductorName) > 0:
            
            for cn in ConductorName:
                if cn.NAME != None:
                    Conductor = cn.NAME
                else:
                    Conductor = 0
                    
                if cn.NUMEMPLEADO != None:
                    NUMEMPLEADO = int(str(cn.NUMEMPLEADO).rstrip())
                else:
                    NUMEMPLEADO = 0
                
        else:
            Conductor = "None"

    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))
        Conductor = "NONE"
        NUMEMPLEADO = 00000

    return [str(Conductor), int(NUMEMPLEADO)]

#getCondutor

#GetAllCondutorLIST

def GetAllCondutorLIST():
    
    Conductor = []
   
    try:
        #ConductorName = Tablas.Conductor.query_one({"NUMEMPLEADO": ID})
        ConductorName = db_session.query(Tablas.Conductor.ID,
                                         Tablas.Conductor.NAME,
                                         Tablas.Conductor.ACTIVE,
                                         Tablas.Conductor.NUMEMPLEADO).\
                                             filter(Tablas.Conductor.ACTIVE == 1).all()
        
        for i in ConductorName:
            Obj_Condutor = Tablas.Conductor()
            Obj_Condutor.ID = i.ID
            Obj_Condutor.NAME = i.NAME
            
            if i.NAME == "None"  or i.NAME == None:
                Obj_Condutor.NAME = "Sin Nombre"
                
            Obj_Condutor.ACTIVE = i.ACTIVE
            Obj_Condutor.NUMEMPLEADO = i.NUMEMPLEADO
            
            if i.NUMEMPLEADO == "None" or i.NUMEMPLEADO == None:
                Obj_Condutor.NUMEMPLEADO = "0"
                
            Conductor.append(Obj_Condutor)

    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return Conductor

#GetAllCondutorLIST

#getCondutorList

def getCondutorList(CondutorLIST, ID):
    
    Conductor = ""
    NUMEMPLEADO = 00000
   
    try:
        
        for i in CondutorLIST:
            if (i.ID == ID):
                Conductor = i.NAME.rstrip()
                NUMEMPLEADO = int(i.NUMEMPLEADO.rstrip())
                break

    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))
        Conductor = "NONE"
        NUMEMPLEADO = 00000

    return [str(Conductor), int(NUMEMPLEADO)]

#getCondutorList

#Parada_Origen_Desc

def Parada_Origen_Desc(ID):
    
    paradaDesc = ""
    
    try:
        #parada = Tablas.Parada.query_one({"ID": ID})
        parada= db_session.query(Tablas.Parada.ID,
                                 Tablas.Parada.NAME,
                                 Tablas.Parada.ACTIVE,
                                 Tablas.Parada.COLOR_ID,
                                 Tablas.Parada.PARADA_TIPO_ID,
                                 Tablas.Parada.ZONA_HORARIA_ID).\
                                 filter(Tablas.Parada.ID == ID).\
                                 limit(1).all()

        if parada != None or  len(parada) >= 0:
            
            for cn in parada:
                paradaDesc = str(cn.NAME)
           
        else:
             paradaDesc = "None"

    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return str(paradaDesc)

#Parada_Origen_Desc

#Parada_Destino_Desc

def Parada_Destino_Desc(ID):
    
    paradaDesc = ""

    try:
        #parada = Tablas.Parada.query_one({"ID": ID})
        parada= db_session.query(Tablas.Parada.ID,
                                 Tablas.Parada.NAME,
                                 Tablas.Parada.ACTIVE,
                                 Tablas.Parada.COLOR_ID,
                                 Tablas.Parada.PARADA_TIPO_ID,
                                 Tablas.Parada.ZONA_HORARIA_ID).\
                                 filter(Tablas.Parada.ID == ID).\
                                 limit(1).all()

        if parada != None or  len(parada) >= 0:
            
            for cn in parada:
                paradaDesc = str(cn.NAME)
           
        else:
             paradaDesc = "None"

    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return str(paradaDesc)

#Parada_Destino_Desc

#SelectPametros

def SelectPametrosTop(parametros, json):

    Anterior = ""
    Parada = 5
    proximos = 0
    proximos_salida = 0

    try:

        if json == "paradas":
            for param in parametros:
                if parametros[param]['LLAVE'] == "gen-json-top-aut-ant":
                    Anterior = parametros[param]['VALOR']

                if parametros[param]['LLAVE'] == "gen-json-top-aut-par":
                    Parada = parametros[param]['VALOR']
                

                if parametros[param]['LLAVE'] == "gen-json-top-aut-prox":
                    proximos = parametros[param]['VALOR']
                    
                if parametros[param]['LLAVE'] == "gen-json-top-aut-prox-sal":
                    proximos_salida = parametros[param]['VALOR']


    except Exception as ex:
        print(str(ex))
        print(traceback.format_exc())
    
    return [Anterior , Parada, proximos, proximos_salida]

#SelectPametros


#SelectPametros

def SelectPametros(parametros, json):

    URL = ""
    SleepTime = 5
    Dimension_X = 0
    Dimension_Y = 0
    Sangria_X = 80
    Sangria_Y = 80
    Sangria_M_Y = 80
    active_sim = 0
    try:
        
        
        
        if json == "sinoptico_resumen":
            for param in parametros:
                if parametros[param]['LLAVE'] == "gen-json-nodejs-url":
                    URL = parametros[param]['VALOR']
        
        if json == "sinoptico_eventos":
            for param in parametros:
                if parametros[param]['LLAVE'] == "gen-json-nodejs-url":
                    URL = parametros[param]['VALOR']
                    
        if json == "sinoptico":
            for param in parametros:
                if parametros[param]['LLAVE'] == "gen-json-nodejs-url":
                    URL = parametros[param]['VALOR']

        if json == "rutas":
            for param in parametros:
                if parametros[param]['LLAVE'] == "gen-json-nodejs-url":
                    URL = parametros[param]['VALOR']

        if json == "paradas":
            for param in parametros:
                if parametros[param]['LLAVE'] == "gen-json-nodejs-url":
                    URL = parametros[param]['VALOR']

                if parametros[param]['LLAVE'] == "gen-json-res-max-x":
                    Dimension_X = parametros[param]['VALOR']
                

                if parametros[param]['LLAVE'] == "gen-json-res-max-y":
                    Dimension_Y = parametros[param]['VALOR']
                
                if parametros[param]['LLAVE'] == "gen-json-san-max-x":
                    Sangria_X = int(parametros[param]['VALOR'])
                    
                if parametros[param]['LLAVE'] == "gen-json-san-max-y":
                    Sangria_Y = int(parametros[param]['VALOR'])
                
                if parametros[param]['LLAVE'] == "gen-json-san-min-y":
                    Sangria_M_Y = int(parametros[param]['VALOR'])

        if json == "mensajes":
            for param in parametros:
                if parametros[param]['LLAVE'] == "gen-json-nodejs-url":
                    URL = parametros[param]['VALOR']

        if json == "viajes":
            for param in parametros:
                if parametros[param]['LLAVE'] == "gen-json-nodejs-url":
                    URL = parametros[param]['VALOR']
            
                if parametros[param]['LLAVE'] == "gen-json-envio-viajes-sleep-time-secs":
                    SleepTime = int(parametros[param]['VALOR'])

                if parametros[param]['LLAVE'] == "gen-json-res-max-x":
                    Dimension_X = parametros[param]['VALOR']

                if parametros[param]['LLAVE'] == "gen-json-res-max-y":
                    Dimension_Y = parametros[param]['VALOR']
                    
                if parametros[param]['LLAVE'] == "gen-json-san-max-x":
                    Sangria_X = int(parametros[param]['VALOR'])
                    
                if parametros[param]['LLAVE'] == "gen-json-san-max-y":
                    Sangria_Y = int(parametros[param]['VALOR'])
                
                if parametros[param]['LLAVE'] == "gen-json-san-min-y":
                    Sangria_M_Y = int(parametros[param]['VALOR'])
                    
                if parametros[param]['LLAVE'] == "gen-json-sim-active":
                    active_sim = int(parametros[param]['VALOR'])

        if json == "trazados":
            for param in parametros:
                if parametros[param]['LLAVE'] == "gen-json-nodejs-url":
                    URL = parametros[param]['VALOR']

                if parametros[param]['LLAVE'] == "gen-json-res-max-x":
                    Dimension_X = parametros[param]['VALOR']

                if parametros[param]['LLAVE'] == "gen-json-res-max-y":
                    Dimension_Y = parametros[param]['VALOR']
                
                if parametros[param]['LLAVE'] == "gen-json-san-max-x":
                    Sangria_X = int(parametros[param]['VALOR'])
                    
                if parametros[param]['LLAVE'] == "gen-json-san-max-y":
                    Sangria_Y = int(parametros[param]['VALOR'])
                
                if parametros[param]['LLAVE'] == "gen-json-san-min-y":
                    Sangria_M_Y = int(parametros[param]['VALOR'])

        if json == "devtest":
            for param in parametros:
                if parametros[param]['LLAVE'] == "gen-json-nodejs-url":
                    URL = parametros[param]['VALOR']

    except Exception as ex:
        print(str(ex))
        print(traceback.format_exc())
    
    return [URL , SleepTime, Dimension_X, Dimension_Y, Sangria_X, Sangria_Y, Sangria_M_Y, active_sim]

#SelectPametros

#coordenadas_trechos

def coordenadas_trechos():
    
    Trechos = []

    try:
        #Trechos = Tablas.Trecho.query_all({})
        # Trechos =db_session.query(Tablas.Trecho.ID,
        #                          Tablas.Trecho.NAME,
        #                          Tablas.Trecho.ACTIVE,
        #                          Tablas.Trecho.COLOR_ID,
        #                          Tablas.Trecho.PARADA_INI,
        #                          Tablas.Trecho.PARADA_FIN,
        #                          Tablas.Trecho.TRECHO_TIPO_ID,
        #                          Tablas.Trecho.ENTRENADO).\
        #                          filter(Tablas.Trecho.ACTIVE == 1, Tablas.Trecho.ENTRENADO == 1).all()
        
        sql = text(" SELECT DISTINCT TRECHO.ID, TRECHO.NAME, TRECHO.ACTIVE, TRECHO.COLOR_ID, TRECHO.PARADA_INI, TRECHO.PARADA_FIN, TRECHO.TRECHO_TIPO_ID , ENTRENADO FROM TRECHO INNER JOIN RUTA_TRECHO ON RUTA_TRECHO.TRECHO_ID = TRECHO.ID  " +
              " INNER JOIN MULTIRUTA_TRECHO ON MULTIRUTA_TRECHO.TRECHO_ID = RUTA_TRECHO.TRECHO_ID  " +
              " INNER JOIN MULTIRUTA ON MULTIRUTA.ID = MULTIRUTA_TRECHO.MULTIRUTA_ID  " +
              " WHERE MULTIRUTA.ACTIVE = 1 AND TRECHO.ENTRENADO = 1 AND TRECHO.ACTIVE = 1 ORDER BY TRECHO.ID ")
        
        Trechos = Ejecutor.execute(sql)
         
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return Trechos

#coordenadas_trechos


#coordenadas_trechos

def coordenadas_trechos_s(Id):
    
    Trechos = []

    try:
        #Trechos = Tablas.Trecho.query_all({})
        # Trechos =db_session.query(Tablas.Trecho.ID,
        #                          Tablas.Trecho.NAME,
        #                          Tablas.Trecho.ACTIVE,
        #                          Tablas.Trecho.COLOR_ID,
        #                          Tablas.Trecho.PARADA_INI,
        #                          Tablas.Trecho.PARADA_FIN,
        #                          Tablas.Trecho.TRECHO_TIPO_ID,
        #                          Tablas.Trecho.ENTRENADO).\
        #                          filter(Tablas.Trecho.ACTIVE == 1, Tablas.Trecho.ENTRENADO == 1).all()
        
        sql = text(" SELECT DISTINCT TRECHO.ID, TRECHO.NAME, TRECHO.ACTIVE, TRECHO.COLOR_ID, TRECHO.PARADA_INI, TRECHO.PARADA_FIN, TRECHO.TRECHO_TIPO_ID , ENTRENADO FROM TRECHO INNER JOIN RUTA_TRECHO ON RUTA_TRECHO.TRECHO_ID = TRECHO.ID  " +
              " INNER JOIN MULTIRUTA_TRECHO ON MULTIRUTA_TRECHO.TRECHO_ID = RUTA_TRECHO.TRECHO_ID  " +
              " INNER JOIN MULTIRUTA ON MULTIRUTA.ID = MULTIRUTA_TRECHO.MULTIRUTA_ID  " +
              " WHERE MULTIRUTA.ACTIVE = 1 AND TRECHO.ENTRENADO = 1 AND TRECHO.ACTIVE = 1 AND MULTIRUTA.ID = " + str(Id) +"   ORDER BY TRECHO.ID ")
        
        Trechos = Ejecutor.execute(sql)
         
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return Trechos

#coordenadas_trechos

#getSinopticoTrazadov2

def getSinopticoTrazadov2(ID):
    
    Sinoptico = []
    #init_db()
    try:

        sql = text(' SELECT DISTINCT TRECHO_TRAZADO.TRECHO_ID, MULTIRUTA.ID, TRECHO_TRAZADO.ID AS SINOPTICO_ID ' +
                   ' FROM TRECHO_TRAZADO  ' +
                   ' INNER JOIN TRECHO ON TRECHO.ID = TRECHO_TRAZADO.TRECHO_ID ' +
                   ' INNER JOIN RUTA_TRECHO ON RUTA_TRECHO.TRECHO_ID = TRECHO_TRAZADO.TRECHO_ID  ' +
                   ' INNER JOIN MULTIRUTA_TRECHO ON MULTIRUTA_TRECHO.TRECHO_ID = RUTA_TRECHO.TRECHO_ID  ' +
                   ' INNER JOIN MULTIRUTA ON MULTIRUTA.ID = MULTIRUTA_TRECHO.MULTIRUTA_ID  ' +
                   ' WHERE TRECHO_TRAZADO.ID =  ' + str(ID) + '  AND MULTIRUTA.ACTIVE = 1')

        sinopticos = Ejecutor.execute(sql)
        
        if len(sinopticos) > 0:
            for sip in sinopticos:
                Sinoptico.append(int(sinopticos[sip]['ID']))
                #Sinoptico.append(int(sinopticos['row1']['ID']))
                #break
        else:
            Sinoptico.append(int(0))

        if Sinoptico == "":
            Sinoptico.append(int(0))

    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    #end_db()

    return Sinoptico

#getSinopticoTrazadov2

#getSinopticoTrazadov2ALL

def getSinopticoTrazadov2ALL():
    
    Sinoptico = []
    #init_db()
    try:

        sql = text(' SELECT DISTINCT TRECHO_TRAZADO.TRECHO_ID, MULTIRUTA.ID AS SINIPTICO, TRECHO_TRAZADO.ID AS TRAZADO ' +
                   ' FROM TRECHO_TRAZADO  ' +
                   ' INNER JOIN TRECHO ON TRECHO.ID = TRECHO_TRAZADO.TRECHO_ID ' +
                   ' INNER JOIN RUTA_TRECHO ON RUTA_TRECHO.TRECHO_ID = TRECHO_TRAZADO.TRECHO_ID  ' +
                   ' INNER JOIN MULTIRUTA_TRECHO ON MULTIRUTA_TRECHO.TRECHO_ID = RUTA_TRECHO.TRECHO_ID  ' +
                   ' INNER JOIN MULTIRUTA ON MULTIRUTA.ID = MULTIRUTA_TRECHO.MULTIRUTA_ID  ' +
                   ' WHERE MULTIRUTA.ACTIVE = 1')

        sinopticos = Ejecutor.execute(sql)
        
        for s in sinopticos:
            objSinopticos = Trechos_Class.Trechos()
            objSinopticos.Trecho_Id = sinopticos[s]['TRAZADO']
            objSinopticos.Trecho_Sinoptico = sinopticos[s]['SINIPTICO']
            Sinoptico.append(objSinopticos)
        
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    #end_db()

    return Sinoptico

#getSinopticoTrazadov2ALL

#getAllTrechosMultiRuta

def getAllTrechosMultiRuta():
    
    Sinoptico = []
    #init_db()
    try:

        sql = text(' SELECT DISTINCT TRECHO.ID AS TRECHO_ID, MULTIRUTA_TRECHO.MULTIRUTA_ID AS ID ' +
                   ' FROM TRECHO_TRAZADO ' +
                   ' INNER JOIN TRECHO ON TRECHO.ID = TRECHO_TRAZADO.TRECHO_ID ' +
                   ' INNER JOIN MULTIRUTA_TRECHO ON MULTIRUTA_TRECHO.TRECHO_ID =  TRECHO.ID ' +
                   ' INNER JOIN MULTIRUTA ON MULTIRUTA.ID = MULTIRUTA_TRECHO.MULTIRUTA_ID ' +
				   ' WHERE MULTIRUTA.ACTIVE = 1 ' +
                   ' ORDER BY TRECHO.ID ')

        sinopticos = Ejecutor.execute(sql)
        
        for s in sinopticos:
            objSinopticos = Trechos_Class.Trechos()
            objSinopticos.Trecho_Id = sinopticos[s]['TRECHO_ID']
            objSinopticos.Trecho_Sinoptico = sinopticos[s]['ID']
            Sinoptico.append(objSinopticos)
        
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    #end_db()

    return Sinoptico

#getAllTrechosMultiRuta

def getSinopticoTrazadov2Trecho(SinopticosList, ID):
    Sinoptico = []
    
    for s in SinopticosList:
        if(s.Trecho_Id == ID):
                Sinoptico.append(int(s.Trecho_Sinoptico))
       
    if(len(Sinoptico) == 0 ):
          Sinoptico.append(0)

    return Sinoptico
#getAutobuses_Anteriores

def getAutobuses_Anteriores(ID, TOP, Sinoptico):

    today = convertlocaldate(datetime.datetime.now() )
    Fecha = datetime.datetime.strptime(today, "%Y-%m-%d %H:%M:%S" )
    Fecha = Fecha.strftime("%Y/%m/%d")
    Fecha_I = str(Fecha) + " 00:00:00"
    Fecha_F = str(Fecha) + " 23:59:59"
    
    autobus = []

    try:
        
        sql = text(" SELECT * from dbo.FUN_PUNTUALIDAD_PARADA(" + str(ID) + " , " + str(Sinoptico) + ", '" + str(Fecha_I) + "', '" + str(Fecha_F) + "' )")

        autobus = Ejecutor.execute(sql)
        
        
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    #end_db()

    return autobus

#getAutobuses_Anteriores

#getParadaFrecuencia

def getParadaFrecuencia(ID, TOP, Sinoptico):

    autobus = []
    value = 0
    
    try:
        
        sql = text(" SELECT [dbo].[FUN_PARADA_FRECUENCIA](" + str(Sinoptico) + ", " + str(ID) + ")")

        autobus = Ejecutor.execute(sql)
        
        value = autobus['row1']['']
        
            
        if value == "":
            value = 0
        
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    #end_db()

    return value

#getParadaFrecuencia

#getAutobuses_Parada

def getAutobuses_Parada(ID, TOP, Sinoptico):

    autobus = []

    try:
        
        sql = text(" SELECT * FROM dbo.[FUN_PARADAS_AUTOBUSES_EN](" + str(Sinoptico) + ", " + str(ID) + ")")

        autobus = Ejecutor.execute(sql)
        
        
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    #end_db()

    return autobus

#getAutobuses_Parada

#getAutobuses_Proximas

def getAutobuses_Proximas(ID, TOP, Sinoptico):

    autobus = []

    try:

        sql = text("SELECT * FROM dbo.[FUN_PARADAS_PROXIMAS_LLEGADAS]("+ str(Sinoptico) +"," + str(ID) + ") ORDER BY ETA ASC")

        autobus = Ejecutor.execute(sql)
        
        
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    #end_db()

    return autobus

#getAutobuses_Proximas

#getAutobuses_Proximas_Salidas

def getAutobuses_Proximas_Salidas(ID, TOP, Sinoptico):

    autobus = []
    
    try:
        
        sql = text(" SELECT * FROM dbo.[FUN_PARADAS_PROXIMAS_SALIDAS_TERMINAL](" + str(Sinoptico) + "," + str(ID) + ") ")

        autobus = Ejecutor.execute(sql)
        
        
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    #end_db()

    return autobus

#getAutobuses_Proximas_Salidas

#getTrazados

def getTrazados(ID):
    
    #init_db()
    trazados = []
    lista = []
    try:
        #trazados = Tablas.Trecho_Trazado.query_all({"TRECHO_ID": ID})
        sql = text("SELECT MAX(PRIORIDAD) AS PRIORIDAD FROM TRECHO_TRAZADO WHERE TRECHO_TRAZADO.TRECHO_ID = " + str(ID) +" ")

        Prioridad = Ejecutor.execute(sql)
        
        Condicion = Prioridad['row1']['PRIORIDAD']
        
        if Condicion != None:
            value = 0
        
            if Prioridad != None:
                value = Prioridad['row1']['PRIORIDAD']
        
            else:
                value = 0
        
            sql = text ("SELECT ID, NAME, TRECHO_ID, PRIORIDAD, DISTANCIA, TIEMPO FROM TRECHO_TRAZADO WHERE TRECHO_ID = '" + str(ID) + "' AND prioridad >= '" + str(value) + "' AND ACTIVE = '1' " )
            trazados = Ejecutor.execute(sql)

            for i in trazados:
                obj_Trechos_Trazados = Tablas.Trecho_Trazado()
                obj_Trechos_Trazados.ID = trazados[i]["ID"]
                obj_Trechos_Trazados.NAME = trazados[i]["NAME"]
                obj_Trechos_Trazados.TRECHO_ID = trazados[i]["TRECHO_ID"]
                obj_Trechos_Trazados.PRIORIDAD = trazados[i]["PRIORIDAD"]
                obj_Trechos_Trazados.DISTANCIA = trazados[i]["DISTANCIA"]
                obj_Trechos_Trazados.TIEMPO = trazados[i]["TIEMPO"]
                lista.append(obj_Trechos_Trazados)
        else:
            print("Sin Información")
            
        
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))
        trazados = []

    #end_db()

    return lista

#getTrazados

#getTrazadosGetList

def getTrazadosGetList(Trechos):
    
    trazados = []
    lista = []
    
    try:
        for i in Trechos:
            sql = text("SELECT MAX(PRIORIDAD) AS PRIORIDAD FROM TRECHO_TRAZADO WHERE TRECHO_TRAZADO.TRECHO_ID = " + str(Trechos[i]['ID']) +" ")

            Prioridad = Ejecutor.execute(sql)
        
            Condicion = Prioridad['row1']['PRIORIDAD']
        
            if Condicion != None:
                value = 0
        
                if Prioridad != None:
                    value = Prioridad['row1']['PRIORIDAD']
        
                else:
                    value = 0

                sql = text ("SELECT ID, NAME, TRECHO_ID, PRIORIDAD, DISTANCIA, TIEMPO FROM TRECHO_TRAZADO WHERE ACTIVE = '1' AND TRECHO_TRAZADO.TRECHO_ID = " + str(Trechos[i]['ID']) +" ORDER BY TRECHO_ID, PRIORIDAD")
                trazados = Ejecutor.execute(sql)

                for i in trazados:
                        obj_Trechos_Trazados = Tablas.Trecho_Trazado()
                        obj_Trechos_Trazados.ID = trazados[i]["ID"]
                        obj_Trechos_Trazados.NAME = trazados[i]["NAME"]
                        obj_Trechos_Trazados.TRECHO_ID = trazados[i]["TRECHO_ID"]
                        obj_Trechos_Trazados.PRIORIDAD = trazados[i]["PRIORIDAD"]
                        obj_Trechos_Trazados.DISTANCIA = trazados[i]["DISTANCIA"]
                        obj_Trechos_Trazados.TIEMPO = trazados[i]["TIEMPO"]
                        lista.append(obj_Trechos_Trazados)
        
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))
        lista = []

    #end_db()

    return lista

#getTrazadosGetList

#getTrazadosList

def getTrazadosList(List, ID):
    
    #init_db()
    trazados = []
    trecho = int(ID)
    
    try:
        
        for i in List:
            if i.TRECHO_ID == trecho:     
                obj_Trechos_Trazados = Tablas.Trecho_Trazado()       
                obj_Trechos_Trazados.ID = i.ID
                obj_Trechos_Trazados.NAME = i.NAME
                obj_Trechos_Trazados.TRECHO_ID = i.TRECHO_ID
                obj_Trechos_Trazados.PRIORIDAD = i.PRIORIDAD
                obj_Trechos_Trazados.DISTANCIA = i.DISTANCIA
                obj_Trechos_Trazados.TIEMPO = i.TIEMPO
                trazados.append(obj_Trechos_Trazados)
        
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))
        trazados = []

    #end_db()

    return trazados

#getTrazadosList

#GetAutobusesProgramados

def GetAutobusesProgramados():
    Autobus = []
    today = convertlocaldate(datetime.datetime.now() )
    Fecha = datetime.datetime.strptime(today, "%Y-%m-%d %H:%M:%S" )
    FechaFin = datetime.datetime.strptime(Fecha, '%Y/%m/%d %H:%M:%S')
    
    try:
        #trazados = Tablas.Trecho_Trazado.query_all({"TRECHO_ID": ID})
        Autobus = db_session.query(Tablas.Viaje.AUTOBUS_ID).\
                                   filter(Tablas.Viaje.FECHA_HORA_REAL_SALIDA > FechaFin,
                                          Tablas.Viaje.VIAJE_STATUS_ID == 1).\
                                          limit(20).all()

                                 #Tablas.Trecho_Trazado.ACTIVE == 1,
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return Autobus

#GetAutobusesProgramados

#GetEventos

def GetEventos(ID):

    Eventos = []

    try:
        
        sql = text("  SELECT * FROM dbo.[FUN_EVENTOS](" + str(ID) + ") ")

        Eventos = Ejecutor.execute(sql)
        
        
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    #end_db()

    return Eventos

#GetEventos

#getViajesSinopticoR

def getViajesSinoptico(ID):
    
    #- timedelta(hours= 5) 
    today = convertlocaldate(datetime.datetime.now() )
    Fecha = datetime.datetime.strptime(today, "%Y-%m-%d %H:%M:%S" )
    Fecha = Fecha.strftime("%Y-%m-%d")
    Fecha_I = str(Fecha) + "T00:00:00"
    Fecha_F = str(Fecha) + "T23:59:59"

    Viaje = []
    objSinoptico_Resumen = None
    try:
            
        #programados
        
        sql = text("  SELECT * FROM dbo.[FUN_SINOPTICO_RESUMEN](" + str(ID) + ",'" + str(Fecha_I) + "','" + str(Fecha_F) + "')")
        
        Viaje = Ejecutor.execute(sql)
                    
        for v in Viaje:
            
            try:
                objSinoptico_Resumen = SP.SinopticoResumen()
                
                if Viaje[v]['VIAJES_PROGRAMADOS'] != None:
                    objSinoptico_Resumen.Viajes_Programados = Viaje[v]['VIAJES_PROGRAMADOS']
                
                if Viaje[v]['AUTOBUSES_PROGRAMADOS_EN_SINOPTICO'] != None:
                    objSinoptico_Resumen.Autobus_Programdos_Sinoptico = Viaje[v]['AUTOBUSES_PROGRAMADOS_EN_SINOPTICO']
                
                if Viaje[v]['AUTOBUSES_REALES_EN_SINOPTICO'] != None:
                    objSinoptico_Resumen.Autobus_Reales_Sinoptico = Viaje[v]['AUTOBUSES_REALES_EN_SINOPTICO']
                
                if Viaje[v]['AUTOBUSES_RETRASADOS_EN_SINOPTICO'] != None:
                    objSinoptico_Resumen.Autobus_Retrasados_Sinoptico = Viaje[v]['AUTOBUSES_RETRASADOS_EN_SINOPTICO']
                
                if Viaje[v]['AUTOBUSES_PUNTUALES_EN_SINOPTICO'] != None:
                    objSinoptico_Resumen.Autobus_Puntual_Sinoptico = Viaje[v]['AUTOBUSES_PUNTUALES_EN_SINOPTICO']
                
                if Viaje[v]['FRECUENCIA_PASO_EN_SINOPTICO'] != None:
                    objSinoptico_Resumen.Frecuencia_Paso_Sinoptico = Viaje[v]['FRECUENCIA_PASO_EN_SINOPTICO']
                
                if Viaje[v]['FRECUENCIA_SALIDA_EN_TERMINALES'] != None:
                    objSinoptico_Resumen.Frecuencia_Salida_Terminal = Viaje[v]['FRECUENCIA_SALIDA_EN_TERMINALES']
                
                if Viaje[v]['FRECUENCIA_LLEGADA_EN_TERMINALES'] != None:
                    objSinoptico_Resumen.Frecuencia_Llegada_Terminal = Viaje[v]['FRECUENCIA_LLEGADA_EN_TERMINALES']
                
                if Viaje[v]['FRECUENCIA_SALIDA_EN_TERMINALES_EN_SINOPTICO'] != None:
                    objSinoptico_Resumen.Frecuencia_Salida_Sinoptico = Viaje[v]['FRECUENCIA_SALIDA_EN_TERMINALES_EN_SINOPTICO']
                
                if Viaje[v]['FRECUENCIA_LLEGADA_EN_TERMINALES_EN_SINOPTICO'] != None:
                    objSinoptico_Resumen.Frecuencia_Llegada_Sinoptico = Viaje[v]['FRECUENCIA_LLEGADA_EN_TERMINALES_EN_SINOPTICO']
                    
                if Viaje[v]['FRECUENCIA_AUTOBUSES_EN_SINOPTICO'] != None:
                    objSinoptico_Resumen.Frecuencia_Autobuses_En_Sinoptico = Viaje[v]['FRECUENCIA_AUTOBUSES_EN_SINOPTICO']
                    
                    
            except Exception as ex:
                print(traceback.format_exc())
                print(str(ex))  
                
                
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return objSinoptico_Resumen

#getViajesSinopticoR

#GetViajeStatus

def getStatus(ID):
    
    Name = "OTRO"
    
    try:
        
        sql = text("SELECT NAME FROM VIAJE_STATUS WHERE ID = "  + str(ID) +" ")
        
        Prioridad = Ejecutor.execute(sql)
        
        Name = Prioridad['row1']['NAME']

    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return Name

#GetViajesStatus


#getStatusList

def getStatusList():
    
    Name = []
    
    try:
        
        sql = text("SELECT ID,NAME FROM VIAJE_STATUS")
        
        Prioridad = Ejecutor.execute(sql)
        
        for i in Prioridad:
            objCoordenadas =  CoordenadasClass.Coordenadas()
            objCoordenadas.TRECHO_TRAZADO_ID = Prioridad[i]['ID']
            objCoordenadas.Secuencia = Prioridad[i]['NAME']
            Name.append(objCoordenadas)

    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return Name

#GetViajesStatus


#getStatusGetList

def getStatusGetList(List, ID):
    
    Name = ""
    try:
            
        for i in List:
            if i.TRECHO_TRAZADO_ID == ID:
                Name = str(i.Secuencia).rstrip()
                break

        if len(Name) == 0:
            Name = "Sin Estatus"
        
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return Name

#getStatusGetList

#GetConexionViaje

def GetConexionViaje(ID):
    
    Name = "OTRO"
    sql = ""
    
    try:
        
        #sql = text("SELECT VIAJE_POSICION.VIAJE_STATUS_RECORRIDO_ID FROM VIAJE_POSICION WHERE VIAJE_POSICION.ID =  "  + str(ID) +" ")
        sql = text(" SELECT TOP 1	A.ID, A.VIAJE_STATUS_RECORRIDO_ID, B.NAME FROM VIAJE_POSICION AS A " + 
                   " INNER JOIN VIAJE_STATUS_RECORRIDO AS B ON B.ID = A.VIAJE_STATUS_RECORRIDO_ID  " + 
                   " WHERE A.ID = '"  + str(ID) + "' ")
        Status = Ejecutor.execute(sql)
        
        if Status != None:
            
            try:
                Name = Status['row1']['NAME']
                
            except Exception as ex:
                Name = "Sin Estado"
                                
        else:
            Name = "Sin Estado"
        #if len(Status) > 0:
        #    sql = text("SELECT NAME FROM VIAJE_STATUS_RECORRIDO WHERE ID = "  + str(Status['row1']['VIAJE_STATUS_RECORRIDO_ID']) +" ")
        #    Prioridad = Ejecutor.execute(sql)
        #    Name = Prioridad['row1']['NAME']

        
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))
        Name = "Sin Estado"
        
    return Name
    

#GetConexionViaje


#getUltimaAlerta

def getUltimaAlerta(ID):

    Alerta = ""

    try:
        
        sql = text(' SELECT TOP 1 EVENTO_TIPO.DESCRIPTION FROM VIAJE '
                   ' INNER JOIN EVENTO_VIAJE on EVENTO_VIAJE.VIAJE_ID = VIAJE.ID ' + 
                   ' INNER JOIN EVENTO on EVENTO.ID = EVENTO_VIAJE.EVENTO_ID ' + 
                   ' INNER JOIN EVENTO_TIPO on  EVENTO_TIPO.ID = EVENTO.EVENTO_TIPO_ID ' + 
                   ' WHERE EVENTO_VIAJE.VIAJE_ID = ' + str(ID) + '  ' + 
                   ' ORDER BY EVENTO_VIAJE.EVENTO_ID ')

        AlertaSql = Ejecutor.execute(sql)
        
        if len(AlertaSql) > 0:
            Alerta = AlertaSql['row1']['DESCRIPTION']
        
        else:
            Alerta = "Sin Alerta"
        
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    #end_db()

    return Alerta

#getUltimaAlerta

#Func

#???

def getSinopticoTrecho(ID):
    Sinoptico = ""
    try:
        Ruta = Tablas.Ruta_Trecho.query_one({"TRECHO_ID": ID})
        if Ruta != None:
            Multi_Ruta = Tablas.MultiRuta_Trecho.query_one({"TRECHO_ID": Ruta.TRECHO_ID})
            if Multi_Ruta != None:
                Sinoptico = str(Multi_Ruta.MULTIRUTA_ID)

    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    #end_db()

    return Sinoptico

#op

def getColor(ID):
        
    #init_db()

    try:
        color = Tablas.Color.query_one({"ID": ID})
        try:
            Scolor = color.VALUE

        except Exception as ex:
            Scolor = ""

    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    #end_db()
    
    return str(Scolor)

def getRutasTrecho(ID):
        
    #init_db()

    data = {}
    data["Rutas"] = []
    data["Sinopticos"] = []
    r = ""
    try:
        Rutas = Tablas.Ruta_Trecho.query_all({"TRECHO_ID": ID})
        if len(Rutas) != 0:
            for r in Rutas:
                data["Rutas"].append(
                    {
                        'Ruta_Id': int(r.RUTA_ID)
                    }
                )
            
            Sinopticos = getSinopticoTrecho(ID)
            #Sinopticos = getSinopticoTrechov2(ID)
            for s in Sinopticos:
                data["Sinopticos"].append(
                    {
                    "Sinoptico_Id": int(Sinopticos)
                    }
                )

    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    #end_db()

    return [ data["Rutas"], data["Sinopticos"] ]

def getCoordenadas(ID):
    
    #init_db()
    coordenadas = ""

    try:
        coordenadas = Tablas.Trazado.query_all({"TRECHO_TRAZADO_ID": ID})
        #for t in Trechos:
        #   print(t)
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    #end_db()

    return coordenadas

#Adicinal O COPIAS

def getCoordenadasAll():
    
    #init_db()
    coordenadas = []

    try:
        sql = text("SELECT DISTINCT TRECHO_TRAZADO_ID, SEQUENCE, CONVERT(DECIMAL(16,4), LATITUD) AS LATITUD,  CONVERT(DECIMAL(16,4), LONGITUD) AS LONGITUD, DISTANCIA_ACUMULADA AS DISTANCIA_ACUMULADA  FROM TRAZADO ORDER BY TRAZADO.TRECHO_TRAZADO_ID, TRAZADO.SEQUENCE")
        trazado = Ejecutor.execute(sql)
        
        for t in trazado:
            objCoordenadas =  CoordenadasClass.Coordenadas()
            objCoordenadas.TRECHO_TRAZADO_ID = trazado[t]['TRECHO_TRAZADO_ID']
            objCoordenadas.SEQUENCE = trazado[t]['SEQUENCE']
            objCoordenadas.LATITUD = round(trazado[t]['LATITUD'], 4)
            objCoordenadas.LONGITUD = round(trazado[t]['LONGITUD'], 4)
            objCoordenadas.DistanciaAcumulada = trazado[t]['DISTANCIA_ACUMULADA']
            coordenadas.append(objCoordenadas)
        
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    #end_db()

    return coordenadas

def getCoordenadasAllTrecho(CoordenadasList, ID):
    
    
    lista = []
    try:
        
        for t in CoordenadasList:
            if (t.TRECHO_TRAZADO_ID == ID):
                objCoordenadas =  CoordenadasClass.Coordenadas()
                objCoordenadas.TRECHO_TRAZADO_ID = t.TRECHO_TRAZADO_ID
                objCoordenadas.SEQUENCE = t.SEQUENCE
                objCoordenadas.LATITUD = t.LATITUD
                objCoordenadas.LONGITUD = t.LONGITUD
                objCoordenadas.DistanciaAcumulada = t.DistanciaAcumulada
                lista.append(objCoordenadas)

        lista_nueva = []
        ListaCoor = []
        for i in lista:
            if float(i.LATITUD.real) not in ListaCoor:
                objCoordenadas =  CoordenadasClass.Coordenadas()
                objCoordenadas.TRECHO_TRAZADO_ID = i.TRECHO_TRAZADO_ID
                objCoordenadas.SEQUENCE = i.SEQUENCE
                objCoordenadas.LATITUD = float(i.LATITUD.real)
                objCoordenadas.LONGITUD = float(i.LONGITUD.real)
                objCoordenadas.DistanciaAcumulada = float(i.DistanciaAcumulada)
                lista_nueva.append(objCoordenadas)
                ListaCoor.append(float(i.LATITUD.real))
        
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return lista_nueva

def InsertLog(emity, value):
    
    date_time = datetime.datetime.now()  - timedelta(hours= 5) 
    date_time_s = date_time.strftime("%m/%d/%Y, %H:%M:%S")
    stmt = text("INSERT INTO LOG_JSON (emit, valor, fecha) VALUES (:x, :y, :z)")
    stmt  = stmt.bindparams(x=emity, y=value, z=date_time_s)
    sinopticos = Ejecutor.execute(stmt)


#GetViajesPosicion

def getViajePosiciones(ID):
    
    today = convertlocaldate(datetime.datetime.now() )
    Fecha = datetime.datetime.strptime(today, "%Y-%m-%d %H:%M:%S" )
    Fecha = Fecha.strftime("%Y/%m/%d")
    Fecha_I = str(Fecha) + " 00:00:00"
    Fecha_F = str(Fecha) + " 23:59:59"

    Viaje = ""
    
    Color_Frecuencia = "N"
    Color_Puntualidad = "N"

    List_punt = []
    List_frec_ade = []
    List_punt_avg = []
    List_frec_ade_avg = []
    
    Promedio_Punt = 0
    Promedio_Ade = 0
        
    try:
        
        sql = text(" SELECT DISTINCT B.COLOR_PUNTUALIDAD, B.COLOR_FRECUENCIA_ADELANTE FROM VIAJE AS A " +
                   " INNER JOIN VIAJE_POSICION AS B ON B.ID = A.ULTIMO_VIAJE_POSICION_ID " +
                   " INNER JOIN MULTIRUTA_RUTA AS C on A.RUTA_ID = C.RUTA_ID " +
                   " WHERE A.VIAJE_STATUS_ID= 2 AND C.MULTIRUTA_ID = " + str(ID) + " " +
                   " AND A.FECHA_HORA_PROGRAMADA_SALIDA BETWEEN '" + str(Fecha_I) + "' AND '" + str(Fecha_F) + "' ")

        Viaje = Ejecutor.execute(sql)
                    
        for v in Viaje:
            
            if Viaje[v]['COLOR_PUNTUALIDAD'] != None:
                
                if Viaje[v]['COLOR_PUNTUALIDAD'] == "R":
                    List_punt.append(1)
                    
                if Viaje[v]['COLOR_PUNTUALIDAD'] == "V":
                    List_punt.append(2)
                    
                if Viaje[v]['COLOR_PUNTUALIDAD'] == "A":
                    List_punt.append(3)
                    
            if Viaje[v]['COLOR_FRECUENCIA_ADELANTE'] != None:
                    
                if Viaje[v]['COLOR_FRECUENCIA_ADELANTE'] == "R":
                    List_frec_ade.append(1)
                    
                if Viaje[v]['COLOR_FRECUENCIA_ADELANTE'] == "V":
                    List_frec_ade.append(2)
                
                if Viaje[v]['COLOR_FRECUENCIA_ADELANTE'] == "A":
                    List_frec_ade.append(3)
            
        try:
            
            if len(List_punt) > 0:
                    
                Moda = mode(List_punt)
                
                if Moda == 1:
                    Color_Puntualidad = "R"
        
                if Moda == 2:
                    Color_Puntualidad = "V"

                if Moda == 3:
                    Color_Puntualidad = "A"

                if Moda == 4:
                    Color_Puntualidad = "N"
                        
            if len(List_frec_ade) > 0:
                
                Moda = mode(List_frec_ade)
                
                if Moda == 1:
                    Color_Frecuencia = "R"
        
                if Moda == 2:
                    Color_Frecuencia = "V"

                if Moda == 3:
                    Color_Frecuencia = "A"

                if Moda == 4:
                    Color_Trecho = "N"
            
                    
        except Exception as ex:
            print(traceback.format_exc())
            print(str(ex))        
            
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    try:
        
        sql = text(" SELECT	AVG(D.PUNTUALIDAD) AS PUNTUALIDAD, AVG(D.FRECUENCIA_ADELANTE) AS FRECUENCIA " + 
                   " FROM VIAJE  AS A " +
                   " INNER JOIN MULTIRUTA_RUTA AS B ON A.RUTA_ID = B.RUTA_ID " +
                   " INNER JOIN MULTIRUTA AS C ON B.MULTIRUTA_ID = C.ID " +
                   " INNER JOIN VIAJE_POSICION AS D ON A.ULTIMO_VIAJE_POSICION_ID= D.ID " +
                   " WHERE A.FECHA_HORA_PROGRAMADA_SALIDA<= GETDATE() " +
                   " AND A.FECHA_HORA_PROGRAMADA_LLEGADA>= GETDATE() " +
                   " AND A.VIAJE_STATUS_ID in (2) " +
                   " AND C.ID=  " + str(ID) + "")
        
        Viaje = Ejecutor.execute(sql)
                    
        for v in Viaje:
            
            if Viaje[v]['PUNTUALIDAD'] != None:
                Promedio_Punt = int(Viaje[v]['PUNTUALIDAD'])
                
            if Viaje[v]['FRECUENCIA'] != None:
                Promedio_Ade = int(Viaje[v]['FRECUENCIA'])
        
    
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))    
        
    return [Color_Frecuencia, Color_Puntualidad, Promedio_Punt, Promedio_Ade]

#GetViajesPosicion

#getViajeColor

def getViajeColor(ID):
    
    #- timedelta(hours= 5) 
    today = convertlocaldate(datetime.datetime.now() )
    Fecha = datetime.datetime.strptime(today, "%Y-%m-%d %H:%M:%S" )
    Fecha = Fecha.strftime("%Y/%m/%d")
    Fecha_I = str(Fecha) + " 00:00:00"
    Fecha_F = str(Fecha) + " 23:59:59"

    Viaje = ""
    
    Color_Frecuencia = "N"
    Color_Puntualidad = "N"
    
    Promedio_Punt = 0
    Promedio_Ade = 0
        
    try:
        
        sql = text(" SELECT B.COLOR_PUNTUALIDAD, COUNT(*) AS TOTAL_REGISTROS " +
                   " FROM VIAJE AS A " +
                   " INNER JOIN VIAJE_POSICION AS B ON B.ID  = A.ULTIMO_VIAJE_POSICION_ID " +
                   " INNER JOIN MULTIRUTA_TRECHO AS D ON D.TRECHO_ID = B.TRECHO_ACTUAL_ID " +
                   
                   " WHERE A.VIAJE_STATUS_ID = 2 " +
                   " AND D.MULTIRUTA_ID = " + str(ID) + " " +
                   " AND A.FECHA_HORA_PROGRAMADA_SALIDA BETWEEN '" + str(Fecha_I) + "' AND '" + str(Fecha_F) + "' " +
                   " GROUP BY B.COLOR_PUNTUALIDAD " + 
                   " ORDER BY TOTAL_REGISTROS DESC ")
                    
        Viaje = Ejecutor.execute(sql)
                    
        if len(Viaje) > 0:
            Color_Puntualidad = Viaje['row1']['COLOR_PUNTUALIDAD']
            
    except Exception as ex:
        Color_Puntualidad = "N"
        print(traceback.format_exc())
        print(str(ex))
        
        
    try:
        
        sql = text(" SELECT B.COLOR_FRECUENCIA_ADELANTE, COUNT(*) AS TOTAL_REGISTROS " +
                   " FROM VIAJE AS A " +
                   " INNER JOIN VIAJE_POSICION AS B ON B.ID  = A.ULTIMO_VIAJE_POSICION_ID " +
                   " INNER JOIN MULTIRUTA_TRECHO AS D ON D.TRECHO_ID = B.TRECHO_ACTUAL_ID " +
                   
                   " WHERE A.VIAJE_STATUS_ID = 2 " +
                   " AND D.MULTIRUTA_ID = " + str(ID) + " " +
                   " AND A.FECHA_HORA_PROGRAMADA_SALIDA BETWEEN '" + str(Fecha_I) + "' AND '" + str(Fecha_F) + "' " +
                   " AND B.COLOR_FRECUENCIA_ADELANTE IS NOT NULL " +
                   
                   " GROUP BY B.COLOR_FRECUENCIA_ADELANTE " + 
                   " ORDER BY TOTAL_REGISTROS DESC ")
                    
        Viaje = Ejecutor.execute(sql)
                    
        if len(Viaje) > 0:
            Color_Frecuencia = Viaje['row1']['COLOR_FRECUENCIA_ADELANTE']
            
    except Exception as ex:
        Color_Frecuencia = "N"
        print(traceback.format_exc())
        print(str(ex))    
        

    try: 
        
        sql = text(" SELECT AVG(B.PUNTUALIDAD) AS PUNTUALIDAD, AVG(B.FRECUENCIA_ADELANTE) AS FRECUENCIA  " + 
                   " FROM VIAJE  AS A " +
                   " INNER JOIN VIAJE_POSICION AS B ON A.ULTIMO_VIAJE_POSICION_ID = B.ID " +
                   " INNER JOIN MULTIRUTA_TRECHO AS C ON B.TRECHO_ACTUAL_ID = C.TRECHO_ID " +
                  
                   " WHERE A.FECHA_HORA_PROGRAMADA_SALIDA<= GETDATE() " +
                   " AND A.FECHA_HORA_PROGRAMADA_LLEGADA>= GETDATE() " +
                   " AND A.VIAJE_STATUS_ID in (2) " +
                   " AND C.MULTIRUTA_ID =   " + str(ID) + "")
        
        Viaje = Ejecutor.execute(sql)
                    
        for v in Viaje:
            
            if Viaje[v]['PUNTUALIDAD'] != None:
                Promedio_Punt = int(Viaje[v]['PUNTUALIDAD'])
                
            if Viaje[v]['FRECUENCIA'] != None:
                Promedio_Ade = int(Viaje[v]['FRECUENCIA'])
        
    
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))    
        
    return [Color_Frecuencia, Color_Puntualidad, Promedio_Punt, Promedio_Ade]

#getViajeColor

#GetEventoDes

def GetEventoDes(ID):
    
    Name = "OTRO"
    sql = ""
    
    try:
        
        sql = text(" SELECT DESCRIPTION FROM EVENTO_TIPO WHERE EVENTO_TIPO.ID =  "  + str(ID) +" ")
        Status = Ejecutor.execute(sql)
        
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return Status
    
#GetEventoDes

#GetGeotabURL

def getGeotabULR(ID):
    
    Name = "OTRO"
    sql = ""
    URL = "None"
    try:
        
        sql = text(" SELECT A.NUMECONOMICO, A.ID_NUM_ERPCO, A.GEOTAB_DEVICE_ID, G.NAME, G.SERVER, G.BD, G.URL, G.ACTIVE FROM AUTOBUS AS A "
                   " INNER JOIN GEOTAB_SERVER AS G ON G.ID = A.GEOTAB_SERVER_ID " +
                   " WHERE A.NUMECONOMICO = '"  + str(ID) + "' "
                   " AND G.ACTIVE = 1 ")
        
        Status = Ejecutor.execute(sql)
        
        if len(Status) > 0:
            
            URL = str(Status['row1']['URL'].rstrip() + "/#map,liveVehicleIds:!(" + str(Status['row1']['GEOTAB_DEVICE_ID']).rstrip() + ")")
        
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return URL
    
#GetGeotabURL

#GetAllGeotabURL

def GetAllGeotabURL():
    
    Geotab = []
    sql = ""
    URL = "None"
    try:
        
        sql = text(" SELECT A.NUMECONOMICO, A.ID_NUM_ERPCO, A.GEOTAB_DEVICE_ID, G.NAME, G.SERVER, G.BD, G.URL, G.ACTIVE  FROM AUTOBUS AS A "
                   " INNER JOIN GEOTAB_SERVER AS G ON G.ID = A.GEOTAB_SERVER_ID " +
                   " WHERE G.ACTIVE = 1 ")
        
        Status = Ejecutor.execute(sql)
        
        if Status != None:
            for i in Status:
                URL = str(Status[i]['URL'].rstrip() + "/#map,liveVehicleIds:!(" + str(Status[i]['GEOTAB_DEVICE_ID']).rstrip() + ")")
                obj_Geotab = msj.Mensajes()
                obj_Geotab.AUTOBUS = Status[i]['NUMECONOMICO']
                obj_Geotab.MSJ = URL
                Geotab.append(obj_Geotab)
            
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return Geotab
    
#GetAllGeotabURL

#GetGeotabURLLISt
def GetGeotabURLlISt(GetGeotabURLList, ID):
    
    URL = []

    try:
        
        for i in GetGeotabURLList:
            if(i.AUTOBUS.rstrip() == str(ID)):
                URL = i.MSJ
                break
        
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return URL

#GetGeotabURLLISt

def getAllSinopticosTrechos():
    
    Trechos_List = []

    try:

        sql = text(' SELECT DISTINCT TRECHO_TRAZADO.TRECHO_ID, MULTIRUTA_TRECHO.MULTIRUTA_ID AS ID ' +
                   ' FROM TRECHO_TRAZADO ' +
                   ' INNER JOIN TRECHO ON TRECHO.ID = TRECHO_TRAZADO.TRECHO_ID ' +
                   ' INNER JOIN RUTA_TRECHO ON RUTA_TRECHO.TRECHO_ID = TRECHO.ID ' +
                   ' INNER JOIN MULTIRUTA_TRECHO ON MULTIRUTA_TRECHO.TRECHO_ID = RUTA_TRECHO.TRECHO_ID ' +
                   ' INNER JOIN MULTIRUTA ON MULTIRUTA.ID = MULTIRUTA_TRECHO.MULTIRUTA_ID ' +
                   ' WHERE MULTIRUTA.ACTIVE = 1 ' + 
                   ' ORDER BY TRECHO_TRAZADO.TRECHO_ID' )

        trechos = Ejecutor.execute(sql)

        if trechos != None:
            for i in trechos:
                
                obj_Trechos = Trechos_Class.Trechos()
                obj_Trechos.Trecho_Id = trechos[i]['TRECHO_ID']
                obj_Trechos.Trecho_Sinoptico = trechos[i]['ID']
                Trechos_List.append(obj_Trechos)
        
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return Trechos_List

#getAllSinopticosTrechos

#GetGeotabURLLISt

def getAllSinopticosTrechosActive():
    
    Trechos_List = []

    try:

        sql = text(' SELECT DISTINCT TRECHO_TRAZADO.TRECHO_ID, MULTIRUTA_TRECHO.MULTIRUTA_ID AS ID ' +
                   ' FROM TRECHO_TRAZADO ' +
                   ' INNER JOIN TRECHO ON TRECHO.ID = TRECHO_TRAZADO.TRECHO_ID ' +
                   ' INNER JOIN RUTA_TRECHO ON RUTA_TRECHO.TRECHO_ID = TRECHO.ID ' +
                   ' INNER JOIN MULTIRUTA_TRECHO ON MULTIRUTA_TRECHO.TRECHO_ID = RUTA_TRECHO.TRECHO_ID ' +
                   ' INNER JOIN MULTIRUTA ON MULTIRUTA.ID = MULTIRUTA_TRECHO.MULTIRUTA_ID ' +
				   ' WHERE MULTIRUTA.ACTIVE = 1  ORDER BY TRECHO_TRAZADO.TRECHO_ID' )

        trechos = Ejecutor.execute(sql)

        if trechos != None:
            
            try:
                for i in trechos:
                    obj_Trechos = Trechos_Class.Trechos()
                    obj_Trechos.Trecho_Id = trechos[i]['TRECHO_ID']
                    obj_Trechos.Trecho_Sinoptico = trechos[i]['ID']
                    Trechos_List.append(obj_Trechos)
                    
            except Exception as ex:
                print(traceback.format_exc())
                print(str(ex))
        
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return Trechos_List

#getAllSinopticosTrechos

#getAllSinopticosTrechos
def GetSinopticosList(SinopticoIdList, ID):
    
    Trechos_List = []

    try:
        
        for i in SinopticoIdList:
            if(i.Trecho_Id == ID):
                if i.Trecho_Sinoptico not in Trechos_List:
                    Trechos_List.append(i.Trecho_Sinoptico)
        
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))

    return Trechos_List

#GetSinopticosList

def convertlocaldate(fecha):
    berlin_now = None
    try:
        
        tz = pytz.timezone('Mexico/General')
        berlin_now =  pytz.utc.localize(fecha, is_dst=None).astimezone(tz)
        berlin_now = berlin_now.strftime("%Y-%m-%d %H:%M:%S")
    
    except Exception as ex:
        print(traceback.format_exc())
        print(str(ex))
        
    return str(berlin_now)