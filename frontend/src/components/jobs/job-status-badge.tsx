import type { JobStatus } from "@/types/job";

type Props = {
  status: JobStatus;
};

const statusConfig: Record<JobStatus, { label: string; className: string }> = {
  created: {
    label: "Creado",
    className: "bg-slate-100 text-slate-700",
  },
  ready_to_execute: {
    label: "Listo",
    className: "bg-cyan-100 text-cyan-700",
  },
  queued: {
    label: "En cola",
    className: "bg-blue-100 text-blue-700",
  },
  running: {
    label: "Ejecutando",
    className: "bg-amber-100 text-amber-700",
  },
  completed: {
    label: "Completado",
    className: "bg-green-100 text-green-700",
  },
  failed: {
    label: "Fallido",
    className: "bg-red-100 text-red-700",
  },
  approval_pending: {
    label: "Pend. aprobacion",
    className: "bg-violet-100 text-violet-700",
  },
  rejected: {
    label: "Rechazado",
    className: "bg-zinc-200 text-zinc-700",
  },
};

export default function JobStatusBadge({ status }: Props) {
  const config = statusConfig[status] ?? {
    label: status,
    className: "bg-slate-100 text-slate-700",
  };

  return (
    <span
      className={`inline-flex rounded-full px-3 py-1 text-xs font-medium ${config.className}`}
    >
      {config.label}
    </span>
  );
}