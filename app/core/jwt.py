# GENERADOR DE CREDENCIALES DIGITALES (JSON WEB TOKENS)
# Define la logica para crear tokens firmados que permiten el acceso a la API de la ETAP.

from datetime import datetime, timedelta, timezone

from jose import jwt

# SECRET_KEY: Clave maestra para firmar los tokens. Es vital mantenerla secreta.
SECRET_KEY = "CHANGE_THIS_IN_ENV_LATER"

# ALGORITHM: Metodo de cifrado estandar (HS256) para asegurar la integridad del token.
ALGORITHM = "HS256"

# Tiempo de validez: Sesiones de 2 horas (120 minutos) para equilibrar seguridad y comodidad.
ACCESS_TOKEN_EXPIRE_MINUTES = 120


def create_access_token(data: dict) -> str:
    # Genera un token JWT firmado digitalmente.
    # Se implementa para que el cliente (Frontend) pueda navegar por la API de forma segura.
    
    # Creamos una copia de los datos (ID, email, rol) para no modificar el original.
    to_encode = data.copy()
    
    # Calculamos la fecha de caducidad: Momento actual + 120 minutos.
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Añadimos el campo 'exp' (expiration) al cuerpo del token.
    to_encode.update({"exp": expire})
    
    # Firmamos el paquete con la SECRET_KEY y el algoritmo elegido.
    # Esto genera un string largo dividido por puntos que el cliente guardara.
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)