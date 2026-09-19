# ESOP接口自动化测试框架

股权激励系统（ESOP）接口自动化测试框架，支持BOS、Admin、Staff三端，覆盖港美股、未上市、A股三条业务线。

## 技术栈

- **Python 3.8+**
- **pytest** - 测试框架
- **requests** - HTTP请求
- **allure** - 测试报告
- **Jenkins** - CI/CD
- **飞书** - 测试通知

## 项目结构

```
esop-api-automation/
├── config/                 # 配置文件
│   ├── env_config.yaml    # 环境配置
│   ├── user_config.yaml   # 用户配置
│   └── business_config.yaml # 业务配置
├── utils/                  # 工具模块
│   ├── http_client.py     # HTTP客户端
│   ├── logger.py          # 日志工具
│   ├── assertions.py      # 断言工具
│   ├── data_handler.py    # 数据处理
│   └── feishu_notifier.py # 飞书通知
├── api/                    # API封装层
│   ├── bos/               # BOS端API
│   ├── admin/             # Admin端API
│   └── staff/             # Staff端API
├── business/              # 业务流程层
│   ├── hk_us_stock.py    # 港美股业务
│   ├── unlisted_stock.py # 未上市业务
│   └── a_stock.py        # A股业务
├── testcases/            # 测试用例
│   ├── bos/
│   ├── admin/
│   └── staff/
├── testdata/             # 测试数据
├── reports/              # 测试报告
└── scripts/              # 脚本工具
```

## 快速开始

### 1. 安装依赖

```bash
cd esop-api-automation
pip install -r requirements.txt
```

### 2. 配置环境

编辑 `config/env_config.yaml`，配置测试环境URL：

```yaml
current_env: test  # dev/test/staging/prod
```

编辑 `config/user_config.yaml`，配置测试用户账号（注意：敏感信息建议使用环境变量）

### 3. 执行测试

**全量测试：**
```bash
pytest
```

**冒烟测试：**
```bash
pytest -m smoke
```

**按端执行：**
```bash
pytest -m bos      # BOS端
pytest -m admin    # Admin端
pytest -m staff    # Staff端
```

**按业务线执行：**
```bash
pytest -m hk_us      # 港美股
pytest -m unlisted   # 未上市
pytest -m a_stock    # A股
```

**组合标记：**
```bash
pytest -m "bos and hk_us"  # BOS端的港美股用例
pytest -m "smoke and p0"    # 冒烟+高优先级
```

**使用脚本执行：**
```bash
chmod +x scripts/run_tests.sh
./scripts/run_tests.sh --env test --smoke
./scripts/run_tests.sh --env test --bos --hk-us
./scripts/run_tests.sh --env test --p0 --parallel 4
```

### 4. 查看报告

**生成Allure报告：**
```bash
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

**查看日志：**
```bash
tail -f reports/logs/all_*.log
tail -f reports/logs/error_*.log
```

## 测试标记说明

### 端标记
- `@pytest.mark.bos` - BOS端测试
- `@pytest.mark.admin` - Admin端测试
- `@pytest.mark.staff` - Staff端测试

### 业务线标记
- `@pytest.mark.hk_us` - 港美股业务
- `@pytest.mark.unlisted` - 未上市业务
- `@pytest.mark.a_stock` - A股业务

### 优先级标记
- `@pytest.mark.smoke` - 冒烟测试
- `@pytest.mark.p0` - 高优先级
- `@pytest.mark.p1` - 中优先级
- `@pytest.mark.p2` - 低优先级

### 测试类型标记
- `@pytest.mark.regression` - 回归测试
- `@pytest.mark.api` - 接口测试

## Jenkins集成

1. 在Jenkins中创建Pipeline项目
2. 配置SCM，指向代码仓库
3. Pipeline script选择 "Pipeline script from SCM"
4. Script Path填写：`esop-api-automation/Jenkinsfile`
5. 配置构建参数：
   - ENV: 测试环境
   - TEST_TYPE: 测试类型
   - STOCK_TYPE: 股票类型
   - FEISHU_WEBHOOK: 飞书通知地址

## 飞书通知

### 获取飞书机器人Webhook

1. 进入飞书群聊
2. 点击右上角设置 → 群机器人 → 添加机器人
3. 选择"自定义机器人"
4. 复制Webhook地址

### 配置通知

**方式1：环境变量**
```bash
export FEISHU_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
```

**方式2：在Jenkins中配置**
在Pipeline参数中填写FEISHU_WEBHOOK

## 环境变量

```bash
# 测试环境
export TEST_ENV=test  # dev/test/staging/prod

# 飞书通知
export FEISHU_WEBHOOK="your_webhook_url"

# 日志级别
export LOG_LEVEL=INFO  # DEBUG/INFO/WARNING/ERROR
```

## 扩展开发

### 添加新的API

1. 在 `api/{platform}/` 目录下创建新的API文件
2. 继承 `BaseAPI` 类
3. 使用 `@allure.step` 装饰器标注步骤

```python
from api.base_api import BaseAPI
import allure

class NewAPI(BaseAPI):
    @allure.step("新接口调用")
    def new_method(self, params):
        response = self.client.post('/api/path', json=params)
        self.assertions.assert_status_code(response, 200)
        return response.json()
```

### 添加新的测试用例

1. 在 `testcases/{platform}/` 目录下创建测试文件
2. 使用 `@allure` 装饰器和 `@pytest.mark` 标记
3. 使用fixture获取API实例

```python
import pytest
import allure

@allure.feature("功能模块")
@allure.story("用户故事")
@pytest.mark.bos
@pytest.mark.p0
class TestNewFeature:
    @allure.title("测试用例标题")
    def test_case(self, bos_admin_session):
        # 测试逻辑
        pass
```

## 常见问题

### 1. SSL证书验证错误
已在 `http_client.py` 中禁用SSL验证，如需启用请修改：
```python
verify=True
```

### 2. 认证失败
检查 `config/user_config.yaml` 中的用户名密码是否正确

### 3. 报告中文乱码
确保系统编码为UTF-8：
```bash
export LANG=zh_CN.UTF-8
```

### 4. 并行执行冲突
使用 `scope="function"` 的fixture确保测试隔离

## 最佳实践

1. **测试数据隔离**：每个测试用例使用独立的测试数据
2. **清理机制**：使用cleanup fixture清理测试创建的数据
3. **失败重跑**：对于不稳定的测试配置重跑机制
4. **日志记录**：关键步骤记录详细日志便于定位问题
5. **断言清晰**：断言失败时提供清晰的错误信息

## 联系方式

如有问题，请联系测试团队。

---
**版本**: 1.0.0  
**更新日期**: 2024-01-01
