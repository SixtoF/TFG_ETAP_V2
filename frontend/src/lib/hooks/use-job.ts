"use client";

import { useQuery } from "@tanstack/react-query";
import { getJobByIdRequest } from "@/lib/api/jobs";

export function useJob(jobId: string, enabled: boolean = true) {
  return useQuery({
    queryKey: ["job", jobId],
    queryFn: () => getJobByIdRequest(jobId),
    enabled: !!jobId && enabled,
    refetchInterval: 5000,
  });
}