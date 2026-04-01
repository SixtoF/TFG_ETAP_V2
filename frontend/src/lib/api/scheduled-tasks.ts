import { apiRequest } from "./client";
import type {
  CreateScheduledTaskRequest,
  ScheduledTask,
} from "@/types/scheduled-task";

export async function getScheduledTasksRequest(): Promise<ScheduledTask[]> {
  return apiRequest<ScheduledTask[]>("/scheduled-tasks", {
    method: "GET",
    auth: true,
  });
}

export async function createScheduledTaskRequest(
  payload: CreateScheduledTaskRequest
): Promise<ScheduledTask> {
  return apiRequest<ScheduledTask>("/scheduled-tasks", {
    method: "POST",
    auth: true,
    body: JSON.stringify(payload),
  });
}

export async function activateScheduledTaskRequest(
  scheduledTaskId: string
): Promise<ScheduledTask> {
  return apiRequest<ScheduledTask>(`/scheduled-tasks/${scheduledTaskId}/activate`, {
    method: "PATCH",
    auth: true,
  });
}

export async function deactivateScheduledTaskRequest(
  scheduledTaskId: string
): Promise<ScheduledTask> {
  return apiRequest<ScheduledTask>(`/scheduled-tasks/${scheduledTaskId}/deactivate`, {
    method: "PATCH",
    auth: true,
  });
}