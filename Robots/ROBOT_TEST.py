# <editor-fold desc="Importaciones">
import Librerias.Seguridad as Seguridad
import Librerias.Utilerias as Util
import Librerias.Bitacora as Bit
import Librerias.Configuracion as Config

# </editor-fold>

# <editor-fold desc="Inicializaciones">
obj_Configuracion = Config.CONFIG()
# </editor-fold>

# <editor-fold desc="Metodos privados">
#Simplemente generamos carga del procesador a lo pendejo
def _generar_carga():
    Bit.add_bitacora(Bit.Tipo.FUNCIONAL, Bit.USUARIO_ID, "INICIO DE BENCHMARK.",
                     "INICIO DE BENCHMARK", "main", "api_v1_0_benchmark", "", "", "", 1, 1)

    # Simplemente creamos carga a lo pendejo y sin fin
    while (1):
        var_x = 987239478234879 * 98723947823947

    Bit.add_bitacora(Bit.Tipo.FUNCIONAL, Bit.USUARIO_ID, "FIN DE BENCHMARK.",
                     "FIN DE BENCHMARK", "main", "api_v1_0_benchmark", "", "", "", 1, 1)
# </editor-fold>

# <editor-fold desc="Metodos Publicos">
#Prueba del procesamiento
def Test():
   _generar_carga()
# </editor-fold>
