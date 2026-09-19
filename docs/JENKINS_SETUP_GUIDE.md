# Jenkins 配置完整指南

## 📋 前置条件

- ✅ Jenkins 已安装并运行
- ✅ 有 Jenkins 管理员权限
- ✅ 项目代码已提交到 Git 仓库

---

## 第一步：安装必要的 Jenkins 插件

### 1.1 登录 Jenkins
访问你的 Jenkins 地址，例如：`http://localhost:8080` 或 `http://your-jenkins-server:8080`

### 1.2 进入插件管理
```
Jenkins 首页
  → 左侧菜单：Manage Jenkins（系统管理）
    → Manage Plugins（插件管理）
      → Available（可选插件）标签页
```

### 1.3 安装以下插件

在搜索框中搜索并勾选安装：

**必装插件：**
- [x] `Allure Jenkins Plugin` - Allure 报告插件
- [x] `Git Plugin` - Git 支持（通常已安装）
- [x] `Pipeline` - Pipeline 支持（通常已安装）

**推荐插件：**
- [x] `Blue Ocean` - 更好的 Pipeline 界面
- [x] `HTML Publisher` - HTML 报告发布

点击 `Install without restart` 或 `Download now and install after restart`

---

## 第二步：配置 Allure 工具

### 2.1 进入全局工具配置
```
Jenkins 首页
  → Manage Jenkins（系统管理）
    → Global Tool Configuration（全局工具配置）
```

### 2.2 配置 Allure Commandline

向下滚动找到 **Allure Commandline** 部分：

1. 点击 `Add Allure Commandline`
2. 配置：
   - **Name**: `allure`（保持默认）
   - **Install automatically**: ✅ 勾选
   - **Install from Maven Central**: 选择最新版本（如 `2.46.1`）
3. 点击 `Save`（保存）

---

## 第三步：创建 Jenkins Job

### 3.1 创建新任务

1. Jenkins 首页 → 点击左侧 `New Item`（新建任务）
2. 输入任务名称：`ESOP-API-Automation`
3. 选择 `Pipeline`
4. 点击 `OK`

### 3.2 配置任务描述（可选）

在 `Description` 中填写：
```
ESOP 接口自动化测试
- 支持多环境测试（test/staging/dev）
- 自动生成 Allure 报告
- 自动发送飞书通知
```

### 3.3 配置参数化构建

勾选 `This project is parameterized`（参数化构建过程）

添加以下参数：

#### 参数 1：测试环境
- 类型：`Choice Parameter`
- Name: `ENV`
- Choices:（每行一个）
  ```
  test
  staging
  dev
  ```
- Description: `测试环境`

#### 参数 2：测试类型
- 类型：`Choice Parameter`
- Name: `TEST_TYPE`
- Choices:
  ```
  all
  smoke
  regression
  bos
  admin
  staff
  ```
- Description: `测试类型`

#### 参数 3：股票类型
- 类型：`Choice Parameter`
- Name: `STOCK_TYPE`
- Choices:
  ```
  all
  hk_us
  unlisted
  a_stock
  ```
- Description: `股票类型`

### 3.4 配置 Pipeline

滚动到 `Pipeline` 部分：

#### 方式一：从 SCM 读取（推荐）

1. **Definition**: 选择 `Pipeline script from SCM`
2. **SCM**: 选择 `Git`
3. **Repository URL**: 填写你的 Git 仓库地址
   ```
   例如：https://github.com/yourusername/esop-api-automation.git
   或：git@github.com:yourusername/esop-api-automation.git
   ```
4. **Credentials**: 
   - 如果是私有仓库，点击 `Add` 添加 Git 凭据
   - 选择你添加的凭据
5. **Branch Specifier**: `*/main` 或 `*/master`（根据你的分支）
6. **Script Path**: `Jenkinsfile`（保持默认）

#### 方式二：直接粘贴脚本

1. **Definition**: 选择 `Pipeline script`
2. 将项目中的 `Jenkinsfile` 内容复制粘贴到文本框中

### 3.5 保存配置

点击页面底部的 `Save` 按钮

---

## 第四步：配置项目的报告 URL

### 4.1 编辑配置文件

在项目中编辑 `config/notification_config.yaml`：

```yaml
jenkins:
  # 替换为你的 Jenkins 地址
  report_url_template: "http://your-jenkins-server:8080/job/${JOB_NAME}/${BUILD_NUMBER}/allure"
```

**示例：**
```yaml
jenkins:
  report_url_template: "http://192.168.1.100:8080/job/ESOP-API-Automation/${BUILD_NUMBER}/allure"
```

### 4.2 提交代码

```bash
git add config/notification_config.yaml
git commit -m "配置 Jenkins 报告 URL"
git push
```

---

## 第五步：运行第一次构建

### 5.1 触发构建

