# Jenkins Windows 配置快速清单

## ✅ 安装完成后立即执行

### 1. 首次访问 Jenkins（2分钟）
```
1. 浏览器打开: http://localhost:8080
2. 输入初始密码（在安装目录或日志中）
3. 选择"Install suggested plugins"
4. 创建管理员账号
5. 保存并完成
```

---

### 2. 安装 Allure 插件（3分钟）

```
Jenkins 首页
  → Manage Jenkins
    → Manage Plugins
      → Available 标签页
        → 搜索 "Allure"
          → 勾选 "Allure Jenkins Plugin"
            → 点击 "Install without restart"
```

---

### 3. 配置 Allure 工具（2分钟）

```
Jenkins 首页
  → Manage Jenkins
    → Global Tool Configuration
      → 向下滚动找到 "Allure Commandline"
        → 点击 "Add Allure Commandline"
          → Name: allure
          → 勾选 "Install automatically"
          → From Maven Central: 选择最新版本
            → 点击 Save
```

---

### 4. 创建测试任务（5分钟）

#### 4.1 新建任务
```
Jenkins 首页
  → New Item
    → 输入名称: ESOP-API-Automation
    → 选择 Pipeline
    → 点击 OK
```

#### 4.2 配置参数
勾选 "This project is parameterized"，添加 3 个参数：

**参数1：**
- Type: Choice Parameter
- Name: `ENV`
- Choices: test, staging, dev (每行一个)

**参数2：**
- Type: Choice Parameter
- Name: `TEST_TYPE`
- Choices: all, smoke, regression, bos, admin, staff

**参数3：**
- Type: Choice Parameter
- Name: `STOCK_TYPE`
- Choices: all, hk_us, unlisted, a_stock

#### 4.3 配置 Pipeline

**方式A - 如果项目在本地（推荐先用这个）：**

1. Definition: 选择 `Pipeline script`
2. 复制 `Jenkinsfile.windows` 的全部内容粘贴进去
3. 点击 Save

**方式B - 如果项目在 Git：**

1. Definition: 选择 `Pipeline script from SCM`
2. SCM: Git
3. Repository URL: 你的 Git 地址
4. Script Path: `Jenkinsfile.windows`
5. 点击 Save

---

### 5. 配置项目（1分钟）

编辑 `config/notification_config.yaml`：

```yaml
jenkins:
  report_url_template: "http://localhost:8080/job/ESOP-API-Automation/${BUILD_NUMBER}/allure"
```

---

### 6. 运行第一次测试（1分钟）

```
1. 进入 ESOP-API-Automation 任务页面
2. 点击左侧 "Build with Parameters"
3. 选择参数：
   - ENV: test
   - TEST_TYPE: smoke
   - STOCK_TYPE: all
4. 点击 Build
5. 在 Build History 中点击构建编号
6. 点击 Console Output 查看日志
```

---

## 🎯 成功标志

构建完成后，你应该看到：
- ✅ Console Output 显示测试执行成功
- ✅ 左侧出现 "Allure Report" 链接
- ✅ 飞书群收到测试报告通知

---

## ⚠️ 常见问题

### 问题1：找不到 Python
**解决：** 
```
Manage Jenkins 
  → Global Tool Configuration 
    → 添加 Python 路径到 PATH 环境变量
```

### 问题2：Allure 报告无法生成
**检查：**
- Allure 插件是否安装
- Global Tool Configuration 中 Allure 是否配置

### 问题3：代码检出失败
**解决方案：**
- 如果项目在本地，暂时使用 Pipeline script 方式
- 将 Jenkinsfile.windows 内容直接粘贴到配置中

---

## 📞 需要帮助？

如果遇到问题，提供以下信息：
1. Jenkins 版本
2. 错误信息截图
3. Console Output 日志

---

## 📚 相关文件

- Windows版本 Pipeline: `Jenkinsfile.windows`
- 详细配置指南: `docs/JENKINS_SETUP_GUIDE.md`
- 飞书配置: `config/notification_config.yaml`
