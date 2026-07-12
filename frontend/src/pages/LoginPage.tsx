import { Button, Card, Form, Select, Space, Typography } from "antd";
import { Navigate, useNavigate } from "react-router-dom";
import { DemoRole, useAuth } from "../shared/auth";

const roles = [
  { value: "viewer", label: "演示查看者（只读）" }, { value: "tester", label: "研发测试人员（可模拟）" },
  { value: "project_admin", label: "项目管理员（业务配置）" }, { value: "factory_admin", label: "原厂管理员（全量管理）" }
];
export function LoginPage() {
  const auth = useAuth(); const navigate = useNavigate();
  if (auth.role) return <Navigate to="/" replace />;
  return <main className="login-page"><Card className="login-card"><Space direction="vertical" size={20} style={{ width: "100%" }}><div className="brand-mark">游</div><div><Typography.Title level={2}>景区智能体演示台</Typography.Title><Typography.Paragraph type="secondary">选择演示身份进入。此入口不要求、存储或展示密码和 token。</Typography.Paragraph></div><Form layout="vertical" initialValues={{ role: "viewer" }} onFinish={({ role }: { role: DemoRole }) => { auth.login(role); navigate("/"); }}><Form.Item name="role" label="演示身份" rules={[{ required: true }]}><Select size="large" options={roles} /></Form.Item><Button type="primary" htmlType="submit" size="large" block>进入演示</Button></Form></Space></Card></main>;
}
