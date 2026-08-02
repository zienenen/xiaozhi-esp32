import { BookOutlined, CloudSyncOutlined, DashboardOutlined, DatabaseOutlined, EnvironmentOutlined, LinkOutlined, LogoutOutlined, MenuFoldOutlined, MenuOutlined, MenuUnfoldOutlined, MessageOutlined, MobileOutlined, RobotOutlined, TagsOutlined, ToolOutlined, UserOutlined } from "@ant-design/icons";
import { Button, Drawer, Flex, Input, Layout, Menu, Space, Tag, Typography } from "antd";
import { useState } from "react";
import { BrowserRouter, Link, Navigate, Route, Routes, useLocation, useNavigate } from "react-router-dom";
import { AuthProvider, useAuth } from "../shared/auth";
import { AgentsPage } from "../pages/AgentsPage";
import { BindingsPage } from "../pages/BindingsPage";
import { CheckinsPage } from "../pages/CheckinsPage";
import { ConversationsPage } from "../pages/ConversationsPage";
import { DatasetsPage } from "../pages/DatasetsPage";
import { DeviceDetailPage, DevicesPage } from "../pages/DevicesPage";
import { LoginPage } from "../pages/LoginPage";
import { NfcTagsPage } from "../pages/NfcTagsPage";
import { OfficialSyncPage } from "../pages/OfficialSyncPage";
import { OverviewPage } from "../pages/OverviewPage";
import { SimulateCheckinPage } from "../pages/SimulateCheckinPage";
import { SpotsPage } from "../pages/SpotsPage";
import { MyCompanionPage, ScenicGameMapPage, StampBookPage } from "../pages/UserExperiencePages";

const { Header, Content, Sider } = Layout;
const adminItems = [
  { key: "/admin", icon: <DashboardOutlined />, label: <Link to="/admin">演示总览</Link> },
  { key: "/admin/agents", icon: <RobotOutlined />, label: <Link to="/admin/agents">智能体工作台</Link> },
  { key: "/admin/devices", icon: <MobileOutlined />, label: <Link to="/admin/devices">设备</Link> },
  { key: "/admin/bindings", icon: <LinkOutlined />, label: <Link to="/admin/bindings">设备绑定</Link> },
  { key: "/admin/spots", icon: <EnvironmentOutlined />, label: <Link to="/admin/spots">景点 / 点位</Link> },
  { key: "/admin/nfc-tags", icon: <TagsOutlined />, label: <Link to="/admin/nfc-tags">NFC 标签</Link> },
  { key: "/admin/datasets", icon: <DatabaseOutlined />, label: <Link to="/admin/datasets">景区数据集</Link> },
  { key: "/admin/checkins", icon: <DatabaseOutlined />, label: <Link to="/admin/checkins">打卡记录</Link> },
  { key: "/admin/conversations", icon: <MessageOutlined />, label: <Link to="/admin/conversations">对话记录</Link> },
  { key: "/admin/official-sync", icon: <CloudSyncOutlined />, label: <Link to="/admin/official-sync">官网同步</Link> }
];
const roleNames = { factory_admin: "原厂管理员", project_admin: "项目管理员", tester: "研发测试", viewer: "伙伴用户" };

function UserShell() {
  const auth = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  if (!auth.role) return <Navigate to="/login" replace />;
  if (auth.role !== "viewer") return <Navigate to="/admin" replace />;
  const [collapsed, setCollapsed] = useState(false);
  const [drawer, setDrawer] = useState(false);
  const nav = [
    { key: "/", icon: <UserOutlined />, label: <Link to="/">我的伙伴</Link> },
    { key: "/map", icon: <EnvironmentOutlined />, label: <Link to="/map">景区打卡</Link> },
    { key: "/stamps", icon: <BookOutlined />, label: <Link to="/stamps">我的图鉴</Link> }
  ];
  const menu = <Menu mode="inline" items={nav} selectedKeys={[location.pathname]} onClick={() => setDrawer(false)} />;
  const page = location.pathname === "/map" ? ["景区打卡", "游戏化地图与硬件定位联动"] : location.pathname === "/stamps" ? ["我的图鉴", "查看真实 NFC 打卡点亮的印章"] : ["对话", "已绑定专属伙伴，用户不可自行切换"];
  return <Layout className="workspace-shell user-shell">
    <Sider className="workspace-sider desktop-sider" theme="light" width={232} collapsedWidth={72} collapsed={collapsed} trigger={null}>
      <div className="workspace-brand"><span className="workspace-logo">智</span>{!collapsed && <div><strong>盲盒伙伴</strong><small>专属智能体与景区打卡</small></div>}</div>
      {!collapsed && <div className="workspace-nav-section">用户游玩</div>}{menu}
    </Sider>
    <Layout className="workspace-main">
      <Header className="workspace-topbar">
        <Flex align="center" justify="space-between" gap={16}>
          <Space>
            <Button className="desktop-collapse" icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />} onClick={() => setCollapsed(v => !v)} />
            <Button className="mobile-menu" icon={<MenuOutlined />} onClick={() => setDrawer(true)} />
            <span className="workspace-logo">智</span>
            <div><Typography.Title level={4}>{page[0]}</Typography.Title><Typography.Text type="secondary">{page[1]}</Typography.Text></div>
          </Space>
          <Space wrap className="workspace-actions"><Tag color="blue">用户端</Tag><Input placeholder="搜索我的对话或打卡回忆" /><Link to="/map"><Button type="primary">开始打卡</Button></Link><Link to="/stamps"><Button type="primary">查看图鉴</Button></Link><Button type="text" icon={<LogoutOutlined />} onClick={() => { auth.logout(); navigate("/login"); }} /></Space>
        </Flex>
      </Header>
      <Content className="workspace-content"><Routes><Route path="/" element={<MyCompanionPage />} /><Route path="/map" element={<ScenicGameMapPage />} /><Route path="/stamps" element={<StampBookPage />} /><Route path="*" element={<Navigate to="/" replace />} /></Routes></Content>
    </Layout>
    <Drawer title="盲盒伙伴" placement="left" open={drawer} onClose={() => setDrawer(false)} styles={{ body: { padding: 0 } }}>{menu}</Drawer>
  </Layout>;
}

