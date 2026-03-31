/**
 * DESCRIPCION: Utilidad centralizada para realizar peticiones HTTP a la API de FastAPI.
 * Maneja automaticamente la base URL, los tokens de autenticacion y el control de errores.
 */

import { getToken } from "@/lib/auth/token-storage"; // Funcion para recuperar el JWT del almacenamiento

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL; // URL del backend configurada en .env.local

// Definicion de opciones extendidas para incluir el flag de autenticacion
type RequestOptions = RequestInit & {
  auth?: boolean; // Si es true, enviara el token JWT en la cabecera
};

/**
 * Funcion generica para realizar consultas a los endpoints del sistema.
 * @param endpoint Ruta del recurso (ej: "/jobs" o "/auth/login")
 * @param options Configuracion de la peticion (metodo, cuerpo, autenticacion)
 */
export async function apiRequest<T>(
  endpoint: string,
  options: RequestOptions = {}
): Promise<T> {
  const { auth = false, headers, ...restOptions } = options;

  // Inicializacion de las cabeceras de la peticion
  const requestHeaders = new Headers(headers);
  requestHeaders.set("Content-Type", "application/json");

  // Logica de inyeccion automatica del token de seguridad
  if (auth) {
    const token = getToken();
    if (token) {
      // Formato estandar OAuth2 para enviar el token al backend
      requestHeaders.set("Authorization", `Bearer ${token}`);
    }
  }

  // Ejecucion de la peticion fetch al servidor de la ETAP
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...restOptions,
    headers: requestHeaders,
  });

  // Control de respuestas fallidas (codigos 4xx o 5xx)
  if (!response.ok) {
    let errorMessage = "Error inesperado en la API";

    try {
      // Intentamos extraer el mensaje de error detallado enviado por FastAPI
      const errorData = await response.json();
      errorMessage = errorData.detail || errorMessage;
    } catch {
      // Si la respuesta no es un JSON, usamos el codigo de estado HTTP
      errorMessage = `Error HTTP ${response.status}`;
    }

    throw new Error(errorMessage);
  }

  // Devolucion de los datos procesados en formato JSON con el tipado correcto
  return response.json();
}