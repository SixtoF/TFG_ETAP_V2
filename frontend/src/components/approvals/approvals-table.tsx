"use client";

import Link from "next/link";
import type { Approval } from "@/types/approval";
import ApprovalStatusBadge from "./approval-status-badge";
import ApprovalDecisionForm from "./approval-decision-form";

type Props = {
  approvals: Approval[];
  canResolve: boolean;
};

function shortenId(id: string) {
  return `${id.slice(0, 8)}...`;
}

function formatDate(value: string | null) {
  if (!value) return "-";
  return new Date(value).toLocaleString("es-ES");
}

export default function ApprovalsTable({ approvals, canResolve }: Props) {
  return (
    <div className="space-y-4">
      {approvals.map((approval) => {
        const isPending = approval.status === "pending";

        return (
          <article
            key={approval.id}
            className="rounded-2xl bg-white p-6 shadow-sm"
          >
            <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
              <div>
                <h3 className="text-sm font-medium text-slate-500">Approval ID</h3>
                <p className="mt-2 font-mono text-sm text-slate-800">
                  {shortenId(approval.id)}
                </p>
              </div>

              <div>
                <h3 className="text-sm font-medium text-slate-500">Job ID</h3>
                <div className="mt-2">
                  <Link
                    href={`/jobs/${approval.job_id}`}
                    className="font-mono text-sm text-blue-700 hover:underline"
                  >
                    {shortenId(approval.job_id)}
                  </Link>
                </div>
              </div>

              <div>
                <h3 className="text-sm font-medium text-slate-500">Estado</h3>
                <div className="mt-2">
                  <ApprovalStatusBadge status={approval.status} />
                </div>
              </div>

              <div>
                <h3 className="text-sm font-medium text-slate-500">Solicitado</h3>
                <p className="mt-2 text-sm text-slate-800">
                  {formatDate(approval.requested_at)}
                </p>
              </div>
            </div>

            <div className="mt-5 grid gap-4 md:grid-cols-2">
              <div>
                <h3 className="text-sm font-medium text-slate-500">Motivo</h3>
                <p className="mt-2 text-sm text-slate-800">{approval.reason}</p>
              </div>

              <div>
                <h3 className="text-sm font-medium text-slate-500">Resuelto por</h3>
                <p className="mt-2 text-sm text-slate-800">
                  {approval.resolved_by_name ?? "-"}
                </p>
              </div>
            </div>

            <div className="mt-5">
              <h3 className="text-sm font-medium text-slate-500">Comentario</h3>
              <p className="mt-2 text-sm text-slate-800">
                {approval.resolution_comment ?? "-"}
              </p>
            </div>

            {isPending && canResolve && (
              <div className="mt-6 border-t border-slate-200 pt-5">
                <h3 className="text-sm font-medium text-slate-500">Decisión</h3>
                <div className="mt-3">
                  <ApprovalDecisionForm approvalId={approval.id} />
                </div>
              </div>
            )}
          </article>
        );
      })}
    </div>
  );
}