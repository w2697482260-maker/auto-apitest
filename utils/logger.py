"""
日志工具模块
"""
import sys
from pathlib import Path
from loguru import logger


# 移除默认handler
logger.remove()

# 日志目录
log_dir = Path(__file__).parent.parent / 'reports' / 'logs'
log_dir.mkdir(parents=True, exist_ok=True)

# 控制台输出
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO",
    colorize=True
)

# 文件输出 - 所有日志
logger.add(
    log_dir / "all_{time:YYYY-MM-DD}.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG",
    rotation="00:00",  # 每天零点轮转
    retention="30 days",  # 保留30天
    compression="zip",  # 压缩
    encoding="utf-8",
    enqueue=True  # 异步写入
)

# 文件输出 - 错误日志
logger.add(
    log_dir / "error_{time:YYYY-MM-DD}.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="ERROR",
    rotation="00:00",
    retention="30 days",
    compression="zip",
    encoding="utf-8",
    enqueue=True
)

__all__ = ['logger']
