import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from .config import (
    TELEGRAM_BOT_TOKEN, ALIPAY_QR_CODE, WECHAT_QR_CODE
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class CustomerServiceBot:
    def __init__(self):
        self.updater = None
        self.dispatcher = None
        self.initialized = False
        self._init_bot()

    def _init_bot(self):
        try:
            from telegram import Bot
            bot = Bot(token=TELEGRAM_BOT_TOKEN)
            self.updater = Updater(bot=bot)
            self.dispatcher = self.updater.dispatcher
            self._register_handlers()
            self.initialized = True
            logger.info("机器人初始化成功")
        except Exception as e:
            logger.warning(f"机器人初始化失败: {e}")
            self.updater = None
            self.dispatcher = None
            self.initialized = False

    def _register_handlers(self):
        if not self.dispatcher:
            return
        self.dispatcher.add_handler(CommandHandler("start", self.start_command))
        self.dispatcher.add_handler(CallbackQueryHandler(self.handle_callback))

    def start_command(self, update, context):
        keyboard = [
            [InlineKeyboardButton("💚 支付宝", callback_data="payment_alipay")],
            [InlineKeyboardButton("💙 微信", callback_data="payment_wechat")],
            [InlineKeyboardButton("🧧 口令红包", callback_data="red_envelope_guide")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        message_text = """本频道148元终身会员 每日更新 一次付费所有更新内容永久免费阅读

本频道支持 支付宝/微信扫码，支付宝红包口令三种方式

请您选择其中一种付款方式，点击进入，查看具体付款方式完成付款

如有问题请联系 @Landisliu
如不能及时回复，请加店主微信 xymh0923"""

        update.message.reply_text(message_text, reply_markup=reply_markup)



    def handle_callback(self, update, context):
        query = update.callback_query
        query.answer()
        data = query.data
        if data == "payment_alipay":
            self.send_alipay_qr(query)
        elif data == "payment_wechat":
            self.send_wechat_qr(query)
        elif data == "red_envelope_guide":
            self.send_red_envelope_guide(query)
        elif data == "back_to_payment":
            self.back_to_payment_selection(query)

    def send_alipay_qr(self, query):
        try:
            with open(ALIPAY_QR_CODE, 'rb') as photo:
                query.message.reply_photo(
                    photo=photo,
                    caption="💚 支付宝支付二维码\n\n请使用支付宝扫码完成支付",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("⬅️ 返回", callback_data="back_to_payment")]
                    ])
                )
        except FileNotFoundError:
            query.message.reply_text(
                "❌ 支付宝二维码图片未找到，请联系客服获取支付信息。",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("⬅️ 返回", callback_data="back_to_payment")]
                ])
            )

    def send_wechat_qr(self, query):
        try:
            with open(WECHAT_QR_CODE, 'rb') as photo:
                query.message.reply_photo(
                    photo=photo,
                    caption="💙 微信支付二维码\n\n请使用微信扫码完成支付",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("⬅️ 返回", callback_data="back_to_payment")]
                    ])
                )
        except FileNotFoundError:
            query.message.reply_text(
                "❌ 微信二维码图片未找到，请联系客服获取支付信息。",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("⬅️ 返回", callback_data="back_to_payment")]
                ])
            )

    def send_red_envelope_guide(self, query):
        guide_text = """🧧 支付宝口令红包创建方法

📱 创建步骤：
1. 打开支付宝App
2. 点击"蚂蚁森林"或"收钱"
3. 选择"口令红包"
4. 设置金额和口令文字
5. 生成口令链接
6. 复制口令文字分享给用户

💡 口令文字示例：
"恭喜发财，大吉大利"
"谢谢惠顾，祝您好运"
"支付宝到账100元"

⚠️ 注意事项：
• 口令要简洁明了
• 确保红包金额正确
• 及时发送给用户"""
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ 返回", callback_data="back_to_payment")]
        ])
        query.message.reply_text(guide_text, reply_markup=reply_markup)

    def back_to_payment_selection(self, query):
        keyboard = [
            [InlineKeyboardButton("💚 支付宝", callback_data="payment_alipay")],
            [InlineKeyboardButton("💙 微信", callback_data="payment_wechat")],
            [InlineKeyboardButton("🧧 口令红包", callback_data="red_envelope_guide")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        message_text = """本频道148元终身会员 每日更新 一次付费所有更新内容永久免费阅读

本频道支持 支付宝/微信扫码，支付宝红包口令三种方式

请您选择其中一种付款方式，点击进入，查看具体付款方式完成付款

💡 完成付款后，您的申请将自动提交给管理员审核
✅ 审核通过后，您将收到群组邀请链接

如有问题请联系 @Landisliu
如不能及时回复，请加店主微信 xymh0923"""

        query.message.reply_text(message_text, reply_markup=reply_markup)

    def run(self):
        if not self.initialized or not self.updater:
            logger.error("机器人未初始化，无法运行")
            return
        logger.info("启动Telegram客服机器人...")
        self.updater.start_polling()
        self.updater.idle()