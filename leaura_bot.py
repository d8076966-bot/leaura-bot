import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler

logging.basicConfig(level=logging.INFO)

TOKEN = "8693514553:AAEKJnHc5Mxpx4nvN2ez8DPW66CCoWpkwSg"

# Admin ID — сюда будут приходить заявки (замени на свой Telegram ID)
ADMIN_ID = 1196450378

# States
CHOOSING, NAME, PHONE, BUSINESS, SERVICE, BUDGET, CONFIRM = range(7)

# ══════════════════════════════════════════
# ТЕКСТЫ
# ══════════════════════════════════════════

WELCOME_TEXT = """✨ *Добро пожаловать в LE AURA*

Мы — premium AI-агентство нового поколения.

Автоматизируем бизнес с помощью:
🤖 Telegram-ботов
⚡ AI-автоматизации
💬 Чат-ботов для сайтов
🔗 CRM-интеграций

_Выбери что тебя интересует:_"""

ABOUT_TEXT = """👑 *О нас — LE AURA*

Мы не просто делаем ботов.
Мы строим *систему*, которая продаёт за вас 24/7.

📊 *Наши результаты:*
• +320% рост конверсии у клиентов
• -80% рутинных задач
• 7 дней от заявки до запуска
• 50+ успешных проектов

💎 *Почему выбирают нас:*
✅ Индивидуальный подход
✅ Поддержка 24/7
✅ Фиксированные цены без скрытых доп
✅ Результат или возврат денег

_Готовы автоматизировать ваш бизнес?_"""

SERVICES_TEXT = """⚡ *Наши услуги*

🤖 *Telegram-боты* — от $300
Принимают заявки, отвечают клиентам, закрывают сделки. Работают пока вы спите.

💬 *Чат-боты для сайтов* — от $400
GPT-бот на вашем сайте. Конвертирует посетителей в клиентов мгновенно.

⚡ *AI-автоматизация* — от $500
Автоматизируем любые бизнес-процессы. Рассылки, заявки, аналитика.

🔗 *CRM-интеграции* — от $350
Подключаем к AmoCRM, Bitrix24. Ни один лид не потеряется.

💼 *Полный пакет* — от $1000
Всё вместе + поддержка 3 месяца в подарок.

_Хочешь узнать точную стоимость для твоего бизнеса?_"""

PORTFOLIO_TEXT = """🏆 *Наши кейсы*

━━━━━━━━━━━━━━━━━
🏋️ *Фитнес-клуб, Ташкент*
Telegram-бот для записи + CRM
📈 Результат: +340% заявок за месяц

━━━━━━━━━━━━━━━━━
🛍️ *E-commerce магазин*
AI-автоматизация + чат-бот на сайте
📈 Результат: конверсия с 2% до 7.3%

━━━━━━━━━━━━━━━━━
🏗️ *Строительная компания*
Полный пакет автоматизации
📈 Результат: -80% ручной работы

━━━━━━━━━━━━━━━━━
🍕 *Сеть ресторанов*
Бот для заказов + CRM
📈 Результат: +220% онлайн-заказов
━━━━━━━━━━━━━━━━━"""

# ══════════════════════════════════════════
# КЛАВИАТУРЫ
# ══════════════════════════════════════════

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⚡ Наши услуги", callback_data="services"),
         InlineKeyboardButton("🏆 Кейсы", callback_data="portfolio")],
        [InlineKeyboardButton("👑 О нас", callback_data="about"),
         InlineKeyboardButton("💰 Цены", callback_data="prices")],
        [InlineKeyboardButton("🚀 Оставить заявку", callback_data="apply")],
        [InlineKeyboardButton("📞 Связаться сейчас", callback_data="contact")]
    ])

def back_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Оставить заявку", callback_data="apply")],
        [InlineKeyboardButton("◀️ Главное меню", callback_data="main")]
    ])

def service_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎙️ Голосовой ИИ-Ресепшонист", callback_data="svc_voice")],
        [InlineKeyboardButton("🤖 Telegram-бот", callback_data="svc_tg")],
        [InlineKeyboardButton("💬 Чат-бот для сайта", callback_data="svc_chat")],
        [InlineKeyboardButton("⚡ AI-автоматизация", callback_data="svc_ai")],
        [InlineKeyboardButton("🔗 CRM-интеграция", callback_data="svc_crm")],
        [InlineKeyboardButton("💼 Полный пакет", callback_data="svc_full")],
    ])

def budget_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💵 до $500", callback_data="b_500")],
        [InlineKeyboardButton("💵 $500 — $1000", callback_data="b_1000")],
        [InlineKeyboardButton("💎 $1000 — $3000", callback_data="b_3000")],
        [InlineKeyboardButton("👑 $3000+", callback_data="b_3000p")]
    ])

def confirm_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Подтвердить заявку", callback_data="confirm_yes")],
        [InlineKeyboardButton("✏️ Изменить", callback_data="apply")]
    ])

