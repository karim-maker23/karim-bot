
import random

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Токен бота от BotFather
TOKEN = "8931178360:AAFulAdB3WS5lgO8i4_-SZoLbtfmTfURsGQ"


# Список героев Dota 2
HEROES = [
    "Anti-Mage",
    "Axe",
    "Crystal Maiden",
    "Drow Ranger",
    "Earthshaker",
    "Juggernaut",
    "Mirana",
    "Pudge",
    "Shadow Fiend",
    "Invoker",
    "Phantom Assassin",
    "Sniper",
    "Sven",
    "Lion",
    "Lina",
    "Witch Doctor",
    "Rubick",
    "Zeus",
    "Slark",
    "Tidehunter",
    "Tusk",
    "Vengeful Spirit",
    "Windranger",
    "Wraith King",
]


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет!\n\n"
        "Я Dota 2 бот.\n"
        "Могу показать случайного героя и отвечать на специальные сообщения.\n\n"
        "Используй /help, чтобы посмотреть список команд."
    )


# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 Список команд:\n\n"
        "/start — приветствие и описание бота\n"
        "/help — список команд\n"
        "/hero — случайный герой Dota 2\n\n"
        "Также напиши «база», и я отвечу 😎"
    )


# Команда /hero
async def hero(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random_hero = random.choice(HEROES)

    await update.message.reply_text(
        f"🎲 Твой случайный герой:\n\n"
        f"⚔️ {random_hero}"
    )


# Ответ на слово "база"
async def base_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()

    if text == "база":
        await update.message.reply_text(
            "🔥 У Пла нет контр пиков!"
        )


# Запуск бота
def main():
    app = Application.builder().token(TOKEN).build()

    # Команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("hero", hero))

    # Сообщения
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            base_response
        )
    )

    print("🤖 Бот запущен!")

    app.run_polling()


if __name__ == "__main__":
    main()

