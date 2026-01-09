#!/bin/bash

echo "🤖 Telegram客服机器人环境配置助手"
echo "=================================="
echo ""

# 检查.env文件是否存在
if [ -f ".env" ]; then
    echo "⚠️  .env文件已存在。如需重新配置，请先备份并删除现有文件。"
    read -p "是否继续？(y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "配置取消。"
        exit 1
    fi
fi

echo "📝 请按提示输入配置信息："
echo ""

# Telegram Bot Token
read -p "🤖 请输入Telegram机器人Token: " TELEGRAM_BOT_TOKEN
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "❌ 机器人Token不能为空！"
    exit 1
fi

# 群组ID
read -p "👥 请输入私密群组ID (格式: -100xxxxxxxxxx): " PRIVATE_GROUP_ID
if [ -z "$PRIVATE_GROUP_ID" ]; then
    echo "❌ 群组ID不能为空！"
    exit 1
fi

# 超级管理员ID
read -p "👑 请输入你的Telegram用户ID (超级管理员): " SUPER_ADMIN_IDS
if [ -z "$SUPER_ADMIN_IDS" ]; then
    echo "❌ 超级管理员ID不能为空！"
    exit 1
fi

# 客服微信
read -p "💬 请输入客服微信号 (默认: xymh0923): " CUSTOMER_SERVICE_WECHAT
CUSTOMER_SERVICE_WECHAT=${CUSTOMER_SERVICE_WECHAT:-xymh0923}

# 支付宝口令
read -p "🧧 请输入支付宝口令红包文字 (默认: 恭喜发财，大吉大利): " ALIPAY_RED_ENVELOPE_CODE
ALIPAY_RED_ENVELOPE_CODE=${ALIPAY_RED_ENVELOPE_CODE:-"恭喜发财，大吉大利"}

# 监控间隔
read -p "⏱️  请输入群组监控间隔(秒) (默认: 30): " MONITOR_INTERVAL
MONITOR_INTERVAL=${MONITOR_INTERVAL:-30}

# 创建.env文件
cat > .env << EOF
# Telegram Bot 配置
TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN

# Telegram群组配置
PRIVATE_GROUP_ID=$PRIVATE_GROUP_ID

# 超级管理员ID列表
SUPER_ADMIN_IDS=$SUPER_ADMIN_IDS

# 支付配置
ALIPAY_QR_CODE=alipay_qr.png
WECHAT_QR_CODE=wechat_qr.png
ALIPAY_RED_ENVELOPE_CODE=$ALIPAY_RED_ENVELOPE_CODE

# 客服联系方式
CUSTOMER_SERVICE_WECHAT=$CUSTOMER_SERVICE_WECHAT

# 监控间隔（秒）
MONITOR_INTERVAL=$MONITOR_INTERVAL
EOF

echo ""
echo "✅ 环境配置完成！"
echo "📁 已创建 .env 配置文件"
echo ""
echo "🔧 接下来步骤："
echo "1. 确保机器人是群组管理员"
echo "2. 设置群组为私密群组"
echo "3. 运行机器人：python main.py"
echo ""
echo "📚 Telegram群组设置教程："
echo "• 群组设置 → 权限 → 批准新成员"
echo "• 机器人需要管理员权限才能踢出成员"
