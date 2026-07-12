import axios, { AxiosError } from "axios";

export type ApiEnvelope<T> = { success: boolean; data: T; error?: { code?: string; message?: string } | null };
export type ListResult<T> = { results: T[]; count?: number } | T[];

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "/api/v1",
  timeout: 10000,
  headers: { Accept: "application/json", "Content-Type": "application/json" }
});

export function unwrap<T>(value: ApiEnvelope<T> | T): T {
  if (value && typeof value === "object" && "success" in value) {
    const envelope = value as ApiEnvelope<T>;
    if (!envelope.success) throw new Error(envelope.error?.message || envelope.error?.code || "接口请求失败");
    return envelope.data;
  }
  return value as T;
}

export function unwrapList<T>(value: ApiEnvelope<ListResult<T>> | ListResult<T>): T[] {
  const data = unwrap(value);
  return Array.isArray(data) ? data : data.results ?? [];
}

export function readableError(error: unknown): string {
  if (error instanceof AxiosError) {
    if (!error.response) return "后端服务不可用，请确认服务已启动后重试。";
    const body = error.response.data as ApiEnvelope<unknown> | { detail?: string } | undefined;
    if (body && "error" in body && body.error) return body.error.message || body.error.code || `请求失败（${error.response.status}）`;
    if (body && "detail" in body && body.detail) return body.detail;
    return `请求失败（HTTP ${error.response.status}）`;
  }
  return error instanceof Error ? error.message : "发生未知错误，请重试。";
}
