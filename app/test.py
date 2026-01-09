#!/usr/bin/env python3
"""
测试脚本 - 用于测试各个组件功能
"""

import sys
import os
import asyncio

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from .config import *
from .database import DatabaseManager


def test_database():
    """测试数据库功能"""
    print("🗄️ 测试数据库功能...")

    db = DatabaseManager()

    # 测试创建用户
    user_id = 123456789
    success = db.create_user(
        telegram_id=user_id,
        username="test_user",
        first_name="Test",
        last_name="User"
    )
    print(f"创建用户: {'成功' if success else '失败'}")

    # 测试获取用户
    user = db.get_user(user_id)
    print(f"获取用户: {user is not None}")

    # 测试统计
    user_count = db.get_users_count()
    print(f"用户统计: 总{user_count}人")

    print("✅ 数据库测试完成\n")



def test_config():
    """测试配置"""
    print("⚙️ 测试配置...")

    required_configs = [
        ('TELEGRAM_BOT_TOKEN', TELEGRAM_BOT_TOKEN),
    ]

    optional_configs = [
        ('ALIPAY_QR_CODE', ALIPAY_QR_CODE),
        ('WECHAT_QR_CODE', WECHAT_QR_CODE),
        ('ALIPAY_RED_ENVELOPE_CODE', ALIPAY_RED_ENVELOPE_CODE),
        ('CUSTOMER_SERVICE_WECHAT', CUSTOMER_SERVICE_WECHAT),
    ]

    print("必须配置:")
    for name, value in required_configs:
        if value and value not in ['your_bot_token_here', '-1001234567890']:
            print(f"✅ {name}: 已配置")
        else:
            print(f"❌ {name}: 未配置或使用默认值")

    print("\n可选配置:")
    for name, value in optional_configs:
        if value:
            print(f"✅ {name}: {value}")
        else:
            print(f"⚠️ {name}: 未配置")

    print("✅ 配置测试完成\n")


async def main():
    """主测试函数"""
    print("🧪 开始运行Telegram客服机器人测试...\n")

    # 基本配置测试
    test_config()

    # 数据库测试
    test_database()

    print("🎉 所有测试完成！")
    print("\n💡 提示:")
    print("- 请确保所有配置都已正确设置")
    print("- 准备好支付宝和微信二维码图片")
    print("- 运行机器人前请检查网络连接")
    print("- 如有问题，请查看日志文件")


if __name__ == '__main__':
    asyncio.run(main())
