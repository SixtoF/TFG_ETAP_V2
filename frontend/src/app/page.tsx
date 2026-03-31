/**
 * DESCRIPCION: Pagina de entrada principal del frontend.
 * Se encarga de redirigir al usuario segun su estado de autenticacion
 * hacia el Dashboard o hacia el Login.
 */

"use client"; // Indica que este componente se ejecuta en el navegador del cliente

import { useEffect } from "react";
import { useRouter } from "next/navigation"; // Hook de Next.js para navegacion programatica
import { useAuth } from "@/lib/hooks/use-auth"; // Hook personalizado para gestionar la sesion

export default function HomePage() {
  const router = useRouter();
  
  // Obtenemos el estado de autenticacion y si el proceso de carga ha terminado
  const { isAuthenticated, isLoading } = useAuth();

  useEffect(() => {
    // Si el sistema aun esta comprobando el token en el backend, no hacemos nada
    if (isLoading) return;

    // Logica de redireccionamiento basada en el estado de autenticacion
    if (isAuthenticated) {
      // Si el usuario tiene un token valido (Admin u Operador), va al panel de control
      router.replace("/dashboard");
    } else {
      // Si no esta autenticado, se le envia a la pantalla de acceso
      router.replace("/login");
    }
  }, [isAuthenticated, isLoading, router]);

  return (
    // Estructura visual temporal mientras se realiza la comprobacion de seguridad
    <main className="flex min-h-screen items-center justify-center">
      {/* Mensaje de espera para el operador de la planta */}
      <p className="text-sm text-slate-600">Redirigiendo...</p>
    </main>
  );
}