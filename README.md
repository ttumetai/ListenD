<div align="center">

# 🎵 ListenD

**macOS 音乐播放监听与统计工具**

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)
[![Powered by](https://img.shields.io/badge/powered%20by-Google%20Gemini-4285F4.svg)](https://gemini.google.com/)
[![Powered by](https://img.shields.io/badge/powered%20by-Claude-5A67D8.svg)](https://claude.ai/)

[功能特性](#-功能特性) • [快速开始](#-快速开始) • [使用说明](#-使用说明) • [技术栈](#-技术栈) • [开发](#-开发)

</div>

---

## 📖 简介

ListenD 是一个专为 macOS 设计的音乐播放监听与统计工具，能够实时追踪你在 Music App 中的听歌习惯，并通过精美的 Web 界面展示详细的统计数据。

### ✨ 功能特性

- 🎧 **实时监听** - 自动追踪 Music App 播放状态
- 🔔 **桌面通知** - 切歌时显示歌曲信息
- 🔁 **智能检测** - 识别单曲循环、跳过等播放行为
- 📊 **数据统计** - 播放次数、时长、完成度等多维度分析
- 📈 **可视化图表** - 每日趋势、时段分布一目了然
- 🎨 **现代 UI** - 深色玻璃态设计，美观易用
- 📸 **数据导出** - 一键导出统计截图
- 🚀 **后台运行** - 支持开机自启，静默运行

## 🖼️ 界面预览

> ![界面预览](https://github.com/user-attachments/assets/edb522e5-be44-4096-970a-65601a3637d7)

## 🚀 快速开始

### 系统要求

- macOS 10.15+
- Python 3.12+
- Music App

### 安装

```bash
# 克隆项目
git clone https://github.com/yourusername/listend.git
cd listend

# 安装依赖
uv sync
# 或使用 pip
pip install -r requirements.txt
```

### 运行

#### 方式一：一键启动（推荐）

```bash
./start.sh
```

然后访问 http://localhost:5999

#### 方式二：分别启动

```bash
# 终端 1 - 启动监听服务
python main.py

# 终端 2 - 启动 Web 界面
python web_server.py
```

#### 方式三：后台服务（推荐）

```bash
# 安装后台服务（开机自启）
./install_service.sh

# 单独启动 Web 界面
python web_server.py
```

## 📚 使用说明

### 监听服务

监听服务会自动追踪 Music App 的播放状态：

- ✅ 检测切歌并发送通知
- ✅ 记录播放时长和完成度
- ✅ 识别单曲循环行为
- ✅ 区分正常播放、跳过、循环

### Web 统计界面

访问 http://localhost:5999 查看统计数据：

#### 📊 概览数据
- 总播放次数
- 总播放时长
- 播放完成率
- 单曲循环次数

#### 📈 可视化图表
- 每日播放趋势
- 24小时播放时段分布

#### 🏆 排行榜
- 最常听的歌曲 Top 10
- 最常听的艺术家 Top 10

#### ⏱️ 播放记录
- 最近播放列表
- 播放类型标记（正常/循环/跳过）
- 播放完成度统计

#### 🎯 高级功能
- 自定义时间范围查询
- 快捷日期选择（昨天/今天/最近7天/最近30天）
- 实时数据刷新
- 一键导出统计截图

## 🛠️ 技术栈

### 后端
- **Python 3.12** - 核心语言
- **Flask** - Web 框架
- **SQLite** - 数据存储
- **AppleScript** - macOS 系统集成

### 前端
- **Vue 3** - 渐进式框架
- **Element Plus** - UI 组件库
- **Chart.js** - 数据可视化
- **html2canvas** - 截图导出

## 📁 项目结构

```
ListenD/
├── main.py                 # 音乐监听服务
├── web_server.py           # Flask Web 服务器
├── start.sh                # 一键启动脚本
├── install_service.sh      # 后台服务安装
├── uninstall_service.sh    # 后台服务卸载
├── utils/                  # 工具模块
│   ├── db_utils.py         # 数据库操作
│   ├── music_utils.py      # 音乐信息获取
│   └── notification.py     # 桌面通知
├── templates/              # HTML 模板
│   └── index.html          # Web UI 主页
├── static/                 # 静态资源
│   ├── css/
│   ├── js/
│   └── images/
├── db/                     # 数据库文件
│   └── music_history.db
├── logs/                   # 日志文件
├── Dockerfile              # Docker 镜像
├── docker-compose.yml      # Docker 编排
└── README.md
```

## 🔧 开发

### 本地开发

```bash
# 安装开发依赖
uv sync

# 运行监听服务
python main.py

# 运行 Web 服务（开发模式）
FLASK_ENV=development python web_server.py
```

### 数据库结构

```sql
CREATE TABLE play_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    track_name TEXT,           -- 歌曲名
    artist_name TEXT,          -- 艺术家
    album_name TEXT,           -- 专辑
    duration REAL,             -- 歌曲总时长
    started_at DATETIME,       -- 开始播放时间
    ended_at DATETIME,         -- 结束播放时间
    played_duration REAL,      -- 实际播放时长
    completion_rate REAL,      -- 完成度 (0-1)
    is_completed BOOLEAN,      -- 是否听完 (>80%)
    play_type TEXT             -- 类型: normal/repeat/skip
);
```

## 🐳 Docker 部署

> ⚠️ 注意：监听服务（main.py）依赖 macOS 系统，无法在 Docker 中运行。Docker 部署仅用于 Web 统计界面。

```bash
# 构建并启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

详见 [DOCKER.md](DOCKER.md)

## 🔐 后台服务

### 方式一：使用 LaunchAgent（推荐）

#### 安装后台服务

```bash
./install_service.sh
```

服务将：
- ✅ 开机自动启动
- ✅ 崩溃自动重启
- ✅ 后台静默运行
- ✅ 记录日志到 `logs/` 目录

#### 管理服务

```bash
# 查看服务状态
launchctl list | grep listend

# 查看实时日志
tail -f logs/monitor.log

# 查看错误日志
tail -f logs/monitor.error.log

# 停止服务
launchctl unload ~/Library/LaunchAgents/com.listend.monitor.plist

# 启动服务
launchctl load ~/Library/LaunchAgents/com.listend.monitor.plist

# 卸载服务
./uninstall_service.sh
```

### 方式二：使用 nohup

```bash
# 后台运行
nohup python main.py > logs/monitor.log 2>&1 &

# 查看进程
ps aux | grep main.py

# 停止进程
kill <PID>
```

### 方式三：使用 screen

```bash
# 创建 screen 会话
screen -S listend

# 运行程序
python main.py

# 分离会话：按 Ctrl+A 然后按 D

# 重新连接
screen -r listend

# 查看所有会话
screen -ls
```

### 日志位置

- 标准输出：`logs/monitor.log`
- 错误输出：`logs/monitor.error.log`

### 注意事项

1. **通知权限**：首次运行需要授予 terminal-notifier 通知权限
2. **Music App**：确保 Music App 有权限被脚本访问
3. **路径**：plist 文件中的路径必须是绝对路径

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📝 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [Flask](https://flask.palletsprojects.com/) - Web 框架
- [Vue.js](https://vuejs.org/) - 前端框架
- [Element Plus](https://element-plus.org/) - UI 组件库
- [Chart.js](https://www.chartjs.org/) - 图表库
- [Google Gemini](https://gemini.google.com/) - AI 辅助开发
- [Claude](https://claude.ai/) - AI 辅助开发

## 📮 联系方式

如有问题或建议，欢迎通过以下方式联系：

- 提交 [Issue](https://github.com/yourusername/listend/issues)

---

<div align="center">

**[⬆ 回到顶部](#-listend)**

</div>
