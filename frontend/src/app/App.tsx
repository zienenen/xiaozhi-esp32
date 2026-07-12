import { DashboardOutlined, DatabaseOutlined, EnvironmentOutlined, LinkOutlined, LogoutOutlined, MenuOutlined, MobileOutlined, RobotOutlined, TagsOutlined, ToolOutlined } from "@ant-design/icons";
import { Button, Drawer, Flex, Layout, Menu, Space, Tag, Typography } from "antd";
import { useState } from "react";
import { BrowserRouter, Link, Navigate, Route, Routes, useLocation, useNavigate } from "react-router-dom";
import { AuthProvider, useAuth } from "../shared/auth";
import { AgentsPage } from "../pages/AgentsPage";
import { BindingsPage } from "../pages/BindingsPage";
import { CheckinsPage } from "../pages/CheckinsPage";
import { DatasetsPage } from "../pages/DatasetsPage";
import { DeviceDetailPage, DevicesPage } from "../pages/DevicesPage";
import { LoginPage } from "../pages/LoginPage";
import { NfcTagsPage } from "../pages/NfcTagsPage";
import { OverviewPage } from "../pages/OverviewPage";
import { SimulateCheckinPage } from "../pages/SimulateCheckinPage";
import { SpotsPage } from "../pages/SpotsPage";

const { Header, Content, Sider } = Layout;
const baseItems = [
  { key: "/", icon: <DashboardOutlined />, label: <Link to="/">演示总览</Link> }, { key: "/devices", icon: <MobileOutlined />, label: <Link to="/devices">设备</Link> },
  { key: "/agents", icon: <RobotOutlined />, label: <Link to="/agents">角色智能体</Link> }, { key: "/bindings", icon: <LinkOutlined />, label: <Link to="/bindings">角色绑定</Link> },
  { key: "/spots", icon: <EnvironmentOutlined />, label: <Link to="/spots">景点 / 点位</Link> }, { key: "/nfc-tags", icon: <TagsOutlined />, label: <Link to="/nfc-tags">NFC 标签</Link> },
  { key: "/datasets", icon: <DatabaseOutlined />, label: <Link to="/datasets">景区数据集</Link> }, { key: "/checkins", icon: <DatabaseOutlined />, label: <Link to="/checkins">打卡记录</Link> }
];
const roleNames = { factory_admin: "原厂管理员", project_admin: "项目管理员", tester: "研发测试", viewer: "演示查看" };

function ProtectedApp() {
  const auth = useAuth(); const location = useLocation(); const navigate = useNavigate(); const [drawer, setDrawer] = useState(false);
  if (!auth.role) return <Navigate to="/login" replace />;
  const items = auth.canSimulate ? [...baseItems, { key: "/simulate-checkin", icon: <ToolOutlined />, label: <Link to="/simulate-checkin">模拟打卡</Link> }] : baseItems;
  const selected = location.pathname.startsWith("/devices/") ? "/devices" : items.find(item => item.key !== "/" && location.pathname.startsWith(item.key))?.key || "/";
  const menu = <Menu theme="dark" mode="inline" items={items} selectedKeys={[selected]} onClick={() => setDrawer(false)} />;
  return <Layout className="app-shell"><Sider className="desktop-sider" width={230}><div className="brand"><span className="brand-mark small">游</span><span>景区智能体</span></div>{menu}</Sider><Layout><Header className="app-header"><Flex align="center" justify="space-between" gap={12}><Space><Button className="mobile-menu" type="text" icon={<MenuOutlined />} aria-label="打开导航" onClick={() => setDrawer(true)} /><Typography.Title level={4}>演示控制台</Typography.Title></Space><Space><Tag>{roleNames[auth.role]}</Tag><Button type="text" icon={<LogoutOutlined />} onClick={() => { auth.logout(); navigate("/login"); }}>退出</Button></Space></Flex></Header><Content className="app-content"><Routes><Route path="/" element={<OverviewPage />} /><Route path="/devices" element={<DevicesPage />} /><Route path="/devices/:id" element={<DeviceDetailPage />} /><Route path="/agents" element={<AgentsPage />} /><Route path="/bindings" element={<BindingsPage />} /><Route path="/spots" element={<SpotsPage />} /><Route path="/nfc-tags" element={<NfcTagsPage />} /><Route path="/datasets" element={<DatasetsPage />} /><Route path="/checkins" element={<CheckinsPage />} /><Route path="/simulate-checkin" element={<SimulateCheckinPage />} /><Route path="*" element={<Navigate to="/" replace />} /></Routes></Content></Layout><Drawer title="导航" placement="left" open={drawer} onClose={() => setDrawer(false)} styles={{ body: { padding: 0, background: "#102a2a" } }}>{menu}</Drawer></Layout>;
}
export function App() { return <BrowserRouter><AuthProvider><Routes><Route path="/login" element={<LoginPage />} /><Route path="/*" element={<ProtectedApp />} /></Routes></AuthProvider></BrowserRouter>; }
