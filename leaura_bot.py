import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("BOT_TOKEN", "8693514553:AAEKJnHc5Mxpx4nvN2ez8DPW66CCoWpkwSg")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "")
ADMIN_ID = 1196450378

NAME, PHONE, BUSINESS, SERVICE, BUDGET, CONFIRM = range(6)

# ══════════════════════════════════════════
# ТЕКСТЫ
# ══════════════════════════════════════════

WELCOME_TEXT = """✦ *LE AURA — AI Automation Agency*

Автоматизируем будущее вашего бизнеса.

🎙️ Голосовой ИИ-Ресепшонист
💬 ИИ-боты Telegram и WhatsApp
🤵 AI-Консьерж для гостей

_50+ проектов · запуск за 7 дней · результат или возврат_"""

ABOUT_TEXT = """👑 *О нас — LE AURA*

Premium AI-агентство нового поколения.
Специализируемся на автоматизации гостиничного бизнеса.

📊 *Наши результаты:*
• 3.2× рост конверсии у клиентов
• −80% рутинных задач
• 7 дней от заявки до запуска
• 50+ успешных проектов

💎 *Почему выбирают нас:*
✦ Индивидуальный подход к каждому проекту
✦ Поддержка 24/7 после запуска
✦ Фиксированные цены без скрытых доп.
✦ Результат или возврат денег

🌐 leaura.uz"""

SERVICES_TEXT = """⚡ *Наши услуги*

🎙️ *Голосовой ИИ-Ресепшонист*
Принимает звонки и бронирования 24/7 — без выходных и праздников. Русский и английский. Среднее время ответа: менее 3 секунд.
_от $500 настройка + $250/мес_

━━━━━━━━━━━━━━━━━
💬 *ИИ-боты Telegram и WhatsApp*
Мгновенные ответы на вопросы гостей. Онлайн-бронирование прямо в чате. Автоматические напоминания о заезде.
_от $500 настройка + $250/мес_

━━━━━━━━━━━━━━━━━
🤵 *AI-Консьерж для гостей*
После заселения гость пишет: «Где поесть рядом?», «Как вызвать такси?» — ИИ знает всё об отеле и городе.
_входит в тариф Pro_"""

PRICING_TEXT = """💰 *Тарифы для гостиниц*

━━━━━━━━━━━━━━━━━
🏨 *Basic — $500 настройка + $250/мес*

✦ Голосовой ИИ-Ресепшонист — звонки и бронирования 24/7
✦ WhatsApp-бот — ответы и бронирование в мессенджере
✦ Telegram-бот — напоминания и онлайн-бронирование

━━━━━━━━━━━━━━━━━
👑 *Pro — $800 настройка + $250/мес*

✦ Всё из тарифа Basic
✦ Сайт отеля — лендинг с онлайн-бронированием
✦ AI-Консьерж — отвечает гостям после заселения

━━━━━━━━━━━━━━━━━
💡 *ROI первого месяца:*
1 пропущенный звонок = $50–150 потерь
При 10 доп. бронях выручка до $1500
Инвестиция всего $250/мес

_Оплата: Payme, Click, Uzcard, Humo, перевод_"""

PORTFOLIO_TEXT = """🏆 *Кейсы LE AURA*

━━━━━━━━━━━━━━━━━
🏋️ *Фитнес-клуб, Ташкент*
Telegram-бот для записи + CRM
📈 Результат: +340% заявок за месяц

━━━━━━━━━━━━━━━━━
🛍️ *E-commerce магазин*
AI-автоматизация + чат-бот на сайте
📈 Конверсия с 2% до 7.3%

━━━━━━━━━━━━━━━━━
🏗️ *Строительная компания*
Полный пакет автоматизации
📈 −80% ручной работы

━━━━━━━━━━━━━━━━━
🍕 *Сеть ресторанов*
Бот для заказов + CRM
📈 +220% онлайн-заказов
━━━━━━━━━━━━━━━━━

_«За первую неделю заявок стало втрое больше. Не теряем ни одного клиента даже ночью.»_
— Азиз Мамаджанов, владелец фитнес-клуба"""

CONTACT_TEXT = """📞 *Связаться с LE AURA*

✈️ Telegram: @leaura\\_ai
🌐 Сайт: leaura.uz

⏰ Режим работы: Пн–Сб, 9:00 — 21:00
⚡ Отвечаем в течение 15 минут

_Или оставь заявку — мы сами свяжемся!_"""

