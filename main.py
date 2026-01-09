#!/usr/bin/env python3
"""
Telegram客服机器人主启动文件

提供支付指导和客服服务
"""

import asyncio
import logging
import sys
from app.bot import CustomerServiceBot

# 配置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    """主函数"""
    logger.info("启动Telegram客服机器人...")

    try:
        # 初始化机器人
        bot = CustomerServiceBot()

        if not bot.initialized:
            logger.error("机器人初始化失败，无法启动")
            return

        logger.info("机器人初始化成功，开始运行...")

        # 运行机器人
        bot.run()

    except KeyboardInterrupt:
        logger.info("收到键盘中断，正在关闭...")
    except Exception as e:
        logger.error(f"系统运行出错: {e}")


if __name__ == '__main__':
    # 检查Python版本
    if sys.version_info < (3, 8):
        logger.error("需要Python 3.8或更高版本")
        sys.exit(1)

    # 运行机器人
    main()
