import { apiRequest } from "./client";
import type { Job } from "@/types/job";
import type { ExecutionLog } from "@/types/execution-log";
import type { JobExecutionEnqueueResponse } from "@/types/job-execution";

export async function getJobsRequest(): Promise<Job[]> {
  return apiRequest<Job[]>("/jobs", {
    method: "GET",
    auth: true,
  });
}

export async function getJobByIdRequest(jobId: string): Promise<Job> {
  return apiRequest<Job>(`/jobs/${jobId}`, {
    method: "GET",
    auth: true,
  });
}

export async function getJobLogsRequest(jobId: string): Promise<ExecutionLog[]> {
  return apiRequest<ExecutionLog[]>(`/jobs/${jobId}/logs`, {
    method: "GET",
    auth: true,
  });
}

export async function executeJobRequest(jobId: string): Promise<JobExecutionEnqueueResponse> {
  return apiRequest<JobExecutionEnqueueResponse>(`/jobs/${jobId}/execute`, {
    method: "POST",
    auth: true,
  });
}