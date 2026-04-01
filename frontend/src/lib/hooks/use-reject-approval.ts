"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { rejectApprovalRequest } from "@/lib/api/approvals";

export function useRejectApproval() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      approvalId,
      resolutionComment,
    }: {
      approvalId: string;
      resolutionComment: string | null;
    }) =>
      rejectApprovalRequest(approvalId, {
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