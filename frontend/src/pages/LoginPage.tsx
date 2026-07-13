import { App, Button, Card, Form, Input, Select, Space, Typography } from "antd";
import { Navigate, useNavigate } from "react-router-dom";
import { DemoRole, useAuth } from "../shared/auth";
import { readableError } from "../shared/api";

const roles = [
  { value: "viewer", label: "演示查看者（只读）" }, { value: "tester", label: "研发测试人员（可模拟）" },
  { value: "project_admin", label: "项目管理员（业务配置）" }, { value: "factory_admin", label: "原厂管理员（全量管理）" }
];
export function LoginPage() {
  const auth = useAuth(); const navigate = useNavigate(); const { message } = App.useApp();
  if (auth.role) return <Navigate to="/" replace />;
  return <main className="login-page"><Card className="login-card"><Space direction="vertical" size={20} style={{ width: "100%" }}><div className="brand-mark">游</div><div><Typography.Title level={2}>景区智能体演示台</Typography.Title><Typography.Paragraph type="secondary">使用后端演示账号登录。凭据仅保存在当前页面内存中，刷新或退出后清除。</Typography.Paragraph></div><Form layout="vertical" initialValues={{ role: "viewer" }} onFinish={async ({ role, username, password }: { role: DemoRole; username: string; password: string }) => { try { await auth.login(role, username, password); navigate("/"); } catch (error) { message.error(readableError(error)); } }}><Form.Item name="username" label="账号" rules={[{ required: true }]}><Input autoComplete="username" /></Form.Item><Form.Item name="password" label="密码" rules={[{ required: true }]}><Input.Password autoComplete="current-password" /></Form.Item><Form.Item name="role" label="演示身份" rules={[{ required: true }]}><Select size="large" options={roles} /></Form.Item><Button type="primary" htmlType="submit" size="large" block>登录</Button></Form></Space></Card></main>;
}
