"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import AppShell from "@/components/layout/app-shell";
import CreateScheduledTaskForm from "@/components/scheduled-tasks/create-scheduled-task-form";
import ScheduledTasksTable from "@/components/scheduled-tasks/scheduled-tasks-table";
import { useAuth } from "@/lib/hooks/use-auth";
import { useScheduledTasks } from "@/lib/hooks/use-scheduled-tasks";

export default function ScheduledTasksPage() {
  const router = useRouter();
  const { user, isAuthenticated, isLoading: authLoading } = useAuth();
  const { data, isLoading, isError, error } = useScheduledTasks(
    !authLoading && isAuthenticated
  );

  useEffect(() => {
    if (authLoading) return;

    if (!isAuthenticated) {
      router.replace("/login");
    }
  }, [authLoading, isAuthenticated, router]);

  if (authLoading || !isAuthenticated) {
    return (
      <main className="flex min-h-screen items-center justify-center">
        <p className="text-sm text-slate-600">Cargando...</p>
      </main>
    );
  }

  const canManage = user?.role === "admin";

  return (
    <AppShell>
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900">Scheduled Tasks</h1>
          <p className="mt-1 text-sm text-slate-600">
            Gestión de automatizaciones programadas.
          </p>
        </div>

        {canManage && <CreateScheduledTaskForm />}

        {isLoading && (
          <div className="rounded-2xl bg-white p-6 shadow-sm">
            <p className="text-sm text-slate-600">
              Cargando scheduled tasks...
            </p>
          </div>
        )}

        {isError && (
          <div className="rounded-2xl border border-red-200 bg-red-50 p-6 shadow-sm">
            <p className="text-sm text-red-700">
              {error instanceof Error
                ? error.message
                : "Error al cargar scheduled tasks"}
            </p>
          </div>
        )}

        {!isLoading && !isError && data && data.length === 0 && (
          <div className="rounded-2xl bg-white p-6 shadow-sm">
            <p className="text-sm text-slate-600">
              No hay scheduled tasks registradas.
            </p>
          </div>
        )}

        {!isLoading && !isError && data && data.length > 0 && (
          <ScheduledTasksTable scheduledTasks={data} canManage={canManage} />
        )}
      </div>
    </AppShell>
  );
}