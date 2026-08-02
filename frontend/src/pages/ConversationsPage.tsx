import { Alert, Button, Card, Descriptions, Drawer, Input, List, Select, Space, Table, Timeline, Typography } from "antd";
import { useState } from "react";
import { api, readableError, unwrap, unwrapList } from "../shared/api";
import { ConversationMessage, ConversationSession } from "../shared/types";
import { formatTime, Loadable, PageHeader, StateTag } from "../shared/ui";
import { useApiData } from "../shared/useApi";

type Filters = { device_id?: string; agent_id?: string; spot_id?: string; source?: string; date_from?: string; date_to?: string };

function sessionMessages(session: ConversationSession): ConversationMessage[] {
  if (session.messages?.length) return session.messages;
  const rows: ConversationMessage[] = [];
  if (session.user_input) rows.push({ message_id: `${session.session_id}-user`, session_id: session.session_id, role: "user", content: session.user_input, content_source: "api", created_at: session.started_at });
  if (session.ai_reply) rows.push({ message_id: `${session.session_id}-assistant`, session_id: session.session_id, role: "assistant", content: session.ai_reply, content_source: "api", created_at: session.ended_at || session.started_at, metadata: { knowledge_summary: session.knowledge_summary } });
  return rows;
}

export function ConversationsPage() {
  const [filters, setFilters] = useState<Filters>({});
  const [selected, setSelected] = useState<ConversationSession | null>(null);
  const [detailLoading, setDetailLoading] = useState(false);
  const [detailError, setDetailError] = useState<string | null>(null);
  const state = useApiData(
    async () => unwrapList<ConversationSession>((await api.get("/conversation-sessions", { params: filters })).data),
    [filters.device_id, filters.agent_id, filters.spot_id, filters.source, filters.date_from, filters.date_to]
  );

  const openDetail = async (session: ConversationSession) => {
    setSelected(session);
    setDetailError(null);
    setDetailLoading(true);
    try {
      setSelected(unwrap<ConversationSession>((await api.get(`/conversation-sessions/${session.session_id}`)).data));
    } catch (error) {
      setDetailError(readableError(error));
    } finally {
      setDetailLoading(false);
    }
  };

  const set = (key: keyof Filters, value?: string) => setFilters(current => ({ ...current, [key]: value || undefined }));

  return <>
    <PageHeader title="对话记录" description="追溯设备与角色对话、景点上下文、知识片段和数据来源；人工导入或设备日志不会冒充实时语音记录。" />
    <Card className="filter-card">
      <div className="filter-grid">
        <Input allowClear placeholder="设备 ID" aria-label="按设备筛选" onPressEnter={event => set("device_id", event.currentTarget.value)} onBlur={event => set("device_id", event.currentTarget.value)} />
        <Input allowClear placeholder="角色 ID" aria-label="按角色筛选" onPressEnter={event => set("agent_id", event.currentTarget.value)} onBlur={event => set("agent_id", event.currentTarget.value)} />
        <Input allowClear placeholder="点位 ID" aria-label="按点位筛选" onPressEnter={event => set("spot_id", event.currentTarget.value)} onBlur={event => set("spot_id", event.currentTarget.value)} />
        <Select allowClear placeholder="来源" onChange={value => set("source", value)} options={[
          { value: "official_manual_import", label: "官网人工导入" },
          { value: "tool_callback", label: "工具回调" },
          { value: "device_log", label: "设备日志" },
          { value: "self_hosted_voice", label: "自建语音链路" }
        ]} />
        <Input type="date" aria-label="开始日期" onChange={event => set("date_from", event.target.value)} />
        <Input type="date" aria-label="结束日期" onChange={event => set("date_to", event.target.value)} />
      </div>
    </Card>

    <Loadable loading={state.loading} error={state.error} empty={!state.data?.length} onRetry={state.reload}>
      <Card className="section-card">
        <Table
          rowKey="session_id"
          dataSource={state.data || []}
          scroll={{ x: 1050 }}
          pagination={{ pageSize: 10 }}
          columns={[
            { title: "时间", dataIndex: "started_at", width: 180, render: formatTime },
            { title: "设备 / 角色", width: 190, render: (_, row) => <>{row.device_id}<br /><Typography.Text type="secondary">{row.agent_id}</Typography.Text></> },
            { title: "点位", dataIndex: "spot_id", render: value => value || "—" },
            { title: "对话摘要", dataIndex: "summary", ellipsis: true, render: value => value || "暂无摘要" },
            { title: "来源", dataIndex: "source", render: value => <StateTag value={value} /> },
            { title: "状态", dataIndex: "status", render: value => <StateTag value={value} /> },
            { title: "操作", fixed: "right", render: (_, row) => <Button size="small" onClick={() => void openDetail(row)}>查看详情</Button> }
          ]}
        />
      </Card>
    </Loadable>

    <Drawer title="对话详情" width={720} open={Boolean(selected)} onClose={() => setSelected(null)}>
      {selected && <>
        <Descriptions bordered column={{ xs: 1, sm: 2 }} items={[
          { key: "session", label: "会话 ID", children: selected.session_id },
          { key: "source", label: "来源", children: <StateTag value={selected.source} /> },
          { key: "device", label: "设备", children: selected.device_id },
          { key: "agent", label: "角色", children: selected.agent_id },
          { key: "spot", label: "关联点位", children: selected.spot_id || "—" },
          { key: "time", label: "开始时间", children: formatTime(selected.started_at) },
          { key: "status", label: "结果状态", children: <StateTag value={selected.status} /> },
          { key: "summary", label: "会话摘要", children: selected.summary || "—", span: 2 }
        ]} />
        {detailError && <Alert type="warning" showIcon message="详情接口加载失败，当前显示列表摘要" description={detailError} className="section-card" />}
        <Card title="消息内容" loading={detailLoading} className="section-card">
          <Timeline items={sessionMessages(selected).map(message => ({
            color: message.role === "user" ? "blue" : message.role === "assistant" ? "green" : "gray",
            children: <div>
              <Space wrap><Typography.Text strong>{message.role === "user" ? "用户输入" : message.role === "assistant" ? "AI 回复" : message.role}</Typography.Text><StateTag value={message.content_source} /><Typography.Text type="secondary">{formatTime(message.created_at)}</Typography.Text></Space>
              <Typography.Paragraph className="conversation-content">{message.content}</Typography.Paragraph>
              {message.metadata?.knowledge_summary && <Alert type="info" showIcon message="命中知识片段" description={String(message.metadata.knowledge_summary)} />}
              {message.metadata?.dataset_id && <Typography.Text type="secondary">数据集：{String(message.metadata.dataset_id)}</Typography.Text>}
            </div>
          }))} />
          {!detailLoading && sessionMessages(selected).length === 0 && <List locale={{ emptyText: "该会话暂无消息内容" }} />}
        </Card>
      </>}
    </Drawer>
  </>;
}
