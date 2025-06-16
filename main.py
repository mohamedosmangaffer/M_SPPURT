from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
)

# مراحل المحادثة
LANG, MENU, SERVICE_SELECTION, INPUT_DETAILS, PAYMENT = range(5)

# حفظ بيانات المستخدم (لغة، بيانات الطلب)
USER_LANG = {}
USER_DATA = {}

def get_main_menu(lang):
    if lang == "ar":
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
            ["📞 الدعم الفني", "📝 الملاحظات وآراء العملاء"],
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
            ["📞 Technical Support", "📝 Feedback"],
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
    text = update.message.text
    if "🇸🇦" in text:
        USER_LANG[update.effective_user.id] = "ar"
    else:
        USER_LANG[update.effective_user.id] = "en"
    return await main_menu(update, ctx)

async def main_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    lang = USER_LANG.get(update.effective_user.id, "en")
    text, menu = get_main_menu(lang)
    await update.message.reply_text(text, reply_markup=menu)
    return MENU

# خدمات الهواتف (قوائم فرعية)
PHONE_BYPASS_COMPANIES_AR = [
    "Samsung",
    "Xiaomi",
    "Huawei",
    "Oppo",
    "Realme",
    "Infinix",
    "Vivo",
    "Nokia",
    "Tecno",
    "Sony",
    "LG",
    "Motorola",
]
PHONE_BYPASS_COMPANIES_EN = PHONE_BYPASS_COMPANIES_AR

ICLOUD_DEVICES_AR = [
    "iPhone 6",
    "iPhone 7",
    "iPhone 8",
    "iPhone X",
    "iPhone 11",
    "iPhone 12",
    "iPhone 13",
    "iPhone 14",
    "iPhone 15",
    "iPhone 15 Pro Max",
    "iPad",
    "iPod",
]
ICLOUD_DEVICES_EN = ICLOUD_DEVICES_AR

NETWORK_PROVIDERS_AR = [
    "AT&T",
    "Verizon",
    "T-Mobile",
    "Sprint",
    "Orange",
    "Vodafone",
]
NETWORK_PROVIDERS_EN = NETWORK_PROVIDERS_AR

# اشتراكات التطبيقات
APP_SUBSCRIPTIONS_AR = ["نتفليكس", "ChatGPT", "تطبيقات أخرى"]
APP_SUBSCRIPTIONS_EN = ["Netflix", "ChatGPT", "Other Apps"]

# خدمات الألعاب
GAME_SERVICES_AR = ["PUBG", "Free Fire", "ألعاب أخرى"]
GAME_SERVICES_EN = ["PUBG", "Free Fire", "Other Games"]

# اشتراكات ستارلينك
STARLINK_PLANS_AR = ["اشتراك منزلي", "اشتراك متنقل"]
STARLINK_PLANS_EN = ["Home Subscription", "Mobile Subscription"]

# الخدمات المتوقفة
UNAVAILABLE_SERVICES_AR = ["شحن رصيد", "دفع فواتير إنترنت", "أرقام وهمية"]
UNAVAILABLE_SERVICES_EN = ["Recharge", "Internet Bills Payment", "Virtual Numbers"]

