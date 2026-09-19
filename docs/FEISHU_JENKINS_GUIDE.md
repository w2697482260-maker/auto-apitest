# 飞书通知和 Jenkins 集成指南

## 📋 目录
1. [飞书机器人配置](#飞书机器人配置)
2. [Jenkins 配置](#jenkins-配置)
3. [使用方式](#使用方式)
4. [测试通知](#测试通知)

---

## 1. 飞书机器人配置

### 1.1 创建飞书群机器人

1. **进入飞书群** → 点击右上角 `...` → `设置` → `群机器人`
2. **添加机器人** → 选择 `自定义机器人`
3. **配置机器人信息**：
   - 名称：`ESOP API 测试报告`
   - 描述：`自动发送接口测试结果`
4. **安全设置**（可选）：
   - 签名校验（推荐）
   - IP 白名单
5. **复制 Webhook 地址**

### 1.2 配置项目

编辑 `config/notification_config.yaml`：

```yaml
feishu:
  enabled: true  # 启用飞书通知
  webhook_url: "https://open.feishu.cn/open-apis/bot/v2/hook/你的webhook地址"
  
  notify_on:
    success: true   # 全部通过时通知
    failure: true   # 有失败时通知
    always: false   # 始终通知
  
  mention:
    all: false      # @所有人
    users: []       # @指定用户 ["ou_xxx"]
```

### 1.3 通知内容

飞书卡片消息包含：
- ✅ 测试状态（成功/警告/失败）
- 📊 测试统计（总数、通过、失败、跳过）
- ⏱️ 执行耗时
- 🌍 测试环境
- 🔗 报告链接（Jenkins 环境）

---

## 2. Jenkins 配置

### 2.1 安装 Jenkins 插件

需要安装以下插件：

1. **Allure Plugin**
   - Jenkins 管理 → 插件管理 → 搜索 `Allure`
   - 安装 `Allure Jenkins Plugin`

2. **Pipeline Plugin**（通常已安装）

### 2.2 配置 Allure

1. Jenkins 管理 → 全局工具配置 → Allure Commandline
2. 添加 Allure 安装：
   - 名称：`allure`
   - 从 Maven Central 安装：选择最新版本

### 2.3 创建 Jenkins Job

#### 方式一：Pipeline 项目

1. **新建 Item** → 选择 `Pipeline`
2. **配置 Pipeline**：
   - Definition: `Pipeline script from SCM`
   - SCM: `Git`
   - Repository URL: 你的项目地址
   - Script Path: `Jenkinsfile`

#### 方式二：使用现有 Jenkinsfile

项目已包含 `Jenkinsfile`，直接关联即可。

### 2.4 配置参数

Jenkinsfile 已定义的参数：

- **ENV**: 测试环境（test/staging/dev）
- **TEST_TYPE**: 测试类型（all/smoke/regression/bos/admin/staff）
- **STOCK_TYPE**: 股票类型（all/hk_us/unlisted/a_stock）
- **FEISHU_WEBHOOK**: 飞书 Webhook（已弃用，改用配置文件）

### 2.5 配置报告 URL

编辑 `config/notification_config.yaml`：

```yaml
jenkins:
  report_url_template: "http://你的jenkins地址/job/${JOB_NAME}/${BUILD_NUMBER}/allure"
```

示例：
```yaml
jenkins:
  report_url_template: "http://jenkins.example.com/job/${JOB_NAME}/${BUILD_NUMBER}/allure"
```

---

## 3. 使用方式

### 3.1 本地运行（自动通知）

```bash
# 激活虚拟环境
source .venv/Scripts/activate

# 运行测试（测试完成后自动发送飞书通知）
pytest

# 或使用脚本
./run_tests.sh
```

### 3.2 Jenkins 运行

1. 进入 Jenkins Job
2. 点击 `Build with Parameters`
3. 选择参数：
   - ENV: `test`
   - TEST_TYPE: `all`
   - STOCK_TYPE: `all`
4. 点击 `构建`

测试完成后会：
- ✅ 自动生成 Allure 报告
- ✅ 自动发送飞书通知（包含报告链接）

### 3.3 命令行参数

```bash
# 指定环境
export TEST_ENV=test
pytest

# 指定标记
pytest -m smoke          # 只运行冒烟测试
pytest -m "bos and p0"   # BOS端高优先级用例
pytest -m hk_us          # 港美股业务

# 失败重试
pytest --reruns 2 --reruns-delay 1
```

---

## 4. 测试通知

### 4.1 手动测试飞书通知

创建测试脚本 `test_feishu.py`：

```python
from utils.feishu_notifier import FeishuNotifier

webhook_url = "你的webhook地址"
notifier = FeishuNotifier(webhook_url)

# 测试文本消息
notifier.send_text("测试消息 - 飞书通知已配置成功！")

# 测试报告消息
report_data = {
    'total': 10,
    'passed': 8,
    'failed': 1,
    'skipped': 1,
    'duration': 30.5,
    'env': 'test',
    'report_url': 'http://jenkins.example.com/job/test/123/allure'
}
notifier.send_test_report(report_data)
```

运行：
```bash
source .venv/Scripts/activate
python test_feishu.py
```

### 4.2 测试 Jenkins 集成

1. 提交代码到 Git
2. 在 Jenkins 中触发构建
3. 观察控制台输出
4. 检查飞书群是否收到通知

---

## 5. 通知规则配置

### 5.1 条件通知

```yaml
feishu:
  notify_on:
    success: true   # 全部通过才通知
    failure: true   # 有失败就通知
    always: false   # 无论结果都通知
```

### 5.2 @提醒

```yaml
feishu:
  mention:
    all: true       # @所有人（测试失败时）
    users:          # @指定用户
      - "ou_xxxx"   # QA 负责人
      - "ou_yyyy"   # 开发负责人
```

获取用户 open_id：
1. 飞书管理后台 → 通讯录
2. 找到用户 → 复制 Open ID

---

## 6. 故障排查

### 6.1 飞书通知未发送

**检查清单：**
- [ ] `config/notification_config.yaml` 中 `enabled: true`
- [ ] Webhook URL 配置正确
- [ ] 网络可访问飞书 API
- [ ] 查看日志：`reports/logs/pytest.log`

**常见错误：**
```
飞书消息发送失败: {'code': 9499, 'msg': 'Bad Request'}
```
原因：Webhook URL 错误或已过期

### 6.2 Jenkins 报告链接错误

**检查：**
- [ ] Jenkins 安装了 Allure 插件
- [ ] `report_url_template` 配置正确
- [ ] 环境变量 `BUILD_URL` 可用

### 6.3 本地测试通知正常，Jenkins 不发送

**原因：** Jenkins 环境变量未设置

**解决：** 在 Jenkinsfile 中添加：
```groovy
environment {
    BUILD_URL = "${env.BUILD_URL}"
    JOB_NAME = "${env.JOB_NAME}"
    BUILD_NUMBER = "${env.BUILD_NUMBER}"
}
```

---

## 7. 高级配置

### 7.1 多环境通知

不同环境使用不同的飞书群：

```python
# utils/config_helper.py
def get_feishu_webhook(env):
    webhooks = {
        'test': 'webhook_url_1',
        'staging': 'webhook_url_2',
        'prod': 'webhook_url_3'
    }
    return webhooks.get(env)
```

### 7.2 自定义通知内容

修改 `utils/pytest_feishu_plugin.py` 的 `pytest_terminal_summary` 函数。

### 7.3 定时任务

在 Jenkinsfile 添加触发器：

```groovy
triggers {
    cron('H 2 * * *')  // 每天凌晨2点执行
}
```

---

## 8. 示例截图

### 飞书通知效果：

```
┌─────────────────────────────────┐
│ ✅ ESOP接口自动化测试报告        │
├─────────────────────────────────┤
│ 执行时间: 2024-01-01 10:30:00   │
│ 执行环境: test                  │
├─────────────────────────────────┤
│ 总用例数: 22    通过率: 90.91%  │
│ 通过: 20 ✅    失败: 2 ❌       │
│ 跳过: 0 ⏭️     耗时: 30s ⏱️    │
├─────────────────────────────────┤
│        [查看详细报告 📊]         │
└─────────────────────────────────┘
```

---

## 9. 快速开始

### 最小化配置（3步）

1. **获取飞书 Webhook**：创建群机器人并复制 Webhook URL

2. **修改配置文件** `config/notification_config.yaml`：
   ```yaml
   feishu:
     enabled: true
     webhook_url: "你的webhook地址"
   ```

3. **运行测试**：
   ```bash
   pytest
   ```

完成！测试结束后会自动发送飞书通知。

---

## 10. 相关文件

- `config/notification_config.yaml` - 通知配置
- `utils/feishu_notifier.py` - 飞书通知工具
- `utils/pytest_feishu_plugin.py` - Pytest 插件
- `Jenkinsfile` - Jenkins Pipeline 配置
- `conftest.py` - Pytest 插件注册

---

## 需要帮助？

- 查看日志：`reports/logs/pytest.log`
- 检查配置：`config/notification_config.yaml`
- 测试连接：运行 `test_feishu.py`
