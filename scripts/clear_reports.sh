#!/bin/bash
# 清理报告脚本

echo "清理测试报告和日志..."

# 清理Allure结果
if [ -d "reports/allure-results" ]; then
    rm -rf reports/allure-results/*
    echo "✓ 清理 allure-results"
fi

# 清理Allure报告
if [ -d "reports/allure-report" ]; then
    rm -rf reports/allure-report
    echo "✓ 清理 allure-report"
fi

# 清理日志
if [ -d "reports/logs" ]; then
    rm -rf reports/logs/*.log
    echo "✓ 清理日志文件"
fi

# 清理pytest缓存
if [ -d ".pytest_cache" ]; then
    rm -rf .pytest_cache
    echo "✓ 清理 pytest缓存"
fi

# 清理Python缓存
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
echo "✓ 清理 Python缓存"

echo "=========================================="
echo "清理完成！"
echo "=========================================="
