from aiogram.types import WebAppInfo

async def setup_webapp(bot):
    # Создаем команду для запуска веб-приложения
    webapp_button = types.InlineKeyboardButton(
        text="Играть в веб-версию",
        web_app=WebAppInfo(url="https://your-domain.com")  # Замените на ваш домен
    )
    
    # Добавляем кнопку в главное меню
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(webapp_button)
    return keyboard 