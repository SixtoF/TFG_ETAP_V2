/**
 * DESCRIPCION: Panel principal de control de la ETAP.
 * Muestra informacion del usuario logueado y sirve como base para
 * gestionar jobs, aprobaciones y tareas programadas.
 */

"use client"; // Componente de cliente para manejar hooks y navegacion

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import AppShell from "@/components/layout/app-shell"; // Estructura base con menu y navegacion
import { useAuth } from "@/lib/hooks/use-auth"; // Hook para obtener datos del usuario actual

export default function DashboardPage() {
  const router = useRouter();
  
  // Extraemos datos del usuario, estado de auth y estado de carga
  const { user, isAuthenticated, isLoading } = useAuth();

  // Efecto para expulsar al usuario si intenta entrar sin estar autenticado
  useEffect(() => {
    if (isLoading) return;

    if (!isAuthenticated) {
      // Redireccion de seguridad al login
      router.replace("/login");
    }
  }, [isAuthenticated, isLoading, router]);

  // Pantalla de transicion mientras se valida la sesion
  if (isLoading || !isAuthenticated) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-slate-50">
        <p className="text-sm font-medium text-slate-600 animate-pulse">
          Cargando dashboard...
        </p>
      </main>
    );
  }

  return (
    // AppShell proporciona la barra lateral y el diseño consistente
    <AppShell>
      <div className="space-y-6">
        {/* Cabecera del Dashboard */}
        <div>
          <h1 className="text-2xl font-semibold text-slate-900">Dashboard</h1>
          <p className="mt-1 text-sm text-slate-600">
            Bienvenido al panel principal de ETAP.
          </p>
        </div>

        {/* Rejilla de tarjetas de informacion rapida (Kpis) */}
        <div className="grid gap-4 md:grid-cols-3">
          {/* Tarjeta de Identidad */}
          <section className="rounded-2xl bg-white p-5 shadow-sm border border-slate-100">
            <h2 className="text-sm font-medium text-slate-500 uppercase tracking-wider">
              Usuario actual
            </h2>
            <p className="mt-2 text-lg font-semibold text-slate-800">{user?.full_name}</p>
            <p className="text-sm text-slate-500">{user?.email}</p>
          </section>

          {/* Tarjeta de Privilegios */}
          <section className="rounded-2xl bg-white p-5 shadow-sm border border-slate-100">
            <h2 className="text-sm font-medium text-slate-500 uppercase tracking-wider">
              Rol del sistema
            </h2>
            <p className="mt-2 text-lg font-semibold text-indigo-600 capitalize">
              {user?.role}
            </p>
          </section>

          {/* Tarjeta de Estado de Conexion */}
          <section className="rounded-2xl bg-white p-5 shadow-sm border border-slate-100">
            <h2 className="text-sm font-medium text-slate-500 uppercase tracking-wider">
              Estado operativo
            </h2>
            <p className="mt-2 text-lg font-semibold text-green-600">
              Sesion activa
            </p>
          </section>
        </div>

        {/* Seccion de Resumen General */}
        <section className="rounded-2xl bg-white p-6 shadow-sm border border-slate-100">
          <h2 className="text-lg font-semibold text-slate-900">Resumen de Actividad</h2>
          <p className="mt-2 text-sm text-slate-600 leading-relaxed">
            Esta es la base del panel. En la siguiente fase conectaremos el listado 
            de trabajos (Jobs), las autorizaciones pendientes (Approvals) y el 
            planificador de tareas (Scheduled Tasks) sincronizado con el backend.
          </p>
        </section>
      </div>
    </AppShell>
  );
}