"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import {
  activateScheduledTaskRequest,
  deactivateScheduledTaskRequest,
} from "@/lib/api/scheduled-tasks";

export function useToggleScheduledTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      scheduledTaskId,
      shouldActivate,
    }: {
      scheduledTaskId: string;
      shouldActivate: boolean;
    }) => {
      if (shouldActivate) {
        return activateScheduledTaskRequest(scheduledTaskId);
      }

      return deactivateScheduledTaskRequest(scheduledTaskId);
    },
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["scheduled-tasks"] });
    },
  });
}