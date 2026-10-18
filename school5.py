
import json
import os
import random

from dotenv import load_dotenv

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
    ConversationHandler,
    ContextTypes,
    filters,
)

# Загружаем переменные из файла .env
load_dotenv()

# Получаем токен бота из переменной окружения
TOKEN = os.getenv("8931178360:AAFulAdB3WS5lgO8i4_-SZoLbtfmTfURsGQ")

# Проверяем, указан ли токен
if not TOKEN: RuntimeError()
 

# Файл для хранения пользователей
USERS_FILE = "users.json"

# Словарь пользователей
users = {}

# Этапы заполнения профиля
WAITING_NAME, WAITING_AGE = range(2)


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
    "Lion",
    "Sven",
]

# Список шуток
JOKES = [
    "Почему Пудж не ходит в спортзал? Он и так всех притягивает!",
    "Мидер сказал, что сейчас затащит. Прошло 40 минут...",
    "Почему Инвокер не любит математику? Слишком много комбинаций!",
    "Пикнул Пуджа, промахнулся хуком и сказал: «Так и задумано!»",
    "У Пла нет контрпиков, зато есть плохие тиммейты!",
]


# Загружаем пользователей из JSON при запуске
def load_users():
    global users

    if not os.path.exists(USERS_FILE):
        users = {}
        return

    try:
        with open(USERS_FILE, "r", encoding="utf-8") as file:
            loaded_users = json.load(file)

        if isinstance(loaded_users, dict):
            # Ключи Telegram ID должны быть строками
            users = {
                str(user_id): data
                for user_id, data in loaded_users.items()
                if isinstance(data, dict)
            }
        else:
            users = {}

    except (json.JSONDecodeError, OSError):
        print(
            "Не удалось прочитать users.json. "
            "Используется пустой словарь."
        )
        users = {}


# Сохраняем пользователей в JSON
def save_users():
    # Сначала записываем данные во временный файл
    temp_file = USERS_FILE + ".tmp"

    with open(temp_file, "w", encoding="utf-8") as file:
        json.dump(
            users,
            file,
            ensure_ascii=False,
            indent=2,
        )

    # Заменяем основной файл обновлённым
    os.replace(temp_file, USERS_FILE)


# Сохраняем профиль пользователя
def save_user(user_id, name, age):
    users[str(user_id)] = {
        "name": name,
        "age": age,
    }

    # Сохраняем после изменения словаря
    save_users()


# Получаем профиль пользователя
def get_user(user_id):
    return users.get(str(user_id))


