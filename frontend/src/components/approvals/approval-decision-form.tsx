"use client";

import { useState } from "react";
import { useApproveApproval } from "@/lib/hooks/use-approve-approval";
import { useRejectApproval } from "@/lib/hooks/use-reject-approval";

type Props = {
  approvalId: string;
};

export default function ApprovalDecisionForm({ approvalId }: Props) {
  const [comment, setComment] = useState("");
  const [localError, setLocalError] = useState<string | null>(null);

  const approveMutation = useApproveApproval();
  const rejectMutation = useRejectApproval();

  const isPending = approveMutation.isPending || rejectMutation.isPending;

  const handleApprove = async () => {
    setLocalError(null);

    try {
      await approveMutation.mutateAsync({
        approvalId,
        resolutionComment: comment.trim() || null,
      });
      setComment("");
    } catch (error) {
      setLocalError(
        error instanceof Error ? error.message : "Error al aprobar la solicitud"
      );
    }
  };

  const handleReject = async () => {
    setLocalError(null);

    try {
      await rejectMutation.mutateAsync({
        approvalId,
        resolutionComment: comment.trim() || null,
      });
      setComment("");
    } catch (error) {
      setLocalError(
        error instanceof Error ? error.message : "Error al rechazar la solicitud"
      );
    }
  };

  return (
    <div className="space-y-3">
      <textarea
        value={comment}
        onChange={(event) => setComment(event.target.value)}
        placeholder="Comentario de resolución (opcional)"
        className="min-h-24 w-full rounded-xl border border-slate-300 px-3 py-2 text-sm outline-none transition focus:border-slate-500"
      />

      <div className="flex gap-2">
        <button
          onClick={handleApprove}
          disabled={isPending}
          className="rounded-xl bg-green-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-green-700 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {approveMutation.isPending ? "Aprobando..." : "Aprobar"}
        </button>

        <button
          onClick={handleReject}
          disabled={isPending}
          className="rounded-xl bg-red-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-red-700 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {rejectMutation.isPending ? "Rechazando..." : "Rechazar"}
        </button>
      </div>

      {approveMutation.isSuccess && (
        <div className="rounded-xl border border-green-200 bg-green-50 px-4 py-3 text-sm text-green-700">
          Solicitud aprobada correctamente.
        </div>
      )}

      {rejectMutation.isSuccess && (
        <div className="rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-700">
          Solicitud rechazada correctamente.
        </div>
      )}

      {localError && (
        <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          {localError}
        </div>
      )}
    </div>
  );
}