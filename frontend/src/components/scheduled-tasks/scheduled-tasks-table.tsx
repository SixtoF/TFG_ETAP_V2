"use client";

import type { ScheduledTask } from "@/types/scheduled-task";
import ScheduledTaskStatusBadge from "./scheduled-task-status-badge";
import { useToggleScheduledTask } from "@/lib/hooks/use-toggle-scheduled-task";

type Props = {
  scheduledTasks: ScheduledTask[];
  canManage: boolean;
};

function shortenId(id: string) {
  return `${id.slice(0, 8)}...`;
}

function formatDate(value: string | null) {
  if (!value) return "-";
  return new Date(value).toLocaleString("es-ES");
}

export default function ScheduledTasksTable({
  scheduledTasks,
  canManage,
}: Props) {
  const toggleMutation = useToggleScheduledTask();

  const handleToggle = async (task: ScheduledTask) => {
    await toggleMutation.mutateAsync({
      scheduledTaskId: task.id,
      shouldActivate: !task.is_active,
    });
  };

  return (
    <div className="overflow-hidden rounded-2xl bg-white shadow-sm">
      {toggleMutation.isSuccess && (
        <div className="border-b border-green-200 bg-green-50 px-4 py-3 text-sm text-green-700">
          Estado actualizado correctamente.
        </div>
      )}

      {toggleMutation.isError && (
        <div className="border-b border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          {toggleMutation.error instanceof Error
            ? toggleMutation.error.message
            : "Error al cambiar el estado"}
        </div>
      )}

      <div className="overflow-x-auto">
        <table className="min-w-full border-collapse">
          <thead className="bg-slate-50">
            <tr className="text-left text-sm text-slate-600">
              <th className="px-4 py-3 font-medium">ID</th>
              <th className="px-4 py-3 font-medium">Nombre</th>
              <th className="px-4 py-3 font-medium">Estado</th>
              <th className="px-4 py-3 font-medium">Cron</th>
              <th className="px-4 py-3 font-medium">Próxima ejecución</th>
              <th className="px-4 py-3 font-medium">Última ejecución</th>
              <th className="px-4 py-3 font-medium">Acción</th>
            </tr>
          </thead>

          <tbody>
            {scheduledTasks.map((task) => (
              <tr key={task.id} className="border-t border-slate-200 text-sm">
                <td className="px-4 py-3 font-mono text-slate-700">
                  {shortenId(task.id)}
                </td>
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
                <td className="px-4 py-3 text-slate-700">
                  {formatDate(task.last_run_at)}
                </td>
                <td className="px-4 py-3">
                  {canManage ? (
                    <button
                      onClick={() => handleToggle(task)}
                      disabled={toggleMutation.isPending}
                      className="rounded-xl bg-slate-900 px-3 py-2 text-xs font-medium text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
                    >
                      {toggleMutation.isPending
                        ? "Procesando..."
                        : task.is_active
                        ? "Desactivar"
                        : "Activar"}
                    </button>
                  ) : (
                    <span className="text-xs text-slate-500">Solo lectura</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}