async def handle_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    lang = USER_LANG.get(user_id, "en")
    text = update.message.text
    USER_DATA[user_id] = {"service": text}

    # دعم الفني والملاحظات
    if text in ["📞 الدعم الفني", "📞 Technical Support"]:
        msg_ar = (
            "📞 للدعم الفني:\n"
            "تيليجرام: https://t.me/Mstore_bot_support\n"
            "واتساب: +249965812441"
        )
        msg_en = (
            "📞 For technical support:\n"
            "Telegram: https://t.me/Mstore_bot_support\n"
            "WhatsApp: +249965812441"
        )
        await update.message.reply_text(msg_ar if lang == "ar" else msg_en, reply_markup=ReplyKeyboardMarkup([["🔙 رجوع" if lang == "ar" else "🔙 Back"]], resize_keyboard=True))
        return MENU

    if text in ["📝 الملاحظات وآراء العملاء", "📝 Feedback"]:
        prompt = "📝 الرجاء كتابة ملاحظاتك أو رأيك:" if lang == "ar" else "📝 Please write your feedback:"
        await update.message.reply_text(prompt, reply_markup=ReplyKeyboardMarkup([["🔙 رجوع" if lang == "ar" else "🔙 Back"]], resize_keyboard=True))
        return INPUT_DETAILS

    # الخدمات المتوقفة
    if text in ["🚫 الخدمات المتوقفة حاليًا", "🚫 Currently Unavailable Services"]:
        buttons = [[service] for service in (UNAVAILABLE_SERVICES_AR if lang == "ar" else UNAVAILABLE_SERVICES_EN)]
        buttons.append(["🔙 رجوع" if lang == "ar" else "🔙 Back"])
        msg = "🚫 الخدمات المتوقفة حاليًا:" if lang == "ar" else "🚫 Currently Unavailable Services:"
        await update.message.reply_text(msg, reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))
        return MENU

    # اشتراك ستارلينك
    if text in ["🛰️ اشتراك ستارلينك", "🛰️ Starlink Subscription"]:
        buttons = [STARLINK_PLANS_AR if lang == "ar" else STARLINK_PLANS_EN]
        buttons.append(["🔙 رجوع" if lang == "ar" else "🔙 Back"])
        msg = "📡 اختر نوع الاشتراك المطلوب لخدمة ستارلينك:" if lang == "ar" else "📡 Select your desired Starlink plan:"
        await update.message.reply_text(msg, reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))
        return SERVICE_SELECTION

    # اشتراكات التطبيقات
    if text in ["📲 اشتراكات التطبيقات", "📲 App Subscriptions"]:
        buttons = [[s] for s in (APP_SUBSCRIPTIONS_AR if lang == "ar" else APP_SUBSCRIPTIONS_EN)]
        buttons.append(["🔙 رجوع" if lang == "ar" else "🔙 Back"])
        msg = "📲 اختر الاشتراك المطلوب:" if lang == "ar" else "📲 Select the subscription you want:"
        await update.message.reply_text(msg, reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))
        return SERVICE_SELECTION

    # خدمات الألعاب
    if text in ["🎮 خدمات الألعاب", "🎮 Game Services"]:
        buttons = [[s] for s in (GAME_SERVICES_AR if lang == "ar" else GAME_SERVICES_EN)]
        buttons.append(["🔙 رجوع" if lang == "ar" else "🔙 Back"])
        msg = "🎮 اختر اللعبة أو الخدمة المطلوبة:" if lang == "ar" else "🎮 Select the game or service:"
        await update.message.reply_text(msg, reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))
        return SERVICE_SELECTION

    # خدمات الهواتف وتخطي الحمايات
    if text in ["🔐 خدمات الهواتف وتخطي الحمايات", "🔐 Phone & Bypass Services"]:
        main_buttons = [
            ["🔓 تخطي FRP", "🍏 تخطي iCloud"],
            ["📡 تخطي حمايات الشبكات", "📶 كسر شبكة Wi-Fi"],
            ["🔙 رجوع" if lang == "ar" else "🔙 Back"],
        ]
        msg = "🔐 اختر الخدمة المطلوبة:" if lang == "ar" else "🔐 Choose the desired service:"
        await update.message.reply_text(msg, reply_markup=ReplyKeyboardMarkup(main_buttons, resize_keyboard=True))
        return SERVICE_SELECTION

    # تخطي FRP
    if text == "🔓 تخطي FRP":
        buttons = [[c] for c in (PHONE_BYPASS_COMPANIES_AR if lang == "ar" else PHONE_BYPASS_COMPANIES_EN)]
        buttons.append(["🔙 رجوع" if lang == "ar" else "🔙 Back"])
        msg = "📱 اختر شركة الهاتف:" if lang == "ar" else "📱 Select phone company:"
        await update.message.reply_text(msg, reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))
        return SERVICE_SELECTION

    # تخطي iCloud
    if text == "🍏 تخطي iCloud":
        buttons = [[d] for d in (ICLOUD_DEVICES_AR if lang == "ar" else ICLOUD_DEVICES_EN)]
        buttons.append(["🔙 رجوع" if lang == "ar" else "🔙 Back"])
        msg = "🍏 اختر جهاز Apple:" if lang == "ar" else "🍏 Select Apple device:"
        await update.message.reply_text(msg, reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))
        return SERVICE_SELECTION

    # تخطي حمايات الشبكات
    if text == "📡 تخطي حمايات الشبكات":
        buttons = [[p] for p in (NETWORK_PROVIDERS_AR if lang == "ar" else NETWORK_PROVIDERS_EN)]
        buttons.append(["🔙 رجوع" if lang == "ar" else "🔙 Back"])
        msg = "📡 اختر شركة الشبكة:" if lang == "ar" else "📡 Select network provider:"
        await update.message.reply_text(msg, reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))
        return SERVICE_SELECTION

    # كسر شبكة Wi-Fi
    if text == "📶 كسر شبكة Wi-Fi":
        msg = (
            "📶 هذه الخدمة تعمل على كل الشرائح.\n"
            "📝 الرجاء إدخال رقم IMEI أو الرقم التسلسلي:"
            if lang == "ar"
            else "📶 This service works on all SIM cards.\n📝 Please enter IMEI or serial number:"
        )
        await update.message.reply_text(msg, reply_markup=ReplyKeyboardMarkup([["🔙 رجوع" if lang == "ar" else "🔙 Back"]], resize_keyboard=True))
        return INPUT_DETAILS

    # إذا أي خيار فرعي تم اختياره (شركات، أجهزة، مزودين شبكات، ألعاب، اشتراكات.. إلخ)
    # نعتبره نوع الخطة/الخدمة التي سيتم طلبها، وننتقل لطلب البيانات
    service_categories = (
        PHONE_BYPASS_COMPANIES_AR
        + ICLOUD_DEVICES_AR
        + NETWORK_PROVIDERS_AR
        + APP_SUBSCRIPTIONS_AR
        + GAME_SERVICES_AR
        + STARLINK_PLANS_AR
        + UNAVAILABLE_SERVICES_AR
    ) if lang == "ar" else (
        PHONE_BYPASS_COMPANIES_EN
        + ICLOUD_DEVICES_EN
        + NETWORK_PROVIDERS_EN
        + APP_SUBSCRIPTIONS_EN
        + GAME_SERVICES_EN
        + STARLINK_PLANS_EN
        + UNAVAILABLE_SERVICES_EN
    )

    if text in service_categories:
        USER_DATA[user_id]["plan"] = text
        prompt = (
            "📝 الرجاء إدخال البيانات المطلوبة (الاسم، العنوان، رقم الهاتف، IMEI إذا طلب):"
            if lang == "ar"
            else "📝 Please enter your full details (Name, Address, Phone, IMEI if needed):"
        )
        await update.message.reply_text(prompt, reply_markup=ReplyKeyboardMarkup([["🔙 رجوع" if lang == "ar" else "🔙 Back"]], resize_keyboard=True))
        return INPUT_DETAILS

    # زر رجوع في القائمة الرئيسية
    if text in ["🔙 رجوع", "🔙 Back"]:
        return await main_menu(update, ctx)

    # أي رسالة أخرى تعيد القائمة الرئيسية
    return await main_menu(update, ctx)

