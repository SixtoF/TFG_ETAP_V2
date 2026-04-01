"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createScheduledTaskRequest } from "@/lib/api/scheduled-tasks";
import type { CreateScheduledTaskRequest } from "@/types/scheduled-task";

export function useCreateScheduledTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: CreateScheduledTaskRequest) =>
      createScheduledTaskRequest(payload),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["scheduled-tasks"] });
    },
  });
}