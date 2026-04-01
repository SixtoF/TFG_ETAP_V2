export type ApprovalStatus = "pending" | "approved" | "rejected";

export type Approval = {
  id: string;
  job_id: string;
  status: ApprovalStatus;
  reason: string;
  requested_at: string;
  resolved_at: string | null;
  resolved_by_user_id: string | null;
  resolved_by_name: string | null;
  resolution_comment: string | null;
};

export type ApprovalDecisionRequest = {
  resolution_comment: string | null;
};