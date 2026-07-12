import { DashboardOutlined, DatabaseOutlined, EnvironmentOutlined, LinkOutlined, MobileOutlined, RobotOutlined, TagsOutlined, ToolOutlined } from "@ant-design/icons";
import { Layout, Menu, Typography } from "antd";
import { BrowserRouter, Link, Route, Routes } from "react-router-dom";
import { PlaceholderPage } from "../pages/PlaceholderPage";


const { Header, Content, Sider } = Layout;

const items = [
  { key: "/", icon: <DashboardOutlined />, label: <Link to="/">演示总览</Link> },
  { key: "/devices", icon: <MobileOutlined />, label: <Link to="/devices">设备管理</Link> },
  { key: "/agents", icon: <RobotOutlined />, label: <Link to="/agents">角色智能体</Link> },
  { key: "/bindings", icon: <LinkOutlined />, label: <Link to="/bindings">角色绑定</Link> },
  { key: "/spots", icon: <EnvironmentOutlined />, label: <Link to="/spots">景点点位</Link> },
  { key: "/nfc-tags", icon: <TagsOutlined />, label: <Link to="/nfc-tags">NFC 标签</Link> },
  { key: "/checkins", icon: <DatabaseOutlined />, label: <Link to="/checkins">打卡记录</Link> },
  { key: "/datasets", icon: <DatabaseOutlined />, label: <Link to="/datasets">景区知识</Link> },
  { key: "/simulate-checkin", icon: <ToolOutlined />, label: <Link to="/simulate-checkin">模拟打卡</Link> }
];

export function App() {
  return (
    <BrowserRouter>
      <Layout className="app-shell">
        <Sider breakpoint="lg" collapsedWidth="0">
          <Menu theme="dark" mode="inline" items={items} defaultSelectedKeys={["/"]} />
        </Sider>
        <Layout>
          <Header style={{ background: "#fff" }}>
            <Typography.Title level={4} style={{ margin: 0 }}>
              景区智能体演示控制台
            </Typography.Title>
          </Header>
          <Content className="app-content">
            <Routes>
              <Route path="/" element={<PlaceholderPage title="演示总览" module="设备、角色、GPS、NFC、打卡、数据集状态聚合" />} />
              <Route path="/devices" element={<PlaceholderPage title="设备管理" module="设备列表、详情、心跳、最近 GPS 状态" />} />
              <Route path="/agents" element={<PlaceholderPage title="角色智能体" module="角色 prompt、音色、知识库引用、上下文生成" />} />
              <Route path="/bindings" element={<PlaceholderPage title="角色绑定" module="单设备单角色绑定和变更记录" />} />
              <Route path="/spots" element={<PlaceholderPage title="景点点位" module="景点坐标、GPS 半径、打卡文案" />} />
              <Route path="/nfc-tags" element={<PlaceholderPage title="NFC 标签" module="标签注册、点位绑定、启停状态" />} />
              <Route path="/checkins" element={<PlaceholderPage title="打卡记录" module="真实/模拟打卡记录、结果、失败原因" />} />
              <Route path="/datasets" element={<PlaceholderPage title="景区知识" module="真实数据集状态、摘要片段、知识查询" />} />
              <Route path="/simulate-checkin" element={<PlaceholderPage title="模拟打卡" module="无硬件时模拟 GPS/NFC 流程" />} />
            </Routes>
          </Content>
        </Layout>
      </Layout>
    </BrowserRouter>
  );
}
