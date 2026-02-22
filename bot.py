import os
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# link QR ngân hàng của bạn
QR_LINK = "https://i.imgur.com/yourQR.png"


# MENU CHÍNH
@dp.message_handler(commands=['start'])
async def start(msg: types.Message):

    kb = InlineKeyboardMarkup(row_width=1)

    kb.add(
        InlineKeyboardButton("🟢 MUA ROBUX", callback_data="robux"),
        InlineKeyboardButton("🔵 MUA FREE FIRE", callback_data="ff")
    )

    await msg.answer("✨ SHOP HỒ QUỐC ✨\nChọn sản phẩm:", reply_markup=kb)


# ROBUX MENU
@dp.callback_query_handler(lambda c: c.data == "robux")
async def robux(call: types.CallbackQuery):

    kb = InlineKeyboardMarkup(row_width=1)

    kb.add(
        InlineKeyboardButton("💰 150 Robux - 50k", callback_data="buy_150"),
        InlineKeyboardButton("💰 300 Robux - 100k", callback_data="buy_300")
    )

    await call.message.edit_text("Chọn gói Robux:", reply_markup=kb)


# FREE FIRE MENU
@dp.callback_query_handler(lambda c: c.data == "ff")
async def ff(call: types.CallbackQuery):

    kb = InlineKeyboardMarkup(row_width=1)

    kb.add(
        InlineKeyboardButton("💎 566 KC - 100k", callback_data="buy_ff566"),
        InlineKeyboardButton("💎 3113 KC - 550k", callback_data="buy_ff3113")
    )

    await call.message.edit_text("Chọn gói Free Fire:", reply_markup=kb)


# NHẬP TÊN
user_data = {}


@dp.callback_query_handler(lambda c: "buy" in c.data)
async def ask_user(call: types.CallbackQuery):

    user_data[call.from_user.id] = call.data

    await bot.send_message(call.from_user.id, "Nhập tên tài khoản:")


# NHẬN TÊN
@dp.message_handler()
async def get_name(msg: types.Message):

    if msg.from_user.id not in user_data:
        return

    product = user_data[msg.from_user.id]
    username = msg.text

    # gửi QR cho khách
    kb = InlineKeyboardMarkup()

    kb.add(
        InlineKeyboardButton("✅ ĐÃ THANH TOÁN", callback_data=f"paid_{username}_{product}")
    )

    await msg.answer_photo(QR_LINK,
        caption=f"Thanh toán xong bấm nút dưới\nTên: {username}",
        reply_markup=kb
    )


# XÁC NHẬN THANH TOÁN
@dp.callback_query_handler(lambda c: "paid" in c.data)
async def paid(call: types.CallbackQuery):

    data = call.data.replace("paid_", "")

    username, product = data.split("_", 1)

    kb = InlineKeyboardMarkup()

    kb.add(
        InlineKeyboardButton("✅ DUYỆT", callback_data=f"ok_{call.from_user.id}"),
        InlineKeyboardButton("❌ HỦY", callback_data=f"no_{call.from_user.id}")
    )

    await bot.send_message(
        ADMIN_ID,
        f"""
ĐƠN MỚI

User: @{call.from_user.username}

Tên game: {username}

Gói: {product}
""",
        reply_markup=kb
    )

    await call.message.answer("⏳ Chờ admin duyệt")


# ADMIN DUYỆT
@dp.callback_query_handler(lambda c: "ok" in c.data)
async def ok(call: types.CallbackQuery):

    user_id = int(call.data.split("_")[1])

    await bot.send_message(user_id, "✅ Đã duyệt - sẽ gửi sớm")

    await call.message.edit_text("ĐÃ DUYỆT")


# ADMIN HỦY
@dp.callback_query_handler(lambda c: "no" in c.data)
async def no(call: types.CallbackQuery):

    user_id = int(call.data.split("_")[1])

    await bot.send_message(user_id, "❌ Đơn bị hủy")

    await call.message.edit_text("ĐÃ HỦY")


# START BOT
executor.start_polling(dp)
