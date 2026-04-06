"use client";

import Link from "next/link";
import type { ScheduledTask } from "@/types/scheduled-task";
import ScheduledTaskStatusBadge from "@/components/scheduled-tasks/scheduled-task-status-badge";

type Props = {
  scheduledTasks: ScheduledTask[];
};

function formatDate(value: string | null) {
  if (!value) return "-";
  return new Date(value).toLocaleString("es-ES");
}

export default function DashboardScheduledTasksSummary({
  scheduledTasks,
}: Props) {
  return (
    <section className="rounded-2xl bg-white p-6 shadow-sm">
      <div className="flex items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-semibold text-slate-900">Scheduled tasks</h2>
          <p className="mt-1 text-sm text-slate-600">
            Resumen de automatizaciones configuradas.
          </p>
        </div>

        <Link
          href="/scheduled-tasks"
          className="text-sm font-medium text-blue-700 hover:underline"
        >
          Ver scheduled tasks
        </Link>
      </div>

      {scheduledTasks.length === 0 ? (
        <p className="mt-4 text-sm text-slate-600">
          No hay scheduled tasks registradas.
        </p>
      ) : (
        <div className="mt-4 overflow-x-auto">
          <table className="min-w-full border-collapse">
            <thead className="bg-slate-50">
              <tr className="text-left text-sm text-slate-600">
                <th className="px-4 py-3 font-medium">Nombre</th>
                <th className="px-4 py-3 font-medium">Estado</th>
                <th className="px-4 py-3 font-medium">Cron</th>
                <th className="px-4 py-3 font-medium">Próxima ejecución</th>
              </tr>
            </thead>
            <tbody>
              {scheduledTasks.map((task) => (
                <tr key={task.id} className="border-t border-slate-200 text-sm">
                  <td className="px-4 py-3 text-slate-800">{task.name}</td>
                  <td className="px-4 py-3">
                    <ScheduledTaskStatusBadge isActive={task.is_active} />
                  </td>
                  <td className="px-4 py-3 font-mono text-slate-700">
                    {task.cron_expression}
                  </td>
                  <td className="px-4 py-3 text-slate-700">
                    {formatDate(task.next_run_at)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}