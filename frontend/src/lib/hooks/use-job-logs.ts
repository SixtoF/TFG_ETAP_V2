"use client";

import { useQuery } from "@tanstack/react-query";
import { getJobLogsRequest } from "@/lib/api/jobs";

export function useJobLogs(jobId: string, enabled: boolean = true) {
  return useQuery({
    queryKey: ["job-logs", jobId],
    queryFn: () => getJobLogsRequest(jobId),
    enabled: !!jobId && enabled,
    refetchInterval: 5000,
  });
}