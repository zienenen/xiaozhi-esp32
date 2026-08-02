import { EnvironmentOutlined, LockOutlined, RadarChartOutlined } from "@ant-design/icons";
import { Alert, Avatar, Button, Card, Empty, Input, Modal, Progress, Space, Tag, Typography } from "antd";
import { useEffect, useMemo, useState } from "react";
import { api, unwrap } from "../shared/api";
import { UserCompanion, UserMap, UserMapPoint } from "../shared/types";
import { formatTime, Loadable, StateTag } from "../shared/ui";
import { useApiData } from "../shared/useApi";

const mapPositions = [
  { left: "15%", top: "68%" }, { left: "33%", top: "42%" }, { left: "54%", top: "62%" },
  { left: "70%", top: "30%" }, { left: "84%", top: "54%" }
];

export function MyCompanionPage() {
  const state = useApiData(async () => unwrap<UserCompanion>((await api.get("/user/companion", { params: { recent_limit: 5 } })).data), []);
  const item = state.data;
  useEffect(() => {
    const timer = window.setInterval(() => { void state.silentReload(); }, 5000);
    return () => window.clearInterval(timer);
  }, [state.silentReload]);
  const realMessages = useMemo(() => (item?.recent_conversations || [])
    .flatMap(session => (session.messages || []).map(message => ({ ...message, session })))
    .filter(row => ["device_log", "xiaozhi_official_device_log"].includes(row.content_source))
    .sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime())
    .slice(-10), [item?.recent_conversations]);
  const latestMessage = realMessages[realMessages.length - 1];
  const conversationStatus = item?.device.online_status !== "online"
    ? "设备离线"
    : latestMessage?.role === "user"
      ? "思考中"
      : latestMessage?.role === "assistant"
        ? "回复已更新"
        : "空闲";
  const sourceText = (source: string) => ({
    xiaozhi_official_device_log: "小智官方硬件链路",
    device_log: "真实设备日志",
    manual_import: "手工导入",
    manual: "手工录入",
    simulation: "模拟数据"
  }[source] || source);
  return <div className="user-page prototype-chat-page">
    <Loadable loading={state.loading} error={state.error} empty={!item?.agent} onRetry={state.reload}>
      {item?.agent && <div className="prototype-chat-grid">
        <Card className="role-rail" title="我的盲盒伙伴" extra={<Tag color="blue">已绑定专属伙伴</Tag>}>
          <Typography.Paragraph type="secondary">当前硬件已绑定一个专属伙伴，用户不可自行切换。</Typography.Paragraph>
          <div className="role-option active"><Avatar className="avatar-rose">{item.agent.name.slice(0, 1)}</Avatar><div><Typography.Text strong>{item.agent.name}</Typography.Text><small>当前绑定伙伴</small></div></div>
          <div className="role-option unavailable"><Avatar>?</Avatar><div><Typography.Text strong>其他伙伴</Typography.Text><small>暂未拥有，仅作图鉴展示</small></div></div>
          <div className="companion-status-list">
            <div><span>设备</span><StateTag value={item.device.online_status} /></div>
            <div><span>对话状态</span><Tag color={item.device.online_status === "online" ? "processing" : "default"}>{conversationStatus}</Tag></div>
            <div><span>最近在线</span><strong>{formatTime(item.device.last_seen_at)}</strong></div>
          </div>
          <div className="bond-rule"><LockOutlined /><span>已绑定专属伙伴，用户不可自行切换。</span></div>
        </Card>
        <Card className="prototype-chat-shell" title={`最近真实对话 · ${item.agent.name}`} extra={<Space><Tag color="green">5 秒刷新</Tag><StateTag value={item.device.online_status} /></Space>}>
          <Typography.Paragraph type="secondary">内容来自硬件上报并写入后端的 conversation 记录；来源会逐条标识，不使用前端示例数据冒充实时聊天。</Typography.Paragraph>
          <div className="prototype-chat-body">
            {realMessages.map(row => <div key={row.message_id} className={`real-message ${row.role === "user" ? "user" : "assistant"}`}>
              <div className="real-message-meta"><span>{row.role === "user" ? "我" : item.agent?.name}</span><Space size={6}><Tag>{sourceText(row.content_source)}</Tag><span>{formatTime(row.created_at)}</span></Space></div>
              <div>{row.content}</div>
            </div>)}
            {!realMessages.length && <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description={<><div>尚未收到真实硬件对话</div><Typography.Text type="secondary">设备产生并上报 user/assistant 消息后，将在 5 秒内显示于此。</Typography.Text></>} />}
          </div>
          <div className="prototype-chat-input"><Input placeholder="请通过绑定设备与专属伙伴对话" disabled /><Button type="primary" disabled>设备语音对话</Button></div>
        </Card>
      </div>}
    </Loadable>
  </div>;
}

