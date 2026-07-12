import { Card, Select, Space, Table, Typography } from "antd";
import { useState } from "react";
import { useSearchParams } from "react-router-dom";
import { api, unwrapList } from "../shared/api";
import { Checkin } from "../shared/types";
import { formatTime, Loadable, PageHeader, StateTag } from "../shared/ui";
import { useApiData } from "../shared/useApi";

const failureText: Record<string, string> = { tag_unknown: "NFC 标签未登记", tag_disabled: "NFC 标签已停用", spot_mismatch: "标签与点位不匹配", device_not_bound: "设备未绑定角色", spot_disabled: "点位已停用", gps_no_fix: "GPS 无 fix" };
export function CheckinsPage() {
  const [params] = useSearchParams(); const [result, setResult] = useState<string>(); const [source, setSource] = useState<string>(); const deviceId = params.get("device_id") || undefined;
  const state = useApiData(async () => unwrapList<Checkin>((await api.get("/checkins", { params: { device_id: deviceId, result, source } })).data), [deviceId, result, source]);
  return <><PageHeader title="打卡记录" description="查询成功、失败、重复和模拟记录；模拟数据不计入真实验收。" /><Space wrap className="filters"><Select allowClear placeholder="结果" style={{ width: 160 }} onChange={setResult} options={["success", "failed", "duplicate", "simulated"].map(v => ({ value: v, label: v }))} /><Select allowClear placeholder="来源" style={{ width: 160 }} onChange={setSource} options={[{ value: "device", label: "真实设备" }, { value: "simulation", label: "模拟数据" }]} />{deviceId && <Typography.Text>设备筛选：{deviceId}</Typography.Text>}</Space><Loadable loading={state.loading} error={state.error} empty={!state.data?.length} onRetry={state.reload}><Card><Table rowKey="checkin_id" dataSource={state.data || []} scroll={{ x: 980 }} columns={[{ title: "时间", dataIndex: "checked_in_at", render: formatTime }, { title: "设备 / 角色", render: (_, c) => <>{c.device_id}<br/><Typography.Text type="secondary">{c.agent_id || "未绑定"}</Typography.Text></> }, { title: "点位 / 标签", render: (_, c) => <>{c.spot_id || "—"}<br/><Typography.Text type="secondary">{c.tag_id || "—"}</Typography.Text></> }, { title: "结果", dataIndex: "result", render: v => <StateTag value={v} /> }, { title: "来源", dataIndex: "source", render: v => <StateTag value={v} /> }, { title: "失败原因", dataIndex: "failure_code", render: v => v ? (failureText[v] || v) : "—" }]} /></Card></Loadable></>;
}
