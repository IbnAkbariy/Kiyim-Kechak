import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

# Bot uchun loglarni sozlash
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Telegram kanal ID'si
CHANNEL_ID1 = "-1002449977187"  # O'zingizning kanal ID'nizni kiriting
CHANNEL_ID2 = "-1002447315502"

# Qo'llaniladigan bo'limlar
MENU, DONATE_NAME, DONATE_PHONE, DONATE_ADDRESS, HELP_NAME, HELP_PHONE, HELP_ADDRESS, HELP_NEED = range(8)

# Boshlang'ich komandalar
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [["🧥 Kiyim topshirish", "🆘 Yordam so'rash"], ["ℹ️ Biz haqimizda"]]
    await update.message.reply_text(
        "Xush kelibsiz! Sizga qanday yordam bera olamiz?", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    return MENU

# "Biz haqimizda" bo'limi
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Biz eski yoki ortiqcha kiyimlarni muhtoj oilalarga yetkazish uchun yig'amiz.\n"
        "Loyihamiz haqida ko'proq ma'lumot olish uchun bog'laning: @admin_username",
        reply_markup=ReplyKeyboardMarkup([["🔙 Ortga"]], resize_keyboard=True),
    )
    return MENU

# Kiyim topshirish jarayoni
async def donate_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Ismingizni kiriting:")
    return DONATE_NAME

async def donate_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["donate_name"] = update.message.text
    await update.message.reply_text("Telefon raqamingizni kiriting:")
    return DONATE_PHONE

async def donate_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["donate_phone"] = update.message.text
    await update.message.reply_text("Manzilingizni kiriting:")
    return DONATE_ADDRESS

async def donate_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["donate_address"] = update.message.text
    donation = {
        "name": context.user_data["donate_name"],
        "phone": context.user_data["donate_phone"],
        "address": context.user_data["donate_address"],
    }

    # Telegram kanalga yuboriladigan xabar
    message = (
        f"🧥 Yangi kiyim topshirish arizasi\n"
        f"📛 Ism: {donation['name']}\n"
        f"📞 Telefon: {donation['phone']}\n"
        f"📍 Manzil: {donation['address']}"
    )
    await context.bot.send_message(chat_id=CHANNEL_ID1, text=message)

    await update.message.reply_text(
        "Rahmat! Sizning arizangiz qabul qilindi. Tez orada biz siz bilan bog'lanamiz!", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

# Yordam so'rash jarayoni
async def help_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Ismingizni kiriting:")
    return HELP_NAME

async def help_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["help_name"] = update.message.text
    await update.message.reply_text("Telefon raqamingizni kiriting:")
    return HELP_PHONE

async def help_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["help_phone"] = update.message.text
    await update.message.reply_text("Manzilingizni kiriting:")
    return HELP_ADDRESS

async def help_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["help_address"] = update.message.text
    await update.message.reply_text("Sizga qanday yordam kerakligi haqida qisqacha yoza olasizmi ?:")
    return HELP_NEED

async def help_need(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["help_need"] = update.message.text
    help_request = {
        "name": context.user_data["help_name"],
        "phone": context.user_data["help_phone"],
        "address": context.user_data["help_address"],
        "need": context.user_data["help_need"],
    }

    # Telegram kanalga yuboriladigan xabar
    message = (
        f"🆘 Yangi yordam so'rov arizasi\n"
        f"📛 Ism: {help_request['name']}\n"
        f"📞 Telefon: {help_request['phone']}\n"
        f"📍 Manzil: {help_request['address']}\n"
        f"🤲 Yordam turi: {help_request['need']}"
    )
    await context.bot.send_message(chat_id=CHANNEL_ID2, text=message)

    await update.message.reply_text(
        "Rahmat! Sizning arizangiz qabul qilindi. Biz tez orada siz bilan bog'lanamiz!", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

# Ortga qaytish funksiyasi
async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return await start(update, context)

# Asosiy funksiya
def main() -> None:
    application = Application.builder().token("8138020813:AAGsSC1asCt0mTz-0VwlEFTyRyj0t9uFyC8").build()

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MENU: [
                MessageHandler(filters.Regex("^🧥 Kiyim topshirish$"), donate_start),
                MessageHandler(filters.Regex("^🆘 Yordam so'rash$"), help_start),
                MessageHandler(filters.Regex("^ℹ️ Biz haqimizda$"), about),
                MessageHandler(filters.Regex("^🔙 Ortga$"), back_to_menu),
            ],
            DONATE_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, donate_name)],
            DONATE_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, donate_phone)],
            DONATE_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, donate_address)],
            HELP_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, help_name)],
            HELP_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, help_phone)],
            HELP_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, help_address)],
            HELP_NEED: [MessageHandler(filters.TEXT & ~filters.COMMAND, help_need)],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conversation_handler)
    application.run_polling()

if __name__ == "__main__":
    main()