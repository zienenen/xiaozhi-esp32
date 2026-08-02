import { Alert, Button, Card, List, Space, Typography } from "antd";
import { Link } from "react-router-dom";
import { api, unwrap } from "../shared/api";
import { Overview } from "../shared/types";
import { FailureReason, formatTime, Loadable, MetricCard, PageHeader, StateTag } from "../shared/ui";
import { useApiData } from "../shared/useApi";

export function OverviewPage() {
  const state = useApiData(async () => unwrap<Overview>((await api.get("/demo/overview")).data), []);
  const item = state.data;
  const failure = item?.failure_code || (item?.device?.online_status === "offline" ? "device_offline" : item?.gps?.fix === false ? "gps_no_fix" : item?.nfc?.status === "unknown" ? "tag_unknown" : item?.nfc?.status === "disabled" ? "tag_disabled" : item?.latest_checkin?.result === "duplicate" ? "duplicate" : item?.dataset?.status === "failed" ? "dataset_failed" : undefined);

  return <>
    <PageHeader title="演示总览" description="一屏确认设备、角色、GPS、NFC、打卡与景区知识链路。" extra={<Button onClick={state.reload}>刷新状态</Button>} />
    <div className="quick-links">
      <Link to="/admin/agents"><Card hoverable><Typography.Text type="secondary">配置源</Typography.Text><Typography.Title level={4}>角色配置</Typography.Title><Typography.Text>维护 Prompt、音色、知识引用和版本</Typography.Text></Card></Link>
      <Link to="/admin/conversations"><Card hoverable><Typography.Text type="secondary">内容证据</Typography.Text><Typography.Title level={4}>对话记录</Typography.Title><Typography.Text>追溯用户输入、AI 回复与知识来源</Typography.Text></Card></Link>
      <Link to="/admin/official-sync"><Card hoverable><Typography.Text type="secondary">官网对接</Typography.Text><Typography.Title level={4}>同步状态与快照</Typography.Title><Typography.Text>复制配置并记录人工同步结果</Typography.Text></Card></Link>
    </div>
    <Loadable loading={state.loading} error={state.error} empty={!item} onRetry={state.reload}>
      {item && <>
        <div className="page-grid">
          <MetricCard title="当前设备" value={item.device?.name || item.device?.device_id || "未接入"} status={item.device?.online_status} detail={<Typography.Text type="secondary">{item.device?.sn || "无 SN"} · 最近在线 {formatTime(item.device?.last_seen_at)}</Typography.Text>} />
          <MetricCard title="绑定角色" value={item.agent?.name || "未绑定"} status={item.agent?.status} detail={<Typography.Text type="secondary">音色 {item.agent?.voice_id || "未配置"}</Typography.Text>} />
          <MetricCard title="GPS 粗定位" value={item.gps?.near_spot ? "已接近，请 NFC 确认" : item.gps?.fix ? "已定位" : "等待定位"} status={item.gps?.fix ? (item.gps?.near_spot ? "near_spot" : "fixed") : "no_fix"} detail={<Typography.Text type="secondary">更新 {formatTime(item.gps?.updated_at)}</Typography.Text>} />
          <MetricCard title="NFC 精准确认" value={item.nfc?.tag_id || "等待刷卡"} status={item.nfc?.status} detail={<Typography.Text type="secondary">点位 {item.nfc?.spot_id || "未识别"}</Typography.Text>} />
          <MetricCard title="最近打卡" value={item.latest_checkin?.spot_name || item.latest_checkin?.spot_id || "暂无"} status={item.latest_checkin?.result} detail={<Space wrap><StateTag value={item.latest_checkin?.source} /><Typography.Text type="secondary">{formatTime(item.latest_checkin?.checked_in_at)}</Typography.Text></Space>} />
          <MetricCard title="景区数据集" value={item.dataset?.name || "未关联"} status={item.dataset?.status} detail={<Typography.Text type="secondary">{item.dataset?.chunk_count ?? 0} 个片段 · {formatTime(item.dataset?.updated_at)}</Typography.Text>} />
        </div>
        <Card className="section-card" title="当前链路判断">
          <FailureReason code={failure} detail={item.gps?.reason || item.nfc?.reason || item.dataset?.failure_reason} />
          {!failure && <Alert type="success" showIcon message="演示链路状态正常" description="GPS 只负责接近提醒，最终打卡以合法 NFC 标签确认为准。" />}
        </Card>
        {item.events && item.events.length > 0 && <Card className="section-card" title="最近事件"><List dataSource={item.events.slice(0, 5)} renderItem={event => <List.Item><Typography.Text>{event.message}</Typography.Text><Typography.Text type="secondary">{formatTime(event.time)}</Typography.Text></List.Item>} /></Card>}
        <Space wrap className="section-card"><Link to={`/admin/devices/${item.device?.device_id || ""}`}><Button disabled={!item.device?.device_id}>设备详情</Button></Link><Link to={`/admin/checkins?device_id=${item.device?.device_id || ""}`}><Button disabled={!item.device?.device_id}>最近记录</Button></Link></Space>
      </>}
    </Loadable>
  </>;
}