FAQ_TEXT = """❓ *Частые вопросы*

*Сколько времени занимает запуск?*
Базовый пакет — 5 рабочих дней. Полный Pro-пакет — до 14 дней.

*Что входит в $250/мес?*
Поддержка 24/7, мониторинг, обновления, новые функции. Никаких скрытых платежей.

*Нужны ли технические знания?*
Нет. Делаем всё под ключ и обучаем команду. Управление через простую панель.

*Гарантия результата?*
Да. Если за 30 дней нет измеримого результата — возврат денег или доработка бесплатно.

*Работаете ли с малым бизнесом?*
Да, есть пакеты от $300. Автоматизация доступна для бизнеса любого размера."""

# ══════════════════════════════════════════
# КЛАВИАТУРЫ
# ══════════════════════════════════════════

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎙️ Услуги", callback_data="services"),
         InlineKeyboardButton("💰 Тарифы", callback_data="pricing")],
        [InlineKeyboardButton("🏆 Кейсы", callback_data="portfolio"),
         InlineKeyboardButton("👑 О нас", callback_data="about")],
        [InlineKeyboardButton("❓ FAQ", callback_data="faq"),
         InlineKeyboardButton("📞 Контакты", callback_data="contact")],
        [InlineKeyboardButton("🚀 Оставить заявку", callback_data="apply")],
    ])

def back_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Оставить заявку", callback_data="apply")],
        [InlineKeyboardButton("◀️ Главное меню", callback_data="main")]
    ])

def service_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎙️ Голосовой ИИ-Ресепшонист", callback_data="svc_voice")],
        [InlineKeyboardButton("💬 ИИ-боты Telegram и WhatsApp", callback_data="svc_tg")],
        [InlineKeyboardButton("🤵 AI-Консьерж для гостей", callback_data="svc_concierge")],
        [InlineKeyboardButton("🏨 Пакет Basic ($500+$250/мес)", callback_data="svc_basic")],
        [InlineKeyboardButton("👑 Пакет Pro ($800+$250/мес)", callback_data="svc_pro")],
        [InlineKeyboardButton("🔧 Другое / Индивидуально", callback_data="svc_custom")],
    ])

def budget_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏨 Basic — $500+$250/мес", callback_data="b_basic")],
        [InlineKeyboardButton("👑 Pro — $800+$250/мес", callback_data="b_pro")],
        [InlineKeyboardButton("💼 Индивидуальный проект", callback_data="b_custom")],
        [InlineKeyboardButton("💬 Обсудить с менеджером", callback_data="b_discuss")],
    ])

def confirm_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Подтвердить заявку", callback_data="confirm_yes")],
        [InlineKeyboardButton("✏️ Начать заново", callback_data="apply")]
    ])

