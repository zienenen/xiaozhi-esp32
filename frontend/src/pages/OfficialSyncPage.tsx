import { Alert, Button, Card, Descriptions, Drawer, Form, Input, Modal, Select, Space, Table, Typography, message } from "antd";
import { useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { api, readableError, unwrapList } from "../shared/api";
import { useAuth } from "../shared/auth";
import { Agent, OfficialSyncLog, OfficialSyncSnapshot } from "../shared/types";
import { formatTime, Loadable, PageHeader, StateTag } from "../shared/ui";
import { useApiData } from "../shared/useApi";

function snapshotText(snapshot: OfficialSyncSnapshot) {
  return [
    `配置版本：${snapshot.config_version || "—"}`,
    `Prompt：${snapshot.personality_prompt || snapshot.prompt || "—"}`,
    `voice_id：${snapshot.voice_id || "—"}`,
    `工具 URL：${snapshot.tool_url || snapshot.tool_urls?.join(", ") || "—"}`,
    `知识库引用：${snapshot.knowledge_reference || snapshot.dataset_id || "—"}`
  ].join("\n\n");
}

export function OfficialSyncPage() {
  const auth = useAuth();
  const [params] = useSearchParams();
  const initialAgentId = params.get("agent_id") || undefined;
  const [targetType, setTargetType] = useState<"agent" | "device">(initialAgentId ? "agent" : "agent");
  const [agentId, setAgentId] = useState(initialAgentId);
  const [status, setStatus] = useState<string>();
  const [selected, setSelected] = useState<OfficialSyncLog | null>(null);
  const [updating, setUpdating] = useState<OfficialSyncLog | null>(null);
  const [form] = Form.useForm();
  const [messageApi, context] = message.useMessage();
  const agents = useApiData(async () => unwrapList<Agent>((await api.get("/agents")).data), []);
  const logs = useApiData(
    async () => unwrapList<OfficialSyncLog>((await api.get("/official-sync-logs", { params: { target_type: targetType, target_id: agentId, status } })).data),
    [targetType, agentId, status]
  );
  const names = useMemo(() => new Map((agents.data || []).map(agent => [agent.agent_id, agent.name])), [agents.data]);

  const copy = async (snapshot: OfficialSyncSnapshot) => {
    try {
      await navigator.clipboard.writeText(snapshotText(snapshot));
      messageApi.success("官网配置快照已复制");
    } catch {
      messageApi.error("复制失败，请在快照详情中手动选择文本");
    }
  };

  const openUpdate = (log: OfficialSyncLog, nextStatus: "synced" | "failed" | "manual_required") => {
    setUpdating(log);
    form.setFieldsValue({ status: nextStatus, operator: log.operator, failure_reason: log.failure_reason, note: log.note });
  };

  const saveUpdate = async (values: { status: string; operator: string; failure_reason?: string; note?: string }) => {
    if (!updating) return;
    try {
      await api.patch(`/official-sync-logs/${updating.sync_id}`, values);
      messageApi.success("官网同步状态已更新并留痕");
      setUpdating(null);
      await logs.reload();
    } catch (error) {
      messageApi.error(readableError(error));
    }
  };

  return <>
    {context}
    <PageHeader title="小智官网同步" description="查看角色配置是否已同步，复制脱敏快照，并记录人工或半自动同步结果。" />
    <Alert type="info" showIcon message="一期采用半自动同步：本页生成配置快照和留痕，不会自动登录或修改小智官网。" />
    <Card className="section-card filter-card">
      <Space wrap>
        <Select
          value={targetType}
          style={{ width: 150 }}
          onChange={value => { setTargetType(value); setAgentId(undefined); }}
          options={[{ value: "agent", label: "角色配置" }, { value: "device", label: "设备配置" }]}
        />
        {targetType === "agent" ? <Select
            allowClear
            showSearch
            loading={agents.loading}
            value={agentId}
            placeholder="筛选角色"
            style={{ width: 240 }}
            onChange={setAgentId}
            options={(agents.data || []).map(agent => ({ value: agent.agent_id, label: `${agent.name} · ${agent.agent_id}` }))}
          /> : <Input allowClear placeholder="筛选设备 ID" style={{ width: 240 }} onPressEnter={event => setAgentId(event.currentTarget.value || undefined)} onBlur={event => setAgentId(event.currentTarget.value || undefined)} />}
        <Select
          allowClear
          value={status}
          placeholder="同步状态"
          style={{ width: 180 }}
          onChange={setStatus}
          options={[
            { value: "pending", label: "待同步" },
            { value: "synced", label: "已同步" },
            { value: "failed", label: "失败" },
            { value: "manual_required", label: "需人工处理" }
          ]}
        />
        <Button onClick={logs.reload}>刷新状态</Button>
      </Space>
    </Card>

    <Loadable loading={logs.loading} error={logs.error} empty={!logs.data?.length} onRetry={logs.reload}>
      <Card className="section-card">
        <Table
          rowKey="sync_id"
          dataSource={logs.data || []}
          scroll={{ x: 1180 }}
          pagination={{ pageSize: 10 }}
          columns={[
            { title: "同步对象", width: 190, render: (_, row) => <><Space><StateTag value={row.target_type} /><Typography.Text strong>{row.target_name || names.get(row.target_id) || row.target_id}</Typography.Text></Space><br /><Typography.Text type="secondary">{row.target_id}</Typography.Text></> },
            { title: "配置版本", render: (_, row) => row.payload_snapshot.config_version || "—" },
            { title: "同步状态", dataIndex: "status", render: value => <StateTag value={value} /> },
            { title: "同步方式", dataIndex: "sync_mode", render: value => value === "manual_copy" ? "人工复制" : value === "semi_auto" ? "半自动" : "API" },
            { title: "操作人", dataIndex: "operator", render: value => value || "—" },
            { title: "最近同步", dataIndex: "synced_at", render: formatTime },
            { title: "失败原因 / 备注", ellipsis: true, render: (_, row) => row.failure_reason || row.note || "—" },
            { title: "操作", fixed: "right", width: 260, render: (_, row) => <Space><Button size="small" onClick={() => setSelected(row)}>查看快照</Button><Button size="small" onClick={() => void copy(row.payload_snapshot)}>复制</Button>{auth.canManage && <Button size="small" type="primary" onClick={() => openUpdate(row, "synced")}>标记结果</Button>}</Space> }
          ]}
        />
      </Card>
    </Loadable>

    <Drawer title="官网配置快照" width={720} open={Boolean(selected)} onClose={() => setSelected(null)} extra={selected && <Button type="primary" onClick={() => void copy(selected.payload_snapshot)}>复制全部配置</Button>}>
      {selected && <>
        <Descriptions bordered column={1} items={[
          { key: "target", label: "同步对象", children: <Space><StateTag value={selected.target_type} />{selected.target_name || names.get(selected.target_id) || selected.target_id}</Space> },
          { key: "status", label: "同步状态", children: <StateTag value={selected.status} /> },
          { key: "version", label: "配置版本", children: selected.payload_snapshot.config_version || "—" },
          { key: "prompt", label: "Prompt / 性格设定", children: <Typography.Paragraph className="pre-wrap">{selected.payload_snapshot.personality_prompt || selected.payload_snapshot.prompt || "未配置"}</Typography.Paragraph> },
          { key: "voice", label: "voice_id", children: selected.payload_snapshot.voice_id || "未配置" },
          { key: "tool", label: "工具 URL", children: selected.payload_snapshot.tool_url || selected.payload_snapshot.tool_urls?.join("\n") || "未配置" },
          { key: "knowledge", label: "知识库引用", children: selected.payload_snapshot.knowledge_reference || selected.payload_snapshot.dataset_id || "未配置" },
          { key: "operator", label: "操作人", children: selected.operator || "—" },
          { key: "time", label: "同步时间", children: formatTime(selected.synced_at) },
          { key: "failure", label: "失败原因", children: selected.failure_reason || "—" },
          { key: "note", label: "人工备注", children: selected.note || "—" }
        ]} />
        <Alert type="warning" showIcon message="快照不包含官网账号、密码、token 等敏感信息。" className="section-card" />
      </>}
    </Drawer>

    <Modal title="记录官网同步结果" open={Boolean(updating)} onCancel={() => setUpdating(null)} onOk={() => form.submit()} destroyOnClose>
      <Form form={form} layout="vertical" onFinish={saveUpdate}>
        <Form.Item name="status" label="同步状态" rules={[{ required: true }]}>
          <Select options={[
            { value: "synced", label: "已同步" },
            { value: "failed", label: "失败" },
            { value: "manual_required", label: "需人工处理" },
            { value: "pending", label: "待同步" }
          ]} />
        </Form.Item>
        <Form.Item name="operator" label="操作人" rules={[{ required: true }]}><Input /></Form.Item>
        <Form.Item name="failure_reason" label="失败原因"><Input.TextArea rows={3} /></Form.Item>
        <Form.Item name="note" label="人工备注"><Input.TextArea rows={3} /></Form.Item>
      </Form>
    </Modal>
  </>;
}
