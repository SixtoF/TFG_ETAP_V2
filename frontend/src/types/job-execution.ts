export type JobExecutionEnqueueResponse = {
  job_id: string;
  status: string;
  message: string;
  celery_task_id: string;
};