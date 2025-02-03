from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)
#import os
#from datetime import datetime
#import pytz

# Kanallar (o'zingizning kanal usernamalaringizni yozing)
DONATIONS_CHANNEL = "-1002449977187"
REQUESTS_CHANNEL = "-1002447315502"

# Suhbat holatlari
(
    MENU,
    DONOR_NAME,
    DONOR_PHONE,
    DONOR_ADDRESS,
    DONOR_DESCRIPTION,
    DONOR_CONFIRM,
    REQUESTER_NAME,
    REQUESTER_PHONE,
    REQUESTER_ADDRESS,
    REQUESTER_DESCRIPTION,
    REQUESTER_CONFIRM,
) = range(11)

# Admin IDlari (o'zingizning Telegram ID raqamingizni yozing)
ADMIN_IDS = [123456789]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start komandasi"""
    keyboard = [
        ["🎁 Kiyim topshirish"],
        ["🤲 Yordam so'rash"],
        ["📞 Biz bilan aloqa"]
    ]
    if update.effective_user.id in ADMIN_IDS:
        keyboard.append(["👨‍💼 Admin panel"])
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    message = (
        "Assalomu alaykum va rahmatullohi va barakatuh! 🌟\n\n"
        "«Xayrli kiyimlar» loyihasiga xush kelibsiz!\n\n"
        "Bu loyiha orqali siz o'zingizga ortiqcha bo'lgan kiyimlarni "
        "muhtoj insonlarga yetkazishda ko'mak bera olasiz.\n\n"
        "«Kim bir mo'minning dunyodagi g'amlaridan birini ketkazsa, "
        "Alloh undan oxiratdagi g'amlaridan birini ketkazadi» (Hadis)\n\n"
        "Quyidagi menyudan kerakli bo'limni tanlang:"
    )
    
    await update.message.reply_text(message, reply_markup=reply_markup)
    return MENU

async def donate_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kiyim topshirish jarayonini boshlash"""
    await update.message.reply_text(
        "Iltimos, ismingizni kiriting:",
        reply_markup=ReplyKeyboardRemove()
    )
    return DONOR_NAME

async def donor_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kiyim topshiruvchining ismini saqlash"""
    context.user_data['donor_name'] = update.message.text
    await update.message.reply_text("Telefon raqamingizni kiriting (+998 formatida):")
    return DONOR_PHONE

async def donor_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Telefon raqamni tekshirish va saqlash"""
    phone = update.message.text
    if not phone.startswith("+998") or len(phone) != 13:
        await update.message.reply_text("Iltimos, telefon raqamni to'g'ri formatda kiriting (+998xxxxxxxxx):")
        return DONOR_PHONE
    
    context.user_data['donor_phone'] = phone
    await update.message.reply_text("Manzilingizni kiriting:")
    return DONOR_ADDRESS

