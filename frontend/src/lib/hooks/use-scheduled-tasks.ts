"use client";

import { useQuery } from "@tanstack/react-query";
import { getScheduledTasksRequest } from "@/lib/api/scheduled-tasks";

export function useScheduledTasks(enabled: boolean = true) {
  return useQuery({
    queryKey: ["scheduled-tasks"],
    queryFn: getScheduledTasksRequest,
    enabled,
    refetchInterval: 10000,
  });
}