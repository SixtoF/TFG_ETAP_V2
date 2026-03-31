/**
 * DESCRIPCION: Layout raiz del frontend de la ETAP. 
 * Define la estructura HTML base, carga los estilos globales y 
 * envuelve la aplicacion en los Providers necesarios para el estado y consultas.
 */

import "./globals.css"; // Importacion de estilos globales (Tailwind CSS)
import type { Metadata } from "next"; // Tipado para los metadatos de la pagina
import Providers from "@/app/providers"; // Componente que agrupa contextos (Auth, QueryClient, etc.)

// Definicion de los metadatos que apareceran en la pestana del navegador
export const metadata: Metadata = {
  title: "ETAP Frontend",
  description: "Dashboard de ETAP",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode; // Representa el contenido de la pagina actual que se este visitando
}>) {
  return (
    <html lang="es">
      {/* Aplicamos clases de Tailwind para un fondo gris industrial y texto legible */}
      <body className="bg-slate-100 text-slate-900">
        {/* Envolvemos toda la aplicacion con Providers para que los subcomponentes 
            puedan acceder a la sesion del usuario o a los datos de la API */}
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}