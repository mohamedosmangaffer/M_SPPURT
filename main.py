import os
import asyncio
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, ConversationHandler, filters
from dotenv import load_dotenv

# تحميل المتغيرات من .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# مراحل المحادثة
LANG, MENU, APP_SUB = range(3)

USER_LANG = {}

def get_lang(user_id):
    return USER_LANG.get(user_id, 'en')

# بدء البوت
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    txt = (
        "🔰 Welcome to M.store – Your Gateway to Premium Digital Services\n"
        "🔰 مرحبًا بك في متجر M.store – بوابتك للخدمات الرقمية المتميزة\n\n"
        "👇 Please select your preferred language to continue\n"
        "👇 يرجى اختيار لغتك المفضلة للمتابعة"
    )
    kb = [[KeyboardButton("🇸🇦 العربية"), KeyboardButton("🇬🇧 English")]]
    await update.message.reply_text(txt, reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True))
    return LANG

async def set_lang(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    uid = update.effective_user.id
    lang = 'ar' if "عرب" in update.message.text else 'en'
    USER_LANG[uid] = lang
    return await main_menu(update, ctx)

# القائمة الرئيسية
async def main_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    lang = get_lang(update.effective_user.id)
    if lang == 'ar':
        txt = (
            "🎯 مرحبًا بك في قائمة خدمات M.store\n"
            "✅ جميع الخدمات موثوقة ومجربة\n\n"
            "📞 للتواصل والدعم:\n"
            "Telegram: https://t.me/Mstore_bot_support\n"
            "WhatsApp: +249965812441"
        )
        menu = [
            ["🔐 خدمات الهواتف وتخطي الحمايات"],
            ["📲 اشتراكات التطبيقات", "🎮 خدمات الألعاب"],
            ["🛰️ اشتراك ستارلينك"],
            ["📦 الخدمات المتوقفة حاليًا"],
            ["📞 الدعم الفني", "💬 الملاحظات وآراء العملاء"]
        ]
    else:
        txt = (
            "🎯 Welcome to M.store Services Menu\n"
            "✅ All services are trusted and verified\n\n"
            "📞 Contact Support:\n"
            "Telegram: https://t.me/Mstore_bot_support\n"
            "WhatsApp: +249965812441"
        )
        menu = [
            ["🔐 Phones & Unlocking Services"],
            ["📲 App Subscriptions", "🎮 Game Services"],
            ["🛰️ Starlink Subscription"],
            ["📦 Archived Services"],
            ["📞 Technical Support", "💬 Feedback"]
        ]
    await update.message.reply_text(txt, reply_markup=ReplyKeyboardMarkup(menu, resize_keyboard=True))
    return MENU

# معالجات القائمة الرئيسية
async def handle_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    lang = get_lang(update.effective_user.id)

    if text == "📲 اشتراكات التطبيقات":
        if lang == 'ar':
            await update.message.reply_text("🔽 اختر نوع الاشتراك:", reply_markup=ReplyKeyboardMarkup([
                ["Netflix", "ChatGPT"], ["YouTube Premium", "Spotify"], ["🔙 رجوع"]], resize_keyboard=True))
        else:
            await update.message.reply_text("🔽 Select subscription:", reply_markup=ReplyKeyboardMarkup([
                ["Netflix", "ChatGPT"], ["YouTube Premium", "Spotify"], ["🔙 Back"]], resize_keyboard=True))
        return APP_SUB

    await update.message.reply_text("❗ يرجى اختيار خيار صحيح من القائمة.")
    return MENU

# تشغيل البوت
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANG: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_lang)],
            MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu)],
            APP_SUB: [MessageHandler(filters.TEXT & ~filters.COMMAND, main_menu)]
        },
        fallbacks=[]
    )

    app.add_handler(conv)
    print("✅ M.store bot is running...")
    asyncio.run(app.run_polling())