export function ScenicGameMapPage() {
  const map = useApiData(async () => unwrap<UserMap>((await api.get("/user/map")).data), []);
  const [selected, setSelected] = useState<UserMapPoint | null>(null);
  const completed = useMemo(() => new Set((map.data?.points || []).filter(point => point.state === "stamped").map(point => point.spot_id)), [map.data]);
  const progress = map.data?.stamp_summary.total ? Math.round(map.data.stamp_summary.earned / map.data.stamp_summary.total * 100) : 0;
  return <div className="user-page">
    <section className="map-heading">
      <div><Typography.Text className="eyebrow">SANFANG QIXIANG ADVENTURE</Typography.Text><Typography.Title>景区打卡地图</Typography.Title><Typography.Paragraph>跟随伙伴靠近故事点，GPS 负责发现，NFC 负责盖下真实印章。</Typography.Paragraph></div>
      <div className="map-progress"><Progress type="circle" percent={progress} size={72} strokeColor="#ec8c45" /><span>探索进度</span></div>
    </section>
    <Loadable loading={map.loading} error={map.error} empty={!map.data?.points.length} onRetry={map.reload}>
      <div className="prototype-map-grid">
      <Card className="adventure-map" styles={{ body: { padding: 0 } }}>
        <div className="prototype-map-title"><Typography.Title level={2}>三坊七巷打卡地图</Typography.Title><Typography.Text type="secondary">硬件定位联动 · 靠近点位后用 NFC 点亮印章</Typography.Text></div>
        <div className="prototype-map-tools"><Tag color="blue">GPS {map.data?.location.gps_status || "等待连接"}</Tag><Tag color="orange">NFC {map.data?.nfc.status || "待确认"}</Tag></div>
        <div className="map-sun" /><div className="map-river" /><div className="map-path" />
        <div className="map-legend"><span><i className="legend-dot current" />当前位置</span><span><i className="legend-dot complete" />已盖章</span><span><i className="legend-dot locked" />待探索</span></div>
        {(map.data?.points || []).map((spot, index) => {
          const done = completed.has(spot.spot_id);
          const near = spot.is_nearby;
          return <button key={spot.spot_id} className={`map-node ${done ? "done" : near ? "near" : ""}`} style={mapPositions[index % mapPositions.length]} onClick={() => setSelected(spot)}>
            {near && <span className="location-radar" />}<span className="node-pin">{done ? "✓" : index + 1}</span><span className="node-label">{spot.name}</span>
          </button>;
        })}
        <div className="map-status-card"><RadarChartOutlined /><div><Typography.Text strong>{map.data?.location.is_near_spot ? "已进入点位范围" : map.data?.location.gps_status === "valid" ? "GPS 已连接" : "等待 GPS 定位"}</Typography.Text><br /><Typography.Text type="secondary">{map.data?.location.is_near_spot ? "请靠近 NFC 标签完成精准确认" : "GPS 只用于接近提醒"}</Typography.Text></div></div>
      </Card>
      <Card className="prototype-map-side" title="探索进度">
        <Typography.Paragraph type="secondary">像小游戏一样收集景区印章，但真实触发来自硬件定位。</Typography.Paragraph>
        <Progress percent={progress} strokeColor="#2563eb" />
        <div className="prototype-mini-stamps">{(map.data?.points || []).map(point => <div key={point.spot_id} className={point.state === "stamped" ? "done" : ""}>{point.name}<small>{point.state === "stamped" ? "已点亮" : "待探索"}</small></div>)}</div>
        <div className="prototype-quest"><strong>当前任务</strong><span>进入目标 GPS 范围后，寻找 NFC 点位完成真实打卡。</span></div>
        <div className="prototype-quest"><strong>角色陪伴</strong><span>专属伙伴会根据点位状态播报提示。</span></div>
        <div className="prototype-quest"><strong>硬件联动</strong><span>GPS 负责接近提醒，NFC 负责精准确认。</span></div>
      </Card>
      </div>
    </Loadable>
    <Modal title={selected?.name} open={Boolean(selected)} onCancel={() => setSelected(null)} footer={null}>
      {selected && <Space direction="vertical" size={16} style={{ width: "100%" }}>
        <Typography.Paragraph>{selected.checkin_message || `来到${selected.name}，让伙伴为你讲一个藏在街巷里的故事。`}</Typography.Paragraph>
        <div className="spot-facts"><Tag icon={<EnvironmentOutlined />}>{selected.scenic_area_name || "三坊七巷"}</Tag><Tag>{selected.gps_radius_meters} 米发现范围</Tag><StateTag value={selected.state} /></div>
        {completed.has(selected.spot_id) ? <Alert type="success" showIcon message="印章已点亮" description="这段旅程已经收进你的图鉴。" /> : <Alert type="info" showIcon message="打卡方法" description="先进入 GPS 范围，再用绑定的 NFC 标签完成精准确认。" />}
      </Space>}
    </Modal>
  </div>;
}

export function StampBookPage() {
  const map = useApiData(async () => unwrap<UserMap>((await api.get("/user/map")).data), []);
  return <div className="user-page">
    <section className="map-heading"><div><Typography.Text className="eyebrow">MY MEMORY COLLECTION</Typography.Text><Typography.Title>我的图鉴</Typography.Title><Typography.Paragraph>每一枚印章都来自真实设备与 NFC 的精准确认。</Typography.Paragraph></div></section>
    <Loadable loading={map.loading} error={map.error} empty={!map.data?.points.length} onRetry={map.reload}>
      <div className="stamp-grid">{(map.data?.points || []).map((spot, index) => {
        const record = spot.stamp;
        return <Card key={spot.spot_id} className={`stamp-card ${record ? "unlocked" : "locked"}`}>
          <div className="stamp-seal">{record ? <><span>游</span><small>已到访</small></> : <LockOutlined />}</div>
          <Typography.Title level={4}>{record ? spot.name : `故事点 ${index + 1}`}</Typography.Title>
          <Typography.Text type="secondary">{record ? formatTime(record.checked_in_at) : "继续探索后解锁"}</Typography.Text>
        </Card>;
      })}</div>
      {!map.data?.points.length && <Empty description="还没有可收集的景点印章" />}
    </Loadable>
  </div>;
}
