export type ExecutionLogLevel = "INFO" | "WARNING" | "ERROR";

export type ExecutionLog = {
  id: number;
  job_id: string;
  job_step_id: string | null;
  level: ExecutionLogLevel;
  message: string;
  details_json: Record<string, unknown> | null;
  created_at: string;
};