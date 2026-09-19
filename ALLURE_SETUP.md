# Allure 报告生成指南

## 当前状态
✅ Allure 原始数据已经生成在 `reports/allure-results/` 目录
❌ 需要安装 Allure 命令行工具来生成 HTML 报告

## 安装 Allure 命令行工具

### 方法一：使用 Scoop（推荐，适用于 Windows）

1. 安装 Scoop（如果还没安装）：
```powershell
# 在 PowerShell 中运行
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex
```

2. 安装 Allure：
```bash
scoop install allure
```

### 方法二：手动下载安装

1. 下载 Allure：
   - 访问：https://github.com/allure-framework/allure2/releases
   - 下载最新版本的 `allure-x.x.x.zip`

2. 解压到某个目录（例如：`C:\allure`）

3. 添加到系统环境变量 PATH：
   - 将 `C:\allure\bin` 添加到系统 PATH

### 方法三：使用 npm（如果已安装 Node.js）

```bash
npm install -g allure-commandline
```

## 生成 Allure 报告

安装完成后，运行以下命令生成报告：

```bash
# 生成并自动打开报告
allure serve reports/allure-results

# 或者生成静态 HTML 报告
allure generate reports/allure-results -o reports/allure-report --clean
```

## 运行测试并生成报告的完整流程

```bash
# 1. 激活虚拟环境
source .venv/Scripts/activate

# 2. 运行测试（原始数据会自动生成到 reports/allure-results/）
pytest

# 3. 生成并打开报告
allure serve reports/allure-results
```

## 注意事项

1. **原始数据已生成**：每次运行 pytest 时，测试结果会自动保存到 `reports/allure-results/`
2. **需要 Allure 工具**：必须安装 Allure 命令行工具才能查看 HTML 报告
3. **自动清理**：`pytest.ini` 中配置了 `--clean-alluredir`，每次运行会清理旧数据

## 快速验证

安装完 Allure 后，运行以下命令验证：

```bash
allure --version
```

应该显示类似：`2.x.x`

## 当前测试结果

根据最近的测试运行，所有测试都因为 SSL 连接问题失败了：
- 测试服务器：`bos-test.esop.com`、`admin-test.esop.com`、`staff-test.esop.com`
- 错误：`SSL: TLSV1_UNRECOGNIZED_NAME`
- 原因：测试服务器的 SSL 配置有问题（不是代码问题）

建议联系服务器管理员修复 SSL 配置，或者修改 `config/env_config.yaml` 指向可用的测试环境。
