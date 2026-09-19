#!/bin/bash
# 运行测试并生成 Allure 报告的完整脚本

# 设置 JAVA_HOME
export JAVA_HOME="/c/Program Files/Microsoft/jdk-17.0.20.101-hotspot"
export PATH="$JAVA_HOME/bin:$PATH"

echo "=========================================="
echo "  ESOP API 自动化测试"
echo "=========================================="
echo ""

# 激活虚拟环境
echo "1. 激活虚拟环境..."
source .venv/Scripts/activate

# 运行测试
echo "2. 运行测试..."
pytest "$@"

TEST_RESULT=$?

# 生成报告
echo ""
echo "3. 生成 Allure 报告..."
allure generate reports/allure-results -o reports/allure-report --clean

if [ $? -eq 0 ]; then
    echo "✅ 报告生成成功: reports/allure-report"
    echo ""
    echo "打开报告: start reports/allure-report/index.html"
    echo "或使用命令: allure open reports/allure-report"
    echo ""

    # 询问是否打开报告
    read -p "是否现在打开报告? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        start reports/allure-report/index.html
    fi
else
    echo "❌ 报告生成失败"
fi

exit $TEST_RESULT
