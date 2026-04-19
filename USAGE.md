# Seekie Pet 使用说明

## 版本说明

项目目前有两个版本：

### 1. 原版 (稳定版)
- **文件**: `main.py`
- **版本**: 3.2.0 (Web设置窗口版)
- **特点**: 经过充分测试，功能完整稳定
- **启动**: `python main.py` 或 `run.bat`

### 2. 重构版 (开发版)
- **文件**: `main_refactored.py`
- **版本**: 3.3.0 (模块化重构版)
- **特点**: 模块化架构，增强错误处理，改进配置管理
- **启动**: `python main_refactored.py` 或 `run_refactored.bat`

## 如何选择

### 对于普通用户
- **推荐使用原版** (`main.py`)
- 稳定可靠，功能完整
- 启动方式: `run.bat` 或 `python main.py`

### 对于开发者或想要新功能的用户
- **可以尝试重构版** (`main_refactored.py`)
- 模块化架构，便于维护和扩展
- 启动方式: `run_refactored.bat` 或 `python main_refactored.py`

## 智能启动器

`run.bat` 现在是一个智能启动器，提供三种启动模式：

1. **原版 (稳定版)** - 直接运行 `main.py`
2. **重构版 (开发版)** - 直接运行 `main_refactored.py`
3. **自动选择 (推荐)** - 优先尝试重构版，失败则自动切换到原版

## 功能对比

| 功能 | 原版 | 重构版 |
|------|------|--------|
| 核心功能 | ✅ | ✅ |
| Web设置窗口 | ✅ | ✅ |
| 系统托盘 | ✅ | ✅ |
| 快捷键支持 | ✅ | ✅ |
| 输入活动检测 | ✅ | ✅ |
| 睡眠模式 | ✅ | ✅ |
| 模块化架构 | ❌ | ✅ |
| 增强错误处理 | ❌ | ✅ |
| 智能图片加载 | ❌ | ✅ |
| 完整日志系统 | ❌ | ✅ |
| 配置版本管理 | ❌ | ✅ |

## 共享资源

两个版本共享相同的资源：
- ✅ 配置文件: `config.json`
- ✅ 图片资源: `main_pic/` 目录
- ✅ 依赖要求: `requirements.txt`

## 常见问题

### Q: 我应该使用哪个版本？
A: 如果你是普通用户，使用原版 (`main.py`)。如果你是开发者或想要尝试新功能，使用重构版 (`main_refactored.py`)。

### Q: 两个版本可以同时运行吗？
A: 不建议同时运行，因为它们会使用相同的系统托盘位置和配置文件。

### Q: 如何从原版切换到重构版？
A: 直接运行 `run_refactored.bat` 或 `python main_refactored.py`。配置和图片会自动共享。

### Q: 重构版有问题怎么办？
A: 使用 `run.bat` 的自动选择模式，它会优先尝试重构版，如果失败则自动切换到原版。

## 文件结构

```
seekie_pet/
├── main.py              # 原版主程序 (v3.2.0)
├── main_refactored.py   # 重构版主程序 (v3.3.0)
├── run.bat              # 智能启动器 (推荐)
├── run_refactored.bat   # 重构版专用启动器
├── config.json          # 配置文件 (共享)
├── main_pic/            # 图片资源目录 (共享)
│   ├── Robot_50x50.png
│   ├── Sleep.png
│   └── robot-icon.png
├── config/              # 配置管理模块 (重构版)
├── utils/               # 工具模块 (重构版)
├── logs/                # 日志目录 (重构版)
└── web_settings/        # Web设置窗口 (共享)
```

## 启动方式

### 方式1: 智能启动器 (推荐)
```bash
run.bat
```

### 方式2: 直接运行原版
```bash
python main.py
```

### 方式3: 直接运行重构版
```bash
python main_refactored.py
```

### 方式4: 重构版专用启动器
```bash
run_refactored.bat
```

## 依赖安装

所有依赖已包含在 `requirements.txt` 中：

```bash
pip install -r requirements.txt
```

或手动安装：
```bash
pip install pillow pystray keyboard
```

## 技术支持

如果遇到问题：
1. 检查日志文件: `logs/seekie_pet.log` (重构版)
2. 查看控制台输出
3. 尝试使用原版 (`main.py`)
4. 检查依赖是否安装完整
