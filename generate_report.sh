#!/bin/bash
# Allure 报告生成脚本

# 设置 JAVA_HOME
export JAVA_HOME="/c/Program Files/Microsoft/jdk-17.0.20.101-hotspot"
export PATH="$JAVA_HOME/bin:$PATH"

echo "正在生成 Allure 报告..."

# 生成报告
allure generate reports/allure-results -o reports/allure-report --clean

if [ $? -eq 0 ]; then
    echo "✅ 报告生成成功: reports/allure-report"
    echo "正在打开报告..."
    start reports/allure-report/index.html
else
    echo "❌ 报告生成失败"
    exit 1
fi
