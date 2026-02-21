import os
import sqlite3
from telegram import (
Update,
InlineKeyboardButton,
InlineKeyboardMarkup,
InputFile
)
from telegram.ext import (
ApplicationBuilder,
CommandHandler,
CallbackQueryHandler,
ContextTypes
)
TOKEN = "8462718923:AAEaghAn9KqEgvu-uUJJXMK0G51YZgk1YIU"
ADMIN_ID = 8337495954

QR = "qr.png"

# database
conn = sqlite3.connect("shop.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(
user_id INTEGER,
product TEXT,
paid INTEGER DEFAULT 0
)
""")

conn.commit()


# lay acc ff
def get_acc(file):

    with open(file,"r") as f:

        accs=f.readlines()

    acc=accs[0]

    with open(file,"w") as f:

        f.writelines(accs[1:])

    return acc


# start
async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):

    keyboard=[

        [
        InlineKeyboardButton("Mua Robux",callback_data="robux")
        ],

        [
        InlineKeyboardButton("Mua Acc Free Fire",callback_data="ff")
        ]

    ]

    await update.message.reply_text(

    "Shop Ho Quoc",

    reply_markup=InlineKeyboardMarkup(keyboard)

    )


# chon san pham
async def button(update:Update,context):

    query=update.callback_query

    user=query.from_user.id

    data=query.data


    if data=="robux":

        keyboard=[

        [
        InlineKeyboardButton("120 Robux = 50k",callback_data="buy_robux")
        ]

        ]

        await query.message.reply_text(

        "Chon goi robux",

        reply_markup=InlineKeyboardMarkup(keyboard)

        )


    elif data=="ff":

        keyboard=[

        [
        InlineKeyboardButton("Acc Free Fire 120k",callback_data="buy_ff")
        ]

        ]

        await query.message.reply_text(

        "Acc random",

        reply_markup=InlineKeyboardMarkup(keyboard)

        )


    elif data=="buy_ff" or data=="buy_robux":

        cursor.execute(

        "SELECT paid FROM orders WHERE user_id=?",

        (user,)
        )

        check=cursor.fetchone()


        if check and check[0]==1:

            await query.answer("Ban da mua roi")
            return


        product="ff" if data=="buy_ff" else "robux"


        cursor.execute(

        "INSERT OR REPLACE INTO orders(user_id,product,paid) VALUES(?,?,0)",

        (user,product)

        )

        conn.commit()


        keyboard=[

        [
        InlineKeyboardButton("Da thanh toan",callback_data="paid")
        ]

        ]


        await query.message.reply_photo(

        photo=InputFile(QR),

        caption="Quet QR roi bam da thanh toan",

        reply_markup=InlineKeyboardMarkup(keyboard)

        )


    elif data=="paid":

        cursor.execute(

        "UPDATE orders SET paid=1 WHERE user_id=?",

        (user,)
        )

        conn.commit()


        keyboard=[

        [
        InlineKeyboardButton(

        "DUYET",

        callback_data=f"duyet_{user}"

        )

        ]

        ]


        await context.bot.send_message(

        ADMIN_ID,

        f"user {user} da thanh toan",

        reply_markup=InlineKeyboardMarkup(keyboard)

        )


        await query.answer("Cho admin duyet")


    elif data.startswith("duyet"):

        user=int(data.split("_")[1])


        cursor.execute(

        "SELECT product FROM orders WHERE user_id=?",

        (user,)
        )

        product=cursor.fetchone()[0]


        if product=="ff":

            acc=get_acc("acc.txt")

            await context.bot.send_message(

            user,

            f"ACC FREE FIRE:\n{acc}"

            )


        elif product=="robux":

            await context.bot.send_message(

            user,

            "Admin se nap robux cho ban"

            )


        await query.answer("Da duyet")


# run
app=ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start",start))

app.add_handler(CallbackQueryHandler(button))

app.run_polling()

