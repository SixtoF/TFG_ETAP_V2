"use client";

import Link from "next/link";
import type { Approval } from "@/types/approval";
import ApprovalStatusBadge from "@/components/approvals/approval-status-badge";

type Props = {
  approvals: Approval[];
};

function shortenId(id: string) {
  return `${id.slice(0, 8)}...`;
}

function formatDate(value: string) {
  return new Date(value).toLocaleString("es-ES");
}

export default function DashboardPendingApprovals({ approvals }: Props) {
  return (
    <section className="rounded-2xl bg-white p-6 shadow-sm">
      <div className="flex items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-semibold">Approvals pendientes</h2>
          <p className="mt-1 text-sm text-slate-600">
            Solicitudes pendientes de decisión.
          </p>
        </div>

        <Link
          href="/approvals"
          className="text-sm font-medium text-blue-700 hover:underline"
        >
          Ir a approvals
        </Link>
      </div>

      {approvals.length === 0 ? (
        <p className="mt-4 text-sm text-slate-600">
          No hay approvals pendientes.
        </p>
      ) : (
        <div className="mt-4 space-y-3">
          {approvals.map((approval) => (
            <article
              key={approval.id}
              className="rounded-xl border border-slate-200 p-4"
            >
              <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
                <div className="space-y-2">
                  <div className="flex items-center gap-3">
                    <ApprovalStatusBadge status={approval.status} />
                    <Link
                      href={`/jobs/${approval.job_id}`}
                      className="font-mono text-sm text-blue-700 hover:underline"
                    >
                      Job {shortenId(approval.job_id)}
                    </Link>
                  </div>

                  <p className="text-sm text-slate-800">{approval.reason}</p>
                </div>

                <p className="text-xs text-slate-500">
                  {formatDate(approval.requested_at)}
                </p>
              </div>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}