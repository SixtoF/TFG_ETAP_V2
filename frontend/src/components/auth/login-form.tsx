"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/hooks/use-auth";

type LoginFormValues = {
  email: string;
  password: string;
};

export default function LoginForm() {
  const router = useRouter();
  const { login } = useAuth();
  const [apiError, setApiError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormValues>();

  const onSubmit = async (data: LoginFormValues) => {
    setApiError(null);

    try {
      await login(data.email, data.password);
      router.replace("/dashboard");
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Error al iniciar sesion";
      setApiError(message);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label htmlFor="email" className="mb-1 block text-sm font-medium text-slate-900">
          Email
        </label>
        <input
          id="email"
          type="email"
          className="w-full rounded-xl border border-slate-300 px-3 py-2 outline-none transition focus:border-slate-500"
          {...register("email", {
            required: "El email es obligatorio",
          })}
        />
        {errors.email && (
          <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="password" className="mb-1 block text-sm font-medium text-slate-900">
          Contraseña
        </label>
        <input
          id="password"
          type="password"
          className="w-full rounded-xl border border-slate-300 px-3 py-2 outline-none transition focus:border-slate-500"
          {...register("password", {
            required: "La contraseña es obligatoria",
          })}
        />
        {errors.password && (
          <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>
        )}
      </div>

      {apiError && (
        <div className="rounded-xl border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
          {apiError}
        </div>
      )}

      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full rounded-xl bg-slate-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-70"
      >
        {isSubmitting ? "Entrando..." : "Iniciar sesión"}
      </button>
    </form>
  );
}