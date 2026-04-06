"use client";

import type { ExecutionLog } from "@/types/execution-log";

type Props = {
  logs: ExecutionLog[];
  isLoading: boolean;
  isError: boolean;
  errorMessage?: string;
};

function formatDate(value: string) {
  return new Date(value).toLocaleString("es-ES");
}

function levelClasses(level: string) {
  if (level === "ERROR") return "bg-red-100 text-red-700";
  if (level === "WARNING") return "bg-amber-100 text-amber-700";
  return "bg-blue-100 text-blue-700";
}

export default function JobLogsPanel({
  logs,
  isLoading,
  isError,
  errorMessage,
}: Props) {
  if (isLoading) {
    return (
      <section className="rounded-2xl bg-white p-6 shadow-sm">
        <h2 className="text-lg font-semibold text-slate-900">Logs</h2>
        <p className="mt-4 text-sm text-slate-600">Cargando logs...</p>
      </section>
    );
  }

  if (isError) {
    return (
      <section className="rounded-2xl border border-red-200 bg-red-50 p-6 shadow-sm">
        <h2 className="text-lg font-semibold text-slate-900">Logs</h2>
        <p className="mt-4 text-sm text-red-700">
          {errorMessage ?? "Error al cargar logs"}
        </p>
      </section>
    );
  }

  if (logs.length === 0) {
    return (
      <section className="rounded-2xl bg-white p-6 shadow-sm">
        <h2 className="text-lg font-semibold text-slate-900">Logs</h2>
        <p className="mt-4 text-sm text-slate-600">
          Este job todavía no tiene logs registrados.
        </p>
      </section>
    );
  }

  return (
    <section className="rounded-2xl bg-white p-6 shadow-sm">
      <h2 className="text-lg font-semibold text-slate-900">Logs</h2>

      <div className="mt-4 space-y-4">
        {logs.map((log) => (
          <article
            key={log.id}
            className="rounded-xl border border-slate-200 p-4"
          >
            <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
              <div className="flex items-center gap-3">
                <span
                  className={`inline-flex rounded-full px-3 py-1 text-xs font-medium ${levelClasses(
                    log.level
                  )}`}
                >
                  {log.level}
                </span>
                <p className="text-sm font-medium text-slate-800">
                  {log.message}
                </p>
              </div>

              <p className="text-xs text-slate-500">{formatDate(log.created_at)}</p>
            </div>

            {log.details_json && (
              <details className="mt-3 rounded-lg bg-slate-50 p-3">
                <summary className="cursor-pointer text-sm font-medium text-slate-700">
                  Ver detalles
                </summary>
                <pre className="mt-3 overflow-x-auto whitespace-pre-wrap text-xs text-slate-700">
                  {JSON.stringify(log.details_json, null, 2)}
                </pre>
              </details>
            )}
          </article>
        ))}
      </div>
    </section>
  );
}