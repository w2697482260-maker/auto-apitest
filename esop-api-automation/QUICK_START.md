# ESOP接口自动化测试框架 - 快速开始

## 📋 项目概览

已为你创建了一个完整的接口自动化测试框架，包含：

- ✅ **33个Python文件** - 核心代码和测试用例
- ✅ **6个配置文件** - 环境、用户、业务配置
- ✅ **2个Shell脚本** - 测试执行和清理
- ✅ **完整的项目结构** - 分层清晰，易于维护

## 🎯 核心特性

### 1. 多端支持
- **BOS端**: 股权计划创建、审批、授予管理
- **Admin端**: 审批流程、员工管理
- **Staff端**: 股权查看、行权操作

### 2. 多业务线
- **港美股**: 支持HK/US市场，多币种
- **未上市**: 私募股权，估值管理
- **A股**: 遵循A股交易规则（100股倍数）

### 3. 测试能力
- HTTP请求封装（自动重试、日志记录）
- 完善的断言工具
- 测试数据生成
- Allure报告集成
- 飞书通知
- Jenkins CI/CD

## 🚀 10分钟上手

### 第一步：安装依赖

```bash
cd esop-api-automation
pip install -r requirements.txt
```

### 第二步：配置环境

编辑 `config/env_config.yaml`：

```yaml
current_env: test  # 选择测试环境

environments:
  test:
    bos:
      base_url: https://bos-test.esop.com  # 修改为实际地址
    admin:
      base_url: https://admin-test.esop.com
    staff:
      base_url: https://staff-test.esop.com
```

编辑 `config/user_config.yaml`：

```yaml
bos_users:
  admin_user:
    username: your_username  # 修改为实际账号
    password: your_password
```

### 第三步：运行测试

**方式1: 使用pytest直接运行**

```bash
# 运行所有测试
pytest

# 冒烟测试
pytest -m smoke

# BOS端港美股测试
pytest -m "bos and hk_us"

# 查看详细输出
pytest -v -s
```

**方式2: 使用执行脚本**

```bash
# 添加执行权限
chmod +x scripts/run_tests.sh

# 冒烟测试
./scripts/run_tests.sh --smoke

# 指定环境的BOS测试
./scripts/run_tests.sh --env test --bos

# 并行执行
./scripts/run_tests.sh --p0 --parallel 4
```

### 第四步：查看报告

```bash
# 生成并打开Allure报告
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report

# 查看日志
tail -f reports/logs/all_*.log
```

## 📁 项目结构详解

```
esop-api-automation/
│
├── config/                      # 📝 配置层
│   ├── env_config.yaml         # 环境配置（URL、超时等）
│   ├── user_config.yaml        # 测试用户账号
│   └── business_config.yaml    # 业务规则配置
│
├── utils/                       # 🔧 工具层
│   ├── http_client.py          # HTTP客户端（请求/重试/日志）
│   ├── logger.py               # 日志工具（文件+控制台）
│   ├── assertions.py           # 断言工具
│   ├── data_handler.py         # 数据处理/生成
│   └── feishu_notifier.py      # 飞书通知
│
├── api/                         # 🌐 API层（接口封装）
│   ├── base_api.py             # API基类
│   ├── bos/                    # BOS端API
│   │   ├── auth_api.py         # 认证接口
│   │   └── equity_api.py       # 股权接口
│   ├── admin/                  # Admin端API
│   │   ├── auth_api.py
│   │   └── management_api.py
│   └── staff/                  # Staff端API
│       ├── auth_api.py
│       └── equity_api.py
│
├── business/                    # 💼 业务层（流程封装）
│   ├── hk_us_stock.py          # 港美股业务流程
│   ├── unlisted_stock.py       # 未上市业务流程
│   └── a_stock.py              # A股业务流程
│
├── testcases/                   # 🧪 测试用例层
│   ├── conftest.py             # pytest配置（fixtures）
│   ├── bos/                    # BOS端测试
│   │   ├── test_hk_us_stock.py
│   │   ├── test_unlisted_stock.py
│   │   └── test_a_stock.py
│   ├── admin/
│   │   └── test_admin_management.py
│   └── staff/
│       └── test_staff_equity.py
│
├── testdata/                    # 📊 测试数据
│   ├── bos_testdata.yaml
│   ├── admin_testdata.yaml
│   └── staff_testdata.yaml
│
├── reports/                     # 📈 测试报告
│   ├── allure-results/         # Allure原始数据
│   ├── allure-report/          # Allure HTML报告
│   └── logs/                   # 测试日志
│
├── scripts/                     # 📜 执行脚本
│   ├── run_tests.sh            # 测试执行脚本
│   └── clear_reports.sh        # 清理报告脚本
│
├── pytest.ini                   # Pytest配置
├── requirements.txt             # Python依赖
├── Jenkinsfile                  # Jenkins Pipeline
└── README.md                    # 项目文档
```

## 🏷️ 测试标记使用

框架支持灵活的测试标记组合：

