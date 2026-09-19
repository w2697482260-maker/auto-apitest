# Jenkins Allure 插件正确配置指南

## 问题根源
Allure Jenkins 插件已安装，但没有配置 Allure Commandline 工具，导致无法生成报告页面。

---

## 完整配置步骤

### 步骤 1：确认 Allure Jenkins 插件已安装

1. 进入 Jenkins：`http://192.168.2.104:8080`
2. `Manage Jenkins` → `Manage Plugins` → `Installed` 标签页
3. 搜索：`Allure Jenkins Plugin`
4. 如果没有，去 `Available` 标签页安装

### 步骤 2：配置 Allure Commandline（关键！）

这是最重要的步骤，之前缺少这个配置：

1. 进入：`Manage Jenkins` → `Global Tool Configuration`
2. 向下滚动找到 **Allure Commandline** 部分
3. 点击 `Add Allure Commandline` 按钮
4. 填写配置：

```
Name: allure
☑️ Install automatically (勾选)

Install from Maven Central:
  Version: 2.25.0 (选择最新版本)
```

5. 点击 `Save` 保存

**这一步是必须的！** 如果不配置，Allure 插件无法工作。

### 步骤 3：验证 Jenkins Job 配置

你的 Pipeline Job 不需要额外配置，Jenkinsfile 已经包含了 Allure 配置。

检查 Jenkinsfile 中的这段代码：

```groovy
stage('生成报告') {
    steps {
        echo '生成Allure报告...'
        script {
            allure([
                includeProperties: false,
                jdk: '',
                properties: [],
                reportBuildPolicy: 'ALWAYS',
                results: [[path: 'reports/allure-results']]
            ])
        }
    }
}
```

### 步骤 4：提交代码并构建

```bash
# 提交 Jenkinsfile 更新
git add Jenkinsfile config/notification_config.yaml
git commit -m "修复：恢复 Allure Jenkins 插件配置

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
git push origin test
```

### 步骤 5：触发 Jenkins 构建

1. 进入 Jenkins Job 页面
2. 点击 `Build with Parameters`
3. 选择环境和测试类型
4. 点击 `Build`

### 步骤 6：验证报告

构建完成后：

#### 在 Jenkins 构建页面检查：

左侧菜单应该显示：
- ✅ **Allure Report** 链接（蓝色图标）

点击 "Allure Report"，应该能看到：
- 测试概览
- 测试用例列表
- 图表统计
- 时间线等

#### 检查 URL：

```
http://192.168.2.104:8080/job/你的任务名/123/allure
                                          ↑构建号    ↑这个路径
```

#### 检查飞书通知：

飞书通知中的"查看详细报告"按钮，点击后应该打开完整的 Allure 报告。

---

## 常见问题排查

### Q1: 构建后左侧没有 "Allure Report" 链接

**原因**：Allure Commandline 没有配置

**解决**：按步骤 2 配置 Global Tool Configuration

### Q2: 点击 Allure Report 显示空白或 404

**可能原因**：
1. 测试没有生成 allure-results
2. Allure 工具自动下载失败

**检查方法**：
查看构建日志（Console Output），搜索 `allure`，应该看到：
```
[Allure] Allure report was successfully generated.
```

如果看到错误：
```
ERROR: No Allure commandline installations defined
```
说明步骤 2 没有配置。

### Q3: 构建日志显示 "No test results found"

**原因**：`reports/allure-results/` 目录为空

**检查**：
- 测试是否执行成功？
- pytest.ini 中的 `--alluredir=reports/allure-results` 配置是否正确？

### Q4: Allure 工具下载很慢或失败

**解决**：
在 Jenkins 服务器上手动预装 Allure（之前提供的安装命令）

---

## 核对清单

- [ ] Jenkins 已安装 Allure Jenkins Plugin
- [ ] Global Tool Configuration 中已配置 Allure Commandline
  - Name: `allure`
  - Install automatically: ✅
  - Version: 2.25.0 或更高
- [ ] Jenkinsfile 包含 allure() 配置
- [ ] 提交并推送了最新代码
- [ ] 触发了新的构建
- [ ] 构建成功完成
- [ ] Jenkins 构建页面左侧有 "Allure Report" 链接
- [ ] 点击链接能看到完整报告
- [ ] 飞书通知中的链接能正常打开

---

## 为什么之前不工作？

**根本原因**：Allure Jenkins Plugin 只是一个"发布器"，它本身不包含生成报告的工具。

它需要 **Allure Commandline** 工具来：
1. 读取 `allure-results/` 中的 JSON 数据
2. 生成 HTML 报告
3. 发布到 Jenkins

如果没有配置 Allure Commandline，插件就无法工作。

---

## 重点

**最关键的一步：配置 Global Tool Configuration 中的 Allure Commandline**

这一步完成后，所有问题都会解决。
