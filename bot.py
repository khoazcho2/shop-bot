import os
import time
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

TOKEN = "8462718923:AAEaghAn9KqEgvu-uUJJXMK0G51YZgk1YIU"
ADMIN_ID = 8337495954

cooldown = {}
waiting = {}

COOLDOWN = 600


# ===== START =====

def start(update: Update, context: CallbackContext):

    keyboard = [

        [InlineKeyboardButton("🎮 Acc Free Fire 120K", callback_data="ff120")],

        [InlineKeyboardButton("💎 Robux 120H", callback_data="robux")],

    ]

    update.message.reply_text(

        "🔥 SHOP HỒ QUỐC 🔥",

        reply_markup=InlineKeyboardMarkup(keyboard)

    )


# ===== BUTTON =====

def button(update: Update, context: CallbackContext):

    query = update.callback_query
    query.answer()

    user = query.from_user


# ===== ACC FF =====

    if query.data == "ff120":

        send_qr(query, context, "ACC FREE FIRE 120K")


# ===== MENU ROBUX =====

    elif query.data == "robux":

        keyboard = [

            [InlineKeyboardButton("50K = 150 Robux", callback_data="rb50")],

            [InlineKeyboardButton("100K = 300 Robux", callback_data="rb100")],

            [InlineKeyboardButton("200K = 600 Robux", callback_data="rb200")],

            [InlineKeyboardButton("500K = 1500 Robux", callback_data="rb500")],

            [InlineKeyboardButton("1M = 3000 Robux", callback_data="rb1m")],

        ]

        query.message.reply_text(

            "💎 ROBUX 120H (ĐÃ THUẾ)",

            reply_markup=InlineKeyboardMarkup(keyboard)

        )


# ===== ROBUX OPTIONS =====

    elif query.data == "rb50":

        send_qr(query, context, "150 ROBUX (50K)")


    elif query.data == "rb100":

        send_qr(query, context, "300 ROBUX (100K)")


    elif query.data == "rb200":

        send_qr(query, context, "600 ROBUX (200K)")


    elif query.data == "rb500":

        send_qr(query, context, "1500 ROBUX (500K)")


    elif query.data == "rb1m":

        send_qr(query, context, "3000 ROBUX (1M)")


# ===== PAID =====

    elif query.data == "paid":

        now = time.time()

        if user.id in cooldown and now - cooldown[user.id] < COOLDOWN:

            query.message.reply_text("⛔ Chờ 10 phút rồi thử lại")
            return


        cooldown[user.id] = now
        waiting[user.id] = True


        query.message.reply_text(

            "✅ Đã gửi\n⏳ Chờ admin duyệt"

        )


        keyboard = [

            [InlineKeyboardButton("DUYỆT", callback_data=f"approve_{user.id}")]

        ]


        context.bot.send_message(

            ADMIN_ID,

            f"""

KHÁCH ĐÃ THANH TOÁN

User: @{user.username}

ID: {user.id}

""",

            reply_markup=InlineKeyboardMarkup(keyboard)

        )


# ===== ADMIN DUYỆT =====

    elif query.data.startswith("approve_"):

        if query.from_user.id != ADMIN_ID:
            return


        uid = int(query.data.split("_")[1])


        if uid in waiting:

            context.bot.send_message(

                uid,

                "🎉 Đã duyệt thành công\nRobux sẽ vào sau 120H"

            )

            del waiting[uid]

            query.message.reply_text("ĐÃ DUYỆT")


# ===== SEND QR =====

def send_qr(query, context, text):

    keyboard = [

        [InlineKeyboardButton("✅ Đã thanh toán", callback_data="paid")]

    ]

    context.bot.send_photo(

        query.message.chat_id,

        photo=open("qr.jpg", "rb"),

        caption=text,

        reply_markup=InlineKeyboardMarkup(keyboard)

    )


# ===== MAIN =====

def main():

    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()

    updater.idle()


main()


