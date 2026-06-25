import os
from telegram import Update
from telegram.ext import ContextTypes
from src.weather import get_weather


AWAITING_CITY_STATE = "awaiting_city"


async def start_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Respond to the /start command with a personalized welcome text"""
    user = update.effective_user.first_name if update.effective_user else "друг"
    await update.message.reply_text(
        f"Привіт, {user}! 👋\n"
        "Я офіційний бот погоди. Напиши /weather, щоб дізнатися статус."
    )


async def help_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Display comprehensive information regarding available capabilities"""
    await update.message.reply_text(
        "📌 Доступні команди:\n"
        "/start - Запустити бота\n"
        "/help - Показати довідку за командами\n"
        "/weather - Запитати поточні погодні умови в місті"
    )


async def weather_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Put user session state to city waiting and prompt for target query"""
    context.user_data["state"] = AWAITING_CITY_STATE
    await update.message.reply_text("Вкажіть назву міста (наприклад: Київ):")


async def handle_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Process message intercepts, assessing state contexts sequentially"""
    state = context.user_data.get("state")

    if state == AWAITING_CITY_STATE:
        city = update.message.text.strip()
        api_key = os.getenv("OPENWEATHER_API_KEY")

        if not api_key:
            await update.message.reply_text(
                "❌ Помилка конфігурації: відсутній API-ключ OpenWeather."
            )
            context.user_data["state"] = None
            return

        await update.message.reply_chat_action("typing")
        data = get_weather(city, api_key)

        if data:
            city_name = data.get("name")
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            desc = data["weather"][0]["description"]

            report = (
                f"🌤 Погода в місті {city_name}:\n"
                f"🌡 Температура: {temp}°C\n"
                f"💧 Вологість: {humidity}%\n"
                f"📝 Опис: {desc.capitalize()}"
            )
            await update.message.reply_text(report)
        else:
            await update.message.reply_text(
                f"❌ Не вдалося знайти місто '{city}'. Спробуйте ще раз."
            )

        context.user_data["state"] = None
    else:
        await update.message.reply_text(
            "Невідома команда. Скористайтеся /help для довідки."
        )
        