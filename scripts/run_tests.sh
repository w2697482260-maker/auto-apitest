#!/bin/bash
# 测试执行脚本

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}ESOP接口自动化测试${NC}"
echo -e "${GREEN}========================================${NC}"

# 默认参数
ENV=${TEST_ENV:-test}
MARKERS=""
RERUNS=0
WORKERS=1

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --env)
            ENV="$2"
            shift 2
            ;;
        --smoke)
            MARKERS="smoke"
            shift
            ;;
        --bos)
            MARKERS="bos"
            shift
            ;;
        --admin)
            MARKERS="admin"
            shift
            ;;
        --staff)
            MARKERS="staff"
            shift
            ;;
        --hk-us)
            MARKERS="hk_us"
            shift
            ;;
        --unlisted)
            MARKERS="unlisted"
            shift
            ;;
        --a-stock)
            MARKERS="a_stock"
            shift
            ;;
        --p0)
            MARKERS="p0"
            shift
            ;;
        --reruns)
            RERUNS="$2"
            shift 2
            ;;
        --parallel)
            WORKERS="$2"
            shift 2
            ;;
        *)
            echo -e "${RED}未知参数: $1${NC}"
            exit 1
            ;;
    esac
done

echo -e "${YELLOW}测试环境: ${ENV}${NC}"
export TEST_ENV=$ENV

# 构建pytest命令
CMD="pytest"

if [ -n "$MARKERS" ]; then
    CMD="$CMD -m $MARKERS"
    echo -e "${YELLOW}测试标记: ${MARKERS}${NC}"
fi

if [ $RERUNS -gt 0 ]; then
    CMD="$CMD --reruns $RERUNS"
    echo -e "${YELLOW}失败重跑: ${RERUNS}次${NC}"
fi

if [ $WORKERS -gt 1 ]; then
    CMD="$CMD -n $WORKERS"
    echo -e "${YELLOW}并行执行: ${WORKERS}个进程${NC}"
fi

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}开始执行测试...${NC}"
echo -e "${GREEN}========================================${NC}"

# 执行测试
$CMD

# 获取退出码
EXIT_CODE=$?

echo -e "${GREEN}========================================${NC}"
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✓ 测试执行完成${NC}"
else
    echo -e "${RED}✗ 测试执行失败 (退出码: $EXIT_CODE)${NC}"
fi
echo -e "${GREEN}========================================${NC}"

# 生成Allure报告
if command -v allure &> /dev/null; then
    echo -e "${YELLOW}生成Allure报告...${NC}"
    allure generate reports/allure-results -o reports/allure-report --clean
    echo -e "${GREEN}✓ Allure报告已生成: reports/allure-report${NC}"
    echo -e "${YELLOW}查看报告: allure open reports/allure-report${NC}"
else
    echo -e "${YELLOW}⚠ Allure未安装，跳过报告生成${NC}"
fi

exit $EXIT_CODE
