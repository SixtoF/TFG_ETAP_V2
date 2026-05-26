"use client";

import { useEffect } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import AppShell from "@/components/layout/app-shell";
import JobStatusBadge from "@/components/jobs/job-status-badge";
import JobLogsPanel from "@/components/jobs/job-logs-panel";
import ExecuteJobButton from "@/components/jobs/execute-job-button";
import { useAuth } from "@/lib/hooks/use-auth";
import { useJob } from "@/lib/hooks/use-job";
import { useJobLogs } from "@/lib/hooks/use-job-logs";

function formatDate(value: string | null) {
  if (!value) return "-";
  const date = new Date(value);
  return isNaN(date.getTime()) ? "-" : date.toLocaleString("es-ES");
}

export default function JobDetailPage() {
  const params = useParams<{ id: string }>();
  const router = useRouter();
  const { isAuthenticated, isLoading: authLoading } = useAuth();
  const jobId = params.id;

  const { data: job, isLoading, isError, error } = useJob(
  jobId,
  !authLoading && isAuthenticated
);

const {
  data: logs,
  isLoading: logsLoading,
  isError: logsError,
  error: logsErrorValue,
} = useJobLogs(jobId, !authLoading && isAuthenticated);

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
        <div className="flex items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-semibold text-slate-900">Detalle de Trabajo</h1>
            <p className="mt-1 text-sm text-slate-600">
              Vista detallada del trabajo, ejecución y trazabilidad.
            </p>
          </div>

          <Link
            href="/jobs"
            className="rounded-xl border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-50"
          >
            Volver
          </Link>
        </div>

        {isLoading && (
          <div className="rounded-2xl bg-white p-6 shadow-sm">
            <p className="text-sm text-slate-600">Cargando detalle del trabajo...</p>
          </div>
        )}

        {isError && (
          <div className="rounded-2xl border border-red-200 bg-red-50 p-6 shadow-sm">
            <p className="text-sm text-red-700">
              {error instanceof Error ? error.message : "Error al cargar el trabajo"}
            </p>
          </div>
        )}

        {!isLoading && !isError && job && (
          <>
            {job.status === "running" && (
              <div className="rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-700">
              Este trabajo se está ejecutando en este momento...
              </div>
            )}
            <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
              <div className="rounded-2xl bg-white p-5 shadow-sm">
                <h2 className="text-sm font-medium text-slate-500">ID</h2>
                <p className="mt-2 break-all font-mono text-sm text-slate-800">
                  {job.id}
                </p>
              </div>

              <div className="rounded-2xl bg-white p-5 shadow-sm">
                <h2 className="text-sm font-medium text-slate-500">Intento</h2>
                <p className="mt-2 text-slate-800">{job.intent_name}</p>
              </div>

              <div className="rounded-2xl bg-white p-5 shadow-sm">
                <h2 className="text-sm font-medium text-slate-500">Estado</h2>
                <div className="mt-2">
                  <JobStatusBadge status={job.status} />
                </div>
              </div>

              <div className="rounded-2xl bg-white p-5 shadow-sm">
                <h2 className="text-sm font-medium text-slate-500">Riesgo</h2>
                <p className="mt-2 capitalize text-slate-800">
                  {job.risk_level ? job.risk_level : "-"}
                </p>
              </div>

              <div className="rounded-2xl bg-white p-5 shadow-sm">
                <h2 className="text-sm font-medium text-slate-500">Creado</h2>
                <p className="mt-2 text-slate-800">{formatDate(job.created_at)}</p>
              </div>

              <div className="rounded-2xl bg-white p-5 shadow-sm">
                <h2 className="text-sm font-medium text-slate-500">Finalizado</h2>
                <p className="mt-2 text-slate-800">{formatDate(job.finished_at)}</p>
              </div>
            </section>

            <section className="rounded-2xl bg-white p-6 shadow-sm">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <h2 className="text-lg font-semibold text-slate-900">Acciones</h2>
                  <p className="mt-1 text-sm text-slate-600">
                    Ejecuta manualmente el trabajo si su estado lo permite.
                  </p>
                </div>
              </div>

              <div className="mt-4">
                <ExecuteJobButton jobId={job.id} status={job.status} />
              </div>
            </section>

            <section className="rounded-2xl bg-white p-6 shadow-sm">
              <h2 className="text-lg font-semibold text-slate-900">Pasos del Trabajo</h2>

              {job.steps.length === 0 ? (
                <p className="mt-4 text-sm text-slate-600">
                  Este trabajo no tiene pasos.
                </p>
              ) : (
                <div className="mt-4 overflow-x-auto">
                  <table className="min-w-full border-collapse">
                    <thead className="bg-slate-50">
                      <tr className="text-left text-sm text-slate-600">
                        <th className="px-4 py-3 font-medium">Orden</th>
                        <th className="px-4 py-3 font-medium">Nombre</th>
                        <th className="px-4 py-3 font-medium">Tipo</th>
                        <th className="px-4 py-3 font-medium">Conector</th>
                        <th className="px-4 py-3 font-medium">Estado</th>
                      </tr>
                    </thead>
                    <tbody>
                      {job.steps.map((step) => (
                        <tr key={step.id} className="border-t border-slate-200 text-sm">
                          <td className="px-4 py-3 text-slate-800">{step.step_order}</td>
                          <td className="px-4 py-3 text-slate-800">{step.name}</td>
                          <td className="px-4 py-3 text-slate-700">{step.step_type}</td>
                          <td className="px-4 py-3 text-slate-700">
                            {step.connector_type ?? "-"}
                          </td>
                          <td className="px-4 py-3">
                            <span className="inline-flex rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700">
                               {step.status}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </section>

            <JobLogsPanel
              logs={logs ?? []}
              isLoading={logsLoading}
              isError={logsError}
              errorMessage={
                logsErrorValue instanceof Error ? logsErrorValue.message : "Error al cargar registros"
              }
            />

            <section className="rounded-2xl bg-white p-6 shadow-sm">
              <h2 className="text-lg font-semibold text-slate-900">Resultado</h2>

              {!job.job_result ? (
                <p className="mt-4 text-sm text-slate-600">
                  Este trabajo todavía no tiene resultado final.
                </p>
              ) : (
                <div className="mt-4 space-y-2 text-sm">
                  <p>
                    <span className="font-medium">Éxito:</span>{" "}
                    {job.job_result.success ? "Sí" : "No"}
                  </p>
                  <p>
                    <span className="font-medium">Resumen:</span>{" "}
                    {job.job_result.summary ?? "-"}
                  </p>
                  <p>
                    <span className="font-medium">Creado:</span>{" "}
                    {formatDate(job.job_result.created_at)}
                  </p>
                </div>
              )}
            </section>
          </>
        )}
      </div>
    </AppShell>
  );
}