1. 进入 Jenkins Job 页面：`ESOP-API-Automation`
2. 点击左侧 `Build with Parameters`（参数化构建）
3. 选择参数：
   - ENV: `test`
   - TEST_TYPE: `smoke`（先运行冒烟测试）
   - STOCK_TYPE: `all`
4. 点击 `Build`（构建）

### 5.2 查看构建过程

1. 在 `Build History` 中可以看到新的构建
2. 点击构建编号（如 `#1`）
3. 点击 `Console Output` 查看日志

### 5.3 查看报告

构建完成后：
1. 在构建页面左侧会出现 `Allure Report` 链接
2. 点击查看详细测试报告
3. 同时飞书群会收到通知（包含报告链接）

---

## 第六步：配置定时构建（可选）

### 6.1 编辑 Jenkins Job

在 Job 配置页面，找到 `Build Triggers`（构建触发器）

### 6.2 配置定时任务

勾选 `Build periodically`（定期构建）

在 `Schedule` 中填写 cron 表达式：

**示例：**
```bash
# 每天凌晨 2 点执行
H 2 * * *

# 每天早上 9 点和下午 6 点执行
0 9,18 * * *

# 每小时执行一次
H * * * *

# 工作日每天 9 点执行
0 9 * * 1-5
```

### 6.3 保存

点击 `Save` 保存配置

---

## 第七步：验证完整流程

### 7.1 运行一次完整测试

1. Build with Parameters
2. 选择：
   - ENV: `test`
   - TEST_TYPE: `all`
   - STOCK_TYPE: `all`
3. 点击 Build

### 7.2 检查点

构建过程中检查：
- [x] 代码检出成功
- [x] 依赖安装成功
- [x] 测试执行完成
- [x] Allure 报告生成
- [x] 飞书通知发送成功（检查群消息）

### 7.3 查看报告

1. 点击构建 → `Allure Report`
2. 检查报告内容完整
3. 复制报告 URL，确认可以访问

---

## 常见问题排查

### 问题 1：Allure 报告无法生成

**现象：** 构建失败，提示找不到 Allure

**解决：**
1. 检查 Allure 插件是否安装
2. 检查全局工具配置中 Allure Commandline 是否配置
3. 在 Jenkinsfile 中检查 allure 配置

### 问题 2：飞书通知未发送

**现象：** 测试完成但未收到飞书消息

**检查：**
1. `config/notification_config.yaml` 中 `enabled: true`
2. Webhook URL 配置正确
3. 查看 Jenkins Console Output 中的日志

### 问题 3：Git 认证失败

**现象：** 无法检出代码

**解决：**
1. Jenkins → Credentials → Add Credentials
2. 添加 Git 用户名密码或 SSH Key
3. 在 Job 配置中选择对应凭据

### 问题 4：Python 依赖安装失败

**现象：** pip install 报错

**解决：**
在 Jenkinsfile 的安装依赖部分添加镜像源：
```groovy
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 高级配置

### 1. 配置构建后操作

在 Jenkinsfile 的 `post` 部分可以添加：

```groovy
post {
    always {
        // 归档测试报告
        archiveArtifacts artifacts: 'reports/**/*', allowEmptyArchive: true
        
        // 发布 HTML 报告（需要 HTML Publisher 插件）
        publishHTML([
            reportDir: 'reports/allure-report',
            reportFiles: 'index.html',
            reportName: 'Test Report'
        ])
    }
}
```

### 2. 配置邮件通知

安装 `Email Extension Plugin`，在 `post` 中添加：

```groovy
post {
    failure {
        emailext (
            subject: "测试失败: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
            body: "请查看: ${env.BUILD_URL}",
            to: "team@example.com"
        )
    }
}
```

### 3. 多分支 Pipeline

如果需要支持多分支：
1. 创建 `Multibranch Pipeline` 而不是普通 Pipeline
2. 配置 Branch Sources
3. Jenkinsfile 会自动应用到所有分支

---

## 📚 相关文档

- Jenkinsfile: 项目根目录的 `Jenkinsfile`
- 飞书配置: `config/notification_config.yaml`
- 飞书通知指南: `docs/FEISHU_JENKINS_GUIDE.md`

---

## ✅ 配置完成检查清单

- [ ] Jenkins 已安装并运行
- [ ] Allure 插件已安装
- [ ] Allure Commandline 已配置
- [ ] Jenkins Job 已创建
- [ ] Git 仓库已配置
- [ ] 参数化构建已配置
- [ ] Pipeline 配置完成
- [ ] 报告 URL 已配置
- [ ] 运行测试构建成功
- [ ] Allure 报告可访问
- [ ] 飞书通知发送成功

全部完成后，你的 CI/CD 流程就配置好了！

---

## 🎯 日常使用

### 手动触发
1. 进入 Job 页面
2. Build with Parameters
3. 选择参数后构建

### 自动触发
- 定时任务自动执行
- 或配置 Git Webhook 在代码提交后自动触发

### 查看结果
- Jenkins 页面查看 Allure 报告
- 飞书群接收实时通知
