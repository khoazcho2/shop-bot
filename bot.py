import json
import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputFile
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

TOKEN = os.getenv("8462718923:AAEmsMjDI4Ih0IkKkcrnqaIXTIxNVEd68xs")
ADMIN_ID = 8337495954

QR = "qr.png"
DATA = "data.json"
ACC_FILE = "acc.txt"


# ========= LOAD SAVE =========

def load():
    if not os.path.exists(DATA):
        return {}
    with open(DATA,"r",encoding="utf-8") as f:
        return json.load(f)

def save(data):
    with open(DATA,"w",encoding="utf-8") as f:
        json.dump(data,f)


# ========= ROBUX =========

ROBUX = {

    "r50": ("150 Robux", "50.000đ"),

    "r100": ("300 Robux", "100.000đ"),

    "r200": ("600 Robux", "200.000đ"),

    "r400": ("1200 Robux", "400.000đ"),

    "r500": ("1500 Robux", "500.000đ"),

}


# ========= START =========

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
╔══════════════════╗
   🏪 SHOP HỒ QUỐC
╚══════════════════╝

🛒 Chào mừng bạn đến shop

💎 Bán Robux chính hãng
🔥 Bán Acc Free Fire giá rẻ

👇 Chọn dịch vụ bên dưới
"""

    keyboard = [

        [InlineKeyboardButton("💎 Mua Robux", callback_data="robux")],

        [InlineKeyboardButton("🔥 Mua Acc Free Fire 120K", callback_data="ff")]

    ]

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ========= MENU ROBUX =========

async def menu_robux(update: Update, context):

    query = update.callback_query
    await query.answer()

    keyboard=[]

    for key,value in ROBUX.items():

        keyboard.append([

            InlineKeyboardButton(
                f"💎 {value[0]} | 💰 {value[1]}",
                callback_data=key
            )

        ])

    await query.edit_message_text(

"""
💎 DANH SÁCH ROBUX

✔ Đã bao gồm thuế
✔ Nạp nhanh

👇 Chọn gói
""",

        reply_markup=InlineKeyboardMarkup(keyboard)

    )


# ========= CHỌN ROBUX =========

async def select_robux(update: Update, context):

    query = update.callback_query

    data = load()

    user = str(query.from_user.id)

    if user in data:

        await query.answer("⚠️ Bạn đã tạo đơn rồi", show_alert=True)
        return

    pack = query.data

    data[user] = {

        "type":"robux",

        "pack":pack

    }

    save(data)

    await query.message.reply_photo(

        photo=InputFile(QR),

        caption="""
💳 THANH TOÁN ROBUX

📌 Chuyển khoản theo QR
📌 Nội dung: ID TELEGRAM

Sau đó bấm nút bên dưới
"""

    )

    keyboard=[

        [InlineKeyboardButton(
            "✅ Đã thanh toán",
            callback_data="paid"
        )]

    ]

    await query.message.reply_text(
        "👇 Sau khi chuyển khoản bấm nút",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ========= MUA FF =========

async def buy_ff(update: Update, context):

    query = update.callback_query

    data = load()

    user=str(query.from_user.id)

    if user in data:

        await query.answer("⚠️ Bạn đã tạo đơn", show_alert=True)
        return

    data[user]={

        "type":"ff"

    }

    save(data)

    await query.message.reply_photo(

        photo=InputFile(QR),

        caption="""
🔥 MUA ACC FREE FIRE

💰 Giá: 120.000đ

📌 Chuyển khoản theo QR
"""

    )

    keyboard=[

        [InlineKeyboardButton(
            "✅ Đã thanh toán",
            callback_data="paid"
        )]

    ]

    await query.message.reply_text(
        "👇 Sau khi chuyển khoản bấm nút",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ========= ĐÃ THANH TOÁN =========

async def paid(update: Update, context):

    query=update.callback_query

    data=load()

    user=str(query.from_user.id)

    keyboard=[

        [

            InlineKeyboardButton(
                "✔️ DUYỆT",
                callback_data=f"ok_{user}"
            )

        ]

    ]

    await context.bot.send_message(

        ADMIN_ID,

f"""
💰 ĐƠN HÀNG MỚI

👤 User: {user}

Bấm duyệt
""",

        reply_markup=InlineKeyboardMarkup(keyboard)

    )

    await query.answer("⏳ Đợi admin duyệt")


# ========= ADMIN DUYỆT =========

async def approve(update: Update, context):

    query=update.callback_query

    user=query.data.split("_")[1]

    data=load()

    order=data[user]

    if order["type"]=="ff":

        with open(ACC_FILE,"r") as f:
            acc=f.readlines()

        send=acc[0]

        with open(ACC_FILE,"w") as f:
            f.writelines(acc[1:])

        await context.bot.send_message(

            user,

f"""
🎮 ACC FREE FIRE

{send}

Chúc bạn chơi game vui vẻ 🎉
"""

        )

    else:

        await context.bot.send_message(

            user,

"""
💎 ROBUX

Admin sẽ nạp sớm nhất
"""

        )


    del data[user]

    save(data)

    await query.edit_message_text("✅ Đã duyệt")


# ========= BUTTON =========

async def button(update: Update, context):

    query=update.callback_query

    if query.data=="robux":
        await menu_robux(update,context)

    elif query.data=="ff":
        await buy_ff(update,context)

    elif query.data=="paid":
        await paid(update,context)

    elif query.data.startswith("ok_"):
        await approve(update,context)

    elif query.data.startswith("r"):
        await select_robux(update,context)


# ========= RUN =========

app=Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start",start))

app.add_handler(CallbackQueryHandler(button))

app.run_polling()
