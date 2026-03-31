import type { JobRiskLevel } from "@/types/job";

type Props = {
  level: JobRiskLevel | string;
};

const riskConfig: Record<JobRiskLevel, { label: string; className: string }> = {
  low: {
    label: "Bajo",
    className: "bg-green-100 text-green-700",
  },
  medium: {
    label: "Medio",
    className: "bg-amber-100 text-amber-700",
  },
  high: {
    label: "Alto",
    className: "bg-red-100 text-red-700",
  },
  unknown: {
    label: "Desconocido",
    className: "bg-slate-100 text-slate-700",
  },
};

export default function JobRiskBadge({ level }: Props) {
  const config =
    riskConfig[level as JobRiskLevel] ?? riskConfig.unknown;

  return (
    <span
      className={`inline-flex rounded-full px-3 py-1 text-xs font-medium ${config.className}`}
    >
      {config.label}
    </span>
  );
}