# Команда /start — главное меню
async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    keyboard = [
        [
            InlineKeyboardButton(
                "ℹ️ О боте",
                callback_data="about",
            ),
            InlineKeyboardButton(
                "😂 Шутка",
                callback_data="joke",
            ),
            InlineKeyboardButton(
                "👤 Автор",
                callback_data="author",
            ),
        ],
        [
            InlineKeyboardButton(
                "💾 Сохранить данные",
                callback_data="save_profile",
            ),
            InlineKeyboardButton(
                "📋 Мои данные",
                callback_data="my_profile",
            ),
        ],
    ]

    await update.message.reply_text(
        "👋 Привет! Я бот по Dota 2!\n\n"
        "🎮 Случайные герои\n"
        "😂 Шутки\n"
        "💾 Сохранение профиля\n\n"
        "Выбирай действие ниже 👇",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# Обработка inline-кнопок
async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    await query.answer()

    if query.data == "about":
        await query.message.reply_text(
            "🤖 Я бот по Dota 2!\n\n"
            "🎮 Выдаю случайных героев.\n"
            "😂 Рассказываю шутки.\n"
            "💾 Сохраняю твой профиль.\n"
            "📋 Показываю сохранённые данные.\n\n"
            "🔥 У Пла нет контрпиков!"
        )

    elif query.data == "joke":
        await query.message.reply_text(
            "😂 " + random.choice(JOKES)
        )

    elif query.data == "author":
        await query.message.reply_text(
            "👤 Автор этого бота — лох 😎"
        )

    elif query.data == "my_profile":
        user = get_user(query.from_user.id)

        if user:
            await query.message.reply_text(
                "📋 Твой профиль:\n\n"
                f"👤 Имя: {user['name']}\n"
                f"🎂 Возраст: {user['age']} лет"
            )
        else:
            keyboard = [[
                InlineKeyboardButton(
                    "💾 Создать профиль",
                    callback_data="save_profile",
                )
            ]]

            await query.message.reply_text(
                "📭 У тебя ещё нет профиля.\n"
                "Нажми кнопку ниже, чтобы создать его.",
                reply_markup=InlineKeyboardMarkup(keyboard),
            )


# Начинаем заполнение профиля
async def start_save(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    await query.answer()

    context.user_data.pop("profile_name", None)

    await query.message.reply_text(
        "💾 Создаём профиль!\n\n"
        "Напиши своё имя:"
    )

    return WAITING_NAME


# Получаем имя пользователя
async def receive_name(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    name = update.message.text.strip()

    if not name or len(name) > 100:
        await update.message.reply_text(
            "❌ Имя должно содержать от 1 до 100 символов.\n"
            "Попробуй ещё раз:"
        )
        return WAITING_NAME

    context.user_data["profile_name"] = name

    await update.message.reply_text(
        f"Приятно познакомиться, {name}! 😊\n\n"
        "Теперь напиши свой возраст от 1 до 120:"
    )

    return WAITING_AGE


# Получаем возраст и сохраняем профиль
async def receive_age(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    age_text = update.message.text.strip()

    if not age_text.isdigit():
        await update.message.reply_text(
            "❌ Возраст должен быть целым числом.\n"
            "Введи возраст от 1 до 120:"
        )
        return WAITING_AGE

    age = int(age_text)

    if not 1 <= age <= 120:
        await update.message.reply_text(
            "❌ Возраст должен быть от 1 до 120.\n"
            "Попробуй ещё раз:"
        )
        return WAITING_AGE

    name = context.user_data.get("profile_name")

    if not name:
        await update.message.reply_text(
            "Не удалось получить имя. Начни заново через /start."
        )
        return ConversationHandler.END

    # Сохраняем профиль в users и users.json
    save_user(update.effective_user.id, name, age)

    context.user_data.pop("profile_name", None)

    await update.message.reply_text(
        "✅ Профиль успешно сохранён!\n\n"
        f"👤 Имя: {name}\n"
        f"🎂 Возраст: {age} лет\n\n"
        "Нажми «📋 Мои данные» в меню, "
        "чтобы посмотреть профиль."
    )

    return ConversationHandler.END


# Отмена заполнения профиля
async def cancel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    context.user_data.pop("profile_name", None)

    await update.message.reply_text(
        "❌ Заполнение профиля отменено."
    )

    return ConversationHandler.END


# Команда /help
async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await update.message.reply_text(
        "📚 Список команд:\n\n"
        "/start — открыть главное меню\n"
        "/help — список команд\n"
        "/hero — случайный герой Dota 2\n"
        "/cancel — отменить заполнение профиля\n\n"
        "Напиши «база», чтобы проверить мою базу!"
    )


# Команда /hero
async def hero(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await update.message.reply_text(
        "🎲 Твой случайный герой:\n\n"
        f"⚔️ {random.choice(HEROES)}"
    )


# Ответ на слово «база»
async def base_response(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if update.message.text.lower().strip() == "база":
        await update.message.reply_text(
            "🔥 У Пла нет контр пиков!"
        )


# Запускаем бота
def main():
    # Загружаем пользователей перед запуском
    load_users()

    # Создаём приложение Telegram
    app = Application.builder().token(TOKEN).build()

    # Регистрируем диалог заполнения профиля
    profile_conversation = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                start_save,
                pattern=r"^save_profile$",
            )
        ],
        states={
            WAITING_NAME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    receive_name,
                )
            ],
            WAITING_AGE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    receive_age,
                )
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
        ],
        per_chat=True,
        per_user=True,
        per_message=False,
    )

    # Сначала регистрируем диалог
    app.add_handler(profile_conversation)

    # Регистрируем команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("hero", hero))

    # Регистрируем остальные inline-кнопки
    app.add_handler(CallbackQueryHandler(button_handler))

    # Обрабатываем обычные сообщения
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            base_response,
        )
    )

    print("🤖 Бот запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()