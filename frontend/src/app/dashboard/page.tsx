/**
 * DESCRIPCION: Panel principal de control de la ETAP.
 * Muestra informacion del usuario logueado y sirve como base para
 * gestionar jobs, aprobaciones y tareas programadas.
 */

"use client";

import { useEffect, useMemo } from "react";
import { useRouter } from "next/navigation";
import AppShell from "@/components/layout/app-shell";
import DashboardSummaryCards from "@/components/dashboard/dashboard-summary-cards";
import DashboardRecentJobs from "@/components/dashboard/dashboard-recent-jobs";
import DashboardPendingApprovals from "@/components/dashboard/dashboard-pending-approvals";
import DashboardScheduledTasksSummary from "@/components/dashboard/dashboard-scheduled-tasks-summary";
import { useAuth } from "@/lib/hooks/use-auth";
import { useJobs } from "@/lib/hooks/use-jobs";
import { useApprovals } from "@/lib/hooks/use-approvals";
import { useScheduledTasks } from "@/lib/hooks/use-scheduled-tasks";
import type { DashboardSummary } from "@/types/dashboard";

export default function DashboardPage() {
  const router = useRouter();
  const { user, isAuthenticated, isLoading: authLoading } = useAuth();
  const enabled = !authLoading && isAuthenticated;

const {
  data: jobs,
  isLoading: jobsLoading,
  isError: jobsError,
  error: jobsErrorValue,
} = useJobs(enabled);

const {
  data: approvals,
  isLoading: approvalsLoading,
  isError: approvalsError,
  error: approvalsErrorValue,
} = useApprovals(enabled);

const {
  data: scheduledTasks,
  isLoading: scheduledTasksLoading,
  isError: scheduledTasksError,
  error: scheduledTasksErrorValue,
} = useScheduledTasks(enabled);

  useEffect(() => {
    if (authLoading) return;

    if (!isAuthenticated) {
      router.replace("/login");
    }
  }, [isAuthenticated, authLoading, router]);

  const isLoading =
    authLoading || jobsLoading || approvalsLoading || scheduledTasksLoading;

  const isError = jobsError || approvalsError || scheduledTasksError;

  const summary: DashboardSummary = useMemo(() => {
    const jobsData = jobs ?? [];
    const approvalsData = approvals ?? [];
    const scheduledTasksData = scheduledTasks ?? [];

    return {
      totalJobs: jobsData.length,
      runningJobs: jobsData.filter((job) => job.status === "running").length,
      approvalPendingJobs: jobsData.filter(
        (job) => job.status === "approval_pending"
      ).length,
      failedJobs: jobsData.filter((job) => job.status === "failed").length,
      pendingApprovals: approvalsData.filter(
        (approval) => approval.status === "pending"
      ).length,
      activeScheduledTasks: scheduledTasksData.filter((task) => task.is_active)
        .length,
    };
  }, [jobs, approvals, scheduledTasks]);

  const recentJobs = useMemo(() => {
    return [...(jobs ?? [])]
      .sort(
        (a, b) =>
          new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      )
      .slice(0, 5);
  }, [jobs]);

  const pendingApprovals = useMemo(() => {
    return (approvals ?? [])
      .filter((approval) => approval.status === "pending")
      .sort(
        (a, b) =>
          new Date(b.requested_at).getTime() - new Date(a.requested_at).getTime()
      )
      .slice(0, 5);
  }, [approvals]);

  const scheduledTasksPreview = useMemo(() => {
    return [...(scheduledTasks ?? [])]
      .sort(
        (a, b) =>
          new Date(a.next_run_at).getTime() - new Date(b.next_run_at).getTime()
      )
      .slice(0, 5);
  }, [scheduledTasks]);

  if (authLoading || !isAuthenticated) {
    return (
      <main className="flex min-h-screen items-center justify-center">
        <p className="text-sm text-slate-600">Cargando dashboard...</p>
      </main>
    );
  }

  return (
    <AppShell>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900">Dashboard</h1>
          <p className="mt-2 text-sm text-slate-600">
            Visión operativa del estado actual de ETAP.
          </p>
        </div>

        <section className="rounded-2xl bg-white p-5 shadow-sm">
          <h2 className="text-sm font-medium text-slate-500">Sesión actual</h2>
          <div className="mt-3 flex flex-col gap-1 text-sm text-slate-800">
            <p>
              <span className="font-medium">Usuario:</span> {user?.full_name}
            </p>
            <p>
              <span className="font-medium">Email:</span> {user?.email}
            </p>
            <p>
              <span className="font-medium">Rol:</span> {user?.role}
            </p>
          </div>
        </section>

        {isLoading && (
          <div className="rounded-2xl bg-white p-6 shadow-sm">
            <p className="text-sm text-slate-600">Cargando dashboard...</p>
          </div>
        )}

        {isError && (
          <div className="rounded-2xl border border-red-200 bg-red-50 p-6 shadow-sm">
            <p className="text-sm text-red-700">
              {jobsErrorValue instanceof Error
                ? jobsErrorValue.message
                : approvalsErrorValue instanceof Error
                ? approvalsErrorValue.message
                : scheduledTasksErrorValue instanceof Error
                ? scheduledTasksErrorValue.message
                : "Error al cargar los datos del dashboard"}
            </p>
          </div>
        )}

        {!isLoading && !isError && (
          <>
            <DashboardSummaryCards summary={summary} />

            <div className="grid gap-6 xl:grid-cols-2">
              <DashboardRecentJobs jobs={recentJobs} />
              <DashboardPendingApprovals approvals={pendingApprovals} />
            </div>

            <DashboardScheduledTasksSummary
              scheduledTasks={scheduledTasksPreview}
            />
          </>
        )}
      </div>
    </AppShell>
  );
}