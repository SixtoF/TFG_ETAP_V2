import { apiRequest } from "./client";
import type { Approval, ApprovalDecisionRequest } from "@/types/approval";

export async function getApprovalsRequest(): Promise<Approval[]> {
  return apiRequest<Approval[]>("/approvals", {
    method: "GET",
    auth: true,
  });
}

export async function approveApprovalRequest(
  approvalId: string,
  payload: ApprovalDecisionRequest
): Promise<Approval> {
  return apiRequest<Approval>(`/approvals/${approvalId}/approve`, {
    method: "POST",
    auth: true,
    body: JSON.stringify(payload),
  });
}

export async function rejectApprovalRequest(
  approvalId: string,
  payload: ApprovalDecisionRequest
): Promise<Approval> {
  return apiRequest<Approval>(`/approvals/${approvalId}/reject`, {
    method: "POST",
    auth: true,
    body: JSON.stringify(payload),
  });
}