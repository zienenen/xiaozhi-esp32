import { Button, Card, Descriptions, Input, Select, Space, Table, Typography } from "antd";
import { useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api, unwrap, unwrapList } from "../shared/api";
import { Device } from "../shared/types";
import { formatTime, Loadable, PageHeader, StateTag } from "../shared/ui";
import { useApiData } from "../shared/useApi";

export function DevicesPage() {
  const state = useApiData(async () => unwrapList<Device>((await api.get("/devices")).data), []); const [query, setQuery] = useState(""); const [status, setStatus] = useState<string>();
  const rows = useMemo(() => (state.data || []).filter((d) => (!status || d.online_status === status) && [d.device_id, d.sn, d.name, d.bound_agent_id].some(v => v?.toLowerCase().includes(query.toLowerCase()))), [state.data, query, status]);
  return <><PageHeader title="设备" description="查看设备身份、唯一绑定角色、在线与最近 GPS 状态。" /><Space wrap className="filters"><Input.Search aria-label="搜索设备" placeholder="搜索名称、SN、角色" allowClear onChange={e => setQuery(e.target.value)} /><Select allowClear placeholder="在线状态" style={{ width: 150 }} onChange={setStatus} options={[{ value: "online", label: "在线" }, { value: "offline", label: "离线" }, { value: "unknown", label: "未知" }]} /></Space><Loadable loading={state.loading} error={state.error} empty={!rows.length} onRetry={state.reload}><Card><Table rowKey="device_id" dataSource={rows} scroll={{ x: 760 }} pagination={{ pageSize: 8 }} columns={[{ title: "设备", render: (_, d) => <><Link to={`/admin/devices/${d.device_id}`}>{d.name || d.device_id}</Link><br/><Typography.Text type="secondary">{d.sn}</Typography.Text></> }, { title: "状态", dataIndex: "online_status", render: v => <StateTag value={v} /> }, { title: "唯一绑定角色", dataIndex: "bound_agent_id", render: v => v || <Typography.Text type="secondary">未绑定</Typography.Text> }, { title: "最近在线", dataIndex: "last_seen_at", render: formatTime }, { title: "GPS", dataIndex: "last_gps_status", render: v => <StateTag value={v} /> }, { title: "操作", render: (_, d) => <Link to={`/admin/devices/${d.device_id}`}><Button size="small">详情</Button></Link> }]} /></Card></Loadable></>;
}
export function DeviceDetailPage() {
  const { id } = useParams(); const state = useApiData(async () => unwrap<Device>((await api.get(`/devices/${id}`)).data), [id]); const d = state.data;
  return <><PageHeader title="设备详情" description="设备配置、在线、GPS 与绑定状态。" /><Loadable loading={state.loading} error={state.error} empty={!d} onRetry={state.reload}>{d && <Card><Descriptions bordered column={{ xs: 1, sm: 2 }} items={[{ key: "id", label: "device_id", children: d.device_id }, { key: "sn", label: "SN", children: d.sn }, { key: "name", label: "名称", children: d.name || "—" }, { key: "online", label: "在线状态", children: <StateTag value={d.online_status} /> }, { key: "agent", label: "唯一绑定角色", children: d.bound_agent_id || "未绑定" }, { key: "seen", label: "最近在线", children: formatTime(d.last_seen_at) }, { key: "gps", label: "最近 GPS", children: <StateTag value={d.last_gps_status} /> }, { key: "checkin", label: "最近打卡", children: formatTime(d.last_checkin_at) }]} /><Typography.Paragraph type="secondary" className="safe-note">安全说明：页面不请求、不显示完整 device token。</Typography.Paragraph></Card>}</Loadable></>;
}
