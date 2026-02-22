import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.utils import executor


# Railway Variables
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


# file QR
QR_PATH = "qr.jpg"


# lưu dữ liệu
choosing = {}
pending = {}

# chống spam
paid_users = set()



# START
@dp.message_handler(commands=['start'])
async def start(msg: types.Message):

    kb = InlineKeyboardMarkup()

    kb.add(
        InlineKeyboardButton("💎 MUA ROBUX", callback_data="robux")
    )

    await msg.answer(
        "🏪 SHOP HỒ QUỐC 🏪\n\n"
        "💎 Robux chính hãng\n"
        "🛡 Uy tín - An toàn\n\n"
        "👇 Chọn bên dưới",
        reply_markup=kb
    )



# MENU ROBUX
@dp.callback_query_handler(lambda c: c.data == "robux")
async def robux(call: types.CallbackQuery):

    kb = InlineKeyboardMarkup(row_width=1)

    kb.add(

        InlineKeyboardButton("💎 150 Robux - 50K", callback_data="150"),

        InlineKeyboardButton("💎 300 Robux - 100K", callback_data="300"),

        InlineKeyboardButton("💎 600 Robux - 200K", callback_data="600"),

        InlineKeyboardButton("💎 900 Robux - 300K", callback_data="900"),

        InlineKeyboardButton("💎 1200 Robux - 400K", callback_data="1200"),

        InlineKeyboardButton("💎 1500 Robux - 500K", callback_data="1500")

    )

    await call.message.answer(
        "📦 Chọn gói Robux:",
        reply_markup=kb
    )



# CHỌN GÓI
@dp.callback_query_handler(lambda c: c.data in ["150","300","600","900","1200","1500"])
async def buy(call: types.CallbackQuery):

    choosing[call.from_user.id] = call.data

    await call.message.answer(
        "👤 Nhập tên tài khoản Roblox:"
    )



# NHẬP USERNAME → gửi QR
@dp.message_handler()
async def get_username(msg: types.Message):

    user_id = msg.from_user.id

    if user_id not in choosing:
        return

    username = msg.text
    robux = choosing[user_id]

    pending[user_id] = (username, robux)

    kb = InlineKeyboardMarkup()

    kb.add(
        InlineKeyboardButton("✅ ĐÃ THANH TOÁN", callback_data="paid")
    )

    photo = InputFile(QR_PATH)

    await msg.answer_photo(

        photo,

        caption=f"""
💳 Quét QR để thanh toán

👤 Roblox: {username}
💎 Gói: {robux} Robux

Sau khi chuyển bấm nút dưới
""",

        reply_markup=kb
    )



# USER BẤM ĐÃ THANH TOÁN
@dp.callback_query_handler(lambda c: c.data == "paid")
async def paid(call: types.CallbackQuery):

    user_id = call.from_user.id


    # lấy username telegram
    tele_username = call.from_user.username

    if tele_username:
        tele = f"@{tele_username}"
    else:
        tele = "Không có username"


    # chống spam
    if user_id in paid_users:

        await call.answer(
            "⚠️ Bạn đã gửi yêu cầu rồi!",
            show_alert=True
        )

        return


    paid_users.add(user_id)


    username, robux = pending[user_id]


    kb = InlineKeyboardMarkup()

    kb.add(

        InlineKeyboardButton("✅ DUYỆT", callback_data=f"ok_{user_id}"),

        InlineKeyboardButton("❌ HỦY", callback_data=f"no_{user_id}")

    )


    await bot.send_message(

        ADMIN_ID,

        f"""
🛒 ĐƠN MUA ROBUX

👤 Telegram: {tele}

🆔 ID: {user_id}

🎮 Roblox: {username}

💎 Gói: {robux} Robux
""",

        reply_markup=kb
    )


    await call.message.answer(
        "⏳ Đã gửi admin duyệt"
    )



# ADMIN DUYỆT
@dp.callback_query_handler(lambda c: c.data.startswith("ok_"))
async def ok(call: types.CallbackQuery):

    user_id = int(call.data.split("_")[1])

    paid_users.discard(user_id)


    await bot.send_message(

        user_id,

        "🎉 Thanh toán thành công\n"
        "💎 Robux sẽ được gửi sớm\n"
        "Cảm ơn bạn ❤️"

    )


    await call.message.edit_text("✅ ĐÃ DUYỆT")



# ADMIN HỦY
@dp.callback_query_handler(lambda c: c.data.startswith("no_"))
async def no(call: types.CallbackQuery):

    user_id = int(call.data.split("_")[1])

    paid_users.discard(user_id)


    await bot.send_message(

        user_id,

        "❌ Thanh toán bị từ chối"

    )


    await call.message.edit_text("❌ ĐÃ HỦY")



# RUN BOT
if __name__ == "__main__":

    print("Bot is running...")

    executor.start_polling(dp, skip_updates=True)
