# POBDD - Playwright + pytest-bdd 测试框架

基于 Playwright 和 pytest-bdd 的自动化测试框架

## 特性

- 使用 Playwright 进行Web自动化测试
- 支持 BDD (Behavior Driven Development) 测试风格
- 页面对象模式 (POM) 设计
- 多环境配置支持
- 详细的测试报告 (Allure)
- 完善的日志系统
- 异常处理机制
- 测试数据管理
- 支持并行测试
- 失败重试机制
- 截图和视频记录

## 安装

1. 克隆项目
```bash
git clone [项目地址]
cd POBDD
```

2. 创建虚拟环境
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
playwright install
```

## 项目结构

```
POBDD/
├── config/                 # 配置文件
├── data/                  # 测试数据
├── pages/                 # 页面对象
├── tests/                 # 测试用例
├── utils/                 # 工具类
├── reports/               # 测试报告
└── logs/                  # 日志文件
```

## 运行测试

1. 运行所有测试
```bash
pytest
```

2. 运行特定测试
```bash
pytest tests/steps/test_baidu_steps.py
```

3. 生成Allure报告
```bash
pytest --alluredir=./reports/allure-results
allure serve ./reports/allure-results
```

## 配置说明

1. 环境配置
- 修改 `config/config.py` 中的配置项
- 支持 test/staging/prod 多环境配置

2. 浏览器配置
- 支持 chromium/firefox/webkit
- 可配置无头模式、视窗大小等

3. 测试报告配置
- 自动截图
- 失败重试
- 视频录制

## 开发指南

1. 添加新的页面对象
- 在 `pages/` 目录下创建新的页面类
- 继承 `BasePage` 类

2. 添加新的测试场景
- 在 `tests/features/` 下添加 .feature 文件
- 在 `tests/steps/` 下实现步骤定义

3. 添加测试数据
- 在 `data/` 目录下添加对应环境的数据文件

## 最佳实践

1. 使用页面对象模式
2. 保持测试数据的独立性
3. 合理使用夹具（fixtures）
4. 编写清晰的测试步骤
5. 及时处理和记录异常

## 常见问题

1. 浏览器启动失败
- 检查 Playwright 安装
- 确认浏览器驱动是否正确安装

2. 测试报告生成失败
- 确保 Allure 命令行工具已安装
- 检查报告目录权限

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交变更
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License 