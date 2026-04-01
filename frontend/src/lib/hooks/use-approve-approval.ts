"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { approveApprovalRequest } from "@/lib/api/approvals";

export function useApproveApproval() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      approvalId,
      resolutionComment,
    }: {
      approvalId: string;
      resolutionComment: string | null;
    }) =>
      approveApprovalRequest(approvalId, {
        resolution_comment: resolutionComment,
      }),
    onSuccess: async () => {
      await Promise.all([
        queryClient.invalidateQueries({ queryKey: ["approvals"] }),
        queryClient.invalidateQueries({ queryKey: ["jobs"] }),
      ]);
    },
  });
}