/**
 * DESCRIPCION: Utilidades para la gestion del token JWT en el navegador.
 * Permite guardar, recuperar y eliminar las credenciales de acceso de forma persistente.
 */

// Clave unica para identificar el token de la ETAP en el almacenamiento del navegador
const TOKEN_KEY = "etap_access_token";

/**
 * Guarda el token recibido tras un login exitoso.
 * @param token Cadena de texto con el JWT generado por FastAPI.
 */
export function saveToken(token: string) {
  // Verificamos si estamos en el navegador (cliente) antes de acceder a localStorage
  if (typeof window === "undefined") return;
  localStorage.setItem(TOKEN_KEY, token);
}

/**
 * Recupera el token guardado para enviarlo en las peticiones a la API.
 * @returns El token como string o null si no existe sesion activa.
 */
export function getToken(): string | null {
  // Si se ejecuta en el servidor (durante el renderizado inicial), devolvemos null
  if (typeof window === "undefined") return null;
  return localStorage.getItem(TOKEN_KEY);
}

/**
 * Elimina el token del almacenamiento.
 * Se utiliza principalmente para la funcionalidad de Logout.
 */
export function removeToken() {
  // Aseguramos que solo se intente borrar si estamos en el cliente
  if (typeof window === "undefined") return;
  localStorage.removeItem(TOKEN_KEY);
}