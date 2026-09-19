# 飞书和 Jenkins 集成 - 快速配置清单

## ✅ 配置步骤

### 1. 飞书机器人配置（5分钟）

- [ ] 在飞书群中创建自定义机器人
- [ ] 复制 Webhook URL
- [ ] 编辑 `config/notification_config.yaml`
- [ ] 将 Webhook URL 填入配置文件
- [ ] 设置 `enabled: true`

### 2. 测试飞书通知（1分钟）

```bash
# 激活虚拟环境
source .venv/Scripts/activate

# 运行测试脚本
python test_feishu.py
```

如果看到 "🎉 所有测试通过！" 说明配置成功。

### 3. Jenkins 配置（10分钟）

**前置条件：**
- [ ] Jenkins 已安装
- [ ] 安装 Allure Jenkins Plugin

**步骤：**
- [ ] 创建 Pipeline 项目
- [ ] 配置 Git 仓库地址
- [ ] 设置 Script Path: `Jenkinsfile`
- [ ] 编辑 `config/notification_config.yaml` 中的 `jenkins.report_url_template`
- [ ] 保存并运行一次构建测试

### 4. 验证（2分钟）

**本地测试：**
```bash
pytest
```
测试完成后应该收到飞书通知

**Jenkins 测试：**
- 在 Jenkins 中点击 "Build with Parameters"
- 选择参数后点击构建
- 检查飞书群是否收到通知

---

## 📝 配置文件示例

### config/notification_config.yaml

```yaml
feishu:
  enabled: true
  webhook_url: "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxxxx"
  
  notify_on:
    success: true
    failure: true
    always: false
  
  mention:
    all: false
    users: []

jenkins:
  report_url_template: "http://your-jenkins.com/job/${JOB_NAME}/${BUILD_NUMBER}/allure"
```

---

## 🎯 功能特性

✅ **已实现：**
- [x] 自动发送测试报告到飞书
- [x] 美观的卡片消息格式
- [x] 通过率计算和状态展示
- [x] Jenkins 报告链接自动生成
- [x] 可配置的通知规则
- [x] 支持 @提醒
- [x] 本地和 Jenkins 环境均可用

---

## 🚀 使用方式

### 方式一：本地运行（自动通知）
```bash
pytest
```

### 方式二：使用脚本
```bash
./run_tests.sh
```

### 方式三：Jenkins 自动化
在 Jenkins 中配置定时任务或手动触发

---

## 📚 相关文档

- 详细配置指南: `docs/FEISHU_JENKINS_GUIDE.md`
- Allure 报告: `ALLURE_SETUP.md`
- 项目说明: `项目说明.md`

---

## 🔧 故障排查

如果通知未发送，检查：
1. `config/notification_config.yaml` 中 `enabled: true`
2. Webhook URL 正确且有效
3. 查看日志: `reports/logs/pytest.log`
4. 运行测试脚本: `python test_feishu.py`

---

## 📞 获取帮助

运行测试脚本诊断问题：
```bash
python test_feishu.py
```

它会告诉你配置是否正确以及哪里有问题。
