"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import AppShell from "@/components/layout/app-shell";
import JobsTable from "@/components/jobs/jobs-table";
import { useAuth } from "@/lib/hooks/use-auth";
import { useJobs } from "@/lib/hooks/use-jobs";

export default function JobsPage() {
  const router = useRouter();
  const { isAuthenticated, isLoading: authLoading } = useAuth();
  const { data, isLoading, isError, error } = useJobs(!authLoading && isAuthenticated);

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

  return (
    <AppShell>
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-semibold">Jobs</h1>
          <p className="mt-1 text-sm text-slate-600">
            Lista de trabajos generados por ETAP.
          </p>
        </div>

        {isLoading && (
          <div className="rounded-2xl bg-white p-6 shadow-sm">
            <p className="text-sm text-slate-600">Cargando jobs...</p>
          </div>
        )}

        {isError && (
          <div className="rounded-2xl border border-red-200 bg-red-50 p-6 shadow-sm">
            <p className="text-sm text-red-700">
              {error instanceof Error ? error.message : "Error al cargar jobs"}
            </p>
          </div>
        )}

        {!isLoading && !isError && data && data.length === 0 && (
          <div className="rounded-2xl bg-white p-6 shadow-sm">
            <p className="text-sm text-slate-600">No hay jobs registrados.</p>
          </div>
        )}

        {!isLoading && !isError && data && data.length > 0 && (
          <JobsTable jobs={data} />
        )}
      </div>
    </AppShell>
  );
}