# ══════════════════════════════════════════
# ХЭНДЛЕРЫ
# ══════════════════════════════════════════

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    user = update.message.from_user
    name = user.first_name or "Гость"
    await update.message.reply_text(
        f"✦ Добро пожаловать, *{name}*!\n\n" + WELCOME_TEXT,
        parse_mode='Markdown',
        reply_markup=main_menu()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "main":
        await query.edit_message_text(WELCOME_TEXT, parse_mode='Markdown', reply_markup=main_menu())
    elif data == "about":
        await query.edit_message_text(ABOUT_TEXT, parse_mode='Markdown', reply_markup=back_menu())
    elif data == "services":
        await query.edit_message_text(SERVICES_TEXT, parse_mode='Markdown', reply_markup=back_menu())
    elif data == "pricing":
        await query.edit_message_text(PRICING_TEXT, parse_mode='Markdown', reply_markup=back_menu())
    elif data == "portfolio":
        await query.edit_message_text(PORTFOLIO_TEXT, parse_mode='Markdown', reply_markup=back_menu())
    elif data == "contact":
        await query.edit_message_text(CONTACT_TEXT, parse_mode='Markdown', reply_markup=back_menu())
    elif data == "faq":
        await query.edit_message_text(FAQ_TEXT, parse_mode='Markdown', reply_markup=back_menu())


async def start_application(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data.clear()
    await query.edit_message_text(
        "🚀 *Оставить заявку*\n\n"
        "Шаг 1 из 4 — Как вас зовут?\n\n"
        "_Введите ваше имя:_",
        parse_mode='Markdown'
    )
    return NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text(
        f"✦ Приятно познакомиться, *{update.message.text}*!\n\n"
        "Шаг 2 из 4 — Ваш Telegram или номер телефона:",
        parse_mode='Markdown'
    )
    return PHONE


async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['phone'] = update.message.text
    await update.message.reply_text(
        "🏢 Шаг 3 из 4 — Расскажите о вашем бизнесе:\n\n"
        "_Например: отель 30 номеров в Ташкенте, фитнес-клуб, агентство недвижимости..._",
        parse_mode='Markdown'
    )
    return BUSINESS


async def get_business(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['business'] = update.message.text
    await update.message.reply_text(
        "⚡ Шаг 4 из 4 — Какое решение вас интересует?",
        parse_mode='Markdown',
        reply_markup=service_menu()
    )
    return SERVICE


async def select_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    services = {
        "svc_voice": "🎙️ Голосовой ИИ-Ресепшонист",
        "svc_tg": "💬 ИИ-боты Telegram и WhatsApp",
        "svc_concierge": "🤵 AI-Консьерж для гостей",
        "svc_basic": "🏨 Пакет Basic",
        "svc_pro": "👑 Пакет Pro",
        "svc_custom": "🔧 Индивидуальное решение",
    }
    context.user_data['service'] = services.get(query.data, "Не указано")
    await query.edit_message_text(
        f"✅ Выбрано: *{context.user_data['service']}*\n\n"
        "Какой бюджет вы рассматриваете?",
        parse_mode='Markdown',
        reply_markup=budget_menu()
    )
    return BUDGET


async def select_budget(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    budgets = {
        "b_basic": "Basic — $500 настройка + $250/мес",
        "b_pro": "Pro — $800 настройка + $250/мес",
        "b_custom": "Индивидуальный проект",
        "b_discuss": "Хочу обсудить с менеджером",
    }
    context.user_data['budget'] = budgets.get(query.data, "Не указано")

    name = context.user_data.get('name', '—')
    phone = context.user_data.get('phone', '—')
    service = context.user_data.get('service', '—')
    budget = context.user_data.get('budget', '—')
    business = context.user_data.get('business', '—')

    summary = (
        "📋 *Проверьте заявку:*\n\n"
        f"👤 Имя: *{name}*\n"
        f"📱 Контакт: *{phone}*\n"
        f"🏢 Бизнес: *{business}*\n"
        f"⚡ Решение: *{service}*\n"
        f"💰 Бюджет: *{budget}*\n\n"
        "_Всё верно?_"
    )
    await query.edit_message_text(summary, parse_mode='Markdown', reply_markup=confirm_menu())
    return CONFIRM


async def confirm_application(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    name = context.user_data.get('name', '—')
    phone = context.user_data.get('phone', '—')
    service = context.user_data.get('service', '—')
    budget = context.user_data.get('budget', '—')
    business = context.user_data.get('business', '—')
    user = query.from_user

    await query.edit_message_text(
        "✅ *Заявка принята!*\n\n"
        "Спасибо! Мы свяжемся с вами в течение *15 минут*.\n\n"
        "✦ *LE AURA* — автоматизируем будущее вашего бизнеса\n\n"
        "_Пока ждёте — изучите наши кейсы 👇_",
        parse_mode='Markdown',
        reply_markup=back_menu()
    )

    if ADMIN_ID:
        admin_msg = (
            "🔥 *НОВАЯ ЗАЯВКА — LE AURA*\n\n"
            f"👤 Имя: {name}\n"
            f"📱 Контакт: {phone}\n"
            f"🏢 Бизнес: {business}\n"
            f"⚡ Решение: {service}\n"
            f"💰 Бюджет: {budget}\n\n"
            f"👤 TG: @{user.username or 'нет'} | ID: {user.id}"
        )
        try:
            await context.bot.send_message(ADMIN_ID, admin_msg, parse_mode='Markdown')
        except Exception as e:
            logging.error(f"Admin notify error: {e}")

    context.user_data.clear()
    return ConversationHandler.END


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✦ Используй кнопки меню или напиши /start",
        reply_markup=main_menu()
    )

# ══════════════════════════════════════════
# ЗАПУСК
# ══════════════════════════════════════════

def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_application, pattern="^apply$")],
        states={
            NAME:     [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            PHONE:    [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            BUSINESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_business)],
            SERVICE:  [CallbackQueryHandler(select_service, pattern="^svc_")],
            BUDGET:   [CallbackQueryHandler(select_budget, pattern="^b_")],
            CONFIRM:  [CallbackQueryHandler(confirm_application, pattern="^confirm_yes$")],
        },
        fallbacks=[CommandHandler("start", start)],
        per_message=False,
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown))

    if WEBHOOK_URL:
        PORT = int(os.environ.get("PORT", 8443))
        print("LE AURA Bot started (webhook)!")
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            webhook_url=WEBHOOK_URL,
        )
    else:
        print("LE AURA Bot started (polling)!")
        app.run_polling()

if __name__ == "__main__":
    main()
