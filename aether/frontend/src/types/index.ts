export interface User {
  id: string;
  email: string;
  full_name?: string;
  is_active: boolean;
  subscription_tier: string;
  created_at: string;
}

export interface Agent {
  id: string;
  name: string;
  description?: string;
  type: string;
  status: string;
  configuration: any;
  execution_count: number;
  last_execution?: string;
  created_at: string;
  updated_at?: string;
  user_id: string;
}

export interface AgentExecution {
  id: string;
  task_input?: any;
  task_output?: any;
  status: string;
  execution_time_ms?: number;
  error_message?: string;
  created_at: string;
  completed_at?: string;
  agent_id: string;
  user_id: string;
}