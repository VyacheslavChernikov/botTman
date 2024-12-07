from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import config
from database.models import Session, User, Game
from game.game_logic import GameSession
import asyncio
from aiohttp import web
import json

bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

active_games = {}

routes = web.RouteTableDef()

@routes.get('/')
async def handle_webapp(request):
    return web.FileResponse('./webapp/index.html')

@routes.post('/webhook')
async def handle_webhook(request):
    data = await request.json()
    if data.get('action') == 'gameEnd':
        user_id = data.get('user_id')
        score = data.get('score')
        # Обработка результатов игры
        await process_game_results(user_id, score)
    return web.Response(text='OK')

def get_main_keyboard() -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton("Начать миссию", callback_data="start_game"),
        types.InlineKeyboardButton("Магазин", callback_data="shop"),
        types.InlineKeyboardButton("Баланс", callback_data="balance")
    )
    return keyboard

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Добро пожаловать в T-MAN Game!", reply_markup=get_main_keyboard())

@dp.callback_query_handler(lambda c: c.data == 'start_game')
async def start_game(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    
    # Создаем новую игровую сессию
    game = GameSession(user_id)
    active_games[user_id] = game
    
    await callback_query.message.answer("Игра начинается! Нажимайте на плохие карточки!")
    
    # Запускаем игровой цикл
    await game_loop(callback_query.message, game)

async def game_loop(message: types.Message, game: GameSession):
    game.is_running = True
    start_time = asyncio.get_event_loop().time()
    
    while game.is_running:
        current_time = asyncio.get_event_loop().time()
        if current_time - start_time >= config.GAME_DURATION:
            break
            
        card_text, is_bad = await game.generate_card()
        
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(
            "Нажми!", callback_data=f"tap_{is_bad}"
        ))
        
        await message.answer(card_text, reply_markup=keyboard)
        
        # Ждем интервал в зависимости от сложности
        await asyncio.sleep(
            config.EASY_MODE_INTERVAL if game.difficulty == "easy"
            else config.HARD_MODE_INTERVAL
        )
    
    # Сохраняем результаты игры
    session = Session()
    new_game = Game(
        user_id=game.user_id,
        score=game.score,
        tokens_earned=game.tokens_earned,
        difficulty=game.difficulty
    )
    session.add(new_game)
    
    user = session.query(User).filter_by(telegram_id=game.user_id).first()
    if user:
        user.tokens += game.tokens_earned
        user.games_played += 1
        user.best_score = max(user.best_score, game.score)
    
    session.commit()
    session.close()
    
    await message.answer(
        f"Игра окончена!\n"
        f"Ваш счёт: {game.score}\n"
        f"Заработано токенов: {game.tokens_earned}"
    )
    
    await message.answer("Выберите действие:", reply_markup=get_main_keyboard())

@dp.callback_query_handler(lambda c: c.data.startswith('tap_'))
async def process_tap(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    game = active_games.get(user_id)
    
    if not game:
        await callback_query.answer("Игра не найдена!")
        return
        
    was_bad_card = callback_query.data == "tap_True"
    points = game.process_tap(was_bad_card)
    
    await callback_query.answer(f"{'Правильно!' if points > 0 else 'Неправильно!'} {points} очков")
    await callback_query.message.delete()

@dp.callback_query_handler(lambda c: c.data == 'shop')
async def shop_handler(callback_query: types.CallbackQuery):
    from shop.shop_handler import show_shop
    await show_shop(callback_query.message)

@dp.callback_query_handler(lambda c: c.data.startswith('buy_'))
async def buy_handler(callback_query: types.CallbackQuery):
    from shop.shop_handler import process_purchase
    item = callback_query.data.replace('buy_', '')
    await process_purchase(callback_query, item)

@dp.callback_query_handler(lambda c: c.data == 'balance')
async def balance_handler(callback_query: types.CallbackQuery):
    session = Session()
    user = session.query(User).filter_by(telegram_id=callback_query.from_user.id).first()
    
    if not user:
        user = User(telegram_id=callback_query.from_user.id, username=callback_query.from_user.username)
        session.add(user)
        session.commit()
    
    await callback_query.message.answer(
        f"Ваш баланс:\n"
        f"Токены: {user.tokens}\n"
        f"Игр сыграно: {user.games_played}\n"
        f"Лучший счёт: {user.best_score}"
    )
    session.close()

if __name__ == '__main__':
    app = web.Application()
    app.add_routes(routes)
    app.router.add_static('/static', './webapp')
    
    # Запускаем бота и веб-сервер
    loop = asyncio.get_event_loop()
    loop.create_task(web._run_app(app, host='0.0.0.0', port=8080))
    executor.start_polling(dp, skip_updates=True) 