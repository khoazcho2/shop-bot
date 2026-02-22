import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# =========================
# CẤU HÌNH
# =========================

TOKEN = "8462718923:AAEmsMjDI4Ih0IkKkcrnqaIXTIxNVEd68xs"
ADMIN_ID = 8337495954

# =========================
# MENU
# =========================

menu = [
    ["🛒 Mua Robux", "🎮 Mua Acc FF"],
    ["💳 Thanh toán", "📞 Admin"]
]

# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
✨ SHOP HỒ QUỐC ✨

🛒 Bán Robux Chính Hãng
🎮 Bán Acc Free Fire 120K

Chọn chức năng bên dưới 👇
"""

    await update.message.reply_text(
        text,
        reply_markup=ReplyKeyboardMarkup(menu, resize_keyboard=True)
    )

# =========================
# XỬ LÝ MENU
# =========================

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    msg = update.message.text
    user = update.message.from_user

    if msg == "🛒 Mua Robux":

        await update.message.reply_text(
            """
💰 BẢNG GIÁ ROBUX

120K = 400 Robux
240K = 800 Robux
500K = 1700 Robux

📩 Nhắn số lượng để mua
"""
        )

    elif msg == "🎮 Mua Acc FF":

        await update.message.reply_text(
            """
🎮 ACC FREE FIRE

💵 Giá: 120.000đ

📩 Nhắn "MUA ACC" để mua
"""
        )

    elif msg == "💳 Thanh toán":

        await update.message.reply_text(
            """
💳 THANH TOÁN

MB BANK
STK: 123456789
Tên: HO QUOC

📩 Sau khi chuyển gửi ảnh
"""
        )

    elif msg == "📞 Admin":

        await update.message.reply_text(
            "📞 Liên hệ: @username_admin"
        )

    else:

        await context.bot.send_message(

            chat_id=ADMIN_ID,

            text=f"""
📩 ĐƠN MỚI

👤 User: @{user.username}
🆔 ID: {user.id}

💬 Nội dung:
{msg}
"""
        )

        await update.message.reply_text(
            "✅ Đã gửi admin"
        )

# =========================
# MAIN
# =========================

def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(MessageHandler(filters.TEXT, message))

    print("Bot đang chạy...")

    app.run_polling()

# =========================

if __name__ == "__main__":
    main()
