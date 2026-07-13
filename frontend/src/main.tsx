import React from "react";
import ReactDOM from "react-dom/client";
import { App as AntdApp, ConfigProvider } from "antd";
import zhCN from "antd/locale/zh_CN";
import { App } from "./app/App";
import "./styles.css";


ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <ConfigProvider locale={zhCN} theme={{ token: { colorPrimary: "#0f766e", borderRadius: 12, colorBgLayout: "#f3f7f5" } }}>
      <AntdApp>
        <App />
      </AntdApp>
    </ConfigProvider>
  </React.StrictMode>
);
