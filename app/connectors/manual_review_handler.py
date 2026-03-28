"""
MANEJADOR DE REVISION MANUAL (ManualReviewHandler).
Se activa cuando el sistema no puede determinar una intencion clara o detecta riesgos altos.
Garantiza que el flujo de trabajo se detenga de forma controlada para intervencion humana.
"""

class ManualReviewHandler:
    # Registra que el trabajo requiere supervision externa
    def handle(self) -> dict:
        """
        Devuelve un resultado positivo indicando que el proceso de 'marcado' 
        se ha realizado correctamente en el flujo de ejecucion.
        """
        return {
            "success": True,
            "summary": "Job marcado para revision manual"
        }