"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import AppShell from "@/components/layout/app-shell";
import ApprovalsTable from "@/components/approvals/approvals-table";
import { useAuth } from "@/lib/hooks/use-auth";
import { useApprovals } from "@/lib/hooks/use-approvals";

export default function ApprovalsPage() {
  const router = useRouter();
  const { user, isAuthenticated, isLoading: authLoading } = useAuth();
  const { data, isLoading, isError, error } = useApprovals(
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

  const canResolve = user?.role === "admin";

  return (
    <AppShell>
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900">Aprobaciones</h1>
          <p className="mt-1 text-sm text-slate-600">
            Gestión de aprobaciones pendientes y resueltas.
          </p>
        </div>

        {isLoading && (
          <div className="rounded-2xl bg-white p-6 shadow-sm">
            <p className="text-sm text-slate-600">Cargando aprobaciones...</p>
          </div>
        )}

        {isError && (
          <div className="rounded-2xl border border-red-200 bg-red-50 p-6 shadow-sm">
            <p className="text-sm text-red-700">
              {error instanceof Error ? error.message : "Error al cargar aprobaciones"}
            </p>
          </div>
        )}

        {!isLoading && !isError && data && data.length === 0 && (
          <div className="rounded-2xl bg-white p-6 shadow-sm">
            <p className="text-sm text-slate-600">
              No hay aprobaciones registradas.
            </p>
          </div>
        )}

        {!isLoading && !isError && data && data.length > 0 && (
          <ApprovalsTable approvals={data} canResolve={canResolve} />
        )}
      </div>
    </AppShell>
  );
}