#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
飞书通知测试脚本
用于测试飞书机器人配置是否正确
"""

import yaml
from pathlib import Path
from utils.feishu_notifier import FeishuNotifier
from utils.logger import logger


def test_feishu_notification():
    """测试飞书通知功能"""

    # 读取配置
    config_file = Path(__file__).parent / 'config' / 'notification_config.yaml'

    if not config_file.exists():
        print("❌ 配置文件不存在: config/notification_config.yaml")
        return False

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ 读取配置文件失败: {e}")
        return False

    # 检查飞书配置
    feishu_config = config.get('feishu', {})

    if not feishu_config.get('enabled', False):
        print("❌ 飞书通知未启用")
        print("请在 config/notification_config.yaml 中设置 feishu.enabled: true")
        return False

    webhook_url = feishu_config.get('webhook_url', '')

    if not webhook_url:
        print("❌ 未配置 Webhook URL")
        return False

    if 'your-webhook-token-here' in webhook_url:
        print("❌ 请在 config/notification_config.yaml 中配置真实的 Webhook URL")
        print("当前配置: " + webhook_url)
        return False

    print(f"✓ 配置文件读取成功")
    print(f"✓ Webhook URL: {webhook_url[:50]}...")
    print()

    # 创建通知器
    notifier = FeishuNotifier(webhook_url)

    # 测试1: 发送文本消息
    print("测试 1/3: 发送文本消息...")
    success1 = notifier.send_text("🎉 飞书通知测试 - 文本消息发送成功！")

    if success1:
        print("✅ 文本消息发送成功")
    else:
        print("❌ 文本消息发送失败")

    print()

    # 测试2: 发送富文本消息
    print("测试 2/3: 发送富文本消息...")
    content = [
        [
            {"tag": "text", "text": "这是一条"},
            {"tag": "text", "text": "富文本测试消息", "style": ["bold"]},
        ],
        [
            {"tag": "text", "text": "支持多种样式："},
        ],
        [
            {"tag": "text", "text": "加粗", "style": ["bold"]},
            {"tag": "text", "text": " | "},
            {"tag": "text", "text": "斜体", "style": ["italic"]},
            {"tag": "text", "text": " | "},
            {"tag": "text", "text": "删除线", "style": ["lineThrough"]},
        ]
    ]
    success2 = notifier.send_rich_text("飞书通知测试", content)

    if success2:
        print("✅ 富文本消息发送成功")
    else:
        print("❌ 富文本消息发送失败")

    print()

    # 测试3: 发送测试报告
    print("测试 3/3: 发送测试报告卡片...")
    report_data = {
        'total': 22,
        'passed': 18,
        'failed': 3,
        'skipped': 1,
        'duration': 45.8,
        'env': 'test',
        'report_url': 'http://jenkins.example.com/job/esop-api-test/123/allure'
    }
    success3 = notifier.send_test_report(report_data)

    if success3:
        print("✅ 测试报告发送成功")
    else:
        print("❌ 测试报告发送失败")

    print()
    print("=" * 50)

    # 总结
    all_success = success1 and success2 and success3

    if all_success:
        print("🎉 所有测试通过！飞书通知配置正确")
        print()
        print("接下来可以：")
        print("1. 运行 pytest 进行实际测试")
        print("2. 测试完成后会自动发送飞书通知")
        return True
    else:
        print("⚠️ 部分测试失败，请检查：")
        print("1. Webhook URL 是否正确")
        print("2. 机器人是否被移除群聊")
        print("3. 网络是否可以访问飞书 API")
        print("4. 查看详细日志: reports/logs/pytest.log")
        return False


if __name__ == '__main__':
    print("=" * 50)
    print("      飞书通知测试脚本")
    print("=" * 50)
    print()

    test_feishu_notification()
