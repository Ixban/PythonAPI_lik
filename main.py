from datetime import datetime, timedelta
import json
from math import sqrt
import time
import numpy as np
import socketio 
import _thread
from threading import Thread
import random
import concurrent.futures

from flask import Flask, render_template, jsonify, make_response
from flask_httpauth import HTTPBasicAuth

import Librerias.Clases.Coordenadas as Coor
import Librerias.Clases.Trazados as Traz
import Librerias.Clases.DatabaseCoordenadas as DataCoordenadas
import Librerias.Clases.Trechos as Trech
import Librerias.Seguridad as Seguridad
import Librerias.Clases.SinopticoEC as SinocticoEC
import traceback

import sys
import time

app = Flask(__name__)

import concurrent.futures

VAR_EXEC_MENSAJES = False
VAR_EXEC_PARADAS = False
VAR_EXEC_RUTAS = False
VAR_EXEC_SINOPTICOS = False
VAR_EXEC_SINOPTICOSRESUMEN = False
VAR_EXEC_TRAMAEVENTOS = False
VAR_EXEC_TRECHOS = False
VAR_EXEC_VIAJES = False
VAR_EXEC_ALL = False
VAR_EXEC_UPDATE = False
VAR_EXEC_POSICION = False

global VAR_ENCENDIDO
VAR_ENCENDIDO = True

global VAR_ENCENDIDO_LOG_CONSOLE
VAR_ENCENDIDO_LOG_CONSOLE = True

global Parametros
Parametros = []
global Sinopticos
Sinopticos = []
global Dimension
Dimension = []
global Trechos_C
Trechos_C = []
global Sinopticos_for
Sinopticos_for = []
global SinopticoIdList
SinopticoIdList = []
global SinopticoIdListActive
SinopticoIdListActive = []
global GeotabULRLIST
GeotabULRLIST = []
global CondutorLIST
CondutorLIST = []
global Parada_Info
Parada_Info = []
global CoordenadasParadasLIST
CoordenadasParadasLIST = []
global CoordenadasTrazadoList
CoordenadasTrazadoList = []
global SinoticosTrazadosList
SinoticosTrazadosList = []
global ColorTrechosList
ColorTrechosList = []
global EstatusList
EstatusList = []
global RutasList
RutasList = []
global Trechos_MultiRuta_ID
Trechos_MultiRuta_ID  = []
global Trechos_Trazados_list
Trechos_Trazados_list = []
global ViajesJson_cache
ViajesJson_cache = []
# Iniciamos el motor de seguridad
auth = HTTPBasicAuth()
#Cloud = "Local I"
Cloud = "Cloud G"


@auth.verify_password
def Login(username, password):
    return Seguridad.autenticar(username,password)

@app.route('/')
def root():
    return 'Indice Servicio Stream SAE versión 1.5', 200

@app.route('/API/v1.0/GetRutas')
def GetRutas():
    
    global VAR_EXEC_RUTAS
    
    try:
        if VAR_EXEC_RUTAS is False:
            
            _thread.start_new_thread(RutasThread,())
            return "Operando"
        
        else:
            #Esta Ocupado    
            return "Ocupado"
    except Exception as ex:
        
        VAR_EXEC_RUTAS = False
        str_error = "Error al invocar el hilo rutas" + ex.__str__()
        print(str_error, file=sys.stderr)
        return str_error
    
#Json Rutas (THREAD)

