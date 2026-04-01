import type { ApprovalStatus } from "@/types/approval";

type Props = {
  status: ApprovalStatus;
};

const statusConfig: Record<ApprovalStatus, { label: string; className: string }> = {
  pending: {
    label: "Pendiente",
    className: "bg-violet-100 text-violet-700",
  },
  approved: {
    label: "Aprobado",
    className: "bg-green-100 text-green-700",
  },
  rejected: {
    label: "Rechazado",
    className: "bg-zinc-200 text-zinc-700",
  },
};

export default function ApprovalStatusBadge({ status }: Props) {
  const config = statusConfig[status];

  return (
    <span
      className={`inline-flex rounded-full px-3 py-1 text-xs font-medium ${config.className}`}
    >
      {config.label}
    </span>
  );
}