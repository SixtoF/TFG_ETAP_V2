/**
 * DESCRIPCION: Componente de cabecera superior.
 * Muestra informacion del usuario logueado (nombre y rol) y 
 * gestiona el cierre de sesion seguro.
 */

"use client"; // Componente de cliente para manejar eventos de clic y navegacion

import { useRouter } from "next/navigation"; // Hook para redirigir al usuario
import { useAuth } from "@/lib/hooks/use-auth"; // Hook para acceder a los datos de sesion

export default function Topbar() {
  const router = useRouter();
  
  // Extraemos los datos del usuario actual y la funcion de logout del contexto
  const { user, logout } = useAuth();

  /**
   * Manejador para el cierre de sesion.
   * Ejecuta la limpieza de tokens y redirige a la pantalla de acceso.
   */
  const handleLogout = () => {
    logout(); // Llama a la funcion que borra el token en el storage y el estado
    router.replace("/login"); // Redireccion inmediata para proteger el area privada
  };

  return (
    // Contenedor de la cabecera con borde inferior sutil y fondo blanco
    <header className="border-b border-slate-200 bg-white px-6 py-4">
      <div className="flex items-center justify-between">
        
        {/* Seccion izquierda: Titulo de contexto de la aplicacion */}
        <div>
          <p className="text-sm text-slate-500 font-medium">Panel ETAP</p>
          <h1 className="text-lg font-semibold text-slate-900">Operacion</h1>
        </div>

        {/* Seccion derecha: Datos del usuario y boton de salida */}
        <div className="flex items-center gap-4">
          
          {/* Informacion del perfil: alineada a la derecha */}
          <div className="text-right">
            {/* Muestra el nombre completo obtenido del backend de FastAPI */}
            <p className="text-sm font-semibold text-slate-800">{user?.full_name}</p>
            {/* Muestra el rol (admin/operador) en mayusculas para mayor claridad */}
            <p className="text-[10px] font-bold uppercase tracking-wider text-slate-500">
              {user?.role}
            </p>
          </div>

          {/* Boton de Logout con estilos de Tailwind */}
          <button
            onClick={handleLogout}
            className="rounded-xl border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700 transition-all duration-200 hover:bg-slate-50 hover:border-slate-400 active:scale-95"
          >
            Cerrar Sesion
          </button>
        </div>
      </div>
    </header>
  );
}