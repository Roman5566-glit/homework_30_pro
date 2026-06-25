# Weather Integration Telegram Bot

Асинхронний Telegram-бот для отримання актуальних даних про погоду через зовнішню інтеграцію з OpenWeatherMap API.

## Використані технології & API
* **Мова розробки:** Python 3.10+
* **Зовнішнє API:** OpenWeatherMap API (Current Weather Data)
* **Бібліотеки:** `requests` (для HTTP-запитів), `python-telegram-bot` (v20+ асинхронний фреймворк), `python-dotenv` (керування конфігурацією).

## Як запустити проєкт локально

1. **Клонуйте репозиторій або розпакуйте архів з проєктом.**
2. **Створіть та активуйте віртуальне оточення:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Windows: venv\Scripts\activate