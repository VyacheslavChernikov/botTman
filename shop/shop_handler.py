from aiogram import types
from database.models import Session, User
from config import config

async def show_shop(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton(
            f"Быстрая кисть ({config.QUICK_BRUSH_PRICE} токенов)",
            callback_data="buy_quick_brush"
        ),
        types.InlineKeyboardButton(
            f"Дополнительное время ({config.EXTRA_TIME_PRICE} токенов)",
            callback_data="buy_extra_time"
        ),
        types.InlineKeyboardButton(
            f"Сканер карточек ({config.CARD_SCANNER_PRICE} токенов)",
            callback_data="buy_card_scanner"
        )
    )
    
    await message.answer("Добро пожаловать в магазин!", reply_markup=keyboard)

async def process_purchase(callback_query: types.CallbackQuery, item: str):
    session = Session()
    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    
    if not user:
        await callback_query.answer("Поль��ователь не найден!")
        return
    
    prices = {
        "quick_brush": config.QUICK_BRUSH_PRICE,
        "extra_time": config.EXTRA_TIME_PRICE,
        "card_scanner": config.CARD_SCANNER_PRICE
    }
    
    price = prices.get(item)
    if user.tokens < price:
        await callback_query.answer("Недостаточно токенов!")
        return
    
    user.tokens -= price
    setattr(user, item, getattr(user, item) + 1)
    session.commit()
    
    await callback_query.answer(f"Улучшение {item} куплено!") 