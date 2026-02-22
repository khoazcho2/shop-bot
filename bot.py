import os
import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# ===== QR IMAGE =====
QR_URL = "https://i.imgur.com/yourQR.png"


# ===== START =====

@dp.message_handler(commands=['start'])
async def start(message: types.Message):

    kb = InlineKeyboardMarkup(row_width=2)

    kb.add(
        InlineKeyboardButton("🟢 MUA ROBUX", callback_data="robux"),
        InlineKeyboardButton("🔵 MUA FREE FIRE", callback_data="ff")
    )

    await message.answer(
        "✨ SHOP HỒ QUỐC ✨\n\nChọn sản phẩm:",
        reply_markup=kb
    )


# ===== ROBUX PACK =====

@dp.callback_query_handler(lambda c: c.data == "robux")
async def robux(callback: types.CallbackQuery):

    kb = InlineKeyboardMarkup()

    kb.add(
        InlineKeyboardButton("120 Robux - 20k", callback_data="rb_120"),
        InlineKeyboardButton("400 Robux - 60k", callback_data="rb_400"),
        InlineKeyboardButton("800 Robux - 120k", callback_data="rb_800")
    )

    await callback.message.edit_text(
        "Chọn gói Robux:",
        reply_markup=kb
    )


# ===== FF PACK =====

@dp.callback_query_handler(lambda c: c.data == "ff")
async def ff(callback: types.CallbackQuery):

    kb = InlineKeyboardMarkup()

    kb.add(
        InlineKeyboardButton("120 KC - 20k", callback_data="ff_120"),
        InlineKeyboardButton("310 KC - 50k", callback_data="ff_310"),
        InlineKeyboardButton("520 KC - 80k", callback_data="ff_520")
    )

    await callback.message.edit_text(
        "Chọn gói Free Fire:",
        reply_markup=kb
    )


# ===== USERNAME INPUT =====

user_data = {}

@dp.callback_query_handler(lambda c: c.data.startswith("rb_") or c.data.startswith("ff_"))
async def ask_user(callback: types.CallbackQuery):

    user_data[callback.from_user.id] = callback.data

    await bot.send_message(
        callback.from_user.id,
        "Nhập username game:"
    )


@dp.message_handler(lambda message: message.from_user.id in user_data)
async def get_username(message: types.Message):

    pack = user_data[message.from_user.id]
    username = message.text

    kb = InlineKeyboardMarkup()

    kb.add(
        InlineKeyboardButton(
            "💳 THANH TOÁN",
            callback_data=f"pay|{pack}|{username}"
        )
    )

    await message.answer(
        f"Gói: {pack}\nUser: {username}",
        reply_markup=kb
    )

    del user_data[message.from_user.id]


# ===== PAYMENT =====

@dp.callback_query_handler(lambda c: c.data.startswith("pay"))
async def payment(callback: types.CallbackQuery):

    data = callback.data.split("|")

    pack = data[1]
    username = data[2]
    user_id = callback.from_user.id

    # gửi QR cho user
    await bot.send_photo(
        user_id,
        QR_URL,
        caption="Quét QR để thanh toán"
    )

    # gửi admin

    kb = InlineKeyboardMarkup()

    kb.add(
        InlineKeyboardButton(
            "✅ DUYỆT",
            callback_data=f"ok|{user_id}"
        ),
        InlineKeyboardButton(
            "❌ HỦY",
            callback_data=f"no|{user_id}"
        )
    )

    await bot.send_message(
        ADMIN_ID,
        f"""
Đơn hàng mới

User: {username}
Gói: {pack}
ID: {user_id}
        """,
        reply_markup=kb
    )


# ===== ADMIN APPROVE =====

@dp.callback_query_handler(lambda c: c.data.startswith("ok"))
async def approve(callback: types.CallbackQuery):

    user_id = int(callback.data.split("|")[1])

    await bot.send_message(
        user_id,
        "✅ Đơn đã được duyệt\nVui lòng chờ nhận"
    )

    await callback.answer("Đã duyệt")


# ===== ADMIN CANCEL =====

@dp.callback_query_handler(lambda c: c.data.startswith("no"))
async def cancel(callback: types.CallbackQuery):

    user_id = int(callback.data.split("|")[1])

    await bot.send_message(
        user_id,
        "❌ Đơn đã bị hủy"
    )

    await callback.answer("Đã hủy")


# ===== RUN =====

if __name__ == "__main__":
    executor.start_polling(dp)
