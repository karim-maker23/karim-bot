
import random

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# Вставь сюда токен своего бота от BotFather
TOKEN = "8931178360:AAFulAdB3WS5lgO8i4_-SZoLbtfmTfURsGQ"

# Список героев Dota 2
HEROES = [
    "Anti-Mage",
    "Axe",
    "Crystal Maiden",
    "Drow Ranger",
    "Pudge",
    "Shadow Fiend",
    "Invoker",
    "Phantom Assassin",
    "Sniper",
    "Juggernaut",
    "Rubick",
    "Zeus",
    "Slark",
    "Lina",
    "Wraith King",
]

# Список случайных шуток
JOKES = [
    "Почему Пудж не ходит в спортзал? Он и так всех притягивает!",
    "Мидер сказал, что сейчас затащит. Прошло 40 минут...",
    "Почему Инвокер не любит математику? У него и так слишком много комбинаций!",
    "Пикнул Пуджа, промахнулся хуком и сказал: «Так и задумано!»",
    "Почему Shadow Fiend всегда злой? У него души не на месте!",
]


# Команда /start — приветствие и кнопки
async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    # Создаём три inline-кнопки
    keyboard = [
        [
            InlineKeyboardButton(
                "ℹ️ О боте",
                callback_data="about"
            ),
            InlineKeyboardButton(
                "😂 Шутка",
                callback_data="joke"
            ),
            InlineKeyboardButton(
                "👤 Автор",
                callback_data="author"
            ),
        ]
    ]

    # Добавляем клавиатуру под сообщением
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Привет! Я бот по Dota 2!\n\n"
        "Нажми на одну из кнопок ниже 👇",
        reply_markup=reply_markup
    )


# Обработка нажатий на inline-кнопки
async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    # Получаем запрос от нажатой кнопки
    query = update.callback_query

    # Подтверждаем нажатие кнопки
    await query.answer()

    # Кнопка «О боте»
    if query.data == "about":
        await query.message.reply_text(
            "🤖 Я бот по Dota 2!\n\n"
            "🎮 Могу выдавать случайных героев.\n"
            "😂 Могу рассказывать шутки.\n"
            "🔥 И помню главное: у Пла нет контрпиков!"
        )

    # Кнопка «Шутка»
    elif query.data == "joke":
        await query.message.reply_text(
            "😂 " + random.choice(JOKES)
        )

    # Кнопка «Автор»
    elif query.data == "author":
        await query.message.reply_text(
            "👤 Автор этого бота — лох 😎"
        )


# Команда /help — список команд
async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "📚 Список команд:\n\n"
        "/start — запустить бота\n"
        "/help — список команд\n"
        "/hero — случайный герой Dota 2\n\n"
        "Напиши «база», чтобы проверить мою базу!"
    )


# Команда /hero — случайный герой
async def hero(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    random_hero = random.choice(HEROES)

    await update.message.reply_text(
        f"🎲 Твой случайный герой:\n\n"
        f"⚔️ {random_hero}"
    )


# Ответ на сообщение «база»
async def base_response(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    text = update.message.text.lower().strip()

    if text == "база":
        await update.message.reply_text(
            "🔥 У Пла нет контр пиков!"
        )


# Запуск бота
def main():
    # Создаём приложение
    app = Application.builder().token(TOKEN).build()

    # Регистрируем команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("hero", hero))

    # Регистрируем обработчик inline-кнопок
    app.add_handler(
        CallbackQueryHandler(button_handler)
    )

    # Регистрируем обработчик обычных сообщений
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            base_response
        )
    )

    # Запускаем бота
    print("Бот запущен!")
    app.run_polling()


# Запускаем программу
if __name__ == "__main__":
    main()
