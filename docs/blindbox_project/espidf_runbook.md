# ESP-IDF 构建、烧录与硬件联调手册

文档状态：todo
主责角色：硬件/固件研发，研发主管验收
更新时间：2026-07-12

## 1. 当前定位

本文是一期硬件/固件研发的占位运行手册，正式内容需在硬件开工前由硬件/固件研发补齐。

当前已确认：

- 固件目录为 `main/`。
- 先不动 ESP32 固件核心，软件闭环稳定后再接真实 GPS/NFC。
- GPS 按预算清单采购，优先 NEO-6M；ATGM336H 也可接受，关键要求是 UART NMEA 输出。
- NFC 模块确认为 PN532。
- 设备约 10 秒一次上报 GPS 位置信息和定位质量。
- NFC 合法标签触发打卡，GPS 只做接近提醒。

## 2. 必须补齐内容

硬件/固件研发开工前必须补齐：

| 项 | 要求 |
| --- | --- |
| ESP-IDF 环境 | 版本、安装方式、环境变量、验证命令 |
| 构建命令 | `idf.py build` 或项目实际构建命令 |
| 烧录命令 | 串口、flash 参数、烧录步骤 |
| 串口日志 | 查看命令、波特率、关键日志样例 |
| GPS 接线表 | GPS VCC/GND/TX/RX 与 ESP32 引脚映射 |
| PN532 接线表 | I2C/SPI/UART 模式选择和引脚映射 |
| 麦克风/功放接线 | INMP441、MAX98357A、喇叭接线 |
| 电池供电 | 18650、TP4056、升压模块接线和注意事项 |
| 网络配置 | 设备连接公网后端的配置方式 |
| 故障处理 | GPS 无 fix、NFC 读不到、网络失败、供电重启 |

## 3. 关联资料

- [development_task_ownership.md](development_task_ownership.md)
- [phase1_single_robot_budget.md](phase1_single_robot_budget.md)
- [web_api_contract.md](web_api_contract.md)
- [testing_and_quality.md](testing_and_quality.md)
- [release_operations_runbook.md](release_operations_runbook.md)