# ══════════════════════════════════════════
# ХЭНДЛЕРЫ
# ══════════════════════════════════════════

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        WELCOME_TEXT,
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

    elif data == "portfolio":
        await query.edit_message_text(PORTFOLIO_TEXT, parse_mode='Markdown', reply_markup=back_menu())

    elif data == "prices":
        prices_text = """💰 *Прайс-лист LE AURA*

🤖 *Telegram-бот*
├ Базовый — от $300
├ Продвинутый — от $600
└ С AI/GPT — от $900

💬 *Чат-бот для сайта*
├ Базовый — от $400
└ С GPT — от $700

⚡ *AI-автоматизация*
└ от $500 (зависит от задачи)

🔗 *CRM-интеграция*
└ от $350

💼 *Полный пакет*
└ от $1000 _(скидка 20%)_

━━━━━━━━━━━━━━━
🎁 *Акция:* первый бот бесплатно при заказе пакета!
━━━━━━━━━━━━━━━

_Точная стоимость — после бесплатного аудита_"""
        await query.edit_message_text(prices_text, parse_mode='Markdown', reply_markup=back_menu())

    elif data == "contact":
        contact_text = """📞 *Связаться с нами*

👤 Менеджер: @leaura\\_ai
📱 Telegram: @leaura\\_bot
🌐 Сайт: leaura.uz

⏰ Работаем: Пн-Сб 9:00 — 21:00
⚡ Отвечаем в течение 15 минут

_Или оставь заявку — мы сами свяжемся!_"""
        await query.edit_message_text(contact_text, parse_mode='Markdown', reply_markup=back_menu())


async def start_application(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data.clear()
    await query.edit_message_text(
        "🚀 *Оставить заявку*\n\nШаг 1/5 — Как вас зовут?\n\n_Введите ваше имя:_",
        parse_mode='Markdown'
    )
    return NAME


async def select_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    services = {
        "svc_tg": "🤖 Telegram-бот",
        "svc_chat": "💬 Чат-бот для сайта",
        "svc_ai": "⚡ AI-автоматизация",
        "svc_crm": "🔗 CRM-интеграция",
        "svc_full": "💼 Полный пакет",
        "svc_voice": "🎙️ Голосовой ИИ-Ресепшонист"
    }
    context.user_data['service'] = services.get(query.data, "Не указано")
    await query.edit_message_text(
        f"✅ Выбрано: *{context.user_data['service']}*\n\nШаг 5/5 — Ваш бюджет?",
        parse_mode='Markdown',
        reply_markup=budget_menu()
    )
    return BUDGET


async def select_budget(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    budgets = {
        "b_500": "до $500",
        "b_1000": "$500 — $1000",
        "b_3000": "$1000 — $3000",
        "b_3000p": "$3000+"
    }
    context.user_data['budget'] = budgets.get(query.data, "Не указано")

    name = context.user_data.get('name', '—')
    phone = context.user_data.get('phone', '—')
    service = context.user_data.get('service', '—')
    budget = context.user_data.get('budget', '—')
    business = context.user_data.get('business', '—')

    summary = f"""📋 *Проверьте заявку:*

👤 Имя: *{name}*
📱 Контакт: *{phone}*
🏢 Бизнес: *{business}*
⚡ Услуга: *{service}*
💰 Бюджет: *{budget}*

_Всё верно?_"""
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

    success_text = """✅ *Заявка принята!*

Спасибо! Мы свяжемся с вами в течение *15 минут*.

👑 *LE AURA* — автоматизируем ваш бизнес

_Пока ждёте — изучите наши кейсы 👇_"""
    await query.edit_message_text(success_text, parse_mode='Markdown', reply_markup=back_menu())

    if ADMIN_ID:
        admin_msg = f"""🔥 *НОВАЯ ЗАЯВКА — LE AURA*

👤 Имя: {name}
📱 Контакт: {phone}
🏢 Бизнес: {business}
⚡ Услуга: {service}
💰 Бюджет: {budget}

👤 TG: @{user.username or 'нет'} | ID: {user.id}"""
        try:
            await context.bot.send_message(ADMIN_ID, admin_msg, parse_mode='Markdown')
        except Exception as e:
            logging.error(f"Admin notify error: {e}")

    context.user_data.clear()
    return ConversationHandler.END

# ══════════════════════════════════════════
# CONVERSATION — ФОРМА ЗАЯВКИ
# ══════════════════════════════════════════

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text(
        f"👋 Приятно познакомиться, *{update.message.text}*!\n\nШаг 2/4 — Ваш Telegram или номер телефона:",
        parse_mode='Markdown'
    )
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['phone'] = update.message.text
    await update.message.reply_text(
        "🏢 Шаг 3/4 — Опишите ваш бизнес:\n\n_Например: интернет-магазин одежды, фитнес-клуб, агентство недвижимости..._",
        parse_mode='Markdown'
    )
    return BUSINESS

async def get_business(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['business'] = update.message.text
    await update.message.reply_text(
        "⚡ Шаг 4/4 — Какая услуга вас интересует?",
        parse_mode='Markdown',
        reply_markup=service_menu()
    )
    return SERVICE

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Используй кнопки меню или напиши /start",
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
        fallbacks=[CommandHandler("start", start)]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown))

    print("LE AURA Bot zapushen!")
    app.run_polling()

if __name__ == "__main__":
    main()
