M.store Market Bot - النسخة النهائية

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove from telegram.ext import (ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, ConversationHandler, filters)

LANG, MENU, SERVICE_FLOW, INPUT_DETAILS, PAYMENT = range(5) USER_LANG = {} USER_DATA = {}

def get_main_menu(lang): if lang == 'ar': text = ( "🎯 مرحبًا بك في M.store\n" "بوابتك للخدمات الرقمية الاحترافية.\n" "💡 اختر نوع الخدمة، أو تواصل معنا:\n" "📞 تيليجرام الدعم: https://t.me/Mstore_bot_support\n" "📱 واتساب: +249965812441" ) buttons = [["🔐 خدمات الهواتف وتخطي الحمايات"], ["📲 اشتراكات التطبيقات", "🎮 خدمات الألعاب"], ["🛰️ اشتراك ستارلينك"], ["🚫 الخدمات المتوقفة حاليًا"], ["📞 الدعم الفني", "📝 الملاحظات وآراء العملاء"]] else: text = ( "🎯 Welcome to M.store\n" "Your gateway to premium digital services.\n" "💡 Choose a service or contact us:\n" "📞 Telegram Support: https://t.me/Mstore_bot_support\n" "📱 WhatsApp: +249965812441" ) buttons = [["🔐 Phone & Bypass Services"], ["📲 App Subscriptions", "🎮 Game Services"], ["🛰️ Starlink Subscription"], ["🚫 Currently Unavailable Services"], ["📞 Technical Support", "📝 Feedback"]]

return text, ReplyKeyboardMarkup(buttons, resize_keyboard=True)

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int: text = ( "🔰 Welcome to M.store – Your Gateway to Premium Digital Services\n" "🔰 مرحبًا بك في متجر M.store – بوابتك للخدمات الرقمية المتميزة\n\n" "👇 Please select your preferred language to continue\n" "👇 يرجى اختيار لغتك المفضلة للمتابعة" ) kb = ReplyKeyboardMarkup([["🇸🇦 العربية", "🇬🇧 English"]], resize_keyboard=True) await update.message.reply_text(text, reply_markup=kb) return LANG

async def set_lang(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int: USER_LANG[update.effective_user.id] = 'ar' if '🇸🇦' in update.message.text else 'en' return await main_menu(update, ctx)

async def main_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int: lang = USER_LANG.get(update.effective_user.id, 'en') text, menu = get_main_menu(lang) await update.message.reply_text(text, reply_markup=menu, parse_mode="Markdown") return MENU

async def handle_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int: text = update.message.text lang = USER_LANG.get(update.effective_user.id, 'en') USER_DATA[update.effective_user.id] = {"service": text}

if text == "🛰️ اشتراك ستارلينك" or text == "🛰️ Starlink Subscription":
    msg = "📡 اختر نوع الاشتراك المطلوب لخدمة ستارلينك:" if lang == 'ar' else "📡 Select your desired Starlink plan:"
    buttons = [["📶 اشتراك منزلي", "📦 اشتراك متنقل"], ["🔙 رجوع"]]
    await update.message.reply_text(msg, reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))
    return SERVICE_FLOW
elif text == "🔙 رجوع":
    return await main_menu(update, ctx)
else:
    return await main_menu(update, ctx)

async def service_flow(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int: USER_DATA[update.effective_user.id]["plan"] = update.message.text lang = USER_LANG.get(update.effective_user.id, 'en')

msg = "📝 الرجاء إدخال البيانات المطلوبة (الاسم، العنوان، رقم الهاتف):" if lang == 'ar' \
      else "📝 Please enter your full details (Name, Address, Phone):"
await update.message.reply_text(msg, reply_markup=ReplyKeyboardMarkup([["🔙 رجوع"]], resize_keyboard=True))
return INPUT_DETAILS

async def input_details(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int: USER_DATA[update.effective_user.id]["details"] = update.message.text lang = USER_LANG.get(update.effective_user.id, 'en')

msg = "💳 اختر طريقة الدفع:" if lang == 'ar' else "💳 Choose your payment method:"
buttons = [["💰 تحويل بنكي", "💳 بطاقة/فيزا"], ["🔙 رجوع"]]
await update.message.reply_text(msg, reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))
return PAYMENT

async def payment_step(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int: USER_DATA[update.effective_user.id]["payment"] = update.message.text lang = USER_LANG.get(update.effective_user.id, 'en')

# إرسال الطلب للتليجرام (وربما واتساب لاحقًا)
summary = USER_DATA[update.effective_user.id]
msg = f"✅ طلب جديد من المستخدم: @{update.effective_user.username}\n" \
      f"الخدمة: {summary['service']}\nالنوع: {summary['plan']}\nالبيانات: {summary['details']}\nطريقة الدفع: {summary['payment']}"
await ctx.bot.send_message(chat_id='@Mstore_bot_support', text=msg)
await update.message.reply_text("✅ تم استلام طلبك بنجاح! سيتم التواصل معك قريبًا.", reply_markup=ReplyKeyboardRemove())
return await main_menu(update, ctx)

if name == "main": import os, asyncio from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
app = ApplicationBuilder().token(TOKEN).build()

conv = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        LANG: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_lang)],
        MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu)],
        SERVICE_FLOW: [MessageHandler(filters.TEXT & ~filters.COMMAND, service_flow)],
        INPUT_DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, input_details)],
        PAYMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, payment_step)],
    },
    fallbacks=[MessageHandler(filters.Regex("^🔙 رجوع$"), main_menu)]
)

app.add_handler(conv)
print("✅ M.store bot is running...")
asyncio.run(app.run_polling())

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder, ContextTypes, CommandHandler,
    MessageHandler, ConversationHandler, filters
)

