export type ScheduledTask = {
  id: string;
  name: string;
  description: string | null;
  command_text: string;
  cron_expression: string;
  timezone: string;
  is_active: boolean;
  auto_enqueue: boolean;
  last_run_at: string | null;
  next_run_at: string;
  created_at: string;
  updated_at: string;
};

export type CreateScheduledTaskRequest = {
  name: string;
  description: string | null;
  command_text: string;
  cron_expression: string;
  timezone: string;
  auto_enqueue: boolean;
};