function AdminShell() {
  const auth = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const [drawer, setDrawer] = useState(false);
  const [collapsed, setCollapsed] = useState(false);
  if (!auth.role) return <Navigate to="/login" replace />;
  if (auth.role === "viewer") return <Navigate to="/" replace />;
  const items = auth.canSimulate ? [...adminItems, { key: "/admin/simulate-checkin", icon: <ToolOutlined />, label: <Link to="/admin/simulate-checkin">模拟打卡</Link> }] : adminItems;
  const selected = location.pathname.startsWith("/admin/devices/") ? "/admin/devices" : items.find(item => item.key !== "/admin" && location.pathname.startsWith(item.key))?.key || "/admin";
  const menu = <Menu mode="inline" items={items} selectedKeys={[selected]} onClick={() => setDrawer(false)} />;

  return <Layout className="app-shell admin-shell">
    <Sider className="desktop-sider workspace-sider" theme="light" width={232} collapsedWidth={72} collapsed={collapsed} trigger={null}>
      <div className="workspace-brand"><span className="workspace-logo">智</span>{!collapsed && <div><strong>小智自研平台</strong><small>配置源与演示后台</small></div>}</div>
      {!collapsed && <div className="workspace-nav-section">管理后台</div>}
      {menu}
    </Sider>
    <Layout>
      <Header className="workspace-topbar">
        <Flex align="center" justify="space-between" gap={12}>
          <Space>
            <Button className="desktop-collapse" type="text" icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />} aria-label="收起或展开菜单" onClick={() => setCollapsed(value => !value)} />
            <Button className="mobile-menu" type="text" icon={<MenuOutlined />} aria-label="打开导航" onClick={() => setDrawer(true)} />
            <span className="workspace-logo">智</span><div><Typography.Title level={4}>{selected === "/admin/agents" ? "智能体管理" : "管理后台"}</Typography.Title><Typography.Text type="secondary" className="admin-subtitle">配置角色、绑定设备、生成官网同步快照</Typography.Text></div>
          </Space>
          <Space className="workspace-actions"><Tag color="blue">管理员端</Tag><Input placeholder="搜索智能体、设备或同步状态" /><Link to="/admin/agents"><Button type="primary">添加智能体</Button></Link><Link to="/admin/devices"><Button type="primary">添加设备</Button></Link><Button type="text" icon={<LogoutOutlined />} onClick={() => { auth.logout(); navigate("/login"); }} /></Space>
        </Flex>
      </Header>
      <Content className="app-content">
        <Routes>
          <Route path="/" element={<OverviewPage />} />
          <Route path="/agents" element={<AgentsPage />} />
          <Route path="/devices" element={<DevicesPage />} />
          <Route path="/devices/:id" element={<DeviceDetailPage />} />
          <Route path="/bindings" element={<BindingsPage />} />
          <Route path="/spots" element={<SpotsPage />} />
          <Route path="/nfc-tags" element={<NfcTagsPage />} />
          <Route path="/datasets" element={<DatasetsPage />} />
          <Route path="/checkins" element={<CheckinsPage />} />
          <Route path="/conversations" element={<ConversationsPage />} />
          <Route path="/official-sync" element={<OfficialSyncPage />} />
          <Route path="/simulate-checkin" element={<SimulateCheckinPage />} />
          <Route path="*" element={<Navigate to="/admin" replace />} />
        </Routes>
      </Content>
    </Layout>
    <Drawer title="管理员导航" placement="left" open={drawer} onClose={() => setDrawer(false)} styles={{ body: { padding: 0, background: "#102a2a" } }}>{menu}</Drawer>
  </Layout>;
}

export function App() {
  return <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}><AuthProvider><Routes><Route path="/login" element={<LoginPage />} /><Route path="/admin/*" element={<AdminShell />} /><Route path="/*" element={<UserShell />} /></Routes></AuthProvider></BrowserRouter>;
}
