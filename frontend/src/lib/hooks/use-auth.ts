/**
 * DESCRIPCION: Hook personalizado para acceder al contexto de autenticacion.
 * Facilita el acceso a los datos del usuario y funciones de sesion en cualquier componente.
 */

"use client";

import { useContext } from "react";
import { AuthContext } from "@/lib/auth/auth-context"; // Importamos el contexto base

/**
 * Hook useAuth
 * Permite obtener el estado global de la sesion de forma sencilla.
 */
export function useAuth() {
  // Consumimos el contexto de autenticacion
  const context = useContext(AuthContext);

  // Validacion de seguridad: Si el contexto es undefined, significa que el componente
  // no esta envuelto por el AuthProvider en layout.tsx
  if (!context) {
    throw new Error("useAuth debe usarse dentro de AuthProvider");
  }

  // Retorna { user, isAuthenticated, isLoading, login, logout }
  return context;
}