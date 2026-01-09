"""
配置文件 - 使用环境变量
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# Telegram Bot 配置
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'your_bot_token_here')

# 数据库配置
DATABASE_PATH = 'customer_service_bot.db'

# 支付指导配置
ALIPAY_QR_CODE = os.getenv('ALIPAY_QR_CODE', 'alipay_qr.png')  # 支付宝二维码图片路径
WECHAT_QR_CODE = os.getenv('WECHAT_QR_CODE', 'wechat_qr.png')  # 微信二维码图片路径
ALIPAY_RED_ENVELOPE_CODE = os.getenv('ALIPAY_RED_ENVELOPE_CODE', '你的支付宝口令红包代码')  # 支付宝口令红包

# 客服联系方式
CUSTOMER_SERVICE_WECHAT = os.getenv('CUSTOMER_SERVICE_WECHAT', 'xymh0923')  # 店主微信

# 欢迎信息
WELCOME_MESSAGE = """🎉 欢迎使用客服机器人！

💰 我们提供便捷的支付服务
💳 支持支付宝、微信等多种支付方式
📱 如有问题请及时联系客服

请点击下方按钮选择您需要的服务"""

# 支付指导信息
PAYMENT_GUIDE_MESSAGE = """💰 付款指导

请选择您的支付方式：

• 💚 支付宝 - 支持扫码支付和口令红包
• 💙 微信支付 - 支持扫码支付
• 💬 联系客服 - 如有问题请及时联系

📞 客服微信：{CUSTOMER_SERVICE_WECHAT}"""

# 支付宝支付说明
ALIPAY_GUIDE_MESSAGE = """💚 支付宝支付指导

📱 方法1：扫码支付
点击下方二维码图片，使用支付宝扫码付款

🧧 方法2：口令红包
复制下方口令，在支付宝搜索使用：
`{ALIPAY_RED_ENVELOPE_CODE}`

⚠️ 注意事项：
• 请在有效时间内完成支付
• 支付成功后请截图保存凭证
• 如遇问题请联系客服微信：{CUSTOMER_SERVICE_WECHAT}"""

# 微信支付说明
WECHAT_GUIDE_MESSAGE = """💙 微信支付指导

📱 扫码支付
点击下方二维码图片，使用微信扫码付款

⚠️ 注意事项：
• 请在有效时间内完成支付
• 支付成功后请截图保存凭证
• 如遇问题请联系客服微信：{CUSTOMER_SERVICE_WECHAT}"""

# 管理员帮助信息
ADMIN_HELP_MESSAGE = """
🔧 管理员命令帮助

基本命令：
/admin - 显示管理员面板
/help - 显示此帮助信息

用户管理：
/addadmin <用户ID> - 添加管理员
/removeadmin <用户ID> - 移除管理员
/listadmins - 列出所有管理员
/stats - 显示系统统计

注意：只有超级管理员才能添加/移除管理员。
"""

# 权限类型
PERMISSION_TYPES = {
    'member': '普通用户',
    'admin': '管理员',
    'super_admin': '超级管理员'
}
