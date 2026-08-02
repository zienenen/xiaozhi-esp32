export type Device = {
  device_id: string;
  sn: string;
  name?: string;
  online_status: string;
  bound_agent_id?: string;
  last_seen_at?: string;
  last_gps_status?: string;
  last_checkin_at?: string;
};

export type Agent = {
  agent_id: string;
  name: string;
  personality_prompt: string;
  voice_id?: string;
  dataset_id?: string;
  status: string;
  prompt_version?: string;
  official_sync_status?: "not_synced" | "synced" | "failed" | "manual_required";
  official_synced_at?: string;
  official_sync_operator?: string;
  official_sync_failure_reason?: string;
  updated_at?: string;
};

export type Spot = { spot_id: string; name: string; scenic_area_name?: string; latitude: number; longitude: number; gps_radius_meters: number; dataset_id?: string; checkin_message?: string; status: string };
export type NfcTag = { tag_id: string; spot_id?: string; label?: string; status: string; last_seen_at?: string; last_seen_device_id?: string };
export type Checkin = { checkin_id: string; device_id: string; agent_id?: string; spot_id?: string; tag_id?: string; result: string; failure_code?: string; source: "device" | "simulation"; checked_in_at: string };
export type Dataset = { dataset_id: string; name: string; source_type?: string; status: string; chunk_count?: number; updated_at?: string; failure_reason?: string; summary_items?: Array<{ title: string; summary: string; source_ref?: string }>; agent_ids?: string[]; spot_ids?: string[] };
export type Overview = { device?: Device; agent?: Agent; gps?: { status?: string; fix?: boolean; near_spot?: boolean; updated_at?: string; reason?: string }; nfc?: { status?: string; tag_id?: string; spot_id?: string; reason?: string }; latest_checkin?: Checkin & { spot_name?: string; agent_name?: string }; dataset?: Dataset; failure_code?: string; events?: Array<{ time?: string; message: string }> };

export type UserCompanion = {
  device: Device;
  binding?: { agent_id: string; binding_type: string; bound_at?: string; bound_by?: string };
  agent?: Agent;
  recent_conversations: ConversationSession[];
};

export type UserMapPoint = {
  spot_id: string;
  name: string;
  scenic_area_name?: string;
  latitude: number;
  longitude: number;
  gps_radius_meters: number;
  checkin_message?: string;
  state: "stamped" | "nearby" | "available";
  is_nearby: boolean;
  distance_meters?: number;
  nfc_status: "ready" | "unavailable";
  stamp?: { checkin_id: string; checked_in_at: string; tag_id?: string; source: "device" };
};

export type UserMap = {
  device_id: string;
  location: {
    gps_status?: string;
    latitude?: number;
    longitude?: number;
    quality?: string;
    updated_at?: string;
    nearest_spot_id?: string;
    nearest_distance_meters?: number;
    is_near_spot: boolean;
  };
  nfc: { status?: string; tag_id?: string; spot_id?: string; last_seen_at?: string };
  stamp_summary: { earned: number; total: number; simulation_excluded: boolean };
  points: UserMapPoint[];
};

export type ConversationMessage = {
  message_id: string;
  session_id: string;
  role: "user" | "assistant" | "system" | "tool";
  content: string;
  content_source: "manual" | "manual_import" | "simulation" | "official_export" | "device_log" | "xiaozhi_official_device_log" | "api";
  created_at: string;
  metadata?: { knowledge_summary?: string; dataset_id?: string; [key: string]: unknown };
};

export type ConversationSession = {
  session_id: string;
  device_id: string;
  agent_id: string;
  spot_id?: string;
  source: "official_manual_import" | "manual_import" | "simulation" | "tool_callback" | "device_log" | "xiaozhi_official" | "self_hosted_voice";
  started_at: string;
  ended_at?: string;
  summary?: string;
  status: "open" | "closed" | "failed";
  messages?: ConversationMessage[];
  user_input?: string;
  ai_reply?: string;
  knowledge_summary?: string;
};

export type OfficialSyncSnapshot = {
  personality_prompt?: string;
  prompt?: string;
  voice_id?: string;
  tool_url?: string;
  tool_urls?: string[];
  dataset_id?: string;
  knowledge_reference?: string;
  config_version?: string;
  [key: string]: unknown;
};

export type OfficialSyncLog = {
  sync_id: string;
  target_type: "agent" | "device" | "tool" | "voice";
  target_id: string;
  target_name?: string;
  payload_snapshot: OfficialSyncSnapshot;
  sync_mode: "manual_copy" | "semi_auto" | "api";
  status: "pending" | "synced" | "failed" | "manual_required";
  operator?: string;
  synced_at?: string;
  failure_reason?: string;
  note?: string;
  created_at?: string;
};
