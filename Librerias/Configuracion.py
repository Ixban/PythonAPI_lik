# <editor-fold desc="Importaciones">
import platform
# </editor-fold>

# <editor-fold desc="Clase de Configuración">
class CONFIG:
    # <editor-fold desc="Sistema Operativo y Entorno">
    MACHINE_Name = ""
    # </editor-fold>

    # <editor-fold desc="Bitacora">
    BIT_bol_envio_bitacora = True
    BIT_url_psicopompo_bitacora = ""
    BIT_url_psicopompo_bitacora_version = "/API/v1.0"
    # </editor-fold>


    # <editor-fold desc="Constructor">
    def __init__(self):

        try:
            self.MACHINE_Name = platform.node()
        except Exception as ex:
            self.MACHINE_Name = "LOCAL"

    # </editor-fold>
# </editor-fold>




