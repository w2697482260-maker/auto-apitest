"""
Pytest 插件 - 测试完成后自动发送飞书通知
"""
import os
import yaml
import pytest
from datetime import datetime
from pathlib import Path
from utils.feishu_notifier import FeishuNotifier
from utils.logger import logger


def pytest_configure(config):
    """Pytest 配置钩子"""
    config._test_start_time = datetime.now()


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """测试结束后的汇总钩子 - 发送飞书通知"""

    # 读取通知配置
    config_file = Path(__file__).parent.parent / 'config' / 'notification_config.yaml'
    if not config_file.exists():
        logger.warning("通知配置文件不存在，跳过飞书通知")
        return

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            notify_config = yaml.safe_load(f)
    except Exception as e:
        logger.error(f"读取通知配置失败: {e}")
        return

    # 检查是否启用飞书通知
    feishu_config = notify_config.get('feishu', {})
    if not feishu_config.get('enabled', False):
        logger.info("飞书通知未启用")
        return

    webhook_url = feishu_config.get('webhook_url', '')
    if not webhook_url or 'your-webhook-token-here' in webhook_url:
        logger.warning("飞书 Webhook URL 未配置，跳过通知")
        return

    # 收集测试统计信息
    stats = terminalreporter.stats
    total = sum([len(stats.get(key, [])) for key in ['passed', 'failed', 'skipped', 'error']])
    passed = len(stats.get('passed', []))
    failed = len(stats.get('failed', [])) + len(stats.get('error', []))
    skipped = len(stats.get('skipped', []))

    # 计算执行时间
    duration = (datetime.now() - config._test_start_time).total_seconds()

    # 获取环境信息
    from config import config as env_config
    env = env_config.get_current_env()

    # 构建报告 URL
    report_url = None
    jenkins_config = notify_config.get('jenkins', {})
    if os.environ.get('BUILD_NUMBER'):  # 在 Jenkins 环境中
        job_name = os.environ.get('JOB_NAME', '')
        build_number = os.environ.get('BUILD_NUMBER', '')
        url_template = jenkins_config.get('report_url_template', '')
        if url_template:
            report_url = url_template.replace('${JOB_NAME}', job_name).replace('${BUILD_NUMBER}', build_number)

    # 准备报告数据
    report_data = {
        'total': total,
        'passed': passed,
        'failed': failed,
        'skipped': skipped,
        'duration': round(duration, 2),
        'env': env,
        'report_url': report_url
    }

    # 判断是否需要发送通知
    notify_rules = feishu_config.get('notify_on', {})
    should_notify = False

    if notify_rules.get('always', False):
        should_notify = True
    elif failed > 0 and notify_rules.get('failure', True):
        should_notify = True
    elif failed == 0 and notify_rules.get('success', True):
        should_notify = True

    if not should_notify:
        logger.info("根据通知规则，跳过本次通知")
        return

    # 发送飞书通知
    logger.info("正在发送飞书通知...")
    notifier = FeishuNotifier(webhook_url)

    success = notifier.send_test_report(report_data)

    if success:
        logger.info("✅ 飞书通知发送成功")
    else:
        logger.error("❌ 飞书通知发送失败")
