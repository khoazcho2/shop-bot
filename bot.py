import os
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
import os

TOKEN = os.getenv("8462718923:AAEmsMjDI4Ih0IkKkcrnqaIXTIxNVEd68xs")

ADMIN_ID = int(os.getenv("8337495954"))


QR = "https://i.imgur.com/yourQR.png"

# lưu trạng thái
waiting_ff = set()
waiting_robux = {}
waiting_name = {}

# =====================
# LOAD ACC FF
# =====================

def load_ff():

    if not os.path.exists("ff.txt"):
        return []

    with open("ff.txt","r",encoding="utf8") as f:
        return f.read().splitlines()


def save_ff(acc):

    with open("ff.txt","w",encoding="utf8") as f:
        f.write("\n".join(acc))


# =====================
# START
# =====================

async def start(update: Update, context):

    keyboard = ReplyKeyboardMarkup(

        [
            ["🔥 ACC FREE FIRE 120K"],
            ["🪙 MUA ROBUX"]
        ],

        resize_keyboard=True

    )

    await update.message.reply_text(

        "✨ SHOP HỒ QUỐC ✨\n\nChọn sản phẩm:",

        reply_markup=keyboard

    )


# =====================
# MENU FF
# =====================

async def freefire(update, context):

    keyboard = InlineKeyboardMarkup([

        [InlineKeyboardButton("💳 THANH TOÁN", callback_data="pay_ff")]

    ])

    await update.message.reply_text(

        "🔥 ACC FREE FIRE\n💰 Giá: 120K",

        reply_markup=keyboard

    )


# =====================
# MENU ROBUX
# =====================

async def robux(update, context):

    keyboard = InlineKeyboardMarkup([

        [InlineKeyboardButton("💎 150 Robux — 50K", callback_data="rb_150")],

        [InlineKeyboardButton("💎 300 Robux — 100K", callback_data="rb_300")],

        [InlineKeyboardButton("💎 600 Robux — 200K", callback_data="rb_600")],

        [InlineKeyboardButton("💎 1200 Robux — 400K", callback_data="rb_1200")],

        [InlineKeyboardButton("💎 1500 Robux — 500K", callback_data="rb_1500")]

    ])

    await update.message.reply_text(

        "🪙 CHỌN GÓI ROBUX:",

        reply_markup=keyboard

    )


# =====================
# BUTTON
# =====================

async def button(update, context):

    query = update.callback_query

    await query.answer()

    user = query.from_user


# =====================
# PAY FF
# =====================

    if query.data == "pay_ff":

        waiting_ff.add(user.id)

        keyboard = InlineKeyboardMarkup([

            [InlineKeyboardButton("✅ ĐÃ THANH TOÁN", callback_data="done_ff")]

        ])

        await context.bot.send_photo(

            user.id,

            QR,

            caption="💳 Quét QR rồi bấm nút dưới",

            reply_markup=keyboard

        )


# =====================
# DONE FF
# =====================

    elif query.data == "done_ff":

        if user.id not in waiting_ff:
            return


        keyboard = InlineKeyboardMarkup([

            [

                InlineKeyboardButton("✅ DUYỆT", callback_data=f"ok_ff_{user.id}"),

                InlineKeyboardButton("❌ HỦY", callback_data=f"no_ff_{user.id}")

            ]

        ])


        await context.bot.send_message(

            ADMIN_ID,

            f"""

🔥 ĐƠN FREE FIRE

👤 @{user.username}

🆔 {user.id}

""",

            reply_markup=keyboard

        )


        await query.edit_message_caption("⏳ ĐÃ GỬI ADMIN DUYỆT")


# =====================
# CHỌN ROBUX
# =====================

    elif query.data.startswith("rb_"):

        goi = query.data.split("_")[1]

        waiting_robux[user.id] = goi


        await context.bot.send_photo(

            user.id,

            QR,

            caption=f"""

💎 GÓI: {goi} ROBUX

Nhập TÊN ROBLOX:

"""

        )


# =====================
# ADMIN DUYỆT FF
# =====================

    elif query.data.startswith("ok_ff_"):

        uid = int(query.data.split("_")[2])

        acc = load_ff()

        if not acc:

            await query.edit_message_text("Hết acc")

            return


        tk = acc.pop(0)

        save_ff(acc)


        await context.bot.send_message(

            uid,

            f"""

🎉 MUA THÀNH CÔNG

ACC:

{tk}

"""

        )


        await query.edit_message_text("ĐÃ GỬI ACC")


# =====================
# ADMIN HỦY FF
# =====================

    elif query.data.startswith("no_ff_"):

        uid = int(query.data.split("_")[2])

        await context.bot.send_message(

            uid,

            "❌ ĐƠN BỊ HỦY"

        )


        await query.edit_message_text("ĐÃ HỦY")


# =====================
# ADMIN DUYỆT ROBUX
# =====================

    elif query.data.startswith("ok_rb_"):

        uid = int(query.data.split("_")[2])

        await context.bot.send_message(

            uid,

            "🎉 ADMIN SẼ CHUYỂN ROBUX SỚM"

        )


        await query.edit_message_text("ĐÃ DUYỆT")


# =====================
# ADMIN HỦY ROBUX
# =====================

    elif query.data.startswith("no_rb_"):

        uid = int(query.data.split("_")[2])

        await context.bot.send_message(

            uid,

            "❌ ĐƠN BỊ HỦY"

        )


        await query.edit_message_text("ĐÃ HỦY")


# =====================
# NHẬP TÊN ROBLOX
# =====================

async def text(update, context):

    user = update.message.from_user


    if user.id in waiting_robux:

        name = update.message.text

        goi = waiting_robux[user.id]


        keyboard = InlineKeyboardMarkup([

            [

                InlineKeyboardButton("✅ DUYỆT", callback_data=f"ok_rb_{user.id}"),

                InlineKeyboardButton("❌ HỦY", callback_data=f"no_rb_{user.id}")

            ]

        ])


        await context.bot.send_message(

            ADMIN_ID,

            f"""

🪙 ĐƠN ROBUX

👤 @{user.username}

🆔 {user.id}

🎮 Roblox: {name}

💎 Gói: {goi}

""",

            reply_markup=keyboard

        )


        await update.message.reply_text(

            "⏳ ĐÃ GỬI ADMIN DUYỆT"

        )


        del waiting_robux[user.id]


# =====================
# MAIN
# =====================

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(MessageHandler(filters.Regex("FREE FIRE"), freefire))

app.add_handler(MessageHandler(filters.Regex("ROBUX"), robux))

app.add_handler(CallbackQueryHandler(button))

app.add_handler(MessageHandler(filters.TEXT, text))

print("BOT ĐANG CHẠY...")

app.run_polling()
