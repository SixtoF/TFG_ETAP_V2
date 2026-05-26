"use client";

import { useMemo } from "react";
import type { JobStatus } from "@/types/job";
import { useExecuteJob } from "@/lib/hooks/use-execute-job";

type Props = {
  jobId: string;
  status: JobStatus;
};

const EXECUTABLE_STATUSES: JobStatus[] = ["ready_to_execute"];

function getBlockedMessage(status: JobStatus): string {
  switch (status) {
    case "approval_pending":
      return "Pendiente de aprobacion";
    case "queued":
      return "Ya en cola";
    case "running":
      return "En ejecucion";
    case "completed":
      return "Ya completado";
    case "failed":
      return "Fallido";
    case "rejected":
      return "Rechazado";
    case "created":
      return "Aun no listo";
    default:
      return "No disponible";
  }
}

export default function ExecuteJobButton({ jobId, status }: Props) {
  const { mutate, isPending, isSuccess, isError, error, data } = useExecuteJob(jobId);

  const canExecute = useMemo(() => EXECUTABLE_STATUSES.includes(status), [status]);

  const handleExecute = () => {
    if (!canExecute) return;
    mutate();
  };

  return (
    <div className="space-y-3">
      <button
        onClick={handleExecute}
        disabled={!canExecute || isPending || isSuccess}
        className={`rounded-xl px-4 py-2 text-sm font-medium text-white transition ${
          !canExecute || isPending || isSuccess
            ? "cursor-not-allowed bg-slate-400"
            : "bg-slate-900 hover:bg-slate-800"
        }`}
      >
        {isPending ? "Encolando..." : "Ejecutar trabajo"}
      </button>

      {!canExecute && (
        <p className="text-sm text-slate-500">
          No se puede ejecutar manualmente: {getBlockedMessage(status)}.
        </p>
      )}

      {isSuccess && (
        <div className="rounded-xl border border-green-200 bg-green-50 px-4 py-3 text-sm text-green-700">
          {data?.message ?? "trabajo encolado correctamente"}
        </div>
      )}

      {isError && (
        <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          {error instanceof Error ? error.message : "Error al ejecutar trabajo"}
        </div>
      )}
    </div>
  );
}