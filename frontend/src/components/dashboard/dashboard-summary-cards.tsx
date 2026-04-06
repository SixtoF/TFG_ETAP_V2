"use client";

import Link from "next/link";
import type { DashboardSummary } from "@/types/dashboard";

type Props = {
  summary: DashboardSummary;
};

type SummaryCard = {
  title: string;
  value: number;
  href: string;
};

export default function DashboardSummaryCards({ summary }: Props) {
  const cards: SummaryCard[] = [
    {
      title: "Total jobs",
      value: summary.totalJobs,
      href: "/jobs",
    },
    {
      title: "Jobs en running",
      value: summary.runningJobs,
      href: "/jobs",
    },
    {
      title: "Jobs pendientes de aprobación",
      value: summary.approvalPendingJobs,
      href: "/approvals",
    },
    {
      title: "Jobs fallidos",
      value: summary.failedJobs,
      href: "/jobs",
    },
    {
      title: "Approvals pendientes",
      value: summary.pendingApprovals,
      href: "/approvals",
    },
    {
      title: "Scheduled tasks activas",
      value: summary.activeScheduledTasks,
      href: "/scheduled-tasks",
    },
  ];

  return (
    <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
      {cards.map((card) => (
        <article key={card.title} className="rounded-2xl bg-white p-5 shadow-sm border border-slate-200/70">
          <h2 className="text-sm font-medium text-slate-500">{card.title}</h2>
          <p className="mt-3 text-3xl font-semibold text-slate-900">{card.value}</p>
          <div className="mt-4">
            <Link
              href={card.href}
              className="text-sm font-medium text-blue-700 hover:underline"
            >
              Ir a la sección
            </Link>
          </div>
        </article>
      ))}
    </section>
  );
}