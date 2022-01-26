from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import urllib

__params   = urllib.parse.quote_plus(
   '''DRIVER={ODBC Driver 17 for SQL Server};
   SERVER=;
   DATABASE=;
   UID=;
   PWD=''')

# __params   = urllib.parse.quote_plus(
#    '''DRIVER={ODBC Driver 17 for SQL Server};
#    SERVER=35.224.187.243;
#    DATABASE=CEN_SAE_TEST_V15;
#    UID=usrSAE_TEST;
#    PWD=saefuncionarabien!''')

# __params   = urllib.parse.quote_plus(
#    '''DRIVER={ODBC Driver 17 for SQL Server};
#    SERVER=10.54.0.3;
#    DATABASE=CEN_SAE_TEST_V15;
#    UID=usrSAE_TEST;
#    PWD=saefuncionarabien!''')

# __params = urllib.parse.quote_plus(
#     '''DRIVER={ODBC Driver 17 for SQL Server};
#     SERVER=127.0.0.1;
#     DATABASE=CEN_SAE_TEST_V15;
#     UID=usrSAE_TEST;
#     PWD=saefuncionarabien!''')

__engine   = create_engine(
    "mssql+pyodbc:///?odbc_connect=%s" % __params,
    convert_unicode = True)

#35.192.61.233

db_session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=__engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import Almacenamiento.Tablas
    import Almacenamiento.Tablas_Erpco
    import Almacenamiento.Tablas_Menu
    import Almacenamiento.Tablas_SIIAB
    Base.metadata.create_all(bind=__engine)

def end_db():
    db_session.remove()

"""@class Ejecutor
    ejecuta una sentencia sql
    @param      instruction(str)    sentencia sql a ejecutar
    @return     en el caso de una consulta (SELECT) devuelve el resultado en forma de un diccionario
                en el caso de una inseción (INSERT) o exclusion (DELETE) devulve el string 'hecho'
                en caso de que se ubique un error de sintaxis, se devuelve 'error en sentencia sql'
"""
class Ejecutor:
    @staticmethod
    def execute(instruction: str):
        try:
            result = db_session.execute(instruction)
        except:
            return 'error en sentencia sql'
        if result.returns_rows:
            d = {}
            a = {}
            count = 0
            for row in result:
                for column, value in row.items():
                    d = {**d, **{column: value}}
                count +=1
                a.update( {"row" + str(count) : d})
            return  a
        else:
            db_session.commit()
            return 'hecho'
        

