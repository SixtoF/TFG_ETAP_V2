"use client";

import { useQuery } from "@tanstack/react-query";
import { getApprovalsRequest } from "@/lib/api/approvals";

export function useApprovals(enabled: boolean = true) {
  return useQuery({
    queryKey: ["approvals"],
    queryFn: getApprovalsRequest,
    enabled,
    refetchInterval: 10000,
  });
}