```bash
# 端标记
pytest -m bos          # BOS端所有测试
pytest -m admin        # Admin端所有测试
pytest -m staff        # Staff端所有测试

# 业务线标记
pytest -m hk_us        # 港美股业务
pytest -m unlisted     # 未上市业务
pytest -m a_stock      # A股业务

# 优先级标记
pytest -m smoke        # 冒烟测试
pytest -m p0           # 高优先级
pytest -m p1           # 中优先级

# 组合标记
pytest -m "bos and hk_us"              # BOS端的港美股测试
pytest -m "smoke and p0"                # 冒烟+高优
pytest -m "(bos or admin) and smoke"    # BOS或Admin的冒烟测试
```

## 🔥 常用命令

```bash
# 测试执行
pytest -v                           # 详细输出
pytest -s                           # 显示print输出
pytest -x                           # 首次失败后停止
pytest --lf                         # 只运行上次失败的用例
pytest --reruns 2                   # 失败重跑2次
pytest -n 4                         # 4个进程并行
pytest -k "test_create"             # 运行名称包含create的用例

# 报告相关
allure serve reports/allure-results  # 生成并打开报告
./scripts/clear_reports.sh           # 清理报告

# 查看日志
tail -f reports/logs/all_*.log       # 实时查看所有日志
tail -f reports/logs/error_*.log     # 实时查看错误日志
```

## 🎨 编写测试用例示例

```python
import pytest
import allure

@allure.feature("BOS端")
@allure.story("股权管理")
@pytest.mark.bos
@pytest.mark.hk_us
@pytest.mark.p0
class TestEquityManagement:
    
    @allure.title("创建港美股股权计划")
    @allure.description("测试BOS端创建港美股股权计划的完整流程")
    def test_create_hk_us_plan(self, bos_admin_session, data_handler, cleanup_equity_plans):
        # 1. 准备测试数据
        plan_data = data_handler.generate_equity_plan_data('hk_us')
        
        # 2. 执行创建
        with allure.step("创建股权计划"):
            resp = bos_admin_session.create_equity_plan(plan_data)
        
        # 3. 断言验证
        with allure.step("验证创建成功"):
            assert resp['code'] == 0
            plan_id = resp['data']['plan_id']
            cleanup_equity_plans.append(plan_id)
        
        # 4. 查询验证
        with allure.step("查询并验证计划详情"):
            detail = bos_admin_session.get_equity_plan_detail(plan_id)
            assert detail['data']['plan_name'] == plan_data['plan_name']
```

## 🔔 飞书通知配置

### 1. 获取飞书Webhook

- 进入飞书群聊
- 设置 → 群机器人 → 添加机器人
- 选择"自定义机器人"
- 复制Webhook地址

### 2. 配置通知

```bash
# 方式1: 环境变量
export FEISHU_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/xxx"

# 方式2: 在代码中使用
from utils.feishu_notifier import send_feishu_notification

report_data = {
    'env': 'test',
    'total': 50,
    'passed': 45,
    'failed': 3,
    'skipped': 2,
    'duration': 120,
    'report_url': 'http://jenkins/allure'
}

send_feishu_notification(webhook_url, report_data)
```

## 🤖 Jenkins集成

1. **创建Pipeline项目**
2. **配置参数**：
   - ENV: test/staging/prod
   - TEST_TYPE: smoke/regression/all
   - STOCK_TYPE: hk_us/unlisted/a_stock/all
   - FEISHU_WEBHOOK: 飞书通知地址

3. **使用Jenkinsfile**：项目已包含完整的Jenkinsfile

4. **触发构建**：
   - 手动触发
   - 定时触发（cron）
   - 代码提交触发

## 📊 预期测试报告内容

### Allure报告包含：
- ✅ 测试用例执行情况
- ✅ 每个用例的详细步骤
- ✅ 请求和响应详情
- ✅ 断言结果
- ✅ 失败截图/日志
- ✅ 趋势分析
- ✅ 分类统计

### 飞书通知包含：
- 执行时间
- 执行环境
- 总用例数
- 通过率
- 通过/失败/跳过数量
- 执行耗时
- 报告链接

## 🔍 下一步

1. **调整配置**: 根据实际接口修改API路径和响应格式
2. **补充用例**: 添加更多业务场景的测试用例
3. **数据准备**: 准备测试环境和测试数据
4. **CI集成**: 配置Jenkins定时执行
5. **监控告警**: 配置飞书通知接收测试报告

## 💡 最佳实践

1. **数据隔离**: 每个测试用例使用独立数据
2. **清理机制**: 测试后清理创建的数据
3. **幂等性**: 测试用例可重复执行
4. **原子性**: 每个测试只验证一个功能点
5. **独立性**: 测试用例间不依赖执行顺序

## 📞 需要帮助？

框架已经完整搭建，包含：
- ✅ 完整的代码结构
- ✅ 示例测试用例
- ✅ 配置文件模板
- ✅ 执行脚本
- ✅ Jenkins配置
- ✅ 详细文档

你可以直接开始使用，根据实际接口调整配置和API封装即可！
