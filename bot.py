import os
from telegram import *
from telegram.ext import *

TOKEN = "8462718923:AAFVPS1q92tr16czaextWLanU2HsPgZUPaQ"
ADMIN_ID = 8337495954  # ← ID TELEGRAM CỦA BẠN

waiting = {}

# =================
# START
# =================

def start(update, context):

    keyboard = [
        ["🎮 ACC FREE FIRE"]
    ]

    update.message.reply_text(
        "🔥 SHOP HỒ QUỐC 🔥",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# =================
# MENU ACC
# =================

def menu(update, context):

    keyboard = [
        ["💰 ACC 120K"],
        ["💰 ACC 200K"],
        ["⬅️ BACK"]
    ]

    update.message.reply_text(
        "Chọn acc:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# =================
# KHÁCH CHỌN ACC
# =================

def chon_acc(update, context):

    gia = update.message.text.replace("💰 ACC ","").replace("K","")

    user_id = update.message.chat_id

    waiting[user_id] = gia

    context.bot.send_photo(
        user_id,
        photo=open("qr.jpg","rb"),
        caption="Chuyển khoản rồi bấm ĐÃ THANH TOÁN"
    )

    keyboard = [["✅ ĐÃ THANH TOÁN"]]

    update.message.reply_text(
        "Bấm nút sau khi chuyển:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# =================
# KHÁCH BẤM THANH TOÁN
# =================

def thanhtoan(update, context):

    user = update.message.from_user
    user_id = update.message.chat_id

    if user_id not in waiting:
        return

    gia = waiting[user_id]

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "✅ DUYỆT",
                callback_data=f"duyet|{user_id}|{gia}"
            ),
            InlineKeyboardButton(
                "❌ HỦY",
                callback_data=f"huy|{user_id}"
            )
        ]
    ])

    context.bot.send_message(
        ADMIN_ID,
        f"""
KHÁCH ĐÃ THANH TOÁN

User: @{user.username}
ID: {user_id}
Gói: {gia}K
""",
        reply_markup=keyboard
    )

    update.message.reply_text(
        "⏳ Chờ admin xác nhận..."
    )

# =================
# ADMIN DUYỆT
# =================

def callback(update, context):

    query = update.callback_query
    data = query.data.split("|")

    if data[0] == "duyet":

        user_id = int(data[1])
        gia = data[2]

        file = f"acc_ff/{gia}.txt"

        if not os.path.exists(file):

            context.bot.send_message(user_id,"Hết acc")
            return

        with open(file,"r") as f:

            accs = f.readlines()

        if len(accs) == 0:

            context.bot.send_message(user_id,"Hết acc")
            return

        acc = accs[0]

        with open(file,"w") as f:

            f.writelines(accs[1:])

        context.bot.send_message(
            user_id,
            f"""
✅ THANH TOÁN THÀNH CÔNG

ACC CỦA BẠN:

{acc}
"""
        )

        query.edit_message_text("ĐÃ DUYỆT")

    elif data[0] == "huy":

        user_id = int(data[1])

        context.bot.send_message(
            user_id,
            "❌ Thanh toán bị từ chối"
        )

        query.edit_message_text("ĐÃ HỦY")

# =================
# MAIN
# =================

def main():

    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(MessageHandler(Filters.regex("ACC FREE FIRE"), menu))

    dp.add_handler(MessageHandler(Filters.regex("ACC"), chon_acc))

    dp.add_handler(MessageHandler(Filters.regex("ĐÃ THANH TOÁN"), thanhtoan))

    dp.add_handler(CallbackQueryHandler(callback))

    updater.start_polling()

    print("BOT ĐANG CHẠY")

    updater.idle()

main()
