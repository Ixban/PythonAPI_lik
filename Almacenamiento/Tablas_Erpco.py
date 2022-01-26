from sqlalchemy import Column, Integer, VARCHAR, NCHAR, DateTime
from sqlalchemy.exc import SQLAlchemyError
import datetime
from Almacenamiento import db_session, Base
from Almacenamiento.Tablas import Tabla

class Erpco_Clase_Servicio(Base,Tabla):
    __tablename__ = ''
    CLASESERVICIO_ID = Column(Integer, primary_key = True)   #Identity by default
    DESCCLASESERV    = Column(VARCHAR(50))
    STATUS           = Column(Integer)
    CVECLASESERV     = Column(VARCHAR(10))
    RAZONSOCIAL      = Column(VARCHAR(50))

    def __init__(self, 
        CLASESERVICIO_ID: int = None,
        DESCCLASESERV   : str = None,
        STATUS          : int = None,
        CVECLASESERV    : str = None,
        RAZONSOCIAL     : str = None
    ):
        self.CLASESERVICIO_ID = CLASESERVICIO_ID
        self.DESCCLASESERV    = DESCCLASESERV   
        self.STATUS           = STATUS          
        self.CVECLASESERV     = CVECLASESERV    
        self.RAZONSOCIAL      = RAZONSOCIAL     

class ERPCO_CORRIDA_TRAMO(Base,Tabla):
    __tablename__ = ''
    ID                         = Column(Integer, primary_key = True)   #Identity by default
    ERPCO_CORRIDA              = Column(Integer)                     
    AUTOBUS                    = Column(Integer)                     
    REGION_ID                  = Column(Integer)                     
    MARCA_ID                   = Column(Integer)                     
    ORIGEN_ID                  = Column(Integer)    
    ORIGEN_DESCRIPCION         = Column(NCHAR(50))             
    DESTINO_ID                 = Column(Integer)     
    DESTINO_DESCRIPCION        = Column(NCHAR(50))              
    SALIDA                     = Column(DateTime, default=datetime.datetime.utcnow)  
    LLEGADA                    = Column(DateTime, default=datetime.datetime.utcnow)  
    CLASE_SERVICIO_ID          = Column(Integer)            
    CLASE_SERVICIO_DESCRIPCION = Column(NCHAR(50))                     

    def __init__(self, 
        ID                        : int = None,
        ERPCO_CORRIDA             : int = None,
        AUTOBUS                   : int = None,
        REGION_ID                 : int = None,
        MARCA_ID                  : int = None,
        ORIGEN_ID                 : int = None,
        ORIGEN_DESCRIPCION        : str = None,
        DESTINO_ID                : int = None,
        DESTINO_DESCRIPCION       : str = None,
        SALIDA                    : datetime = None,
        LLEGADA                   : datetime = None,
        CLASE_SERVICIO_ID         : int = None,
        CLASE_SERVICIO_DESCRIPCION: str = None
    ):
        self.ID                         = ID                        
        self.ERPCO_CORRIDA              = ERPCO_CORRIDA             
        self.AUTOBUS                    = AUTOBUS                   
        self.REGION_ID                  = REGION_ID                 
        self.MARCA_ID                   = MARCA_ID                  
        self.ORIGEN_ID                  = ORIGEN_ID                 
        self.ORIGEN_DESCRIPCION         = ORIGEN_DESCRIPCION        
        self.DESTINO_ID                 = DESTINO_ID                
        self.DESTINO_DESCRIPCION        = DESTINO_DESCRIPCION       
        self.SALIDA                     = SALIDA                    
        self.LLEGADA                    = LLEGADA                   
        self.CLASE_SERVICIO_ID          = CLASE_SERVICIO_ID         
        self.CLASE_SERVICIO_DESCRIPCION = CLASE_SERVICIO_DESCRIPCION

class Erpco_Marca(Base,Tabla):
    __tablename__    = ''
    MARCA_ID         = Column(Integer, primary_key = True, autoincrement = False)   #Not Identity
    CVEMARCA         = Column(VARCHAR(10))
    STATUS           = Column(Integer)
    NOMBMARCA        = Column(VARCHAR(50))
    RAZONSABREVOCIAL = Column(VARCHAR(6))

    def __init__(self, 
        MARCA_ID        : int = None,
        CVEMARCA        : str = None,
        STATUS          : int = None,
        NOMBMARCA       : str = None,
        RAZONSABREVOCIAL: str = None
    ):
        self.MARCA_ID         = MARCA_ID              
        self.CVEMARCA         = CVEMARCA              
        self.STATUS           = STATUS                
        self.NOMBMARCA        = NOMBMARCA             
        self.RAZONSABREVOCIAL = RAZONSABREVOCIAL 

class Erpco_Region(Base,Tabla):
    __tablename__ = ''
    REGION_ID     = Column(Integer, primary_key = True, autoincrement = False)   #Not Identity
    CVEREGION     = Column(VARCHAR(10))
    STATUS        = Column(Integer)
    NOMBREGION    = Column(VARCHAR(50))

    def __init__(self, 
        REGION_ID : int = None,
        CVEREGION : str = None,
        STATUS    : int = None,
        NOMBREGION: str = None,
    ):
        self.REGION_ID  = REGION_ID 
        self.CVEREGION  = CVEREGION 
        self.STATUS     = STATUS    
        self.NOMBREGION = NOMBREGION