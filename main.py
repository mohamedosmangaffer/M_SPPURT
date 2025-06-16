M.store_sppurt_bot – كود نهائي شامل

import os from telegram import Update, ReplyKeyboardMarkup, KeyboardButton from telegram.ext import (ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, ConversationHandler, filters)

LANG, MENU, SERVICE_STEP = range(3) USER_LANG = {} USER_STATE = {} USER_DATA = {}

def get_lang(user_id): return USER_LANG.get(user_id, 'ar')

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int: text = ( "🔰 Welcome to M.store – Your Gateway to Premium Digital Services\n" "🔰 مرحبًا بك في متجر M.store – بوابتك للخدمات الرقمية المتميزة\n\n" "👇 Please select your preferred language to continue\n" "👇 يرجى اختيار لغتك المفضلة للمتابعة" ) kb = ReplyKeyboardMarkup( [[KeyboardButton("🇸🇦 العربية"), KeyboardButton("🇬🇧 English")]], resize_keyboard=True) await update.message.reply_text(text, reply_markup=kb) return LANG

async def set_lang(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int: lang = 'ar' if 'عرب' in update.message.text else 'en' user_id = update.effective_user.id USER_LANG[user_id] = lang return await main_menu(update, ctx)

async def main_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int: lang = get_lang(update.effective_user.id) if lang == 'ar': text = ( "🎯 مرحبًا بك في M.store\n\n" "⚡ نقدم لك خدمات رقمية مميزة بجودة وموثوقية عالية.\n" "📞 تواصل معنا في أي وقت: https://t.me/Mstore_bot_support\n" "📱 أو واتساب: +249965812441\n\n" "📌 اختر الخدمة

