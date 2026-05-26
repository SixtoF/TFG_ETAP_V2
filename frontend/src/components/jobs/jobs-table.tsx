"use client";

import Link from "next/link";
import type { Job } from "@/types/job";
import JobStatusBadge from "./job-status-badge";
import JobRiskBadge from "./job-risk-badge";

type Props = {
  jobs: Job[];
};

function shortenId(id: string) {
  return `${id.slice(0, 8)}...`;
}

function formatDate(value: string | null) {
  if (!value) return "-";
  const date = new Date(value);
  return isNaN(date.getTime()) ? "-" : date.toLocaleString("es-ES");
}

export default function JobsTable({ jobs }: Props) {
  return (
    <div className="overflow-hidden rounded-2xl bg-white shadow-sm">
      <div className="overflow-x-auto">
        <table className="min-w-full border-collapse">
          <thead className="bg-slate-50">
            <tr className="text-left text-sm text-slate-600">
              <th className="px-4 py-3 font-medium">ID</th>
              <th className="px-4 py-3 font-medium">Intento</th>
              <th className="px-4 py-3 font-medium">Estado</th>
              <th className="px-4 py-3 font-medium">Riesgo</th>
              <th className="px-4 py-3 font-medium">Creado</th>
              <th className="px-4 py-3 font-medium">Acción</th>
            </tr>
          </thead>

          <tbody>
            {jobs.map((job) => (
              <tr key={job.id} className="border-t border-slate-200 text-sm">
                <td className="px-4 py-3 font-mono text-slate-700">
                  {shortenId(job.id)}
                </td>
                <td className="px-4 py-3 text-slate-800">{job.intent_name}</td>
                <td className="px-4 py-3">
                  <JobStatusBadge status={job.status} />
                </td>
                <td className="px-4 py-3">
                  <JobRiskBadge level={job.risk_level} />
                </td>
                <td className="px-4 py-3 text-slate-700">
                  {formatDate(job.created_at)}
                </td>
                <td className="px-4 py-3">
                  <Link
                    href={`/jobs/${job.id}`}
                    className="rounded-xl bg-slate-900 px-3 py-2 text-xs font-medium text-white transition hover:bg-slate-800"
                  >
                    Ver
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}