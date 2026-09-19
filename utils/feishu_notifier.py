"""
飞书通知工具
"""
import json
import time
import requests
from datetime import datetime
from typing import Dict, List, Optional
from .logger import logger


class FeishuNotifier:
    """飞书通知类"""

    def __init__(self, webhook_url: str):
        """
        初始化飞书通知
        :param webhook_url: 飞书机器人webhook地址
        """
        self.webhook_url = webhook_url

    def send_text(self, text: str) -> bool:
        """
        发送文本消息
        :param text: 文本内容
        :return: 是否发送成功
        """
        data = {
            "msg_type": "text",
            "content": {
                "text": text
            }
        }
        return self._send(data)

    def send_rich_text(self, title: str, content: List[List[Dict]]) -> bool:
        """
        发送富文本消息
        :param title: 标题
        :param content: 富文本内容
        :return: 是否发送成功
        """
        data = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": title,
                        "content": content
                    }
                }
            }
        }
        return self._send(data)

    def send_card(self, header: Dict, elements: List[Dict]) -> bool:
        """
        发送卡片消息
        :param header: 卡片标题
        :param elements: 卡片元素列表
        :return: 是否发送成功
        """
        data = {
            "msg_type": "interactive",
            "card": {
                "header": header,
                "elements": elements
            }
        }
        return self._send(data)

    def send_test_report(self, report_data: Dict) -> bool:
        """
        发送测试报告
        :param report_data: 报告数据
        :return: 是否发送成功
        """
        total = report_data.get('total', 0)
        passed = report_data.get('passed', 0)
        failed = report_data.get('failed', 0)
        skipped = report_data.get('skipped', 0)
        duration = report_data.get('duration', 0)
        pass_rate = (passed / total * 100) if total > 0 else 0

        # 根据通过率确定状态颜色
        if pass_rate == 100:
            color = "green"
            status_emoji = "✅"
        elif pass_rate >= 80:
            color = "yellow"
            status_emoji = "⚠️"
        else:
            color = "red"
            status_emoji = "❌"

        # 构建卡片消息
        header = {
            "title": {
                "content": f"{status_emoji} ESOP接口自动化测试报告",
                "tag": "plain_text"
            },
            "template": color
        }

        elements = [
            {
                "tag": "div",
                "text": {
                    "content": f"**执行时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    "tag": "lark_md"
                }
            },
            {
                "tag": "div",
                "text": {
                    "content": f"**执行环境:** {report_data.get('env', 'test')}",
                    "tag": "lark_md"
                }
            },
            {
                "tag": "hr"
            },
            {
                "tag": "div",
                "fields": [
                    {
                        "is_short": True,
                        "text": {
                            "content": f"**总用例数:** {total}",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "content": f"**通过率:** {pass_rate:.2f}%",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "content": f"**通过:** {passed} ✅",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "content": f"**失败:** {failed} ❌",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "content": f"**跳过:** {skipped} ⏭️",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "content": f"**耗时:** {duration}s ⏱️",
                            "tag": "lark_md"
                        }
                    }
                ]
            }
        ]

        # 添加报告链接（如果有）
        if report_data.get('report_url'):
            elements.append({
                "tag": "hr"
            })
            elements.append({
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {
                            "content": "查看详细报告 📊",
                            "tag": "plain_text"
                        },
                        "url": report_data.get('report_url'),
                        "type": "primary"
                    }
                ]
            })

        return self.send_card(header, elements)

    def _send(self, data: Dict) -> bool:
        """
        发送消息到飞书
        :param data: 消息数据
        :return: 是否发送成功
        """
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(
                self.webhook_url,
                headers=headers,
                data=json.dumps(data),
                timeout=10
            )

            result = response.json()
            if result.get('code') == 0:
                logger.info("飞书消息发送成功")
                return True
            else:
                logger.error(f"飞书消息发送失败: {result}")
                return False

        except Exception as e:
            logger.error(f"飞书消息发送异常: {str(e)}")
            return False


# 便捷函数
def send_feishu_notification(webhook_url: str, report_data: Dict):
    """发送飞书测试报告通知"""
    notifier = FeishuNotifier(webhook_url)
    return notifier.send_test_report(report_data)
