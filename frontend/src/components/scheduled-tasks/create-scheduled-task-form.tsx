"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { useCreateScheduledTask } from "@/lib/hooks/use-create-scheduled-task";
import type { CreateScheduledTaskRequest } from "@/types/scheduled-task";

type FormValues = {
  name: string;
  description: string;
  command_text: string;
  cron_expression: string;
  timezone: string;
  auto_enqueue: boolean;
};

export default function CreateScheduledTaskForm() {
  const [apiError, setApiError] = useState<string | null>(null);

  const createMutation = useCreateScheduledTask();

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({
    defaultValues: {
      name: "",
      description: "",
      command_text: "",
      cron_expression: "",
      timezone: "Europe/Madrid",
      auto_enqueue: true,
    },
  });

  const onSubmit = async (data: FormValues) => {
    setApiError(null);

    const payload: CreateScheduledTaskRequest = {
      name: data.name,
      description: data.description.trim() || null,
      command_text: data.command_text,
      cron_expression: data.cron_expression,
      timezone: data.timezone,
      auto_enqueue: data.auto_enqueue,
    };

    try {
      await createMutation.mutateAsync(payload);
      reset();
    } catch (error) {
      setApiError(
        error instanceof Error ? error.message : "Error al crear la tarea"
      );
    }
  };

  return (
    <section className="rounded-2xl bg-white p-6 shadow-sm">
      <h2 className="text-lg font-semibold text-slate-900">Nueva tarea programada</h2>
      <p className="mt-1 text-sm text-slate-600">
        Crea una automatización programada usando expresión cron.
      </p>

      <form onSubmit={handleSubmit(onSubmit)} className="mt-5 space-y-4">
        <div className="grid gap-4 md:grid-cols-2">
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-900">Nombre</label>
            <input
              className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm outline-none transition focus:border-slate-500"
              {...register("name", { required: "El nombre es obligatorio" })}
            />
            {errors.name && (
              <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>
            )}
          </div>

          <div>
            <label className="mb-1 block text-sm font-medium">ZonaHoraria</label>
            <input
              className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm outline-none transition focus:border-slate-500"
              {...register("timezone", {
                required: "La zona horaria es obligatoria",
              })}
            />
            {errors.timezone && (
              <p className="mt-1 text-sm text-red-600">
                {errors.timezone.message}
              </p>
            )}
          </div>
        </div>

        <div>
          <label className="mb-1 block text-sm font-medium text-slate-900">Descripción</label>
          <input
            className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm outline-none transition focus:border-slate-500"
            {...register("description")}
          />
        </div>

        <div>
          <label className="mb-1 block text-sm font-medium text-slate-900">Texto del comando</label>
          <textarea
            className="min-h-24 w-full rounded-xl border border-slate-300 px-3 py-2 text-sm outline-none transition focus:border-slate-500"
            {...register("command_text", {
              required: "El texto es obligatorio",
            })}
          />
          <p className="mt-1 text-xs text-slate-500">
            Ejemplo: Envia el email diario de resumen
          </p>
          {errors.command_text && (
            <p className="mt-1 text-sm text-red-600">
              {errors.command_text.message}
            </p>
          )}
        </div>

        <div>
          <label className="mb-1 block text-sm font-medium text-slate-900">Cron expression</label>
          <input
            placeholder="0 18 * * 1-5"
            className="w-full rounded-xl border border-slate-300 px-3 py-2 text-sm outline-none transition focus:border-slate-500"
            {...register("cron_expression", {
              required: "La expresión cron es obligatoria",
            })}
          />
          <p className="mt-1 text-xs text-slate-500">
            Ejemplo: 0 18 * * 1-5 = laborables a las 18:00
          </p>
          {errors.cron_expression && (
            <p className="mt-1 text-sm text-red-600">
              {errors.cron_expression.message}
            </p>
          )}
        </div>

        <label className="flex items-center gap-2 text-sm text-slate-700">
          <input type="checkbox" {...register("auto_enqueue")} />
          Auto enqueue
        </label>

        {createMutation.isSuccess && (
          <div className="rounded-xl border border-green-200 bg-green-50 px-4 py-3 text-sm text-green-700">
            Programacion de Tarea: Tarea programada, creada correctamente.
          </div>
        )}

        {apiError && (
          <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {apiError}
          </div>
        )}

        <button
          type="submit"
          disabled={isSubmitting || createMutation.isPending}
          className="rounded-xl bg-slate-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isSubmitting || createMutation.isPending ? "Creando..." : "Crear tarea"}
        </button>
      </form>
    </section>
  );
}