async def donor_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manzilni saqlash"""
    context.user_data['donor_address'] = update.message.text
    await update.message.reply_text(
        "Qanday yordam bermoqchi ekanligingiz haqida qisqacha ma'lumot bering:"
    )
    return DONOR_DESCRIPTION

async def donor_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kiyim topshirish tavsifini saqlash va tasdiqlash"""
    context.user_data['donor_description'] = update.message.text
    
    confirm_message = (
        "Iltimos, ma'lumotlaringizni tekshiring:\n\n"
        f"👤 Ism: {context.user_data['donor_name']}\n"
        f"📞 Telefon: {context.user_data['donor_phone']}\n"
        f"📍 Manzil: {context.user_data['donor_address']}\n"
        f"📄 Tavsif: {context.user_data['donor_description']}\n\n"
        "Ma'lumotlar to'g'rimi?"
    )
    
    keyboard = [["✅ Ha", "🔄 Qayta to'ldirish"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(confirm_message, reply_markup=reply_markup)
    return DONOR_CONFIRM

async def donor_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kiyim topshirish ma'lumotlarini tasdiqlash va kanalga yuborish"""
    if update.message.text == "✅ Ha":
        
        # Kanalga yuborish uchun xabar tayyorlash
        message = (
            f"📝 Yangi kiyim topshirish arizasi \n\n"
            f"👤 Ism: {context.user_data['donor_name']}\n"
            f"📞 Telefon: {context.user_data['donor_phone']}\n"
            f"📍 Manzil: {context.user_data['donor_address']}\n"
            f"📄 Tavsif: {context.user_data['donor_description']}"
        )
        
        # Kanalga yuborish
        await context.bot.send_message(chat_id=DONATIONS_CHANNEL, text=message)
        
        # Foydalanuvchiga tasdiqlash xabari
        keyboard = [["🏠 Asosiy menyu"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(
            "✅ Sizning arizangiz qabul qilindi!\n\n"
            "Tez orada siz bilan bog'lanamiz.",
            reply_markup=reply_markup
        )
        return MENU
    
    elif update.message.text == "🔄 Qayta to'ldirish":
        return await donate_start(update, context)

async def request_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yordam so'rash jarayonini boshlash"""
    await update.message.reply_text(
        "Iltimos, ismingizni kiriting:",
        reply_markup=ReplyKeyboardRemove()
    )
    return REQUESTER_NAME

async def requester_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yordam so'rovchining ismini saqlash"""
    context.user_data['requester_name'] = update.message.text
    await update.message.reply_text("Telefon raqamingizni kiriting (+998 formatida):")
    return REQUESTER_PHONE

async def requester_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Telefon raqamni tekshirish va saqlash"""
    phone = update.message.text
    if not phone.startswith("+998") or len(phone) != 13:
        await update.message.reply_text("Iltimos, telefon raqamni to'g'ri formatda kiriting (+998xxxxxxxxx):")
        return REQUESTER_PHONE
    
    context.user_data['requester_phone'] = phone
    await update.message.reply_text("Manzilingizni kiriting:")
    return REQUESTER_ADDRESS

async def requester_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manzilni saqlash"""
    context.user_data['requester_address'] = update.message.text
    await update.message.reply_text(
        "Qanday yordam kerak ekanligini qisqacha yozing:"
    )
    return REQUESTER_DESCRIPTION

async def requester_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yordam so'rash tavsifini saqlash va tasdiqlash"""
    context.user_data['requester_description'] = update.message.text
    
    confirm_message = (
        "Iltimos, ma'lumotlaringizni tekshiring:\n\n"
        f"👤 Ism: {context.user_data['requester_name']}\n"
        f"📞 Telefon: {context.user_data['requester_phone']}\n"
        f"📍 Manzil: {context.user_data['requester_address']}\n"
        f"📄 Tavsif: {context.user_data['requester_description']}\n\n"
        "Ma'lumotlar to'g'rimi?"
    )
    
    keyboard = [["✅ Ha", "🔄 Qayta to'ldirish"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(confirm_message, reply_markup=reply_markup)
    return REQUESTER_CONFIRM

async def requester_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yordam so'rash ma'lumotlarini tasdiqlash va kanalga yuborish"""
    if update.message.text == "✅ Ha":

        # Kanalga yuborish uchun xabar tayyorlash
        message = (
            f"📝 Yangi yordam so'rovi \n\n"
            f"👤 Ism: {context.user_data['requester_name']}\n"
            f"📞 Telefon: {context.user_data['requester_phone']}\n"
            f"📍 Manzil: {context.user_data['requester_address']}\n"
            f"📄 Tavsif: {context.user_data['requester_description']}"
        )
        
        # Kanalga yuborish
        await context.bot.send_message(chat_id=REQUESTS_CHANNEL, text=message)
        
        # Foydalanuvchiga tasdiqlash xabari
        keyboard = [["🏠 Asosiy menyu"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(
            "✅ Sizning so'rovingiz qabul qilindi!\n\n"
            "Tez orada siz bilan bog'lanamiz.",
            reply_markup=reply_markup
        )
        return MENU
    
    elif update.message.text == "🔄 Qayta to'ldirish":
        return await request_start(update, context)

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Aloqa ma'lumotlarini ko'rsatish"""
    keyboard = [["🏠 Asosiy menyu"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    contact_info = (
        "📞 Biz bilan bog'lanish:\n\n"
        "☎️ Telefon: +998939077440\n"
        "📱 Telegram: @EskiKiyim_Admin\n"
    )
    
    await update.message.reply_text(contact_info, reply_markup=reply_markup)
    return MENU

async def admin_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin xabar tarqatish"""
    if update.effective_user.id not in ADMIN_IDS:
        return MENU
    
    await update.message.reply_text(
        "Barcha foydalanuvchilarga yubormoqchi bo'lgan xabaringizni kiriting:",
        reply_markup=ReplyKeyboardMarkup([["🏠 Asosiy menyu"]], resize_keyboard=True)
    )
    return MENU
def main():
    """Botni ishga tushirish"""
    # Application yaratish
    application = (
        Application.builder()
        .token("8138020813:AAGsSC1asCt0mTz-0VwlEFTyRyj0t9uFyC8")  # Bot tokenini yozing
        .build()
    )
    
    # Suhbat holatlarini boshqaruvchi handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MENU: [
                MessageHandler(filters.Regex("^🎁 Kiyim topshirish$"), donate_start),
                MessageHandler(filters.Regex("^🤲 Yordam so'rash$"), request_start),
                MessageHandler(filters.Regex("^📞 Biz bilan aloqa$"), contact),
                MessageHandler(filters.Regex("^👨‍💼 Admin panel$"), admin_broadcast),
            ],
            DONOR_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, donor_name)],
            DONOR_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, donor_phone)],
            DONOR_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, donor_address)],
            DONOR_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, donor_description)],
            DONOR_CONFIRM: [MessageHandler(filters.Regex("^(✅ Ha|🔄 Qayta to'ldirish)$"), donor_confirm)],
            
            REQUESTER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, requester_name)],
            REQUESTER_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, requester_phone)],
            REQUESTER_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, requester_address)],
            REQUESTER_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, requester_description)],
            REQUESTER_CONFIRM: [MessageHandler(filters.Regex("^(✅ Ha|🔄 Qayta to'ldirish)$"), requester_confirm)],
        },
        fallbacks=[MessageHandler(filters.Regex("^🏠 Asosiy menyu$"), start)],
    )
    
    # Handlerni ro'yxatga olish
    application.add_handler(conv_handler)
    
    # Botni ishga tushirish
    application.run_polling()
  
if __name__ == "__main__":
    main()