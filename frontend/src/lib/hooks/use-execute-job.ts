"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { executeJobRequest } from "@/lib/api/jobs";

export function useExecuteJob(jobId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: () => executeJobRequest(jobId),
    onSuccess: async () => {
      await Promise.all([
        queryClient.invalidateQueries({ queryKey: ["job", jobId] }),
        queryClient.invalidateQueries({ queryKey: ["jobs"] }),
        queryClient.invalidateQueries({ queryKey: ["job-logs", jobId] }),
      ]);
    },
  });
}