LANG, MENU, SERVICE_FLOW, INPUT_DETAILS, PAYMENT = range(5)
USER_LANG = {}
USER_DATA = {}

def get_main_menu(lang):
    if lang == 'ar':
        text = (
            "🎯 مرحبًا بك في M.store\n"
            "بوابتك للخدمات الرقمية الاحترافية.\n"
            "💡 اختر نوع الخدمة، أو تواصل معنا:\n"
            "📞 تيليجرام الدعم: https://t.me/Mstore_bot_support\n"
            "📱 واتساب: +249965812441"
        )
        buttons = [
            ["🔐 خدمات الهواتف وتخطي الحمايات"],
            ["📲 اشتراكات التطبيقات", "🎮 خدمات الألعاب"],
            ["🛰️ اشتراك ستارلينك"],
            ["🚫 الخدمات المتوقفة حاليًا"],
            ["📞 الدعم الفني", "📝 الملاحظات وآراء العملاء"]
        ]
    else:
        text = (
            "🎯 Welcome to M.store\n"
            "Your gateway to premium digital services.\n"
            "💡 Choose a service or contact us:\n"
            "📞 Telegram Support: https://t.me/Mstore_bot_support\n"
            "📱 WhatsApp: +249965812441"
        )
        buttons = [
            ["🔐 Phone & Bypass Services"],
            ["📲 App Subscriptions", "🎮 Game Services"],
            ["🛰️ Starlink Subscription"],
            ["🚫 Currently Unavailable Services"],
            ["📞 Technical Support", "📝 Feedback"]
        ]
    return text, ReplyKeyboardMarkup(buttons, resize_keyboard=True)

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    text = (
        "🔰 Welcome to M.store – Your Gateway to Premium Digital Services\n"
        "🔰 مرحبًا بك في متجر M.store – بوابتك للخدمات الرقمية المتميزة\n\n"
        "👇 Please select your preferred language to continue\n"
        "👇 يرجى اختيار لغتك المفضلة للمتابعة"
    )
    kb = ReplyKeyboardMarkup([["🇸🇦 العربية", "🇬🇧 English"]], resize_keyboard=True)
    await update.message.reply_text(text, reply_markup=kb)
    return LANG

async def set_lang(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    USER_LANG[update.effective_user.id] = 'ar' if '🇸🇦' in update.message.text else 'en'
    return await main_menu(update, ctx)

async def main_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    lang = USER_LANG.get(update.effective_user.id, 'en')
    text, menu = get_main_menu(lang)
    await update.message.reply_text(text, reply_markup=menu)
    return MENU

async def handle_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    lang = USER_LANG.get(update.effective_user.id, 'en')
    USER_DATA[update.effective_user.id] = {"service": text}

    if text in ["🛰️ اشتراك ستارلينك", "🛰️ Starlink Subscription"]:
        msg = "📡 اختر نوع الاشتراك المطلوب لخدمة ستارلينك:" if lang == 'ar' else "📡 Select your desired Starlink plan:"
        buttons = [["📶 اشتراك منزلي", "📦 اشتراك متنقل"], ["🔙 رجوع"]]
        await update.message.reply_text(msg, reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))
        return SERVICE_FLOW
    elif text == "🔙 رجوع":
        return await main_menu(update, ctx)
    else:
        return await main_menu(update, ctx)

async def service_flow(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    USER_DATA[update.effective_user.id]["plan"] = update.message.text
    lang = USER_LANG.get(update.effective_user.id, 'en')
    msg = "📝 الرجاء إدخال البيانات المطلوبة (الاسم، العنوان، رقم الهاتف):" if lang == 'ar' else "📝 Please enter your full details (Name, Address, Phone):"
    await update.message.reply_text(msg, reply_markup=ReplyKeyboardMarkup([["🔙 رجوع"]], resize_keyboard=True))
    return INPUT_DETAILS

async def input_details(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    USER_DATA[update.effective_user.id]["details"] = update.message.text
    lang = USER_LANG.get(update.effective_user.id, 'en')
    msg = "💳 اختر طريقة الدفع:" if lang == 'ar' else "💳 Choose your payment method:"
    buttons = [["💰 تحويل بنكي", "💳 بطاقة/فيزا"], ["🔙 رجوع"]]
    await update.message.reply_text(msg, reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))
    return PAYMENT

async def payment_step(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    USER_DATA[update.effective_user.id]["payment"] = update.message.text
    lang = USER_LANG.get(update.effective_user.id, 'en')

    summary = USER_DATA[update.effective_user.id]
    msg = (
        f"✅ طلب جديد من المستخدم: @{update.effective_user.username}\n"
        f"الخدمة: {summary['service']}\n"
        f"النوع: {summary['plan']}\n"
        f"البيانات: {summary['details']}\n"
        f"طريقة الدفع: {summary['payment']}"
    )
    await ctx.bot.send_message(chat_id='@Mstore_bot_support', text=msg)
    await update.message.reply_text("✅ تم استلام طلبك بنجاح! سيتم التواصل معك قريبًا.", reply_markup=ReplyKeyboardRemove())
    return await main_menu(update, ctx)

if __name__ == "__main__":
    import os
    import asyncio
    from dotenv import load_dotenv

    load_dotenv()
    TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANG: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_lang)],
            MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu)],
            SERVICE_FLOW: [MessageHandler(filters.TEXT & ~filters.COMMAND, service_flow)],
            INPUT_DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, input_details)],
            PAYMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, payment_step)],
        },
        fallbacks=[MessageHandler(filters.Regex("^🔙 رجوع$"), main_menu)]
    )

    app.add_handler(conv)
    print("✅ M.store bot is running...")
    asyncio.run(app.run_polling())
