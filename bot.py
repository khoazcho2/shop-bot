import os
from telegram import *
from telegram.ext import *
from flask import Flask
from threading import Thread

# =========================
# CẤU HÌNH
# =========================

TOKEN = "8462718923:AAFVPS1q92tr16czaextWLanU2HsPgZUPaQ"
ADMIN_ID = 8337495954

# =========================
# KEEP ALIVE RENDER
# =========================

app = Flask(__name__)

@app.route('/')
def home():
    return "BOT HO QUOC ONLINE"

def run_web():
    app.run(host="0.0.0.0", port=10000)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# =========================
# DATA
# =========================

waiting_ff = {}

# =========================
# START
# =========================

def start(update, context):

    keyboard = [
        ["🎮 ACC FREE FIRE"],
        ["💎 MUA ROBUX"]
    ]

    update.message.reply_text(

        "🔥 SHOP HỒ QUỐC 🔥\n\nChọn dịch vụ:",

        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )
    )

# =========================
# MENU FREE FIRE
# =========================

def menu_ff(update, context):

    keyboard = [

        ["💰 ACC 120K"],
        ["💰 ACC 200K"],
        ["💰 ACC 300K"],
        ["💰 ACC 500K"]

    ]

    update.message.reply_text(

        "Chọn acc:",

        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )
    )

# =========================
# CHỌN ACC
# =========================

def chon_acc(update, context):

    gia = update.message.text.replace(
        "💰 ACC ", ""
    ).replace("K", "")

    waiting_ff[update.message.chat_id] = gia

    context.bot.send_photo(

        update.message.chat_id,

        photo=open("qr.jpg", "rb"),

        caption=f"""
ACC FF {gia}K

Chuyển khoản rồi bấm:
"""
    )

    keyboard = [["✅ ĐÃ THANH TOÁN"]]

    update.message.reply_text(

        "Sau khi chuyển khoản bấm:",

        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )
    )

# =========================
# KHÁCH BẤM THANH TOÁN
# =========================

def da_thanhtoan(update, context):

    user = update.message.from_user

    user_id = update.message.chat_id

    if user_id not in waiting_ff:
        return

    gia = waiting_ff[user_id]

    keyboard = InlineKeyboardMarkup([

        [

            InlineKeyboardButton(

                "✅ DUYỆT",

                callback_data=f"duyet|{user_id}|{gia}"
            ),

            InlineKeyboardButton(

                "❌ HỦY",

                callback_data="huy"
            )

        ]

    ])

    context.bot.send_message(

        ADMIN_ID,

        f"""
KHÁCH MUA ACC

User: @{user.username}

Gói: {gia}K
""",

        reply_markup=keyboard

    )

    update.message.reply_text(

        "Đã gửi admin xác nhận"
    )

# =========================
# ADMIN DUYỆT
# =========================

def duyet(update, context):

    query = update.callback_query

    data = query.data.split("|")

    user_id = int(data[1])

    gia = data[2]

    file = f"acc_ff/{gia}.txt"

    if not os.path.exists(file):

        context.bot.send_message(
            user_id,
            "Hết acc"
        )

        return

    with open(file, "r", encoding="utf-8") as f:

        accs = f.readlines()

    if len(accs) == 0:

        context.bot.send_message(
            user_id,
            "Hết acc"
        )

        return

    acc = accs[0]

    with open(file, "w", encoding="utf-8") as f:

        f.writelines(accs[1:])

    context.bot.send_message(

        user_id,

        f"""
THANH TOÁN THÀNH CÔNG

ACC CỦA BẠN:

{acc}
"""
    )

    query.edit_message_text(
        "ĐÃ DUYỆT"
    )

# =========================
# MENU ROBUX
# =========================

def robux(update, context):

    keyboard = [

        ["50K"],
        ["100K"],
        ["500K"]

    ]

    update.message.reply_text(

"""
BẢNG GIÁ ROBUX

50K = 150
100K = 300
500K = 1500
""",

        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )
    )

# =========================
# MAIN
# =========================

def main():

    updater = Updater(
        TOKEN,
        use_context=True
    )

    dp = updater.dispatcher

    dp.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    dp.add_handler(
        MessageHandler(
            Filters.regex("ACC FREE FIRE"),
            menu_ff
        )
    )

    dp.add_handler(
        MessageHandler(
            Filters.regex("ACC"),
            chon_acc
        )
    )

    dp.add_handler(
        MessageHandler(
            Filters.regex("ĐÃ THANH TOÁN"),
            da_thanhtoan
        )
    )

    dp.add_handler(
        MessageHandler(
            Filters.regex("ROBUX"),
            robux
        )
    )

    dp.add_handler(
        CallbackQueryHandler(
            duyet,
            pattern="duyet"
        )
    )

    updater.start_polling()

    print("BOT ĐANG CHẠY 24/24...")

    updater.idle()

# =========================
# RUN
# =========================

keep_alive()

main()