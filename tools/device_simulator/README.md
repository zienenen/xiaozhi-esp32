# Device Simulator

仅使用 Python 标准库的设备联调模拟器。它不会模拟语音链路，也不能替代 ESP32 验收。配置、心跳和 GPS 使用设备凭据；NFC 模拟通过受保护的 `/demo/simulate-checkin` 接口执行，由后端固定写入 `source=simulation`。日志不打印任何凭据。

## 配置

支持命令行参数或 `.env.example` 中列出的同名环境变量（脚本不会自动读取 `.env`）。命令行优先。先查看完整参数：

```powershell
python simulate_device.py --help
python simulate_device.py flow --help
```

全流程（GPS 默认上报一次；需要验证约 10 秒周期时指定次数）：

```powershell
python simulate_device.py --base-url http://127.0.0.1:8000/api/v1 --device-id device_001 --device-token demo-device-token --admin-username root --admin-password root flow --gps-count 2 --interval 10
```

单步命令：

```powershell
python simulate_device.py config
python simulate_device.py heartbeat
python simulate_device.py gps --count 3 --interval 10 --event-type near_spot
python simulate_device.py --admin-username root --admin-password root checkin --case success
```

异常用例由后端测试数据决定标签状态。未登记标签默认使用 `UNKNOWN_TAG`，停用标签默认使用 `DISABLED_TAG`，均可用 `--tag-id` 覆盖；重复用例会在一次命令中对同一标签连续请求两次：

```powershell
python simulate_device.py --admin-username root --admin-password root checkin --case unknown --tag-id UNKNOWN_TAG
python simulate_device.py --admin-username root --admin-password root checkin --case disabled --tag-id DISABLED_TAG
python simulate_device.py --admin-username root --admin-password root checkin --case duplicate
```

合法/非法设备可通过切换 `--device-id`、`--device-token` 模拟。NFC 命令必须提供测试/管理员账号（命令行或 `SIM_ADMIN_*` 环境变量）。HTTP 错误、业务 `success=false`、非 JSON 响应和后端不可用都会输出到 stderr 并返回退出码 1。

## 输出样例

成功：

```text
== NFC success ==
{"success": true, "data": {"result": "success", "source": "simulation"}, "error": null}
```

失败：

```text
== NFC unknown ==
ERROR: tag_unknown: NFC 标签未登记
```

完整闭环顺序为：拉配置 → 心跳 → GPS 位置/接近 → NFC 打卡。最后在前端演示总览与打卡记录页确认状态变化及“模拟”标记。