async def input_details(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    USER_DATA[user_id]["details"] = update.message.text
    lang = USER_LANG.get(user_id, "en")

    msg = "💳 اختر طريقة الدفع:" if lang == "ar" else "💳 Choose your payment method:"
    buttons = [["💰 تحويل بنكي", "💳 بطاقة/فيزا"], ["🔙 رجوع" if lang == "ar" else "🔙 Back"]]
    await update.message.reply_text(msg, reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))
    return PAYMENT

async def payment_step(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    USER_DATA[user_id]["payment"] = update.message.text
    lang = USER_LANG.get(user_id, "en")

    summary = USER_DATA[user_id]
    username = update.effective_user.username or "NoUsername"

    msg = (
        f"✅ طلب جديد من المستخدم: @{username}\n"
        f"الخدمة: {summary.get('service', '')}\n"
        f"النوع: {summary.get('plan', '')}\n"
        f"البيانات: {summary.get('details', '')}\n"
        f"طريقة الدفع: {summary.get('payment', '')}"
    )
    # إرسال الطلب لقناة الدعم
    await ctx.bot.send_message(chat_id="@Mstore_bot_support", text=msg)

    # تأكيد الاستلام للمستخدم
    confirm_msg = "✅ تم استلام طلبك بنجاح! سيتم التواصل معك قريبًا." if lang == "ar" else "✅ Your order has been received successfully! We will contact you soon."
    await update.message.reply_text(confirm_msg, reply_markup=ReplyKeyboardRemove())

    # إعادة المستخدم للقائمة الرئيسية
    return await main_menu(update, ctx)

if __name__ == "__main__":
    import os
    import asyncio
    from dotenv import load_dotenv

    load_dotenv()
    TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANG: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_lang)],
            MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu)],
            SERVICE_SELECTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu)],
            INPUT_DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, input_details)],
            PAYMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, payment_step)],
        },
        fallbacks=[MessageHandler(filters.Regex("^(🔙 رجوع|🔙 Back)$"), main_menu)],
        allow_reentry=True,
    )

    app.add_handler(conv_handler)

    print("✅ M.store Market Bot is running...")
    asyncio.run(app.run_polling())
