"""
CLASE BASE PARA CONECTORES (BaseConnector).
Define la interfaz estandar que todos los conectores especificos deben implementar.
Asegura que el motor de ejecucion pueda invocar cualquier conector de forma uniforme.
"""

class BaseConnector:
    # Metodo principal de ejecucion que debe ser sobrescrito por las subclases
    # step_type: Define la accion especifica dentro del conector (ej: 'send_email')
    # input_json: Contiene los parametros necesarios para la operacion
    def execute(self, step_type: str, input_json: dict) -> dict:
        """
        Lanza un error si una subclase intenta usarse sin haber implementado este metodo.
        Esto garantiza que ningun conector se quede 'vacio' por error del desarrollador.
        """
        raise NotImplementedError("Connector execute method not implemented")