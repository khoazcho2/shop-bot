import os
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

# =========================
# CONFIG
# =========================

TOKEN = os.getenv("8462718923:AAEaghAn9KqEgvu-uUJJXMK0G51YZgk1Y1U")
ADMIN_ID = int(os.getenv("8337495954"))

waiting_ff = {}
waiting_robux = {}
waiting_username = {}

last_payment_time = {}

SPAM_TIME = 600  # 10 phút


# =========================
# WEB SERVER chống sleep Railway
# =========================

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"BOT VIP ONLINE")


def run_web():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()


threading.Thread(target=run_web).start()


# =========================
# START
# =========================

def start(update, context):

    keyboard = [
        ["🎮 ACC FREE FIRE"],
        ["💎 ROBUX 120H"]
    ]

    update.message.reply_text(
        "🔥 SHOP HỒ QUỐC VIP 🔥",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )


# =========================
# MENU ACC
# =========================

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


# =========================
# CHỌN ACC
# =========================

def chon_acc(update, context):

    gia = update.message.text.replace("💰 ACC ", "").replace("K","")

    user_id = update.message.chat_id

    waiting_ff[user_id] = gia

    context.bot.send_photo(
        user_id,
        photo=open("qr.jpg","rb"),
        caption="Chuyển khoản rồi bấm ĐÃ THANH TOÁN"
    )

    update.message.reply_text(
        "Sau khi chuyển bấm:",
        reply_markup=ReplyKeyboardMarkup(
            [["✅ ĐÃ THANH TOÁN"]],
            resize_keyboard=True
        )
    )


# =========================
# MENU ROBUX
# =========================

def menu_robux(update, context):

    keyboard = [
        ["💰 50K"],
        ["💰 100K"],
        ["💰 200K"],
        ["💰 500K"],
        ["💰 1M"],
        ["⬅️ BACK"]
    ]

    update.message.reply_text(
"""💎 ROBUX 120H

50K = 150
100K = 300
200K = 600
500K = 1500
1M = 3000
""",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )


# =========================
# CHỌN ROBUX
# =========================

def chon_robux(update, context):

    gia = update.message.text.replace("💰 ","")

    user_id = update.message.chat_id

    waiting_robux[user_id] = gia

    context.bot.send_photo(
        user_id,
        photo=open("qr.jpg","rb"),
        caption="Chuyển khoản rồi bấm ĐÃ THANH TOÁN"
    )

    update.message.reply_text(
        "Sau khi chuyển bấm:",
        reply_markup=ReplyKeyboardMarkup(
            [["✅ ĐÃ THANH TOÁN"]],
            resize_keyboard=True
        )
    )


# =========================
# THANH TOÁN
# =========================

def thanhtoan(update, context):

    user_id = update.message.chat_id

    now = time.time()

    if user_id in last_payment_time:

        if now - last_payment_time[user_id] < SPAM_TIME:

            update.message.reply_text(
                "❌ Bạn đã bấm rồi. Vui lòng chờ 10 phút"
            )
            return

    last_payment_time[user_id] = now

    user = update.message.from_user


    # ACC

    if user_id in waiting_ff:

        gia = waiting_ff[user_id]

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "DUYỆT ACC",
                    callback_data=f"duyet_acc|{user_id}|{gia}"
                )
            ]
        ])

        context.bot.send_message(
            ADMIN_ID,
            f"""
KHÁCH MUA ACC

User: @{user.username}
ID: {user_id}

Gói: {gia}K
""",
            reply_markup=keyboard
        )

        update.message.reply_text("Chờ admin duyệt")


    # ROBUX

    elif user_id in waiting_robux:

        waiting_username[user_id] = True

        update.message.reply_text("Nhập USERNAME ROBLOX:")


# =========================
# NHẬP USERNAME ROBLOX
# =========================

def username(update, context):

    user_id = update.message.chat_id

    if user_id not in waiting_username:
        return

    name = update.message.text

    gia = waiting_robux[user_id]

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "DUYỆT ROBUX",
                callback_data=f"duyet_robux|{user_id}|{gia}|{name}"
            )
        ]
    ])

    context.bot.send_message(
        ADMIN_ID,
        f"""
KHÁCH MUA ROBUX

Username: {name}

Gói: {gia}
""",
        reply_markup=keyboard
    )

    update.message.reply_text("Chờ admin duyệt")

    del waiting_username[user_id]


# =========================
# ADMIN DUYỆT
# =========================

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
            f"ACC CỦA BẠN:\n\n{acc}"
        )


        query.edit_message_text("ĐÃ DUYỆT ACC")



    # DUYỆT ROBUX

    elif data[0] == "duyet_robux":

        user_id = int(data[1])

        gia = data[2]

        username = data[3]


        context.bot.send_message(
            user_id,
            f"""
✅ ROBUX ĐÃ DUYỆT

Username: {username}

Sẽ nhận trong 120h
"""
        )


        query.edit_message_text("ĐÃ DUYỆT ROBUX")



# =========================
# MAIN
# =========================

def main():

    updater = Updater(TOKEN)

    dp = updater.dispatcher


    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(MessageHandler(Filters.regex("ACC FREE FIRE"), menu_ff))

    dp.add_handler(MessageHandler(Filters.regex("ROBUX"), menu_robux))

    dp.add_handler(MessageHandler(Filters.regex("^💰 ACC"), chon_acc))

    dp.add_handler(MessageHandler(Filters.regex("^💰"), chon_robux))

    dp.add_handler(MessageHandler(Filters.regex("ĐÃ THANH TOÁN"), thanhtoan))

    dp.add_handler(MessageHandler(Filters.text, username))

    dp.add_handler(CallbackQueryHandler(callback))


    updater.start_polling()

    print("BOT VIP ONLINE 24/24")

    updater.idle()


main()

