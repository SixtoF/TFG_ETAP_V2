/**
 * DESCRIPCION: Configuracion de proveedores de contexto globales.
 * Establece el cliente de consultas para la API y el contexto de 
 * autenticacion para toda la aplicacion frontend.
 */

"use client"; // Este archivo debe ejecutarse en el cliente para manejar estados de React

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useState } from "react";
import { AuthProvider } from "@/lib/auth/auth-context"; // Proveedor personalizado de sesion

export default function Providers({ children }: { children: React.ReactNode }) {
  // Creamos una instancia unica de QueryClient para gestionar la cache de datos
  // Se usa useState para asegurar que el cliente se mantenga estable entre renderizados
  const [queryClient] = useState(() => new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 60 * 1000, // Los datos se consideran frescos durante 1 minuto
        retry: 1, // Reintenta una vez si la peticion falla
      },
    },
  }));

  return (
    // QueryClientProvider permite usar hooks como useQuery en cualquier pagina
    <QueryClientProvider client={queryClient}>
      {/* AuthProvider permite que cualquier componente sepa quien es el usuario logueado */}
      <AuthProvider>
        {/* Aqui se renderiza el resto de la aplicacion (Layout y Paginas) */}
        {children}
      </AuthProvider>
    </QueryClientProvider>
  );
}