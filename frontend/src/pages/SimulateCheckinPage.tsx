import { Alert, Button, Card, Form, Input, Select, Switch, Typography, message } from "antd";
import { Navigate } from "react-router-dom";
import { api, readableError, unwrapList } from "../shared/api";
import { useAuth } from "../shared/auth";
import { Device, NfcTag, Spot } from "../shared/types";
import { PageHeader, StateTag } from "../shared/ui";
import { useApiData } from "../shared/useApi";

export function SimulateCheckinPage() {
  const auth = useAuth(); const devices = useApiData(async () => unwrapList<Device>((await api.get("/devices")).data), []); const spots = useApiData(async () => unwrapList<Spot>((await api.get("/spots")).data), []); const tags = useApiData(async () => unwrapList<NfcTag>((await api.get("/nfc-tags")).data), []); const [form] = Form.useForm(); const [msg, context] = message.useMessage();
  if (!auth.canSimulate) return <Navigate to="/" replace />;
  const submit = async (values: unknown) => { try { const response = await api.post("/demo/simulate-checkin", values); msg.success({ content: <span>模拟记录已生成 <StateTag value="simulation" /></span> }); form.resetFields(); return response; } catch (e) { msg.error(readableError(e)); } };
  const loadError = devices.error || spots.error || tags.error;
  return <>{context}<PageHeader title="手动模拟打卡" description="仅测试 / 原厂身份可见，用于无硬件或室内联调。" /><Alert type="warning" showIcon message="本页生成的记录始终标记为 source=simulation，不得作为真实验收数据。" className="section-card" />{loadError && <Alert type="error" showIcon message="基础数据加载失败" description={loadError} className="section-card" />}<Card><Form form={form} layout="vertical" initialValues={{ simulate_gps_nearby: true, reason: "indoor demo" }} onFinish={submit}><Form.Item name="device_id" label="设备" rules={[{ required: true }]}><Select loading={devices.loading} options={(devices.data || []).map(d => ({ value: d.device_id, label: `${d.name || d.device_id} · ${d.online_status}` }))} /></Form.Item><Form.Item name="spot_id" label="点位" rules={[{ required: true }]}><Select loading={spots.loading} options={(spots.data || []).filter(s => s.status === "active").map(s => ({ value: s.spot_id, label: s.name }))} /></Form.Item><Form.Item name="tag_id" label="NFC 标签" rules={[{ required: true }]}><Select loading={tags.loading} options={(tags.data || []).filter(t => t.status === "active").map(t => ({ value: t.tag_id, label: `${t.label || t.tag_id} · ${t.spot_id}` }))} /></Form.Item><Form.Item name="simulate_gps_nearby" label="模拟 GPS 已接近" valuePropName="checked"><Switch /></Form.Item><Form.Item name="reason" label="模拟原因" rules={[{ required: true }]}><Input /></Form.Item><Button type="primary" htmlType="submit">生成模拟记录</Button></Form></Card><Typography.Paragraph type="secondary" className="safe-note">真实设备上报请使用设备接口；本页面不会请求或展示 device token。</Typography.Paragraph></>;
}
