import { Alert, Button, Card, Empty, Flex, Skeleton, Space, Tag, Typography } from "antd";
import { ReactNode } from "react";

const stateMap: Record<string, { color: string; text: string }> = {
  online: { color: "success", text: "在线" }, offline: { color: "default", text: "离线" }, unknown: { color: "default", text: "未知" },
  active: { color: "success", text: "启用" }, disabled: { color: "default", text: "停用" }, draft: { color: "warning", text: "草稿" },
  fixed: { color: "success", text: "已定位" }, no_fix: { color: "error", text: "GPS 无 fix" }, stale: { color: "warning", text: "定位过期" }, near_spot: { color: "processing", text: "已接近点位" },
  success: { color: "success", text: "成功" }, failed: { color: "error", text: "失败" }, duplicate: { color: "warning", text: "重复打卡" }, simulated: { color: "purple", text: "模拟成功" },
  vectorized: { color: "success", text: "已向量化" }, ready: { color: "success", text: "可用" }, chunked: { color: "processing", text: "已切分" },
  device: { color: "blue", text: "真实设备" }, simulation: { color: "purple", text: "模拟数据" }, config_error: { color: "error", text: "配置异常" },
  agent: { color: "geekblue", text: "角色" },
  not_synced: { color: "warning", text: "待同步到官网" }, pending: { color: "warning", text: "待同步" }, synced: { color: "success", text: "已同步" },
  manual_required: { color: "orange", text: "需人工处理" }, open: { color: "processing", text: "进行中" }, closed: { color: "success", text: "已结束" },
  official_manual_import: { color: "purple", text: "官网人工导入" }, tool_callback: { color: "blue", text: "工具回调" },
  device_log: { color: "cyan", text: "设备日志" }, self_hosted_voice: { color: "green", text: "自建语音链路" }
};

const failureMap: Record<string, string> = {
  backend_unavailable: "后端不可用", device_offline: "设备离线", gps_no_fix: "GPS 无 fix", tag_unknown: "NFC 标签未登记",
  tag_disabled: "NFC 标签已停用", duplicate: "重复打卡（冷却期内）", dataset_failed: "数据集处理失败", device_not_bound: "设备未绑定角色",
  spot_disabled: "点位已停用", spot_mismatch: "标签与点位不匹配", permission_denied: "无权执行此操作"
};

export function StateTag({ value }: { value?: string | null }) {
  const item = stateMap[value || "unknown"];
  return <Tag color={item?.color}>{item?.text ?? value ?? "未知"}</Tag>;
}

export function FailureReason({ code, detail }: { code?: string | null; detail?: string | null }) {
  if (!code && !detail) return <Typography.Text type="secondary">无异常</Typography.Text>;
  return <Alert type="warning" showIcon message={failureMap[code || ""] || detail || code} />;
}

export function PageHeader({ title, description, extra }: { title: string; description: string; extra?: ReactNode }) {
  return <Flex className="page-header" justify="space-between" align="flex-start" gap={16} wrap><div><Typography.Title level={2}>{title}</Typography.Title><Typography.Paragraph type="secondary">{description}</Typography.Paragraph></div>{extra}</Flex>;
}

export function Loadable({ loading, error, empty, onRetry, children }: { loading: boolean; error?: string | null; empty?: boolean; onRetry: () => void; children: ReactNode }) {
  if (loading) return <Card><Skeleton active paragraph={{ rows: 6 }} /></Card>;
  if (error) return <Alert type="error" showIcon message="数据加载失败" description={error} action={<Button onClick={onRetry}>重试</Button>} />;
  if (empty) return <Card><Empty description="暂无数据"><Button onClick={onRetry}>刷新</Button></Empty></Card>;
  return <>{children}</>;
}

export function MetricCard({ title, value, status, detail }: { title: string; value: ReactNode; status?: string; detail?: ReactNode }) {
  return <Card className="metric-card"><Space direction="vertical" size={8}><Typography.Text type="secondary">{title}</Typography.Text><Typography.Title level={4}>{value}</Typography.Title>{status && <StateTag value={status} />}{detail}</Space></Card>;
}

export function formatTime(value?: string) {
  return value ? new Date(value).toLocaleString("zh-CN", { hour12: false }) : "—";
}
