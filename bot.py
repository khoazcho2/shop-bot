import os
import time
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

TOKEN = os.getenv("8462718923:AAFVPS1q92tr16czaextWLanU2HsPgZUPaQ")
ADMIN_ID = int(os.getenv("8337495954"))

waiting_ff = {}
waiting_robux = {}
waiting_username = {}

last_payment_time = {}
cooldown = 600


# ========= START =========

def start(update, context):

    keyboard = [
        ["🎮 ACC FREE FIRE"],
        ["💎 ROBUX 120H"]
    ]

    update.message.reply_text(
        "🏛 SHOP HỒ QUỐC 🏧\n\nChọn dịch vụ:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )


# ========= MENU ACC =========

def menu_ff(update, context):

    keyboard = [
        ["💰 ACC 120K"],
        ["💰 ACC 200K"],
        ["⬅️ BACK"]
    ]

    update.message.reply_text(
        "Chọn ACC:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )


# ========= CHỌN ACC =========

def chon_acc(update, context):

    gia = update.message.text.replace("💰 ACC ","").replace("K","")

    user_id = update.message.chat_id

    waiting_ff[user_id] = gia

    context.bot.send_photo(
        user_id,
        photo=open("qr.jpg","rb"),
        caption=f"ACC {gia}K\n\nChuyển khoản rồi bấm ĐÃ THANH TOÁN"
    )

    update.message.reply_text(
        "Sau khi chuyển bấm:",
        reply_markup=ReplyKeyboardMarkup(
            [["✅ ĐÃ THANH TOÁN"]],
            resize_keyboard=True
        )
    )


# ========= MENU ROBUX =========

def menu_robux(update, context):

    keyboard = [
        ["💰 50K = 150 ROBUX"],
        ["💰 100K = 300 ROBUX"],
        ["💰 150K = 450 ROBUX"],
        ["💰 500K = 1500 ROBUX"],
        ["💰 1M = 3000 ROBUX"],
        ["⬅️ BACK"]
    ]

    update.message.reply_text(
"""💎 ROBUX 120H

50K = 150
100K = 300
150K = 450
500K = 1500
1M = 3000
""",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )


# ========= CHỌN ROBUX =========

def chon_robux(update, context):

    text = update.message.text

    gia = text.split("=")[0].replace("💰","").strip()

    user_id = update.message.chat_id

    waiting_robux[user_id] = gia

    context.bot.send_photo(
        user_id,
        photo=open("qr.jpg","rb"),
        caption=f"ROBUX {gia}\n\nChuyển khoản rồi bấm ĐÃ THANH TOÁN"
    )

    update.message.reply_text(
        "Sau khi chuyển bấm:",
        reply_markup=ReplyKeyboardMarkup(
            [["✅ ĐÃ THANH TOÁN"]],
            resize_keyboard=True
        )
    )


# ========= THANH TOÁN =========

def thanhtoan(update, context):

    user_id = update.message.chat_id
    user = update.message.from_user

    now = time.time()

    if user_id in last_payment_time:

        remaining = cooldown - (now - last_payment_time[user_id])

        if remaining > 0:

            update.message.reply_text(
                f"❌ Chống spam\nChờ {int(remaining//60)} phút"
            )
            return

    last_payment_time[user_id] = now


    # ACC

    if user_id in waiting_ff:

        gia = waiting_ff[user_id]

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(
                "DUYỆT ACC",
                callback_data=f"duyet_acc|{user_id}|{gia}"
            )]
        ])

        context.bot.send_message(
            ADMIN_ID,
            f"KHÁCH MUA ACC\n@{user.username}\nGói {gia}K",
            reply_markup=keyboard
        )

        update.message.reply_text("Chờ admin duyệt")


    # ROBUX

    elif user_id in waiting_robux:

        waiting_username[user_id] = True

        update.message.reply_text("Nhập USERNAME ROBLOX:")


# ========= USERNAME ROBUX =========

def username(update, context):

    user_id = update.message.chat_id

    if user_id not in waiting_username:
        return

    name = update.message.text

    gia = waiting_robux[user_id]

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            "DUYỆT ROBUX",
            callback_data=f"duyet_robux|{user_id}|{gia}|{name}"
        )]
    ])

    context.bot.send_message(
        ADMIN_ID,
        f"MUA ROBUX\nUsername: {name}\nGói: {gia}",
        reply_markup=keyboard
    )

    update.message.reply_text("Chờ admin duyệt")

    del waiting_username[user_id]


# ========= CALLBACK =========

def callback(update, context):

    query = update.callback_query

    data = query.data.split("|")


    # DUYỆT ACC

    if data[0] == "duyet_acc":

        user_id = int(data[1])
        gia = data[2]

        file = f"acc_ff/{gia}.txt"

        if not os.path.exists(file):

            context.bot.send_message(user_id,"Hết acc")
            return

        with open(file) as f:
            accs = f.readlines()

        acc = accs[0]

        with open(file,"w") as f:
            f.writelines(accs[1:])

        context.bot.send_message(user_id,f"ACC:\n{acc}")

        query.edit_message_text("Đã duyệt ACC")


    # DUYỆT ROBUX

    elif data[0] == "duyet_robux":

        user_id = int(data[1])
        gia = data[2]
        name = data[3]

        context.bot.send_message(
            user_id,
            f"ROBUX ĐÃ DUYỆT\nUsername: {name}\nGói: {gia}"
        )

        query.edit_message_text("Đã duyệt ROBUX")


# ========= MAIN =========

def main():

    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(MessageHandler(Filters.regex("ACC FREE FIRE"), menu_ff))

    dp.add_handler(MessageHandler(Filters.regex("ROBUX"), menu_robux))

    dp.add_handler(MessageHandler(Filters.regex("^💰 ACC"), chon_acc))

    dp.add_handler(MessageHandler(Filters.regex(r"^\💰.*ROBUX"), chon_robux))

    dp.add_handler(MessageHandler(Filters.regex("ĐÃ THANH TOÁN"), thanhtoan))

    dp.add_handler(MessageHandler(Filters.text, username))

    dp.add_handler(CallbackQueryHandler(callback))

    updater.start_polling()

    print("BOT ONLINE")

    updater.idle()


main()

