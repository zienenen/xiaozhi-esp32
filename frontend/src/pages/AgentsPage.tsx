import { Alert, Avatar, Button, Card, Descriptions, Form, Input, Modal, Select, Space, Typography, message } from "antd";
import { useState } from "react";
import { Link } from "react-router-dom";
import { api, readableError, unwrapList } from "../shared/api";
import { useAuth } from "../shared/auth";
import { Agent } from "../shared/types";
import { formatTime, Loadable, PageHeader, StateTag } from "../shared/ui";
import { useApiData } from "../shared/useApi";

export function AgentsPage() {
  const auth = useAuth();
  const state = useApiData(async () => unwrapList<Agent>((await api.get("/agents")).data), []);
  const [editing, setEditing] = useState<Agent | null | undefined>(undefined);
  const [preview, setPreview] = useState<Agent | null>(null);
  const [form] = Form.useForm<Agent>();
  const [saving, setSaving] = useState(false);
  const [messageApi, context] = message.useMessage();

  const open = (agent: Agent | null) => {
    setEditing(agent);
    form.resetFields();
    form.setFieldsValue(agent || { status: "active" } as Agent);
  };

  const save = async (values: Agent) => {
    setSaving(true);
    try {
      if (editing) await api.patch(`/agents/${editing.agent_id}`, values);
      else await api.post("/agents", values);
      messageApi.success("角色配置已保存，并标记为待同步到官网");
      setEditing(undefined);
      await state.reload();
    } catch (error) {
      messageApi.error(readableError(error));
    } finally {
      setSaving(false);
    }
  };

  return <>
    {context}
    <PageHeader
      title="角色配置"
      description="自研平台维护角色 Prompt、性格设定、音色、知识引用与配置版本；修改后需重新同步到小智官网。"
      extra={<Space wrap><Link to="/admin/official-sync"><Button>官网同步状态</Button></Link><Button type="primary" disabled={!auth.canManage} onClick={() => open(null)}>新建角色</Button></Space>}
    />
    {!auth.canManage && <Alert type="info" showIcon message="当前身份为只读，编辑操作已禁用。" className="section-card" />}
    <Loadable loading={state.loading} error={state.error} empty={!state.data?.length} onRetry={state.reload}>
      <div className="agent-workbench">
        {(state.data || []).map(agent => (
          <Card
            key={agent.agent_id}
            className="agent-workbench-card"
            actions={[
              <Button onClick={() => open(agent)} disabled={!auth.canManage}>配置</Button>,
              <Link to={`/admin/conversations?agent_id=${agent.agent_id}`}><Button>对话</Button></Link>,
              <Link to={`/admin/checkins?agent_id=${agent.agent_id}`}><Button>打卡</Button></Link>,
              <Link to={`/admin/official-sync?agent_id=${agent.agent_id}`}><Button>同步</Button></Link>
            ]}
          >
            <div className="agent-card-heading">
              <Avatar size={52}>{agent.name?.slice(0, 1) || "角"}</Avatar>
              <div className="agent-card-title">
                <Space wrap>
                  <Typography.Title level={4}>{agent.name}</Typography.Title>
                  <StateTag value={agent.status} />
                </Space>
                <Typography.Text type="secondary">{agent.agent_id}</Typography.Text>
              </div>
              <StateTag value={agent.official_sync_status || "not_synced"} />
            </div>
            <div className="prototype-agent-meta">
              <div><span>角色</span><strong>{agent.personality_prompt?.slice(0, 8) || "待配置"}</strong></div>
              <div><span>模型 / 音色</span><strong>{agent.voice_id || "待配置"}</strong></div>
              <div><span>最近同步</span><strong>{formatTime(agent.official_synced_at)}</strong></div>
            </div>
          </Card>
        ))}
      </div>
    </Loadable>

    <Modal title={editing ? "编辑角色配置" : "新建角色"} open={editing !== undefined} onCancel={() => setEditing(undefined)} onOk={() => form.submit()} confirmLoading={saving} width={680} destroyOnClose>
      <Alert type="warning" showIcon message="保存后该配置将标记为“待同步到官网”，官网不会自动生效。" className="modal-alert" />
      <Form form={form} layout="vertical" onFinish={save}>
        <div className="form-grid">
          <Form.Item name="agent_id" label="角色 ID" rules={[{ required: true }]}><Input disabled={Boolean(editing)} /></Form.Item>
          <Form.Item name="name" label="角色名称" rules={[{ required: true }]}><Input /></Form.Item>
        </div>
        <Form.Item name="personality_prompt" label="性格设定 / 人格 Prompt" rules={[{ required: true }]}><Input.TextArea rows={7} showCount /></Form.Item>
        <div className="form-grid">
          <Form.Item name="voice_id" label="voice_id"><Input /></Form.Item>
          <Form.Item name="dataset_id" label="知识库 / 数据集引用"><Input /></Form.Item>
          <Form.Item name="prompt_version" label="配置版本"><Input placeholder="例如 v3；保存后由后端校验或生成" /></Form.Item>
          <Form.Item name="status" label="角色状态" rules={[{ required: true }]}>
            <Select options={[{ value: "active", label: "启用" }, { value: "disabled", label: "停用" }, { value: "draft", label: "草稿" }]} />
          </Form.Item>
        </div>
      </Form>
    </Modal>

    <Modal title="角色配置预览" open={Boolean(preview)} onCancel={() => setPreview(null)} footer={<Space><Link to={`/admin/official-sync?agent_id=${preview?.agent_id || ""}`}><Button type="primary">查看同步快照</Button></Link><Button onClick={() => setPreview(null)}>关闭</Button></Space>} width={720}>
      {preview && <Descriptions bordered column={1} items={[
        { key: "name", label: "角色", children: `${preview.name}（${preview.agent_id}）` },
        { key: "version", label: "配置版本", children: preview.prompt_version || "未生成" },
        { key: "prompt", label: "性格设定 / Prompt", children: <Typography.Paragraph className="pre-wrap">{preview.personality_prompt}</Typography.Paragraph> },
        { key: "voice", label: "voice_id", children: preview.voice_id || "未配置" },
        { key: "dataset", label: "知识引用", children: preview.dataset_id || "未配置" },
        { key: "sync", label: "官网同步状态", children: <StateTag value={preview.official_sync_status || "not_synced"} /> },
        { key: "synced", label: "最近同步", children: formatTime(preview.official_synced_at) },
        { key: "operator", label: "操作人", children: preview.official_sync_operator || "—" },
        { key: "failure", label: "失败原因", children: preview.official_sync_failure_reason || "—" }
      ]} />}
    </Modal>
  </>;
}
