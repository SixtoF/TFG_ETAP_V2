export type JobStatus =
  | "created"
  | "ready_to_execute"
  | "queued"
  | "running"
  | "completed"
  | "failed"
  | "approval_pending"
  | "rejected";

export type JobStepStatus =
  | "pending"
  | "running"
  | "completed"
  | "failed"
  | "blocked";

export type JobRiskLevel = "low" | "medium" | "high" | "unknown";

export type JobStep = {
  id: string;
  job_id: string;
  step_order: number;
  name: string;
  step_type: string;
  connector_type: string | null;
  input_json: Record<string, unknown>;
  status: JobStepStatus;
  created_at: string;
  started_at: string | null;
  finished_at: string | null;
};

export type JobResult = {
  id: string;
  job_id: string;
  success: boolean;
  summary: string | null;
  result_json: Record<string, unknown> | null;
  created_at: string;
};

export type Job = {
  id: string;
  command_id: string;
  status: JobStatus;
  intent_name: string;
  risk_level: JobRiskLevel;
  created_at: string;
  started_at: string | null;
  finished_at: string | null;
  steps: JobStep[];
  job_result: JobResult | null;
};