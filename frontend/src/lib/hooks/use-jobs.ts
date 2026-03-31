"use client";

import { useQuery } from "@tanstack/react-query";
import { getJobsRequest } from "@/lib/api/jobs";

export function useJobs(enabled: boolean = true) {
  return useQuery({
    queryKey: ["jobs"],
    queryFn: getJobsRequest,
    enabled,
    refetchInterval: 10000,
  });
}