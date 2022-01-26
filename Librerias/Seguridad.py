# <editor-fold desc="Importaciones">
import Librerias.Utilerias as Util
import Librerias.Bitacora as Bit
# </editor-fold>

# <editor-fold desc="Seguridad">
# Solicitamos autenticación
def autenticar(username, password):
    if username == "app" and password == "app":
        return True
    else:
        return False
# </editor-fold>