#JSON Rutas (JSON)
@app.route('/API/v1.0/GetRutasJson')
def GetRutasJson():
    
    seconds = 0
    data1 = datetime.today()
    rutas = GetRutasv1()
    EmitirJson(rutas[0], rutas[1], rutas[2])
    data2 = datetime.today()
    diff = data2 - data1
    seconds = diff.seconds
    hours = int(diff.seconds // (60 * 60))
    mins = int((diff.seconds // 60) % 60)
    seconds = (seconds % 60)
    
    global VAR_ENCENDIDO_LOG_CONSOLE
    if(VAR_ENCENDIDO_LOG_CONSOLE):
        print('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +' Segundos: ' +  str(seconds) )
    #DataCoordenadas.InsertLog('GetRutasJson', str('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +' Segundos: ' +  str(seconds)))
    return jsonify(rutas[0])
   
#JSON Rutas (JSON)

def RutasThread():
    
    global VAR_EXEC_RUTAS
    VAR_EXEC_RUTAS = True
    data1 = datetime.today()
    rutas_thread = GetRutasv1()
    EmitirJson(rutas_thread[0], rutas_thread[1], rutas_thread[2])
    data2 = datetime.today()
    diff = data2 - data1
    seconds = diff.seconds
    hours = int(diff.seconds // (60 * 60))
    mins = int((diff.seconds // 60) % 60)
    seconds = (seconds % 60)
    global VAR_ENCENDIDO_LOG_CONSOLE
    if(VAR_ENCENDIDO_LOG_CONSOLE):
        print('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +' Segundos: ' +  str(seconds) )
    #DataCoordenadas.InsertLog('GetRutasJson', str('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +' Segundos: ' +  str(seconds)))
    VAR_EXEC_RUTAS = False

#Json Sinopticos (MULTIPLE QUERY)
@app.route('/API/v1.0/GetSinopticos')
def GetSinopticos():
    
    global VAR_EXEC_SINOPTICOS
    
    try:
        if VAR_EXEC_SINOPTICOS is False:
            
            _thread.start_new_thread(SinopticosThread,())
            return "Operando"
        
        else:
            #Esta Ocupado    
            return "Ocupado"
    except Exception as ex:
        
        VAR_EXEC_SINOPTICOS = False
        str_error = "Error al invocar el hilo rutas" + ex.__str__()
        print(str_error, file=sys.stderr)
        return str_error

#Json Sinopticos (MULTIPLE QUERY)

#JSON Sinopticos (JSON)
@app.route('/API/v1.0/GetSinopticosJson')
def GetSinopticosJson():
    
    data1 = datetime.today()
    sinopticos = GetSinopticosv1()
    EmitirJson(sinopticos[0], sinopticos[1], sinopticos[2])
    data2 = datetime.today()
    diff = data2 - data1
    seconds = diff.seconds
    hours = int(diff.seconds // (60 * 60))
    mins = int((diff.seconds // 60) % 60)
    seconds = (seconds % 60)
    
    global VAR_ENCENDIDO_LOG_CONSOLE
    if(VAR_ENCENDIDO_LOG_CONSOLE):
        print('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +' Segundos: ' +  str(seconds) )
    #DataCoordenadas.InsertLog('GetSinopticosJson', str('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +' Segundos: ' +  str(seconds)))
    return jsonify(sinopticos[0])
    
#JSON Sinopticos (JSON)

def SinopticosThread():
    
    global VAR_EXEC_SINOPTICOS
    VAR_EXEC_SINOPTICOS = True
    data1 = datetime.today()
    sinopticos_thread = GetSinopticosv1()
    EmitirJson(sinopticos_thread[0], sinopticos_thread[1], sinopticos_thread[2])
    data2 = datetime.today()
    diff = data2 - data1
    seconds = diff.seconds
    hours = int(diff.seconds // (60 * 60))
    mins = int((diff.seconds // 60) % 60)
    seconds = (seconds % 60)
    
    global VAR_ENCENDIDO_LOG_CONSOLE
    if(VAR_ENCENDIDO_LOG_CONSOLE):
        print('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +' Segundos: ' +  str(seconds) )
    #DataCoordenadas.InsertLog('GetSinopticosJson', str('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +' Segundos: ' +  str(seconds)))
    VAR_EXEC_SINOPTICOS = False

#JSON TRAMA_EVENTOS
@app.route('/API/v1.0/GetTramaEventos')
def GetTramaEventos():
    
    global VAR_EXEC_TRAMAEVENTOS
    
    try:
        if VAR_EXEC_TRAMAEVENTOS is False:
            
            _thread.start_new_thread(Eventos,())
            return "Operando"
        
        else:
            #Esta Ocupado    
            return "Ocupado"
    except Exception as ex:
        
        VAR_EXEC_TRAMAEVENTOS = False
        str_error = "Error al invocar el hilo rutas" + ex.__str__()
        print(str_error, file=sys.stderr)
        return str_error

#JSON TRAMA_EVENTOS

#JSON TRAMA_EVENTOS (JSON)
@app.route('/API/v1.0/GetTramaEventosJson')
def GetTramaEventosJson():

    data1 = datetime.today()
    TramaEventos = GetTramaEventosv1()
    EmitirJson(TramaEventos[0], TramaEventos[1], TramaEventos[2])
    data2 = datetime.today()
    diff = data2 - data1
    seconds = diff.seconds
    hours = int(diff.seconds // (60 * 60))
    mins = int((diff.seconds // 60) % 60)
    seconds = (seconds % 60)
    
    global VAR_ENCENDIDO_LOG_CONSOLE
    if(VAR_ENCENDIDO_LOG_CONSOLE):
        print('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +' Segundos: ' +  str(seconds) )
    #DataCoordenadas.InsertLog('GetTramaEventosJson', str('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +' Segundos: ' +  str(seconds)))
    return jsonify(TramaEventos[0])
    
#JSON TRAMA_EVENTOS (JSON)

def Eventos():
    
    global VAR_EXEC_TRAMAEVENTOS
    VAR_EXEC_TRAMAEVENTOS = True
    data1 = datetime.today()
    TramaEventos = GetTramaEventosv1()
    EmitirJson(TramaEventos[0], TramaEventos[1], TramaEventos[2])
    data2 = datetime.today()
    diff = data2 - data1
    seconds = diff.seconds
    hours = int(diff.seconds // (60 * 60))
    mins = int((diff.seconds // 60) % 60)
    seconds = (seconds % 60)
    
    global VAR_ENCENDIDO_LOG_CONSOLE
    if(VAR_ENCENDIDO_LOG_CONSOLE):
        print('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +' Segundos: ' +  str(seconds) )
    #DataCoordenadas.InsertLog('GetTramaEventosJson', str('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +' Segundos: ' +  str(seconds)))
    VAR_EXEC_TRAMAEVENTOS = False

#JSON MENSAJES
@app.route('/API/v1.0/GetMensajes')
def GetMensajes():
    
    global VAR_EXEC_MENSAJES
    
    try:
        if VAR_EXEC_MENSAJES is False:
            
            _thread.start_new_thread(Mensajes,())
            return "Operando"
        
        else:
            #Esta Ocupado    
            return "Ocupado"
    except Exception as ex:
        
        VAR_EXEC_MENSAJES = False
        str_error = "Error al invocar el hilo rutas" + ex.__str__()
        print(str_error, file=sys.stderr)
        return str_error

#JSON MENSAJES

#JSON MENSAJES (JSON)
@app.route('/API/v1.0/GetMensajesJson')
def GetMensajesJson():

    data1 = datetime.today()
    mensajes = GetMensajesv1()
    EmitirJson(mensajes[0], mensajes[1], mensajes[2])
    data2 = datetime.today()
    diff = data2 - data1
    seconds = diff.seconds
    hours = int(diff.seconds // (60 * 60))
    mins = int((diff.seconds // 60) % 60)
    seconds = (seconds % 60)
    
    global VAR_ENCENDIDO_LOG_CONSOLE
    if(VAR_ENCENDIDO_LOG_CONSOLE):
        print('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +' Segundos: ' +  str(seconds) )
    #DataCoordenadas.InsertLog('GetMensajesJson', str('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +' Segundos: ' +  str(seconds)))
    return jsonify(mensajes[0])
    
#JSON MENSAJES (JSON)

def Mensajes():
    
    global VAR_EXEC_MENSAJES
    VAR_EXEC_MENSAJES = True
    data1 = datetime.today()
    mensajes = GetMensajesv1()
    EmitirJson(mensajes[0], mensajes[1], mensajes[2])    
    data2 = datetime.today()
    diff = data2 - data1
    seconds = diff.seconds
    hours = int(diff.seconds // (60 * 60))
    mins = int((diff.seconds // 60) % 60)
    seconds = (seconds % 60)
    
    global VAR_ENCENDIDO_LOG_CONSOLE
    if(VAR_ENCENDIDO_LOG_CONSOLE):
        print('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +' Segundos: ' +  str(seconds) )
    #DataCoordenadas.InsertLog('GetMensajesJson', str('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +' Segundos: ' +  str(seconds)))
    VAR_EXEC_MENSAJES = False

#JSON TRECHOS (THREAD)
@app.route('/API/v1.0/GetTrechos')
def GetTrechos():

    global VAR_EXEC_TRECHOS
    
    try:
        if VAR_EXEC_TRECHOS == False:
            
            _thread.start_new_thread(Trechos,())
            return "Operando"
        else:
            #Esta Ocupado    
            return "Ocupado"
    except Exception as ex:
        
        VAR_EXEC_TRECHOS = False
        str_error = "Error al invocar el hilo rutas" + ex.__str__()
        print(str_error, file=sys.stderr)
        return str_error

#JSON TRECHOS (THREAD)

#JSON TRECHOS (JSON)
@app.route('/API/v1.0/GetTrechosJson')
def GetTrechosJson():

    data1 = datetime.today()
    trechos = GetTrechosv1()
    EmitirJson(trechos[0], trechos[1], trechos[2])
    data2 = datetime.today()
    diff = data2 - data1
    seconds = diff.seconds
    hours = int(diff.seconds // (60 * 60))
    mins = int((diff.seconds // 60) % 60)
    seconds = (seconds % 60)
    global VAR_ENCENDIDO_LOG_CONSOLE
    if(VAR_ENCENDIDO_LOG_CONSOLE):
        print('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +' Segundos: ' +  str(seconds) )
    #DataCoordenadas.InsertLog('GetTrechosJson', str('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +' Segundos: ' +  str(seconds)))
    return jsonify(trechos[0])
    
#JSON TRECHOS (JSON)

def Trechos():
    
    global VAR_EXEC_TRECHOS
    VAR_EXEC_TRECHOS = True
    data1 = datetime.today()
    trechos = GetTrechosv1()
    a = EmitirJson(trechos[0], trechos[1], trechos[2])
    data2 = datetime.today()
    diff = data2 - data1
    seconds = diff.seconds
    hours = int(diff.seconds // (60 * 60))
    mins = int((diff.seconds // 60) % 60)
    seconds = (seconds % 60)
    
    global VAR_ENCENDIDO_LOG_CONSOLE
    if(VAR_ENCENDIDO_LOG_CONSOLE):
        print('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +' Segundos: ' +  str(seconds) )
    #DataCoordenadas.InsertLog('GetTrechosJson', str('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +' Segundos: ' +  str(seconds)))
    VAR_EXEC_TRECHOS = False
    
#JSON PARADAS (THREAD)
@app.route('/API/v1.0/GetParadas')
def GetParadasTrazado():    
    
    global VAR_EXEC_PARADAS
    
    try:
        if VAR_EXEC_PARADAS is False:
            
            _thread.start_new_thread(Paradas,())
            return "Operando"
        else:
            #Esta Ocupado    
            return "Ocupado"
    except Exception as ex:
        
        VAR_EXEC_PARADAS = False
        str_error = "Error al invocar el hilo rutas" + ex.__str__()
        print(str_error, file=sys.stderr)
        return str_error
    
#JSON PARADAS (THREAD)

#JSON PARADAS (JSON)
@app.route('/API/v1.0/GetParadasJson')
def GetParadasJson():

    data1 = datetime.today()
    paradas = GetParadasTrazadov1()
    EmitirJson(paradas[0], paradas[1], paradas[2])
    data2 = datetime.today()
    diff = data2 - data1
    seconds = diff.seconds
    hours = int(diff.seconds // (60 * 60))
    mins = int((diff.seconds // 60) % 60)
    seconds = (seconds % 60)
    
    global VAR_ENCENDIDO_LOG_CONSOLE
    if(VAR_ENCENDIDO_LOG_CONSOLE):
        print('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +' Segundos: ' +  str(seconds) )
    #DataCoordenadas.InsertLog('GetParadasJson', str('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +' Segundos: ' +  str(seconds)))
    return jsonify(paradas[0])
    
#JSON PARADAS (JSON)

def Paradas():
    
    global VAR_EXEC_PARADAS
    VAR_EXEC_PARADAS = True
    paradas = GetParadasTrazadov1()
    EmitirJson(paradas[0], paradas[1], paradas[2])
    #return jsonify(data_json)
    VAR_EXEC_PARADAS = False
    
#Json Viajes (THREAD)
@app.route('/API/v1.0/GetViajes')
def GetViajes():
    
    global VAR_EXEC_VIAJES
    
    try:
        if VAR_EXEC_VIAJES is False:
            
            _thread.start_new_thread(Viajes,())
            return "Operando" 
                
        else:
            #Esta Ocupado    
            return "Ocupado"
    except Exception as ex:
        
        VAR_EXEC_VIAJES = False
        str_error = "Error al invocar el hilo rutas" + ex.__str__()
        print(str_error, file=sys.stderr)
        return str_error
    
#Json Viajes (THREAD)

#JSON Viajes (JSON)
@app.route('/API/v1.0/GetViajesJson')
def GetViajesJson():

    data1 = datetime.today()
    viajes = GetViajesv1()
    global ViajesJson_cache
    ViajesJson_cache = None
    ViajesJson_cache = viajes[0]
    EmitirJson(viajes[0], viajes[1], viajes[2])
    global ColorTrechosList
    ColorTrechosList = DataCoordenadas.getColorsList()
    data2 = datetime.today()
    diff = data2 - data1
    seconds = diff.seconds
    hours = int(diff.seconds // (60 * 60))
    mins = int((diff.seconds // 60) % 60)
    seconds = (seconds % 60)
    
    global VAR_ENCENDIDO_LOG_CONSOLE
    if(VAR_ENCENDIDO_LOG_CONSOLE):
        print('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +'Segundos: ' +  str(seconds) )
    #DataCoordenadas.InsertLog('GetViajesJson', str('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +'Segundos: ' +  str(seconds)))
    return jsonify(viajes[0])
    
#JSON Viajes (JSON)

def Viajes():
    
    global VAR_EXEC_VIAJES
    VAR_EXEC_VIAJES = True
    data1 = datetime.today()
    viajes = GetViajesv1()
    EmitirJson(viajes[0], viajes[1], viajes[2])
    global ViajesJson_cache
    ViajesJson_cache = None
    ViajesJson_cache = viajes[0]
    global ColorTrechosList
    ColorTrechosList = DataCoordenadas.getColorsList()
    data2 = datetime.today()
    diff = data2 - data1
    seconds = diff.seconds
    hours = int(diff.seconds // (60 * 60))
    mins = int((diff.seconds // 60) % 60)
    seconds = (seconds % 60)
    
    global VAR_ENCENDIDO_LOG_CONSOLE
    if(VAR_ENCENDIDO_LOG_CONSOLE):
        print('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +'Segundos: ' +  str(seconds) )
    #DataCoordenadas.InsertLog('GetViajesJson', str('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +'Segundos: ' +  str(seconds)))
    VAR_EXEC_VIAJES = False
    
#JSON SINOPTICOS_RESUMEN
@app.route('/API/v1.0/GetSinopticosResumen')
def GetSinopticosResumen(): 
    
    global VAR_EXEC_SINOPTICOSRESUMEN
    
    try:
        if VAR_EXEC_SINOPTICOSRESUMEN is False:
            
            _thread.start_new_thread(SinopticoResumen,())
            return "Operando" 
            
        else:
            #Esta Ocupado    
            return "Ocupado"
    except Exception as ex:
        
        VAR_EXEC_SINOPTICOSRESUMEN = False
        str_error = "Error al invocar el hilo rutas" + ex.__str__()
        print(str_error, file=sys.stderr)
        return str_error
#JSON SINOPTICOS_RESUMEN


#JSON Viajes (JSON)
@app.route('/API/v1.0/GetSinopticosResumenJson')
def GetSinopticosResumenJson():

    data1 = datetime.today()
    sinopticoresumen = GetSinopticosResumenv1()
    EmitirJson(sinopticoresumen[0], sinopticoresumen[1], sinopticoresumen[2])
    data2 = datetime.today()
    diff = data2 - data1
    seconds = diff.seconds
    hours = int(diff.seconds // (60 * 60))
    mins = int((diff.seconds // 60) % 60)
    seconds = (seconds % 60)
    
    global VAR_ENCENDIDO_LOG_CONSOLE
    if(VAR_ENCENDIDO_LOG_CONSOLE):
        print('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +'Segundos: ' +  str(seconds) )
    #DataCoordenadas.InsertLog('GetSinopticosResumenJson', str('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +'Segundos: ' +  str(seconds)))
    return jsonify(sinopticoresumen[0])

#JSON Viajes (JSON)

def SinopticoResumen():
    
    global VAR_EXEC_SINOPTICOSRESUMEN
    VAR_EXEC_SINOPTICOSRESUMEN = True
    data1 = datetime.today()
    sinopticosresumen = GetSinopticosResumenv1()
    EmitirJson(sinopticosresumen[0], sinopticosresumen[1], sinopticosresumen[2])
    data2 = datetime.today()
    diff = data2 - data1
    seconds = diff.seconds
    hours = int(diff.seconds // (60 * 60))
    mins = int((diff.seconds // 60) % 60)
    seconds = (seconds % 60)
    print('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +'Segundos: ' +  str(seconds) )
    #DataCoordenadas.InsertLog('GetSinopticosResumenJson', str('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +'Segundos: ' +  str(seconds)))
    
    VAR_EXEC_SINOPTICOSRESUMEN = False
    #return jsonify(data_json)

#Emitir Todos JSON
@app.route('/API/v1.0/GetAll')
def GetAllTRHEAD():

    global VAR_EXEC_ALL
    
    try:
        if VAR_EXEC_ALL is False:
            
            _thread.start_new_thread(All,())
            return "Operando"
        
        else:
            #Esta Ocupado    
            return "Ocupado"
    except Exception as ex:
        
        VAR_EXEC_ALL = False
        str_error = "Error al invocar el hilo rutas" + ex.__str__()
        print(str_error, file=sys.stderr)
        return str_error


def All():
    
    global VAR_EXEC_ALL
    VAR_EXEC_ALL = True
    data1 = datetime.today()
    Rutas = GetRutasv1()
    Sinopticos = GetSinopticosv1()
    TramaEventos = GetTramaEventosv1()
    Mensajes = GetMensajesv1()
    Paradas = GetParadasTrazadov1()
    #Viajes = GetViajesv1()
    Resumen = GetSinopticosResumenv1()
    Trechos = GetTrechosv1()
    
    r1 = EmitirJson_v1(Rutas[0], "rutas")
    r2 = EmitirJson_v1(Sinopticos[0], "sinoptico")
    r3 = EmitirJson_v1(TramaEventos[0], "sinoptico_eventos")
    r4 = EmitirJson_v1(Mensajes[0], "mensajes")
    r6 = EmitirJson_v1(Paradas[0], "paradas")
    #r7 = EmitirJson_v1(Viajes[0], "viajes")
    r5 = EmitirJson_v1(Trechos[0], "trazados")
    r8 = EmitirJson_v1(Resumen[0], "sinoptico_resumen")
    data2 = datetime.today()
    diff = data2 - data1
    seconds = diff.seconds
    hours = int(diff.seconds // (60 * 60))
    mins = int((diff.seconds // 60) % 60)
    seconds = (seconds % 60)
    print('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +' Segundos: ' +  str(seconds) )
    #DataCoordenadas.InsertLog('GetAllJson', str('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +' Segundos: ' +  str(seconds)))
    VAR_EXEC_ALL = False

@app.route('/API/v1.0/GetAllJson')
def GetAllJSON():
    
    data1 = datetime.today()
    data_json = {}
    
    Rutas = GetRutasv1()
    Sinopticos = GetSinopticosv1()
    TramaEventos = GetTramaEventosv1()
    Mensajes = GetMensajesv1()
    Trechos = GetTrechosv1()
    Paradas = GetParadasTrazadov1()
    #Viajes = GetViajesv1()
    Resumen = GetSinopticosResumenv1()
    
    r1 = EmitirJson_v1(Rutas[0], "rutas")
    print ("1")
    r2 = EmitirJson_v1(Sinopticos[0], "sinoptico")
    print ("2")
    r3 = EmitirJson_v1(TramaEventos[0], "sinoptico_eventos")
    print ("3")
    r4 = EmitirJson_v1(Mensajes[0], "mensajes")
    print ("4")
    r5 = EmitirJson_v1(Trechos[0], "trazados")
    print ("5")
    r6 = EmitirJson_v1(Paradas[0], "paradas")
    print ("6")
    #r7 = EmitirJson_v1(Viajes[0], "viajes")
    #print ("7")
    r8 = EmitirJson_v1(Resumen[0], "sinoptico_resumen")
    print ("8")
    
    data_json["GetAll"] = []
    data_json["GetAll"].append(
        {
            "Rutas": str(len(Rutas[0]['Rutas'])) + " Registros - Envio: " + str(r1),
            "Sinopticos" : str(len(Sinopticos[0]['Sinopticos'])) + " Registros - Envio: " + str(r2),
            "SinopticosEventos" : str(len(TramaEventos[0]['Trama_Eventos'])) + " Registros - Envio: " + str(r3),
            "Mensajes" : str(len(Mensajes[0]['Trama_Mensajes'])) + " Registros - Envio: " + str(r4),
            "Trazados" : str(len(Trechos[0]['Trechos'])) + " Registros - Envio: " + str(r5),
            "Paradas" : str(len(Paradas[0]['Paradas'])) + " Registros - Envio: " + str(r6),
            #"Paradas" : str(len(Viajes[0]['Viajes'])) + " Registros - Envio: " + str(r7),                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     "Viajes": str(len(Viajes[0]['Viajes'])) + " Registros - Envio: " + str(r1),
            "SinopticoResumen" : str(len(Resumen[0]['Trama_Resumen_Sinoptico'])) + " Registros - Envio: " + str(r8)
        }
    )
    
    data2 = datetime.today()
    diff = data2 - data1
    seconds = diff.seconds
    hours = int(diff.seconds // (60 * 60))
    mins = int((diff.seconds // 60) % 60)
    seconds = (seconds % 60)
    print('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +' Segundos: ' +  str(seconds) )
    #DataCoordenadas.InsertLog('GetAllJson', str('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +' Segundos: ' +  str(seconds)))
    return jsonify(data_json)

@app.route('/API/v1.0/GetUpdateData')
def GetUpdateData():

    global VAR_EXEC_UPDATE
    
    try:
        if VAR_EXEC_UPDATE is False:
            
            _thread.start_new_thread(update,())
            return "Operando"
        
        else:
            #Esta Ocupado    
            return "Ocupado"
    except Exception as ex:
        
        VAR_EXEC_UPDATE = False
        str_error = "Error al invocar el hilo rutas" + ex.__str__()
        print(str_error, file=sys.stderr)
        return str_error

def update():
    
    global VAR_EXEC_UPDATE
    VAR_EXEC_UPDATE = True
    
    global Parametros
    Parametros = DataCoordenadas.GetParametros()
    
    global Sinopticos
    Sinopticos = DataCoordenadas.getSinopticos()
    
    ParametrosSelection = DataCoordenadas.SelectPametros(Parametros, "trazados")
    
    global Dimension
    Dimension = DataCoordenadas.getPlaneCEv2(ParametrosSelection[2], ParametrosSelection[3])
    
    global Trechos_C 
    Trechos_C = DataCoordenadas.coordenadas_trechos()
    
    global  Sinopticos_for 
    Sinopticos_for = DataCoordenadas.getSinopticossql()
    
    global SinopticoIdList
    SinopticoIdList = DataCoordenadas.getAllSinopticosTrechos()
    
    global SinopticoIdListActive
    SinopticoIdListActive = DataCoordenadas.getAllSinopticosTrechosActive()
    
    global GeotabULRLIST
    GeotabULRLIST = DataCoordenadas.GetAllGeotabURL()
    
    global CondutorLIST
    CondutorLIST = DataCoordenadas.GetAllCondutorLIST()
    
    global CoordenadasParadasLIST
    CoordenadasParadasLIST = DataCoordenadas.getCoordenadasSinopticoList()
    
    global Parada_Info
    Parada_Info = DataCoordenadas.GetParadas()
    
    global CoordenadasTrazadoList
    CoordenadasTrazadoList = DataCoordenadas.getCoordenadasAll()
    
    global SinoticosTrazadosList
    SinoticosTrazadosList = DataCoordenadas.getSinopticoTrazadov2ALL()
    
    global EstatusList
    EstatusList = DataCoordenadas.getStatusList()
    
    global RutasList
    RutasList = DataCoordenadas.getRutas()
    
    global Trechos_MultiRuta_ID
    Trechos_MultiRuta_ID = DataCoordenadas.getAllTrechosMultiRuta()
    
    global Trechos_Trazados_list
    Trechos_Trazados_list = DataCoordenadas.getTrazadosGetList(Trechos_C)
    
    VAR_EXEC_UPDATE = False

@app.route('/API/v1.0/GetViajesPosSim')
def GetPosViajeSim():
    
    global VAR_EXEC_POSICION
    
    try:
        if VAR_EXEC_POSICION is False:
            
            _thread.start_new_thread(simulador,())
            return "Operando"
        
        else:
            #Esta Ocupado    
            return "Ocupado"
    except Exception as ex:
        
        VAR_EXEC_POSICION = False
        str_error = "Error al invocar el hilo rutas" + ex.__str__()
        print(str_error, file=sys.stderr)
        return str_error
    
@app.route('/API/v1.0/GetViajesPosSimOff')
def GetPosViajeSimOff():
    
    global VAR_EXEC_POSICION
    global VAR_ENCENDIDO
    try:
       
       VAR_ENCENDIDO = False
       return("Apagando Simulacion")
       
    except Exception as ex:
        
        VAR_EXEC_POSICION = False
        str_error = "Error al invocar el hilo rutas" + ex.__str__()
        print(str_error, file=sys.stderr)
        return str_error

@app.route('/API/v1.0/GetViajesPosSimOn')
def GetPosViajeSimOn():
    
    global VAR_EXEC_POSICION
    global VAR_ENCENDIDO
    try:
       
       VAR_ENCENDIDO = True
       return("Enciendiedo Simulacion Simulacion")
       
    except Exception as ex:
        
        VAR_EXEC_POSICION = False
        str_error = "Error al invocar el hilo rutas" + ex.__str__()
        print(str_error, file=sys.stderr)
        return str_error


def simulador():
    
    global VAR_EXEC_POSICION
    global VAR_ENCENDIDO
    global VAR_ENCENDIDO_LOG_CONSOLE
    global ViajesJson_cache
    try:
        
        while VAR_ENCENDIDO == True:
            VAR_EXEC_POSICION = True
            data1 = datetime.today()
    
            Viajes = GetViajesPosSim()
            ViajesJson_cache = None
            ViajesJson_cache = Viajes[0]
            
            data2 = datetime.today()
            diff = data2 - data1
            seconds = diff.seconds
            hours = int(diff.seconds // (60 * 60))
            mins = int((diff.seconds // 60) % 60)
            seconds = (seconds % 60)
            
            
            if(VAR_ENCENDIDO_LOG_CONSOLE):
                print('Generacion Completa Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +' Segundos: ' +  str(seconds) )
            
            result = EmitirJson_v1(Viajes[0], Viajes[1])
  
            data2 = datetime.today()
            diff = data2 - data1
            seconds = diff.seconds
            hours = int(diff.seconds // (60 * 60))
            mins = int((diff.seconds // 60) % 60)
            seconds = (seconds % 60)
            
            if(VAR_ENCENDIDO_LOG_CONSOLE):
                print('Simulador Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +' Segundos: ' +  str(seconds) )
            #DataCoordenadas.InsertLog('GetAllJson', str('Horas: ' + str(hours) +  ' Minutos: ' + str(mins) +' Segundos: ' +  str(seconds)))
            #time.sleep(2)
            VAR_EXEC_POSICION = False

    except Exception as ex:
        VAR_EXEC_POSICION = False
        print("ERROR AL EJECUTAR SIMULADOR: " + ex.__str__(),  file=sys.stderr)
        
@app.route('/API/v1.0/GetViajesPosSimJson')
def GetViajesPosSimJson():
    
    
    Viajes = GetViajesPosSim()
    Variable = Viajes[0]
    global ViajesJson_cache
    ViajesJson_cache = None
    ViajesJson_cache = Viajes[0]
    if len(Variable['Viajes']) > 0:
        result = EmitirJson_v1(Viajes[0], Viajes[1])
    
    return jsonify(Viajes[0])
    
def GetViajesPosSim():
    
    toEmit = "viajes"
    
    Scale = 5   
    
    global Parametros
    if len(Parametros) == 0:
        Parametros = DataCoordenadas.GetParametros()

    ParametrosSelection = DataCoordenadas.SelectPametros(Parametros, toEmit)
        
    global Dimension
    if len(Dimension) == 0:
        Dimension = DataCoordenadas.getPlaneCEv2(ParametrosSelection[2], ParametrosSelection[3])
    
    global ViajesJson_cache 
    if ParametrosSelection[7] == 0:
        ViajesJson_cache['Viajes'] = []
    count = 1
    
    Conexion = ""
    
    global VAR_ENCENDIDO_LOG_CONSOLE
    
    for v in ViajesJson_cache['Viajes']:
        
        Conexion = v['Conexion']
        
        if(VAR_ENCENDIDO_LOG_CONSOLE):
            print ("Simulacion Viajes Procesados=" + str(count) + " De " + str(len(ViajesJson_cache['Viajes'])) )
            count = count + 1
        
        if Conexion == "CONECTADO":
            
            Latitud_Actual = v['Latitud']
            Longitud_Actual = v['Longitud']
            Trecho_Id = v['Trecho_Id']
            Trazado_Id = v['Trazado_Id']
            Fecha_Actual = v['Fecha_Actual']
            Velocidad = v['Velocidad'] / 2.5
            #Velocidad = 150
            
            global SinopticoIdList
            if len(SinopticoIdList) != 0:
                SinopticoId = DataCoordenadas.GetSinopticosList(SinopticoIdList, Trecho_Id)
            
            else:
                SinopticoId = DataCoordenadas.getSinopticoTrechov2(Trecho_Id)

            for sinopticoItem in SinopticoId:
            
                Scale = 5 
            
                for i in Dimension:
                
                    if sinopticoItem == i.sinoptico_id:
                        obj_SEC = SinocticoEC.SinopticoEC()
                        obj_SEC.sinoptico_id = int(sinopticoItem)
                        obj_SEC.latitud_min = i.latitud_min
                        obj_SEC.longitud_min = i.longitud_min
                        obj_SEC.proporcion_lat = i.proporcion_lat
                        obj_SEC.proporcion_long = i.proporcion_long
                        obj_SEC.size = i.size
                
                if obj_SEC.size == 1:
                    Scale = 6
                
            
                global CoordenadasTrazadoList
                if len(CoordenadasTrazadoList) != 0:
                    Coordenadas_t = DataCoordenadas.getCoordenadasAllTrecho(CoordenadasTrazadoList, Trazado_Id)
                
                else:
                    Coordenadas_t = DataCoordenadas.getCoordenadas(Trazado_Id)
                
                Distancia_100 = Coordenadas_t[len(Coordenadas_t) - 1].DistanciaAcumulada
                Distancia_Porcent = 0
                
                ListaUnica = []
                lista_nueva = []
                            
                for i in Coordenadas_t:
                    a = float(i.LATITUD)
                    #Distancia_100 = i.DistanciaAcumulada
                    
                    if a not in ListaUnica:
                        obj_Coordenadas_a = Coor.Coordenadas()
                        obj_Coordenadas_a.Secuencia = i.SEQUENCE
                        obj_Coordenadas_a.Eje_Y = i.LATITUD
                        obj_Coordenadas_a.Eje_X = i.LONGITUD
                        obj_Coordenadas_a.DistanciaAcumulada = i.DistanciaAcumulada

                        lista_nueva.append(obj_Coordenadas_a)
                        ListaUnica.append(i.LATITUD)
            
                ListaDeDistancias = []

                pos = 0
            
                for vp in v['Sinoptico_Coordenadas']:
                    MenorDistancia = 0
                    if obj_SEC.sinoptico_id == vp['Sinoptico_Id']:
                    
                        pos = CalculoDistancia(lista_nueva, Latitud_Actual, Longitud_Actual, Fecha_Actual, Velocidad)
                        Distancia_Porcent = lista_nueva[pos].DistanciaAcumulada
                    #print ("la distancia mas pequeña esta en la posicion")
                    #print (pos)
                    
                        Distanca_Porcentaje = 100 * Distancia_Porcent  / Distancia_100

                        Nueva_Latitud_Actual = lista_nueva[pos].Eje_Y
                        Nueva_Longitud_Actual = lista_nueva[pos].Eje_X
                        v['Trecho_Porcentaje'] = Distanca_Porcentaje
                        vp['Eje_Y'] = int(ParametrosSelection[4]) +  (int(ParametrosSelection[2]) - ((float(Nueva_Latitud_Actual)  - obj_SEC.latitud_min) / obj_SEC.proporcion_lat))
                        vp['Eje_X'] = int(ParametrosSelection[Scale]) + ((float(Nueva_Longitud_Actual) - obj_SEC.longitud_min) / obj_SEC.proporcion_long)

                        v['Latitud'] = Nueva_Latitud_Actual
                        v['Longitud'] = Nueva_Longitud_Actual
            
    #result = EmitirJson(ViajesJson, toEmit, ParametrosSelection)
                    v['Fecha_Actual'] = str(datetime.today())
        
    return [ViajesJson_cache, toEmit, ParametrosSelection]

def CalculoDistancia(lista_nueva, Latitud_Actual, Longitud_Actual, Fecha_Actual, Velocidad):
    
    Nueva_Latitud_Actual = 0
    Nueva_Longitud_Actual = 0
    MenorDistancia = 0
    Lista = []
    
    for LastCoor in lista_nueva:
        
        distancia = sqrt((LastCoor.Eje_Y - Latitud_Actual) ** 2 + (LastCoor.Eje_X - Longitud_Actual) ** 2)
                        
        #obj_distancia= Coor.Coordenadas()
        #obj_distancia.Secuencia = pos
        #obj_distancia.Eje_Y = distancia
        Lista.append(distancia)
        #ListaDeDistancias.append(obj_distancia)
                   
        MenorDistancia = Lista[0]
        
    pos = 0
    posicion = 0
        #for distanciaList in ListaDeDistancias:
    
    for distanciaList in Lista:
        
        if distanciaList < MenorDistancia:
            MenorDistancia = distanciaList
            #pos = distanciaList.Secuencia
            pos = posicion
                        
        posicion = posicion + 1    

    
    try:
        Latitud = lista_nueva[pos].Eje_Y
        Longitud = lista_nueva[pos].Eje_X
                    
    except Exception as ex:
        print(str(ex))
        print(traceback.format_exc())
        Latitud =  vp['Eje_Y']
        Longitud = vp['Eje_X'] 
                    
    data2 = datetime.today()
    diff = data2 - datetime.strptime(Fecha_Actual, '%Y-%m-%d %H:%M:%S.%f')
    seconds = diff.seconds
    mins = int((diff.seconds // 60) % 60)
    cadena = str(mins) + '.' + str(seconds)
    time = float(cadena)
    dinstance = (Velocidad / time) / 100000
                    
    if Latitud > Latitud_Actual:
        Nueva_Latitud_Actual = Latitud - dinstance
                    
    if Latitud < Latitud_Actual:
        Nueva_Latitud_Actual = Latitud + dinstance
                    
    if Latitud == Latitud_Actual:
        Nueva_Latitud_Actual = Latitud + dinstance
                    
    if Longitud > Longitud_Actual:
        Nueva_Longitud_Actual = Longitud - dinstance
                    
    if Longitud < Longitud_Actual:
        Nueva_Longitud_Actual = Longitud + dinstance
                    
    if Longitud == Longitud_Actual:
        Nueva_Longitud_Actual = Longitud + dinstance
    
    Lista = []
      
    for LastCoor in lista_nueva:
        
        distancia = sqrt((LastCoor.Eje_Y - Nueva_Latitud_Actual) ** 2 + (LastCoor.Eje_X - Nueva_Longitud_Actual) ** 2)
                        
        #obj_distancia= Coor.Coordenadas()
        #obj_distancia.Secuencia = pos
        #obj_distancia.Eje_Y = distancia
        Lista.append(distancia)
        #ListaDeDistancias.append(obj_distancia)
                   
        MenorDistancia = Lista[0]
        
    pos = 0
    posicion = 0
        #for distanciaList in ListaDeDistancias:
    
    for distanciaList in Lista:
        
        if distanciaList < MenorDistancia:
            MenorDistancia = distanciaList
            #pos = distanciaList.Secuencia
            pos = posicion
                        
        posicion = posicion + 1    

    
    return pos

#Emitir a JSON
def EmitirJson(data_json, emity, PS):
    result = 0
    
    URL = ""
    URL = PS[0]
    #URL = "https://nodejs.sae.siiab.app/"
    URL = "https://nodejs.saeteam.dev/"
    SleepTime = 1
    SleepTime =  PS[1]
    
    global VAR_ENCENDIDO_LOG_CONSOLE

    try:

        sio = socketio.Client()
        
        if(VAR_ENCENDIDO_LOG_CONSOLE):
            print('Created socketio client')

        @sio.event
        def connect():
            print('connected to server')

        @sio.event
        def disconnect():
            print('disconnected from server')

        sio.connect(URL)
        
        if(VAR_ENCENDIDO_LOG_CONSOLE):
            print('SIO sid es: ', sio.sid)

        sio.emit(emity,data_json)

        sio.sleep(SleepTime)

        sio.disconnect()

        sio.wait()

        result = 1
        
        if(VAR_ENCENDIDO_LOG_CONSOLE):
            print("Termine")

        #DataCoordenadas.InsertLog(emity,str(json.dumps(data_json) ))

    except Exception as ex:
        print(str(ex))
        print(traceback.format_exc())
        result = 0
        #DataCoordenadas.InsertLog(emity,str(result))

    #return result
#Emitir a JSON

def EmitirJson_v1(data_json, emity):
    result = "Fail"
    
    #URL = "https://nodejs.saeteam.dev/"
    URL = "https://nodejs.sae.siiab.app/"
    global VAR_ENCENDIDO_LOG_CONSOLE
    try:

        sio = socketio.Client()
        
        
        if(VAR_ENCENDIDO_LOG_CONSOLE):
            print('Created socketio client')

        @sio.event
        def connect():
            print('connected to server')

        @sio.event
        def disconnect():
            print('disconnected from server')

        sio.connect(URL)
        
        
        if(VAR_ENCENDIDO_LOG_CONSOLE):
            print('SIO sid es: ', sio.sid)

        sio.emit(emity,data_json)

        sio.sleep(5)
        
        sio.disconnect()

        sio.wait()

        result = "OK"

    except Exception as ex:
        print(str(ex))
        print(traceback.format_exc())
        result = "Fail"

    return result
#Emitir a JSON

#Json Rutas (MULTIPLE QUERY)
def GetRutasv1():

    data_json = {}
    data_json["Rutas"] = []

    data = {}

    Rutas = DataCoordenadas.getRutas()

    toEmit = "rutas"
    
    global Parametros
    if len(Parametros) == 0:
        Parametros = DataCoordenadas.GetParametros()

    ParametrosSelection = DataCoordenadas.SelectPametros(Parametros, toEmit)
    count = 1
    for r in Rutas:
        
        global VAR_ENCENDIDO_LOG_CONSOLE
        if(VAR_ENCENDIDO_LOG_CONSOLE):
            print ("Rutas Procesadas=" + str(count) + " De " + str(len(Rutas)) + "")
            count = count + 1 
        
        try:
            data['Trechos'] = []
            Trechos = DataCoordenadas.getTrechos(r.ID)
            for t in Trechos:
                data["Trechos"].append(
                    {
                        "Trecho_Id": int(t.TRECHO_ID)
                    }
                )

            data['Sinoptico'] = []
            Sinopticos = DataCoordenadas.getSinopticos_ID_LIST(r.ID)
            for s in Sinopticos:
                data["Sinoptico"].append(
                    {
                        #"Sinoptico_Id": int(s.MULTIRUTA_ID)
                        "Sinoptico_Id": int(Sinopticos[s]['MULTIRUTA_ID'])
                    }
                )

            data_json["Rutas"].append(
                {   
                    'Ruta_Id': int(r.ID),
                    'Ruta_Desc': str(r.NAME).rstrip(),
                    'Ruta_Origen_Id': int(r.PARADA_INI),
  				    'Ruta_Origen_Desc': str(DataCoordenadas.Parada_Origen_Desc(r.PARADA_INI)).rstrip(),
  				    'Ruta_Destino_id': int(r.PARADA_FIN),
  				    'Ruta_Destino_Desc': str(DataCoordenadas.Parada_Destino_Desc(r.PARADA_FIN)).rstrip(),
                    'Trechos': data["Trechos"],
                    'Sinoptico': data['Sinoptico'],
                    #'Origen': "Local"
                }
            )

        except Exception as ex:
            print(str(ex))
            ##print(traceback.format_exc())

    #return json.dumps(data_json, indent=4)s
    
    #if len(data_json["Rutas"]) > 0:
    #result = EmitirJson(data_json, toEmit, ParametrosSelection)

    return [data_json, toEmit, ParametrosSelection]
#Json Rutas (MULTIPLE QUERY)

#Json Sinopticos (MULTIPLE QUERY)
def GetSinopticosv1():
    
    data_json = {}
    data_json["Sinopticos"] = []

    data = {}

    global Sinopticos
    if len(Sinopticos) == 0:
        Sinopticos = DataCoordenadas.getSinopticos()

    toEmit = "sinoptico"
    
    global Parametros
    if len(Parametros) == 0:
        Parametros = DataCoordenadas.GetParametros()

    ParametrosSelection = DataCoordenadas.SelectPametros(Parametros, toEmit)
    count = 1
    for s in Sinopticos:
        
        global VAR_ENCENDIDO_LOG_CONSOLE
        if(VAR_ENCENDIDO_LOG_CONSOLE):
            print ("Sinopticos Procesados=" + str(count) + " De " + str(len(Sinopticos)) + "")
            count = count + 1
        
        try:
            #data['Rutas'] = []
            data['Rutas'] = []
            Sinopticos_M = DataCoordenadas.getSinopticos_MC(s.ID)
            for m in Sinopticos_M:
                #data["Rutas"].append(
                data['Rutas'].append(
                    {
                        #'Ruta_Id': int(m.RUTA_ID)
                        'Ruta_Id': int(m.TRECHO_ID)
                    }
                )

    
            data_json["Sinopticos"].append(
                {
                    'Id': int(s.ID),
                    'Sinoptico': str(s.NAME).rstrip(),
                    #'Rutas': data["Rutas"]
                    'Rutas': data['Rutas']
                }
            )

        except Exception as ex:
            print(str(ex))
            print(traceback.format_exc())

    #if len(data_json["Sinopticos"]) > 0:
    #result = EmitirJson(data_json, toEmit, ParametrosSelection)
    return [data_json, toEmit, ParametrosSelection]
#Json Sinopticos (MULTIPLE QUERY)

#JSON TRAMA_EVENTOS
def GetTramaEventosv1():
    
    data_json = {}
    
    data = {}
        
    data_json["Trama_Eventos"] = []
    
    toEmit = "sinoptico_eventos"
    
    global Parametros
    if len(Parametros) == 0:
        Parametros = DataCoordenadas.GetParametros()
            
    ParametrosSelection = DataCoordenadas.SelectPametros(Parametros, toEmit)
    
    global Sinopticos
    if len(Sinopticos) == 0:
        Sinopticos = DataCoordenadas.getSinopticos()
    
    count = 1
    
    for s in Sinopticos:
        
        global VAR_ENCENDIDO_LOG_CONSOLE
        if(VAR_ENCENDIDO_LOG_CONSOLE):
            print ("Trama Eventos Procesados=" + str(count) + " De " + str(len(Sinopticos)) + "")
            count = count + 1
         
        try:
            
            Eventos = DataCoordenadas.GetEventos(s.ID)

            if len(Eventos) > 0:
                
                data['Eventos'] = []
                
                for e in Eventos:
                    
                    data['Eventos'].append(
                        {
                            "Descripcion": str(Eventos[e]['DESCRIPCION']).rstrip(),
                            "Fecha": str(DataCoordenadas.convertlocaldate(Eventos[e]['EVENTO_FECHA'])),
                            "Mapa": str(Eventos[e]['METADATA']).rstrip(),
                            #"Procesado": Eventos[e]['PROCESADO'],
                            #"Mostrado_En_Sinoptico": str(Eventos[e]['MOSTRADO_EN_SINOPTICO']),
                            "Autobus": int(str(Eventos[e]['AUTOBUS_ID'])),
                            "Conductor": DataCoordenadas.getCondutor(str(Eventos[e]['CONDUCTOR_ID'])),
                            "Ruta": DataCoordenadas.GetRutaName(str(Eventos[e]['RUTA_ID'])).rstrip(),
                            "Inicio": str(DataCoordenadas.convertlocaldate(Eventos[e]['FECHA_HORA_PROGRAMADA_SALIDA'])),
                            "Real": str(DataCoordenadas.convertlocaldate(Eventos[e]['FECHA_HORA_REAL_SALIDA'])),
                            "Fin": str(DataCoordenadas.convertlocaldate(Eventos[e]['FECHA_HORA_REAL_LLEGADA']))
                        }
                    )
                

                data_json["Trama_Eventos"].append(
                    {
                         "Sinoptico_Id": int(s.ID),
                         "Eventos" : data['Eventos']                    
                    }
                )
        
        except Exception as ex:
            print(str(ex))
            print(traceback.format_exc())
            DataCoordenadas.InsertLog(toEmit,str(ex))
                
    #result = EmitirJson(data_json, toEmit, ParametrosSelection)
    return [data_json, toEmit, ParametrosSelection]
#JSON TRAMA_EVENTOS

#JSON TRAMA_EVENTOS UNICO SINOPTICO
def GetTramaEventosSv1(Sinoptico):
    
    data_json = {}
    
    data = {}
        
    data_json["Trama_Eventos"] = []
    
    toEmit = "sinoptico_eventos"
    
    Sinopticos_S = []
    
    global Parametros
    if len(Parametros) == 0:
        Parametros = DataCoordenadas.GetParametros()
            
    ParametrosSelection = DataCoordenadas.SelectPametros(Parametros, toEmit)
    
    global Sinopticos
    if len(Sinopticos) == 0:
        Sinopticos = DataCoordenadas.getSinopticos()
    
    for s in Sinopticos:
        
        if s.ID == int(Sinoptico):
                Sinopticos_S.append(s)
    
    count = 1
    
    for s in Sinopticos_S:
        
        global VAR_ENCENDIDO_LOG_CONSOLE
        if(VAR_ENCENDIDO_LOG_CONSOLE):
            print ("Trama Eventos Procesados=" + str(count) + " De " + str(len(Sinopticos_S)) + "")
            count = count + 1
         
        try:
            
            Eventos = DataCoordenadas.GetEventos(s.ID)

            if len(Eventos) > 0:
                
                data['Eventos'] = []
                
                for e in Eventos:
                    
                    data['Eventos'].append(
                        {
                            "Descripcion": str(Eventos[e]['DESCRIPCION']).rstrip(),
                            "Fecha": str(DataCoordenadas.convertlocaldate(Eventos[e]['EVENTO_FECHA'])),
                            "Mapa": str(Eventos[e]['METADATA']).rstrip(),
                            #"Procesado": Eventos[e]['PROCESADO'],
                            #"Mostrado_En_Sinoptico": str(Eventos[e]['MOSTRADO_EN_SINOPTICO']),
                            "Autobus": int(str(Eventos[e]['AUTOBUS_ID'])),
                            "Conductor": DataCoordenadas.getCondutor(str(Eventos[e]['CONDUCTOR_ID'])),
                            "Ruta": DataCoordenadas.GetRutaName(str(Eventos[e]['RUTA_ID'])).rstrip(),
                            "Inicio": str(DataCoordenadas.convertlocaldate(Eventos[e]['FECHA_HORA_PROGRAMADA_SALIDA'])),
                            "Real": str(DataCoordenadas.convertlocaldate(Eventos[e]['FECHA_HORA_REAL_SALIDA'])),
                            "Fin": str(DataCoordenadas.convertlocaldate(Eventos[e]['FECHA_HORA_REAL_LLEGADA']))
                        }
                    )
                

                data_json["Trama_Eventos"].append(
                    {
                         "Sinoptico_Id": int(s.ID),
                         "Eventos" : data['Eventos']                    
                    }
                )
        
        except Exception as ex:
            print(str(ex))
            print(traceback.format_exc())
            #DataCoordenadas.InsertLog(toEmit,str(ex))
                
    #result = EmitirJson(data_json, toEmit, ParametrosSelection)
    return [data_json, toEmit, ParametrosSelection]
#JSON TRAMA_EVENTOS UNICO SINOPTICO

#JSON MENSAJES
def GetMensajesv1():
    
    data_json = {}
    data_json["Trama_Mensajes"] = []
    Sinoptico_Id = []
    data= {}

    toEmit = "mensajes"
    
    
    global Parametros
    if len(Parametros) == 0:
        Parametros = DataCoordenadas.GetParametros()
    

    ParametrosSelection = DataCoordenadas.SelectPametros(Parametros, toEmit)

    Mensajes = DataCoordenadas.getMensajesSQL()

    data["Mensajes_Recibidos"] = []
    data["Mensajes_Enviados"] = []
    global Trechos_MultiRuta_ID
    
    count = 1
    
    for m in  Mensajes:
        
        global VAR_ENCENDIDO_LOG_CONSOLE
        if(VAR_ENCENDIDO_LOG_CONSOLE):
            print ("Mensajes Procesados=" + str(count) + " De " + str(len(Mensajes)) + "")
            count = count + 1
        
        try:
            
            if m.TO_AUTOBUS == 1:
                
                
                if len(Trechos_MultiRuta_ID) != 0:
                    Sinoptico_Id = DataCoordenadas.getSinopticoTrechoSingleList(Trechos_MultiRuta_ID, m.TRECHO_ACTUAL_ID)
                else:
                    Sinoptico_Id = DataCoordenadas.getSinopticoTrechoSingleActive(m.TRECHO_ACTUAL_ID)
                    
                status = "No Entregado"

                if m.ESTADO == 1:
                    status = "Entregado"
            

                data["Mensajes_Recibidos_Data"]= []
                data["Mensajes_Recibidos_Data"].append(
                    {
                        "Mensaje": m.MSJ,
                        "Autobus": m.AUTOBUS,
                        "Fecha_Enviado": str(m.ENVIADO),
                        "Fecha_Entregado": str(m.ENTREGADO),
                        "Estatus": status
                    }
                )

                for siplist in Sinoptico_Id:
                    data["Mensajes_Recibidos"].append(
                        {
                            "Sinoptico_Id": siplist,
                            "Mensajes": data["Mensajes_Recibidos_Data"]
                        }
                    )

            else:
                
                if len(Trechos_MultiRuta_ID) != 0:
                    Sinoptico_Id = DataCoordenadas.getSinopticoTrechoSingleList(Trechos_MultiRuta_ID,m.TRECHO_ACTUAL_ID)
                else:
                    Sinoptico_Id = DataCoordenadas.getSinopticoTrechoSingleActive(m.TRECHO_ACTUAL_ID)
            
                status = "No Entregado"

                if m.ESTADO == 1:
                    status = "Entregado"
            

                data["Mensajes_Enviados_Data"]= []
                data["Mensajes_Enviados_Data"].append(
                    {
                        "Mensaje": m.MSJ,
                        "Autobus": m.AUTOBUS,
                        "Fecha_Enviado": str(m.ENVIADO),
                        "Fecha_Entregado": str(m.ENTREGADO),
                        "Estatus": status
                    }
                )

                for siplist in Sinoptico_Id:
                    data["Mensajes_Enviados"].append(
                        {
                            "Sinoptico_Id": siplist,
                            "Mensajes": data["Mensajes_Enviados_Data"]
                        }
                    )   
                
        except Exception as ex:
            print(str(ex))
            print(traceback.format_exc())
            #DataCoordenadas.InsertLog(toEmit,str(ex))
        
    data_json["Trama_Mensajes"].append(
        {
            "Mensajes_Recibidos": data["Mensajes_Recibidos"],
            "Mensajes_Enviados": data["Mensajes_Enviados"]
        }
    )
    
    #if len(data_json["Trama_Mensajes"]) > 0:
    #result = EmitirJson(data_json, toEmit, ParametrosSelection)    
    return [data_json, toEmit, ParametrosSelection]
#JSON MENSAJES

#JSON TRECHOS 
def GetTrechosv1():
    
    data_json = {}
    data_json["Trechos"] = []
    
    data= {}

    Scale = 5
    
    obj_SEC = SinocticoEC.SinopticoEC()
    
    toEmit = "trazados"
    
    global Parametros
    if len(Parametros) == 0:
        Parametros = DataCoordenadas.GetParametros()
    
    ParametrosSelection = DataCoordenadas.SelectPametros(Parametros, toEmit)
    
    global Dimension
    if len(Dimension) == 0:
        Dimension = DataCoordenadas.getPlaneCEv2(ParametrosSelection[2], ParametrosSelection[3])

    global Trechos_C
    if len(Trechos_C) == 0:
        Trechos_C = DataCoordenadas.coordenadas_trechos()   

    SinopticoId = 0
    
    x = 0
    count = 1
    for t in Trechos_C:
        #print (str(Trechos_C[t]['ID']))
        
        global VAR_ENCENDIDO_LOG_CONSOLE
        if(VAR_ENCENDIDO_LOG_CONSOLE):
            print ("Trechos Procesados=" + str(count) + " De " + str(len(Trechos_C)) + "")
            count = count + 1
        
        try:
            data["Trazado"] = []
        
            obj_Trechos = Trech.Trechos()
            obj_Trechos.Trecho_Id = int(Trechos_C[t]['ID'])
            obj_Trechos.Trecho_Desc = str(Trechos_C[t]['NAME']).rstrip()
            obj_Trechos.Trecho_Origen_Id = int(Trechos_C[t]['PARADA_INI'])
            obj_Trechos.Trecho_Origen_Desc = str(DataCoordenadas.Parada_Origen_Desc(Trechos_C[t]['PARADA_INI'])).rstrip()
            obj_Trechos.Trecho_Destino_id =  int(Trechos_C[t]['PARADA_FIN'])
            obj_Trechos.Trecho_Destino_Desc = str(DataCoordenadas.Parada_Destino_Desc(Trechos_C[t]['PARADA_FIN'])).rstrip()
            obj_Trechos.Trecho_Puntualidad = int(random.randint(1, 100))
            obj_Trechos.Trecho_Frecuencia = int(random.randint(1, 100))

            global Trechos_Trazados_list
            if len(Trechos_Trazados_list)!= 0:
                Trecho_Trazado = DataCoordenadas.getTrazadosList(Trechos_Trazados_list, str(Trechos_C[t]['ID']))
            else:
                Trecho_Trazado = DataCoordenadas.getTrazados(str(Trechos_C[t]['ID']))
            
            global ColorTrechosList
            if len(ColorTrechosList) != 0:
                Trecho_Color = DataCoordenadas.getColorTrechoList(ColorTrechosList, Trechos_C[t]['ID'])
            else:
                Trecho_Color = DataCoordenadas.getColorTrecho(str(Trechos_C[t]['ID']))

            for y in Trecho_Trazado:
                
                try:
                    
                    obj_Trazados = Traz.Trazados()
                    obj_Trazados.Trazado_Id = int(str(y.ID))
                    obj_Trazados.Trazado_Color = Trecho_Color.strip()
                    obj_Trazados.Trazado_Version = random.randint(1, 10)
                    obj_Trazados.Trazado_Desc = str(y.NAME).rstrip()
                    obj_Trazados.Trazado_Origen_Id = int(str(Trechos_C[t]['PARADA_INI']))
                    obj_Trazados.Trazado_Origen_Desc = str(DataCoordenadas.Parada_Origen_Desc(Trechos_C[t]['PARADA_INI'])).rstrip()
                    obj_Trazados.Trazado_Destino_id = int(str(Trechos_C[t]['PARADA_FIN']))
                    obj_Trazados.Trazado_Destino_Desc = str(DataCoordenadas.Parada_Destino_Desc(Trechos_C[t]['PARADA_FIN'])).rstrip()

                    
                    global SinoticosTrazadosList
                    if len(SinoticosTrazadosList) != 0:
                        SinopticoId = DataCoordenadas.getSinopticoTrazadov2Trecho(SinoticosTrazadosList, y.ID)
                    else:
                        SinopticoId = DataCoordenadas.getSinopticoTrazadov2(y.ID)

               
                    for sinopticoItem in SinopticoId:
                
                        if sinopticoItem != 0:
                            Scale = 5 
                            x = 1
                            for i in Dimension:
                                if sinopticoItem == i.sinoptico_id:
                                    obj_SEC = SinocticoEC.SinopticoEC()
                                    obj_SEC.sinoptico_id = int(sinopticoItem)
                                    obj_SEC.latitud_min = i.latitud_min
                                    obj_SEC.longitud_min = i.longitud_min
                                    obj_SEC.proporcion_lat = i.proporcion_lat
                                    obj_SEC.proporcion_long = i.proporcion_long
                                    obj_SEC.size = i.size
                
                            if obj_SEC.size == 1:
                                Scale = 6

                            data['Coordenadas'] = []

                            global CoordenadasTrazadoList
                            if len(CoordenadasTrazadoList) != 0:
                                Coordenadas_t = DataCoordenadas.getCoordenadasAllTrecho(CoordenadasTrazadoList, y.ID)
                            else:
                                Coordenadas_t = DataCoordenadas.getCoordenadas(y.ID)

                            ListaCoordenadas = []
                            
                            for z in Coordenadas_t:
                                obj_Coordenadas = Coor.Coordenadas()
                                obj_Coordenadas.Secuencia = str(z.SEQUENCE)
                                obj_Coordenadas.Eje_Y = float(ParametrosSelection[4]) + (float(ParametrosSelection[2]) - ((float(z.LATITUD)  - obj_SEC.latitud_min) / obj_SEC.proporcion_lat ))
                                obj_Coordenadas.Eje_X = float(ParametrosSelection[Scale]) + ((float(z.LONGITUD) - obj_SEC.longitud_min) / obj_SEC.proporcion_long )
                                ListaCoordenadas.append(obj_Coordenadas)
                            
                            ListaUnica = []
                            lista_nueva = []
                            
                            for i in ListaCoordenadas:
                                a = float(i.Eje_X)
                                
                                if a not in ListaUnica:
                                    obj_Coordenadas_a = Coor.Coordenadas()
                                    obj_Coordenadas_a.Secuencia = i.Secuencia
                                    obj_Coordenadas_a.Eje_Y = i.Eje_Y
                                    obj_Coordenadas_a.Eje_X = i.Eje_X
                                    
                                    lista_nueva.append(obj_Coordenadas_a)
                                    ListaUnica.append(i.Eje_X)
                                    
                                    
                                
                            for i in lista_nueva:
                                data['Coordenadas'].append(
                                    {
                                        'Secuencia': int(i.Secuencia),
                                        'Eje_X': float(i.Eje_X),
                                        'Eje_Y': float(i.Eje_Y),
                                        'Color': obj_Trazados.Trazado_Color
                                    }
                                )
                                
                        else:
                            x = 0
                
                        data['Trazado'].append({
                            'Trazado_Id': obj_Trazados.Trazado_Id,
                            'Trazado_Color': obj_Trazados.Trazado_Color,
                            'Trazado_Version': obj_Trazados.Trazado_Version,
                            'Trazado_Desc': obj_Trazados.Trazado_Desc,
                            'Trazado_Origen_Id': obj_Trazados.Trazado_Origen_Id,
                            'Trazado_Origen_Desc': obj_Trazados.Trazado_Origen_Desc,
                            'Trazado_Destino_id': obj_Trazados.Trazado_Destino_id,
                            'Trazado_Destino_Desc': obj_Trazados.Trazado_Destino_Desc,
                            'Sinoptico_Id': int(sinopticoItem),
                            'Coordenadas': data['Coordenadas']
                        })
                    
                except Exception as ex:
                    print(traceback.format_exc())
                    print(str(ex))
                
           
            
        
            DataRT = DataCoordenadas.getRutasTrecho(obj_Trechos.Trecho_Id)
            if x != 0: 
                
                data_json["Trechos"].append({
                    'Trecho_Id': obj_Trechos.Trecho_Id,
                    'Trecho_Desc': obj_Trechos.Trecho_Desc,
                    'Trecho_Origen_Id': obj_Trechos.Trecho_Origen_Id,
                    'Trecho_Origen_Desc': obj_Trechos.Trecho_Origen_Desc,
                    'Trecho_Destino_id': obj_Trechos.Trecho_Destino_id,
                    'Trecho_Destino_Desc': obj_Trechos.Trecho_Destino_Desc,
                    'Trecho_Puntualidad': obj_Trechos.Trecho_Puntualidad,
                    'Trecho_Frecuencia': obj_Trechos.Trecho_Frecuencia,
                    "Sinoptico": DataRT[1],
                    'Rutas': DataRT[0],
                    'Trazados': data['Trazado']
                })
                
                
                
            
                        
        except Exception as ex:
            print(traceback.format_exc())
            print(str(ex))

    #if len(data_json["Trechos"]) > 0:
    #result = EmitirJson(data_json, toEmit, ParametrosSelection)
    return [data_json, toEmit, ParametrosSelection]
#JSON TRECHOS

#JSON TRECHOS UNICO SINOPTICO
def GetTrechosSv1(Sinoptico):
    
    data_json = {}
    data_json["Trechos"] = []
        
    data= {}

    Scale = 5
    
    obj_SEC = SinocticoEC.SinopticoEC()
    
    toEmit = "trazados"
    
    global Parametros
    if len(Parametros) == 0:
        Parametros = DataCoordenadas.GetParametros()
    
    ParametrosSelection = DataCoordenadas.SelectPametros(Parametros, toEmit)
    
    global Dimension
    if len(Dimension) == 0:
        Dimension = DataCoordenadas.getPlaneCEv2(ParametrosSelection[2], ParametrosSelection[3])

    
    Trechos_C = DataCoordenadas.coordenadas_trechos_s(Sinoptico)   

    SinopticoId = 0
    
    x = 0
    count = 1
    for t in Trechos_C:
        #print (str(Trechos_C[t]['ID']))
        
        global VAR_ENCENDIDO_LOG_CONSOLE
        if(VAR_ENCENDIDO_LOG_CONSOLE):
            print ("Trechos Procesados=" + str(count) + " De " + str(len(Trechos_C)) + "")
            count = count + 1
        
        try:
            data["Trazado"] = []
        
            obj_Trechos = Trech.Trechos()
            obj_Trechos.Trecho_Id = int(Trechos_C[t]['ID'])
            obj_Trechos.Trecho_Desc = str(Trechos_C[t]['NAME']).rstrip()
            obj_Trechos.Trecho_Origen_Id = int(Trechos_C[t]['PARADA_INI'])
            obj_Trechos.Trecho_Origen_Desc = str(DataCoordenadas.Parada_Origen_Desc(Trechos_C[t]['PARADA_INI'])).rstrip()
            obj_Trechos.Trecho_Destino_id =  int(Trechos_C[t]['PARADA_FIN'])
            obj_Trechos.Trecho_Destino_Desc = str(DataCoordenadas.Parada_Destino_Desc(Trechos_C[t]['PARADA_FIN'])).rstrip()
            obj_Trechos.Trecho_Puntualidad = int(random.randint(1, 100))
            obj_Trechos.Trecho_Frecuencia = int(random.randint(1, 100))

            global Trechos_Trazados_list
            if len(Trechos_Trazados_list)!= 0:
                Trecho_Trazado = DataCoordenadas.getTrazadosList(Trechos_Trazados_list, str(Trechos_C[t]['ID']))
            else:
                Trecho_Trazado = DataCoordenadas.getTrazados(str(Trechos_C[t]['ID']))
            
            global ColorTrechosList
            if len(ColorTrechosList) != 0:
                Trecho_Color = DataCoordenadas.getColorTrechoList(ColorTrechosList, Trechos_C[t]['ID'])
            else:
                Trecho_Color = DataCoordenadas.getColorTrecho(str(Trechos_C[t]['ID']))

            for y in Trecho_Trazado:
                
                try:
                    
                    obj_Trazados = Traz.Trazados()
                    obj_Trazados.Trazado_Id = int(str(y.ID))
                    obj_Trazados.Trazado_Color = Trecho_Color.strip()
                    obj_Trazados.Trazado_Version = random.randint(1, 10)
                    obj_Trazados.Trazado_Desc = str(y.NAME).rstrip()
                    obj_Trazados.Trazado_Origen_Id = int(str(Trechos_C[t]['PARADA_INI']))
                    obj_Trazados.Trazado_Origen_Desc = str(DataCoordenadas.Parada_Origen_Desc(Trechos_C[t]['PARADA_INI'])).rstrip()
                    obj_Trazados.Trazado_Destino_id = int(str(Trechos_C[t]['PARADA_FIN']))
                    obj_Trazados.Trazado_Destino_Desc = str(DataCoordenadas.Parada_Destino_Desc(Trechos_C[t]['PARADA_FIN'])).rstrip()

                    
                    global SinoticosTrazadosList
                    if len(SinoticosTrazadosList) != 0:
                        SinopticoId = DataCoordenadas.getSinopticoTrazadov2Trecho(SinoticosTrazadosList, y.ID)
                    else:
                        SinopticoId = DataCoordenadas.getSinopticoTrazadov2(y.ID)

               
                    for sinopticoItem in SinopticoId:
                
                        if sinopticoItem != 0:
                            Scale = 5 
                            x = 1
                            for i in Dimension:
                                if sinopticoItem == i.sinoptico_id:
                                    obj_SEC = SinocticoEC.SinopticoEC()
                                    obj_SEC.sinoptico_id = int(sinopticoItem)
                                    obj_SEC.latitud_min = i.latitud_min
                                    obj_SEC.longitud_min = i.longitud_min
                                    obj_SEC.proporcion_lat = i.proporcion_lat
                                    obj_SEC.proporcion_long = i.proporcion_long
                                    obj_SEC.size = i.size
                
                            if obj_SEC.size == 1:
                                Scale = 6

                            data['Coordenadas'] = []

                            global CoordenadasTrazadoList
                            if len(CoordenadasTrazadoList) != 0:
                                Coordenadas_t = DataCoordenadas.getCoordenadasAllTrecho(CoordenadasTrazadoList, y.ID)
                            else:
                                Coordenadas_t = DataCoordenadas.getCoordenadas(y.ID)

                            ListaCoordenadas = []
                            
                            for z in Coordenadas_t:
                                obj_Coordenadas = Coor.Coordenadas()
                                obj_Coordenadas.Secuencia = str(z.SEQUENCE)
                                obj_Coordenadas.Eje_Y = float(ParametrosSelection[4]) + (float(ParametrosSelection[2]) - ((float(z.LATITUD)  - obj_SEC.latitud_min) / obj_SEC.proporcion_lat ))
                                obj_Coordenadas.Eje_X = float(ParametrosSelection[Scale]) + ((float(z.LONGITUD) - obj_SEC.longitud_min) / obj_SEC.proporcion_long )
                                ListaCoordenadas.append(obj_Coordenadas)
                            
                            ListaUnica = []
                            lista_nueva = []
                            
                            for i in ListaCoordenadas:
                                a = float(i.Eje_X)
                                
                                if a not in ListaUnica:
                                    obj_Coordenadas_a = Coor.Coordenadas()
                                    obj_Coordenadas_a.Secuencia = i.Secuencia
                                    obj_Coordenadas_a.Eje_Y = i.Eje_Y
                                    obj_Coordenadas_a.Eje_X = i.Eje_X
                                    
                                    lista_nueva.append(obj_Coordenadas_a)
                                    ListaUnica.append(i.Eje_X)
                                    
                                    
                                
                            for i in lista_nueva:
                                data['Coordenadas'].append(
                                    {
                                        'Secuencia': int(i.Secuencia),
                                        'Eje_X': float(i.Eje_X),
                                        'Eje_Y': float(i.Eje_Y),
                                        'Color': obj_Trazados.Trazado_Color
                                    }
                                )
                                
                        else:
                            x = 0
                
                        data['Trazado'].append({
                            'Trazado_Id': obj_Trazados.Trazado_Id,
                            'Trazado_Color': obj_Trazados.Trazado_Color,
                            'Trazado_Version': obj_Trazados.Trazado_Version,
                            'Trazado_Desc': obj_Trazados.Trazado_Desc,
                            'Trazado_Origen_Id': obj_Trazados.Trazado_Origen_Id,
                            'Trazado_Origen_Desc': obj_Trazados.Trazado_Origen_Desc,
                            'Trazado_Destino_id': obj_Trazados.Trazado_Destino_id,
                            'Trazado_Destino_Desc': obj_Trazados.Trazado_Destino_Desc,
                            'Sinoptico_Id': int(sinopticoItem),
                            'Coordenadas': data['Coordenadas']
                        })
                    
                except Exception as ex:
                    print(traceback.format_exc())
                    print(str(ex))
                
           
            
        
            DataRT = DataCoordenadas.getRutasTrecho(obj_Trechos.Trecho_Id)
            if x != 0: 
                
                data_json["Trechos"].append({
                    'Trecho_Id': obj_Trechos.Trecho_Id,
                    'Trecho_Desc': obj_Trechos.Trecho_Desc,
                    'Trecho_Origen_Id': obj_Trechos.Trecho_Origen_Id,
                    'Trecho_Origen_Desc': obj_Trechos.Trecho_Origen_Desc,
                    'Trecho_Destino_id': obj_Trechos.Trecho_Destino_id,
                    'Trecho_Destino_Desc': obj_Trechos.Trecho_Destino_Desc,
                    'Trecho_Puntualidad': obj_Trechos.Trecho_Puntualidad,
                    'Trecho_Frecuencia': obj_Trechos.Trecho_Frecuencia,
                    "Sinoptico": DataRT[1],
                    'Rutas': DataRT[0],
                    'Trazados': data['Trazado']
                })
                
                
                        
        except Exception as ex:
            print(traceback.format_exc())
            print(str(ex))

    #if len(data_json["Trechos"]) > 0:
    #result = EmitirJson(data_json, toEmit, ParametrosSelection)
    return [data_json, toEmit, ParametrosSelection]
#JSON TRECHOS UNICO SINOPTICO

#JSON PARADAS (MULTIPLE QUERY)
def GetParadasTrazadov1():    
    data_json = {}
    data_json["Paradas"] = []

    data= {}
    Latitud = 0
    Longitud = 0
    Secuencia = 0
    Paradas_C = []

    Frecuency = 0
    latitud_min = 1
    proporcion_lat = 0.10
    longitud_min = 1
    proporcion_long = 0.10

    toEmit = "paradas"
    Scale = 5
    
    global Parametros
    if len(Parametros) == 0:
        Parametros = DataCoordenadas.GetParametros()
    
    ParametrosSelection = DataCoordenadas.SelectPametros(Parametros, toEmit)
    
    global Dimension
    if len(Dimension) == 0:
        Dimension = DataCoordenadas.getPlaneCEv2(ParametrosSelection[2], ParametrosSelection[3])

    
    ParametrosSelection = DataCoordenadas.SelectPametros(Parametros, toEmit)
    
    ParametrosTop = DataCoordenadas.SelectPametrosTop(Parametros, toEmit)

    global Parada_Info
    if len(Parada_Info) == 0:
        Parada_Info = DataCoordenadas.GetParadas()
    
    global CoordenadasParadasLIST
    global VAR_ENCENDIDO_LOG_CONSOLE
    
    count = 1
    
    for t in Parada_Info:
        
        
        if(VAR_ENCENDIDO_LOG_CONSOLE):
            print ("Paradas Procesados=" + str(count) + " De " + str(len(Parada_Info)) + "")
            count = count + 1
        
        if len(CoordenadasParadasLIST) != 0:
            Parada_Coordenada = DataCoordenadas.getCoordenadasSinopticoM(CoordenadasParadasLIST, t.ID)
        else:    
            Parada_Coordenada = DataCoordenadas.GetParadacoordenada(t.ID)
        
        if Parada_Coordenada == None:
            Latitud = 0
            Longitud = 0
            Secuencia = 0
        else:
            for pc in Parada_Coordenada:
                Latitud = pc.LATITUD
                Longitud = pc.LONGITUD
                Secuencia = pc.SEQUENCE

        datas_three = DataCoordenadas.getRutasParada(t.ID)

        data["Sinoptico_Coordenadas"] = []

        for l in datas_three[2]:
            for i in Dimension:
                
                Scale = 5 
                
                if i.sinoptico_id == l['Sinoptico_Id']:
                    
                    #global CoordenadasParadasLIST
                    if len(CoordenadasParadasLIST) != 0:
                        Sinoptico_MC = DataCoordenadas.getCoordenadasSinopticoU(CoordenadasParadasLIST, t.ID)
                    else:    
                        Sinoptico_MC = DataCoordenadas.getCoordenadasSinoptico(t.ID)
                        
                    if Sinoptico_MC != None:
                        if Sinoptico_MC.ID != 0:
                            if i.size == 1:
                                Scale = 6
                                
                            Y = 0
                            X = 0
                        
                            try:
                                
                                Y = int(ParametrosSelection[4]) + (int(ParametrosSelection[2]) - ((float(str(Sinoptico_MC.LATITUD))  - i.latitud_min) / i.proporcion_lat ))
                                X = int(ParametrosSelection[Scale]) + ((float(str(Sinoptico_MC.LONGITUD)) - i.longitud_min) / i.proporcion_long)
                            
                            except Exception as ex:
                                X = 0
                                Y = 0
                                print("Error ")
                            
                                
                            data["Sinoptico_Coordenadas"].append(
                                {
                                    "Sinoptico_Id": int(l['Sinoptico_Id']),
                                    "Parada_Y": Y,
                                    "Parada_X": X 
                                }
                            )
                            
                            latitud_min = i.latitud_min
                            proporcion_lat = i.proporcion_lat
                            longitud_min = i.longitud_min
                            proporcion_long = i.proporcion_long
                            break
                    else:
                        for i in Dimension:
                            latitud_min = i.latitud_min
                            proporcion_lat = i.proporcion_lat
                            longitud_min = i.longitud_min
                            proporcion_long = i.proporcion_long
                            break
                                #obj_Coordenadas.Eje_X = str( (float(z.LATITUD)  - latitud_min) / proporcion_lat  )
                                #obj_Coordenadas.Eje_Y = str( (float(z.LONGITUD) - longitud_min) / proporcion_long  ) 
        
        data["Autobuses_En_Parada"] = []

        data["Autobuses_Proximas_Llegadas"] = []
        
        data["Autobuses_Proximas_Salidas"] = []

        data["Autobuses_Anteriores"] = []
        
        for s in datas_three[2]:
            
            #Bus En Paradas
            
            Bus_Parada = DataCoordenadas.getAutobuses_Parada(t.ID, ParametrosTop[1], s['Sinoptico_Id'])
            
            data["data"] = []
            
            for l in Bus_Parada:
                data["data"].append(
                    {
                        "Autobus": int(Bus_Parada[l]['AUTOBUS'])
                    }
                )
        
            data["Autobuses_En_Parada"].append(
                {
                    "Sinoptico_Id" : s['Sinoptico_Id'],
                    "Data": data["data"]   
                }
            )
            
            #Bus Proximas Legadas
            
            Bus_Proximas = DataCoordenadas.getAutobuses_Proximas(t.ID, ParametrosTop[2], s['Sinoptico_Id'])
            
            data["data"] = []
            
            for l in Bus_Proximas:
                data["data"].append(
                    {
                        "Autobus": int(Bus_Proximas[l]['AUTOBUS']),
                        "Llegada": str(DataCoordenadas.convertlocaldate(Bus_Proximas[l]['ETA']))
                    }
                )
        
            data["Autobuses_Proximas_Llegadas"].append(
                {
                    "Sinoptico_Id" : s['Sinoptico_Id'],
                    "Data": data["data"]   
                }
            )
            
            #Bus Proximas salidas
            
            Bus_Proximas = DataCoordenadas.getAutobuses_Proximas_Salidas(t.ID, ParametrosTop[3], s['Sinoptico_Id'])
            
            data["Data"] = []

            for l in Bus_Proximas:
                data["Data"].append(
                    {
                        "Autobus": int(Bus_Proximas[l]['AUTOBUS']),
                        "Salida": str(DataCoordenadas.convertlocaldate(Bus_Proximas[l]['FECHA_HORA_PROGRAMADA_SALIDA']))
                    }
                )
                
            
            data["Autobuses_Proximas_Salidas"].append(
                {
                    "Sinoptico_Id" : s['Sinoptico_Id'],
                    "Data": data["Data"]   
                }
            )
            
            #Bus Anteriores
            
            Bus_Anteriores = DataCoordenadas.getAutobuses_Anteriores(t.ID, ParametrosTop[0], s['Sinoptico_Id'])
            
            data["Data"] = []
            
            Frecuency = 0 
            
            for l in Bus_Anteriores:
                
                
                data["Data"].append(
                    {
                        "Autobus": int(Bus_Anteriores[l]['AUTOBUS']),
                        "Programada": str(DataCoordenadas.convertlocaldate(Bus_Anteriores[l]['FECHA_PROGRAMADA'])),
                        "Real": str(DataCoordenadas.convertlocaldate(Bus_Anteriores[l]['FECHA_COLISION'])),
                        "Diferencia": int(Bus_Anteriores[l]['PUNTUALIDAD_LLEGADA']),
                        "Frecuencia": int(Bus_Anteriores[l]['FRECUENCIA_LLEGADA']) 
                    }
                )
                
                
            Frecuency = DataCoordenadas.getParadaFrecuencia(t.ID, ParametrosTop[0], s['Sinoptico_Id'])
                
            data["Autobuses_Anteriores"].append(
                 {
                   "Sinoptico_Id": s['Sinoptico_Id'],
                    "Data" : data["Data"]
                 }
            )   

        Y = 0
        X = 0
        
        try:
            Y = int(ParametrosSelection[4]) +  (int(ParametrosSelection[2]) - ( (float(Latitud)  - latitud_min) / proporcion_lat  ))
            X = int(ParametrosSelection[Scale]) + ((float(Longitud) - longitud_min) / proporcion_long  )
                            
        except Exception as ex:
            X = 0
            Y = 0
            print("Error ")
        
        #Date = DataCoordenadas.GetDate()
        data_json["Paradas"].append({
            #"FROM" : str(Cloud) + " - "+  str(Date),
            'Parada_Id' :  int(t.ID),
            'Parada_Desc' : str(t.NAME).rstrip(),
            'Parada_Y' : Y,
            'Parada_X' : X,
            'Color' : DataCoordenadas.getColor(t.COLOR_ID).rstrip(),
            'Parada_Puntualidad' : (random.randint(0,10)),
            'Parada_Frecuencia' : int(Frecuency),
            'No_Autobuses_En_Parada': len(data["Autobuses_En_Parada"]),
            'Rutas': datas_three[0],    
            'Trecho_Id': int(0), 
            'Clave': str(t.CLAVE).rstrip(),  
            'Trechos': datas_three[1],
            'Autobuses_En_Parada': data["Autobuses_En_Parada"],
            'Autobuses_Proximas_Llegadas': data["Autobuses_Proximas_Llegadas"],
            'Autobuses_Anteriores': data["Autobuses_Anteriores"],
            'Autobuses_Proximas_Salidas': data["Autobuses_Proximas_Salidas"],
            'Sinoptico': datas_three[2],
            'Sinoptico_Coordenadas': data["Sinoptico_Coordenadas"]
        })

    
    #if len(data_json["Paradas"]) > 0:
    #result = EmitirJson(data_json, toEmit, ParametrosSelection)
    return [data_json, toEmit, ParametrosSelection]
#JSON PARADAS (MULTIPLE QUERY)

#JSON PARADAS (MULTIPLE QUERY) UNICO SINOPTICO
def GetParadasTrazadoSv1(Sinoptico):    
    data_json = {}
    data_json["Paradas"] = []

    data= {}
    Latitud = 0
    Longitud = 0
    Secuencia = 0
    Paradas_C = []

    Frecuency = 0
    latitud_min = 1
    proporcion_lat = 0.10
    longitud_min = 1
    proporcion_long = 0.10

    toEmit = "paradas"
    Scale = 5
    
    global Parametros
    if len(Parametros) == 0:
        Parametros = DataCoordenadas.GetParametros()
    
    ParametrosSelection = DataCoordenadas.SelectPametros(Parametros, toEmit)
    
    global Dimension
    if len(Dimension) == 0:
        Dimension = DataCoordenadas.getPlaneCEv2(ParametrosSelection[2], ParametrosSelection[3])

    
    ParametrosSelection = DataCoordenadas.SelectPametros(Parametros, toEmit)
    
    ParametrosTop = DataCoordenadas.SelectPametrosTop(Parametros, toEmit)

    
    Parada_Info = DataCoordenadas.GetParadasSingle(Sinoptico)
    
    global CoordenadasParadasLIST
    global VAR_ENCENDIDO_LOG_CONSOLE
    
    count = 1
    
    for t in Parada_Info:
        
        
        if(VAR_ENCENDIDO_LOG_CONSOLE):
            print ("Paradas Procesados=" + str(count) + " De " + str(len(Parada_Info)) + "")
            count = count + 1
        
        if len(CoordenadasParadasLIST) != 0:
            Parada_Coordenada = DataCoordenadas.getCoordenadasSinopticoM(CoordenadasParadasLIST, Parada_Info[t]['ID'])
        else:    
            Parada_Coordenada = DataCoordenadas.GetParadacoordenada(Parada_Info[t]['ID'])
        
        if Parada_Coordenada == None:
            Latitud = 0
            Longitud = 0
            Secuencia = 0
        else:
            for pc in Parada_Coordenada:
                Latitud = pc.LATITUD
                Longitud = pc.LONGITUD
                Secuencia = pc.SEQUENCE

        datas_three = DataCoordenadas.getRutasParada(Parada_Info[t]['ID'])

        data["Sinoptico_Coordenadas"] = []

        for l in datas_three[2]:
            for i in Dimension:
                
                Scale = 5 
                
                if i.sinoptico_id == l['Sinoptico_Id']:
                    
                    #global CoordenadasParadasLIST
                    if len(CoordenadasParadasLIST) != 0:
                        Sinoptico_MC = DataCoordenadas.getCoordenadasSinopticoU(CoordenadasParadasLIST, Parada_Info[t]['ID'])
                    else:    
                        Sinoptico_MC = DataCoordenadas.getCoordenadasSinoptico(Parada_Info[t]['ID'])
                        
                    if Sinoptico_MC != None:
                        if Sinoptico_MC.ID != 0:
                            if i.size == 1:
                                Scale = 6
                                
                            Y = 0
                            X = 0
                        
                            try:
                                
                                Y = int(ParametrosSelection[4]) + (int(ParametrosSelection[2]) - ((float(str(Sinoptico_MC.LATITUD))  - i.latitud_min) / i.proporcion_lat ))
                                X = int(ParametrosSelection[Scale]) + ((float(str(Sinoptico_MC.LONGITUD)) - i.longitud_min) / i.proporcion_long)
                            
                            except Exception as ex:
                                X = 0
                                Y = 0
                                print("Error ")
                            
                                
                            data["Sinoptico_Coordenadas"].append(
                                {
                                    "Sinoptico_Id": int(l['Sinoptico_Id']),
                                    "Parada_Y": Y,
                                    "Parada_X": X 
                                }
                            )
                            
                            latitud_min = i.latitud_min
                            proporcion_lat = i.proporcion_lat
                            longitud_min = i.longitud_min
                            proporcion_long = i.proporcion_long
                            break
                    else:
                        for i in Dimension:
                            latitud_min = i.latitud_min
                            proporcion_lat = i.proporcion_lat
                            longitud_min = i.longitud_min
                            proporcion_long = i.proporcion_long
                            break
                                #obj_Coordenadas.Eje_X = str( (float(z.LATITUD)  - latitud_min) / proporcion_lat  )
                                #obj_Coordenadas.Eje_Y = str( (float(z.LONGITUD) - longitud_min) / proporcion_long  ) 
        
        data["Autobuses_En_Parada"] = []

        data["Autobuses_Proximas_Llegadas"] = []
        
        data["Autobuses_Proximas_Salidas"] = []

        data["Autobuses_Anteriores"] = []
        
        for s in datas_three[2]:
            
            #Bus En Paradas
            
            Bus_Parada = DataCoordenadas.getAutobuses_Parada(Parada_Info[t]['ID'], ParametrosTop[1], s['Sinoptico_Id'])
            
            data["data"] = []
            
            for l in Bus_Parada:
                data["data"].append(
                    {
                        "Autobus": int(Bus_Parada[l]['AUTOBUS'])
                    }
                )
        
            data["Autobuses_En_Parada"].append(
                {
                    "Sinoptico_Id" : s['Sinoptico_Id'],
                    "Data": data["data"]   
                }
            )
            
            #Bus Proximas Legadas
            
            Bus_Proximas = DataCoordenadas.getAutobuses_Proximas(Parada_Info[t]['ID'], ParametrosTop[2], s['Sinoptico_Id'])
            
            data["data"] = []
            
            for l in Bus_Proximas:
                data["data"].append(
                    {
                        "Autobus": int(Bus_Proximas[l]['AUTOBUS']),
                        "Llegada": str(DataCoordenadas.convertlocaldate(Bus_Proximas[l]['ETA']))
                    }
                )
        
            data["Autobuses_Proximas_Llegadas"].append(
                {
                    "Sinoptico_Id" : s['Sinoptico_Id'],
                    "Data": data["data"]   
                }
            )
            
            #Bus Proximas salidas
            
            Bus_Proximas = DataCoordenadas.getAutobuses_Proximas_Salidas(Parada_Info[t]['ID'], ParametrosTop[3], s['Sinoptico_Id'])
            
            data["Data"] = []

            for l in Bus_Proximas:
                data["Data"].append(
                    {
                        "Autobus": int(Bus_Proximas[l]['AUTOBUS']),
                        "Salida": str(DataCoordenadas.convertlocaldate(Bus_Proximas[l]['FECHA_HORA_PROGRAMADA_SALIDA']))
                    }
                )
                
            
            data["Autobuses_Proximas_Salidas"].append(
                {
                    "Sinoptico_Id" : s['Sinoptico_Id'],
                    "Data": data["Data"]   
                }
            )
            
            #Bus Anteriores
            
            Bus_Anteriores = DataCoordenadas.getAutobuses_Anteriores(Parada_Info[t]['ID'], ParametrosTop[0], s['Sinoptico_Id'])
            
            data["Data"] = []
            
            Frecuency = 0 
            
            for l in Bus_Anteriores:
                
                
                data["Data"].append(
                    {
                        "Autobus": int(Bus_Anteriores[l]['AUTOBUS']),
                        "Programada": str(DataCoordenadas.convertlocaldate(Bus_Anteriores[l]['FECHA_PROGRAMADA'])),
                        "Real": str(DataCoordenadas.convertlocaldate(Bus_Anteriores[l]['FECHA_COLISION'])),
                        "Diferencia": int(Bus_Anteriores[l]['PUNTUALIDAD_LLEGADA']),
                        "Frecuencia": int(Bus_Anteriores[l]['FRECUENCIA_LLEGADA']) 
                    }
                )
                
                
            Frecuency = DataCoordenadas.getParadaFrecuencia(Parada_Info[t]['ID'], ParametrosTop[0], s['Sinoptico_Id'])
                
            data["Autobuses_Anteriores"].append(
                 {
                   "Sinoptico_Id": s['Sinoptico_Id'],
                    "Data" : data["Data"]
                 }
            )   

        Y = 0
        X = 0
        
        try:
            Y = int(ParametrosSelection[4]) +  (int(ParametrosSelection[2]) - ( (float(Latitud)  - latitud_min) / proporcion_lat  ))
            X = int(ParametrosSelection[Scale]) + ((float(Longitud) - longitud_min) / proporcion_long  )
                            
        except Exception as ex:
            X = 0
            Y = 0
            print("Error ")
        
        #Date = DataCoordenadas.GetDate()
        data_json["Paradas"].append({
            #"FROM" : str(Cloud) + " - "+  str(Date),
            'Parada_Id' :  int(Parada_Info[t]['ID']),
            'Parada_Desc' : str(Parada_Info[t]['NAME']).rstrip(),
            'Parada_Y' : Y,
            'Parada_X' : X,
            'Color' : DataCoordenadas.getColor(Parada_Info[t]['COLOR_ID']).rstrip(),
            'Parada_Puntualidad' : (random.randint(0,10)),
            'Parada_Frecuencia' : int(Frecuency),
            'No_Autobuses_En_Parada': len(data["Autobuses_En_Parada"]),
            'Rutas': datas_three[0],    
            'Trecho_Id': int(0), 
            'Clave': str(Parada_Info[t]['CLAVE']).rstrip(),  
            'Trechos': datas_three[1],
            'Autobuses_En_Parada': data["Autobuses_En_Parada"],
            'Autobuses_Proximas_Llegadas': data["Autobuses_Proximas_Llegadas"],
            'Autobuses_Anteriores': data["Autobuses_Anteriores"],
            'Autobuses_Proximas_Salidas': data["Autobuses_Proximas_Salidas"],
            'Sinoptico': datas_three[2],
            'Sinoptico_Coordenadas': data["Sinoptico_Coordenadas"]
        })

    
    #if len(data_json["Paradas"]) > 0:
    #result = EmitirJson(data_json, toEmit, ParametrosSelection)
    return [data_json, toEmit, ParametrosSelection]
#JSON PARADAS (MULTIPLE QUERY) UNICO SINOPTICO

#Json Viajes (MULTIPLE QUERY ALCHEMY)
def GetViajesv1():
    
    data_json = {}
        
    data_json["Viajes"] = []


    data = {}

    data['autobuses'] = []

    Viaje = DataCoordenadas.getViajesOpt()
    
    toEmit = "viajes"
    
    Scale = 5   
    
    global Parametros
    if len(Parametros) == 0:
        Parametros = DataCoordenadas.GetParametros()

    ParametrosSelection = DataCoordenadas.SelectPametros(Parametros, toEmit)

    global Dimension
    if len(Dimension) == 0:
        Dimension = DataCoordenadas.getPlaneCEv2(ParametrosSelection[2], ParametrosSelection[3])
    
    obj_SEC = SinocticoEC.SinopticoEC()

    count = 1
    ran = 0
    
    global VAR_ENCENDIDO_LOG_CONSOLE
    
    for v in Viaje:
        
        if(VAR_ENCENDIDO_LOG_CONSOLE):
            #ran = random.randint(0, 10)
            print ("Viajes Procesados=" + str(count) + " De " + str(len(Viaje)))
            count = count + 1
        
        try:
            
            viaje_info = DataCoordenadas.getViajePos(Viaje[v]['ULTIMO_VIAJE_POSICION_ID'])
            
            global RutasList
            if len(RutasList) != 0:
                Ruta_info = DataCoordenadas.getRutaList(RutasList, Viaje[v]['RUTA_ID'])
            else:
                Ruta_info = DataCoordenadas.getRuta(Viaje[v]['RUTA_ID'])

            data['Sinoptico_Coordenadas'] = []
            data['Sinoptico'] = []
            
            global SinopticoIdList
            if len(SinopticoIdList) != 0:
                SinopticoId = DataCoordenadas.GetSinopticosList(SinopticoIdList, viaje_info.TRECHO_ACTUAL_ID)
            else:    
                SinopticoId = DataCoordenadas.getSinopticoTrechov2(viaje_info.TRECHO_ACTUAL_ID)

            UltimaAlerta = DataCoordenadas.getUltimaAlerta(Viaje[v]['ID'])
            
            for sinopticoItem in SinopticoId:
                
                Scale = 5 
                
                for i in Dimension:
                    if sinopticoItem == i.sinoptico_id:
                        obj_SEC = SinocticoEC.SinopticoEC()
                        obj_SEC.sinoptico_id = i.sinoptico_id
                        obj_SEC.latitud_min = i.latitud_min
                        obj_SEC.longitud_min = i.longitud_min
                        obj_SEC.proporcion_lat = i.proporcion_lat
                        obj_SEC.proporcion_long = i.proporcion_long
                        obj_SEC.size = i.size
                
                if obj_SEC.size == 1:
                    Scale = 6
                
                Y = 0
                X = 0
                
                try:
                    
                    Y = int(ParametrosSelection[4]) +  (int(ParametrosSelection[2]) - ((float(viaje_info.LATITUD)  - obj_SEC.latitud_min) / obj_SEC.proporcion_lat))
                    X = int(ParametrosSelection[Scale]) + ((float(viaje_info.LONGITUD) - obj_SEC.longitud_min) / obj_SEC.proporcion_long)
                    
                except Exception as ex:
                    X = 0
                    Y = 0
                    print("Error ")
                
                data["Sinoptico_Coordenadas"].append(
                    {
                        "Sinoptico_Id": int(obj_SEC.sinoptico_id),
                        "Eje_Y": Y ,
                        "Eje_X": X
                    }
                )


                data["Sinoptico"].append(
                    {
                        "Sinoptico_Id": int(int(sinopticoItem))
                    }
                )
            
                data['Rutas'] = []
                data["Rutas"].append(
                    {
                        "Ruta_Id": int(Viaje[v]['RUTA_ID'])
                    }
                )

            #Date = DataCoordenadas.GetDate()
            global EstatusList
            if len(EstatusList) != 0:
                Estatus = DataCoordenadas.getStatusGetList(EstatusList, Viaje[v]['VIAJE_STATUS_ID'])
            else:
                Estatus = DataCoordenadas.getStatus(Viaje[v]['VIAJE_STATUS_ID'])
            
            Conexion = DataCoordenadas.GetConexionViaje(Viaje[v]['ULTIMO_VIAJE_POSICION_ID'])
            
            global GeotabULRLIST
            if len(GeotabULRLIST) != 0:
                Geotab = DataCoordenadas.GetGeotabURLlISt(GeotabULRLIST, Viaje[v]['AUTOBUS_ID'])
            else:    
                Geotab = DataCoordenadas.getGeotabULR(Viaje[v]['AUTOBUS_ID'])
            
            global CondutorLIST
            if len(CondutorLIST) != 0:
                Conductor = DataCoordenadas.getCondutorList(CondutorLIST, Viaje[v]['CONDUCTOR_ID'])
            else:
                Conductor = DataCoordenadas.getCondutor(Viaje[v]['CONDUCTOR_ID'])
            
            Trazados = DataCoordenadas.getTrazado_Trecho_Actual(viaje_info.TRECHO_ACTUAL_ID)
            
            data_json["Viajes"].append(
                {
                    #"FROM" : str(Cloud) + " - "+  str(Date),
                    "Autobus": int(Viaje[v]['AUTOBUS_ID']),
                    "Puntualidad": float(viaje_info.PUNTUALIDAD),
                    "Frecuencia_Atras": float(viaje_info.FRECUENCIA_ATRAS),
                    "Frecuencia_Adelante": float(viaje_info.FRECUENCIA_ADELANTE),
                    "Velocidad": float(viaje_info.VELOCIDAD),
                    "Kilometros_Recorridos": float(viaje_info.DISTANCIA),
                    "Clave_Conductor": Conductor[1],
                    "Conductor": str(Conductor[0]).rstrip(),
                    "Color_Puntualidad": str(viaje_info.COLOR_PUNTUALIDAD).rstrip(),
                    "Color_Frecuencia_Adelante": str(viaje_info.COLOR_FRECUENCIA_ADELANTE).rstrip(),
                    "Color_Frecuencia_Atras": str(viaje_info.COLOR_FRECUENCIA_ATRAS).rstrip(),
                    "Color_Estatus": str(viaje_info.COLOR_STATUS).rstrip(),
                    "Conexion": str(Conexion).rstrip(),
                    "Ruta": str(Ruta_info.NAME).rstrip(),
                    "Origen_Id": float(Ruta_info.PARADA_INI),
                    "Origen_Desc": str(DataCoordenadas.Parada_Origen_Desc(Ruta_info.PARADA_INI)).rstrip(),
                    "Destino_Id": float(Ruta_info.PARADA_FIN),
                    "Destino_Desc": str(DataCoordenadas.Parada_Destino_Desc(Ruta_info.PARADA_FIN)).rstrip(),  
                    "Fecha_Salida_Programada": str(Viaje[v]['FECHA_HORA_PROGRAMADA_SALIDA']).rstrip(),
                    "Fecha_Salida_Real": str(Viaje[v]['FECHA_HORA_REAL_SALIDA']).rstrip(),
                    "Fecha_Llegada_Programada": str(Viaje[v]['FECHA_HORA_PROGRAMADA_LLEGADA']).rstrip(),
                    "Fecha_Llegada_Real": str(Viaje[v]['FECHA_HORA_REAL_LLEGADA']).rstrip(),
                    "Estatus": str(Estatus).rstrip(),
                    "Estatus_Id":  float(Viaje[v]['VIAJE_STATUS_ID']),
                    "Fecha_Ultima_Actualizacion":  str(viaje_info.FECHA_HORA_GPS).rstrip(),
                    "Ultima_Alerta": str(UltimaAlerta).rstrip(),
                    "Siguiente_Parada_Id": float(viaje_info.PARADA_SIGUIENTE_ID),
                    "Siguiente_Parada_Desc": str(DataCoordenadas.Parada_Origen_Desc(viaje_info.PARADA_SIGUIENTE_ID)).rstrip(),
                    "Fecha_Siguiente_Parada":  str(viaje_info.FECHA_HORA_SIGUIENTE_PARADA_ESTIMADA).rstrip(),
                    "Latitud":  float(viaje_info.LATITUD),
                    "Longitud": float(viaje_info.LONGITUD),
                    "Metadata": str("https://maps.google.com/?q=" + str(viaje_info.LATITUD) + "," + str(viaje_info.LONGITUD)),
                    "Geotab_URL": str(Geotab),
                    "Trecho_Porcentaje": float(viaje_info.PORCENTAJE_AVANCE_TRECHO),
                    "Viaje_Porcentaje": float(viaje_info.PORCENTAJE_AVANCE_RUTA),
                    "Trecho_Id": int(viaje_info.TRECHO_ACTUAL_ID),
                    "Trazado_Id": int(Trazados[0]),
                    "Sinoptico": data["Sinoptico"],
                    "Rutas": data['Rutas'],
                    "Sinoptico_Coordenadas": data["Sinoptico_Coordenadas"],
                    "Fecha_Actual": str(datetime.today()),
                    #"Random": int(ran)
                }
            )
    
        except Exception as ex:
            print(str(ex))
            print(traceback.format_exc())
            DataCoordenadas.InsertLog(toEmit,str(ex))

    #if len(data_json["Viajes"]) > 0:
    #result = EmitirJson(data_json, toEmit, ParametrosSelection)
    
    return [data_json, toEmit, ParametrosSelection]
#Json Viajes (MULTIPLE QUERY ALCHEMY)

#Json Viajes (MULTIPLE QUERY ALCHEMY) UNICO SINOPTICO
def GetViajesSv1(Sinoptico):
    
    data_json = {}
        
    data_json["Viajes"] = []


    data = {}

    data['autobuses'] = []

    Viaje = DataCoordenadas.getViajesOptSinoptico(Sinoptico)
    
    toEmit = "viajes"
    
    Scale = 5   
    
    global Parametros
    if len(Parametros) == 0:
        Parametros = DataCoordenadas.GetParametros()

    ParametrosSelection = DataCoordenadas.SelectPametros(Parametros, toEmit)

    global Dimension
    if len(Dimension) == 0:
        Dimension = DataCoordenadas.getPlaneCEv2(ParametrosSelection[2], ParametrosSelection[3])
    
    obj_SEC = SinocticoEC.SinopticoEC()

    count = 1
    ran = 0
    
    global VAR_ENCENDIDO_LOG_CONSOLE
    
    for v in Viaje:
        
        if(VAR_ENCENDIDO_LOG_CONSOLE):
            #ran = random.randint(0, 10)
            print ("Viajes Procesados=" + str(count) + " De " + str(len(Viaje)))
            count = count + 1
        
        try:
            
            #viaje_info = DataCoordenadas.getViajePos(Viaje[v]['ULTIMO_VIAJE_POSICION_ID'])
            
            global RutasList
            if len(RutasList) != 0:
                Ruta_info = DataCoordenadas.getRutaList(RutasList, Viaje[v]['RUTA_ID'])
            else:
                Ruta_info = DataCoordenadas.getRuta(Viaje[v]['RUTA_ID'])

            data['Sinoptico_Coordenadas'] = []
            data['Sinoptico'] = []
            
            global SinopticoIdList
            if len(SinopticoIdList) != 0:
                #SinopticoId = DataCoordenadas.GetSinopticosList(SinopticoIdList, viaje_info.TRECHO_ACTUAL_ID)
                SinopticoId = DataCoordenadas.GetSinopticosList(SinopticoIdList, Viaje[v]['TRECHO_ACTUAL_ID'])
            else:    
                SinopticoId = DataCoordenadas.getSinopticoTrechov2(Viaje[v]['TRECHO_ACTUAL_ID'])

            UltimaAlerta = DataCoordenadas.getUltimaAlerta(Viaje[v]['ID'])
            
            for sinopticoItem in SinopticoId:
                
                Scale = 5 
                
                for i in Dimension:
                    if sinopticoItem == i.sinoptico_id:
                        obj_SEC = SinocticoEC.SinopticoEC()
                        obj_SEC.sinoptico_id = i.sinoptico_id
                        obj_SEC.latitud_min = i.latitud_min
                        obj_SEC.longitud_min = i.longitud_min
                        obj_SEC.proporcion_lat = i.proporcion_lat
                        obj_SEC.proporcion_long = i.proporcion_long
                        obj_SEC.size = i.size
                
                if obj_SEC.size == 1:
                    Scale = 6
                
                Y = 0
                X = 0
                
                try:
                    
                    Y = int(ParametrosSelection[4]) +  (int(ParametrosSelection[2]) - ((float(Viaje[v]['LATITUD'])  - obj_SEC.latitud_min) / obj_SEC.proporcion_lat))
                    X = int(ParametrosSelection[Scale]) + ((float(Viaje[v]['LONGITUD']) - obj_SEC.longitud_min) / obj_SEC.proporcion_long)
                    
                except Exception as ex:
                    X = 0
                    Y = 0
                    print("Error ")
                
                data["Sinoptico_Coordenadas"].append(
                    {
                        "Sinoptico_Id": int(obj_SEC.sinoptico_id),
                        "Eje_Y": Y ,
                        "Eje_X": X
                    }
                )


                data["Sinoptico"].append(
                    {
                        "Sinoptico_Id": int(int(sinopticoItem))
                    }
                )
            
                data['Rutas'] = []
                data["Rutas"].append(
                    {
                        "Ruta_Id": int(Viaje[v]['RUTA_ID'])
                    }
                )

            #Date = DataCoordenadas.GetDate()
            global EstatusList
            if len(EstatusList) != 0:
                Estatus = DataCoordenadas.getStatusGetList(EstatusList, Viaje[v]['VIAJE_STATUS_ID'])
            else:
                Estatus = DataCoordenadas.getStatus(Viaje[v]['VIAJE_STATUS_ID'])
            
            Conexion = DataCoordenadas.GetConexionViaje(Viaje[v]['ULTIMO_VIAJE_POSICION_ID'])
            
            global GeotabULRLIST
            if len(GeotabULRLIST) != 0:
                Geotab = DataCoordenadas.GetGeotabURLlISt(GeotabULRLIST, Viaje[v]['AUTOBUS_ID'])
            else:    
                Geotab = DataCoordenadas.getGeotabULR(Viaje[v]['AUTOBUS_ID'])
            
            global CondutorLIST
            if len(CondutorLIST) != 0:
                Conductor = DataCoordenadas.getCondutorList(CondutorLIST, Viaje[v]['CONDUCTOR_ID'])
            else:
                Conductor = DataCoordenadas.getCondutor(Viaje[v]['CONDUCTOR_ID'])
            
            Trazados = DataCoordenadas.getTrazado_Trecho_Actual(Viaje[v]['TRECHO_ACTUAL_ID'])
            
            data_json["Viajes"].append(
                {
                    #"FROM" : str(Cloud) + " - "+  str(Date),
                    "Autobus": int(Viaje[v]['AUTOBUS_ID']),
                    "Puntualidad": float(Viaje[v]['PUNTUALIDAD']),
                    "Frecuencia_Atras": float(Viaje[v]['FRECUENCIA_ATRAS']),
                    "Frecuencia_Adelante": float(Viaje[v]['FRECUENCIA_ADELANTE']),
                    "Velocidad": float(Viaje[v]['VELOCIDAD']),
                    "Kilometros_Recorridos": float(Viaje[v]['DISTANCIA']),
                    "Clave_Conductor": Conductor[1],
                    "Conductor": str(Conductor[0]).rstrip(),
                    "Color_Puntualidad": str(Viaje[v]['COLOR_PUNTUALIDAD']).rstrip(),
                    "Color_Frecuencia_Adelante": str(Viaje[v]['COLOR_FRECUENCIA_ADELANTE']).rstrip(),
                    "Color_Frecuencia_Atras": str(Viaje[v]['COLOR_FRECUENCIA_ATRAS']).rstrip(),
                    "Color_Estatus": str(Viaje[v]['COLOR_STATUS']).rstrip(),
                    "Conexion": str(Conexion).rstrip(),
                    "Ruta": str(Ruta_info.NAME).rstrip(),
                    "Origen_Id": float(Ruta_info.PARADA_INI),
                    "Origen_Desc": str(DataCoordenadas.Parada_Origen_Desc(Ruta_info.PARADA_INI)).rstrip(),
                    "Destino_Id": float(Ruta_info.PARADA_FIN),
                    "Destino_Desc": str(DataCoordenadas.Parada_Destino_Desc(Ruta_info.PARADA_FIN)).rstrip(),  
                    "Fecha_Salida_Programada": str(Viaje[v]['FECHA_HORA_PROGRAMADA_SALIDA']).rstrip(),
                    "Fecha_Salida_Real": str(Viaje[v]['FECHA_HORA_REAL_SALIDA']).rstrip(),
                    "Fecha_Llegada_Programada": str(Viaje[v]['FECHA_HORA_PROGRAMADA_LLEGADA']).rstrip(),
                    "Fecha_Llegada_Real": str(Viaje[v]['FECHA_HORA_REAL_LLEGADA']).rstrip(),
                    "Estatus": str(Estatus).rstrip(),
                    "Estatus_Id":  float(Viaje[v]['VIAJE_STATUS_ID']),
                    "Fecha_Ultima_Actualizacion":  str(Viaje[v]['FECHA_HORA_GPS']).rstrip(),
                    "Ultima_Alerta": str(UltimaAlerta).rstrip(),
                    "Siguiente_Parada_Id": float(Viaje[v]['PARADA_SIGUIENTE_ID']),
                    "Siguiente_Parada_Desc": str(DataCoordenadas.Parada_Origen_Desc(Viaje[v]['PARADA_SIGUIENTE_ID'])).rstrip(),
                    "Fecha_Siguiente_Parada":  str(Viaje[v]['FECHA_HORA_SIGUIENTE_PARADA_ESTIMADA']).rstrip(),
                    "Latitud":  float(Viaje[v]['LATITUD']),
                    "Longitud": float(Viaje[v]['LONGITUD']),
                    "Metadata": str("https://maps.google.com/?q=" + str(Viaje[v]['LATITUD']) + "," + str(Viaje[v]['LONGITUD'])),
                    "Geotab_URL": str(Geotab),
                    "Trecho_Porcentaje": float(Viaje[v]['PORCENTAJE_AVANCE_TRECHO']),
                    "Viaje_Porcentaje": float(Viaje[v]['PORCENTAJE_AVANCE_RUTA']),
                    "Trecho_Id": int(Viaje[v]['TRECHO_ACTUAL_ID']),
                    "Trazado_Id": int(Trazados[0]),
                    "Sinoptico": data["Sinoptico"],
                    "Rutas": data['Rutas'],
                    "Sinoptico_Coordenadas": data["Sinoptico_Coordenadas"],
                    "Fecha_Actual": str(datetime.today()),
                    #"Random": int(ran)
                }
            )
    
        except Exception as ex:
            print(str(ex))
            print(traceback.format_exc())
            DataCoordenadas.InsertLog(toEmit,str(ex))

    #if len(data_json["Viajes"]) > 0:
    #result = EmitirJson(data_json, toEmit, ParametrosSelection)
    
    return [data_json, toEmit, ParametrosSelection]
#Json Viajes (MULTIPLE QUERY ALCHEMY) UNICO SINOPTICO

#JSON SINOPTICOS_RESUMEN
def GetSinopticosResumenv1(): 
    
    data_json = {}
    
    data = {}
        
    data_json["Trama_Resumen_Sinoptico"] = []
    
    toEmit = "sinoptico_resumen"
    
    global Parametros
    if len(Parametros) == 0:
        Parametros = DataCoordenadas.GetParametros()
    
    ParametrosSelection = DataCoordenadas.SelectPametros(Parametros, toEmit)
    
    
    global Sinopticos_for
    if len(Sinopticos_for) == 0:
        Sinopticos_for = DataCoordenadas.getSinopticossql()
    
    count = 1
    
    for s in Sinopticos_for:
        
        global VAR_ENCENDIDO_LOG_CONSOLE
        if(VAR_ENCENDIDO_LOG_CONSOLE):
            print ("Sinoptico Resumen Procesados=" + str(count) + " De " + str(len(Sinopticos_for)) + "")
            count = count + 1
        
        try:
            
            ElementosO = DataCoordenadas.getViajesSinoptico(s.ID)
            ElementosT = DataCoordenadas.getViajeColor(s.ID)
    
            data_json["Trama_Resumen_Sinoptico"].append(
                {
                    "Sinoptico_Id": int(s.ID),
                    "Viajes_Programados" : ElementosO.Viajes_Programados,
                    "Viajes_Programados_Sinoptico" : ElementosO.Autobus_Programdos_Sinoptico,
                    "Viajes_Retrasados_Sinopticos" : ElementosO.Autobus_Retrasados_Sinoptico,
                    "Viajes_Reales_Sinoptico" : ElementosO.Autobus_Reales_Sinoptico,
                    "Puntualidad_Sinoptico" : ElementosO.Autobus_Puntual_Sinoptico,
                    "Frecuencia_Paso_Sinoptico": ElementosO.Frecuencia_Paso_Sinoptico,
                    "Puntualidad_Sinoptico" : ElementosO.Autobus_Puntual_Sinoptico,
                    "Frecuencia_Salida_Terminal": ElementosO.Frecuencia_Salida_Terminal,
                    "Frecuencia_Llegada_Terminal": ElementosO.Frecuencia_Llegada_Terminal,
                    "Frecuencia_Salida_Sinoptico": ElementosO.Frecuencia_Salida_Sinoptico,
                    "Frecuencia_Llegada_Sinoptico": ElementosO.Frecuencia_Llegada_Sinoptico,
                    "Frecuencia_Autobuses_En_Sinoptico": ElementosO.Frecuencia_Autobuses_En_Sinoptico,
                    "Frecuencia_Promedio": int(ElementosT[3]),
                    "Puntualidad_Promedio": int(str(ElementosT[2])),
                    "Color_Puntualidad_Promedio": str(ElementosT[0]),
                    "Color_Frecuencia_Promedio": str(ElementosT[1]),
                    "Calificacion_Servicio": 100
                }
            )
            
        except Exception as ex:
            print(str(ex))
            print(traceback.format_exc())
            DataCoordenadas.InsertLog(toEmit,str(ex))
    
    #result = EmitirJson(data_json, toEmit, ParametrosSelection)
    
    return [data_json, toEmit, ParametrosSelection]
#JSON SINOPTICOS_RESUMEN

#JSON SINOPTICOS_RESUMEN UNICO SINOPTICO
def GetSinopticosResumenSv1(Sinoptico): 
    
    data_json = {}
    
    data = {}
        
    data_json["Trama_Resumen_Sinoptico"] = []
    
    toEmit = "sinoptico_resumen"
    
    global Parametros
    if len(Parametros) == 0:
        Parametros = DataCoordenadas.GetParametros()
    
    ParametrosSelection = DataCoordenadas.SelectPametros(Parametros, toEmit)

    Sinopticos_for_s = []
    
    global Sinopticos_for
    if len(Sinopticos_for) == 0:
        Sinopticos_for = DataCoordenadas.getSinopticossql()
    
    for s in Sinopticos_for:
        
        if s.ID == int(Sinoptico):
                Sinopticos_for_s.append(s)
    
    count = 1
    
    for s in Sinopticos_for_s:
        
        global VAR_ENCENDIDO_LOG_CONSOLE
        if(VAR_ENCENDIDO_LOG_CONSOLE):
            print ("Sinoptico Resumen Procesados=" + str(count) + " De " + str(len(Sinopticos_for_s)) + "")
            count = count + 1
        
        try:
            
            ElementosO = DataCoordenadas.getViajesSinoptico(s.ID)
            ElementosT = DataCoordenadas.getViajeColor(s.ID)
    
            data_json["Trama_Resumen_Sinoptico"].append(
                {
                    "Sinoptico_Id": int(s.ID),
                    "Viajes_Programados" : ElementosO.Viajes_Programados,
                    "Viajes_Programados_Sinoptico" : ElementosO.Autobus_Programdos_Sinoptico,
                    "Viajes_Retrasados_Sinopticos" : ElementosO.Autobus_Retrasados_Sinoptico,
                    "Viajes_Reales_Sinoptico" : ElementosO.Autobus_Reales_Sinoptico,
                    "Puntualidad_Sinoptico" : ElementosO.Autobus_Puntual_Sinoptico,
                    "Frecuencia_Paso_Sinoptico": ElementosO.Frecuencia_Paso_Sinoptico,
                    "Puntualidad_Sinoptico" : ElementosO.Autobus_Puntual_Sinoptico,
                    "Frecuencia_Salida_Terminal": ElementosO.Frecuencia_Salida_Terminal,
                    "Frecuencia_Llegada_Terminal": ElementosO.Frecuencia_Llegada_Terminal,
                    "Frecuencia_Salida_Sinoptico": ElementosO.Frecuencia_Salida_Sinoptico,
                    "Frecuencia_Llegada_Sinoptico": ElementosO.Frecuencia_Llegada_Sinoptico,
                    "Frecuencia_Autobuses_En_Sinoptico": ElementosO.Frecuencia_Autobuses_En_Sinoptico,
                    "Frecuencia_Promedio": int(ElementosT[3]),
                    "Puntualidad_Promedio": int(str(ElementosT[2])),
                    "Color_Puntualidad_Promedio": str(ElementosT[0]),
                    "Color_Frecuencia_Promedio": str(ElementosT[1]),
                    "Calificacion_Servicio": 100
                }
            )
            
        except Exception as ex:
            print(str(ex))
            print(traceback.format_exc())
            #DataCoordenadas.InsertLog(toEmit,str(ex))
    
    #result = EmitirJson(data_json, toEmit, ParametrosSelection)
    
    return [data_json, toEmit, ParametrosSelection]
#JSON SINOPTICOS_RESUMEN UNICO SINOPTICO

@app.route('/API/v1.0/GetJsonSinoptico/<Sinoptico>')
def GetJsonSinoptico(Sinoptico):
    
    Sinoptico = Sinoptico
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        
        Trazados = executor.submit(GetTrazadosSinoptico, Sinoptico)
        Paradas = executor.submit(GetParadasSinoptico, Sinoptico)
        Viajes = executor.submit(GetViajesSinopticos, Sinoptico)
        #Resumen = executor.submit(GetResumenSinoptico, Sinoptico)
        #Eventos = executor.submit(GetEventoSinoptico, Sinoptico)
        
        result_Trazados = Trazados.result()
        result_Paradas = Paradas.result()
        result_Viajes = Viajes.result()
        #result_Resumen = Resumen.result()
        #result_Eventos = Eventos.result()
        
        data= {}
        
        data["Sinoptico"] = []
        
        data['Sinoptico'].append({
            
            'SINOPTICO_ID': Sinoptico,
            'TRAZADOS': result_Trazados['Trechos'],
            'PARADAS': result_Paradas['Paradas'],
            'VIAJES': result_Viajes['Viajes'],
            #'SINOPTICO_RESUMEN': result_Resumen['Trama_Resumen_Sinoptico'],
            #'SINOPTICO_EVENTOS': result_Eventos['Trama_Eventos']
            })
        
        return jsonify(data)

def GetTrazadosSinoptico(Sinoptico):
    
    Result = GetTrechosSv1(Sinoptico)
    return Result[0]

def GetParadasSinoptico(Sinoptico):
    
    Result = GetParadasTrazadoSv1(Sinoptico)
    return Result[0]

def GetViajesSinopticos(Sinoptico):
    
    Result = GetViajesSv1(Sinoptico)
    return Result[0]

def GetResumenSinoptico(Sinoptico):
    
    Result = GetSinopticosResumenSv1(Sinoptico)
    return Result[0]

def GetEventoSinoptico(Sinoptico):
    
    Result = GetTramaEventosSv1(Sinoptico)
    return Result[0]
    
# <editor-fold desc="Manejo de errores">
# En caso de no encontrar la aplicación.
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
# </editor-fold>

# <editor-fold desc="Ejecución principal">
#Ejecución principal
def main():
    app.run(host='127.0.0.1', port=8080, debug=True)

#Preguntamos si es ejecución principal
if __name__ == '__main__':
   main()   