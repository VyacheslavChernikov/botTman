import os
from dataclasses import dataclass

@dataclass
class Config:
    # Токен из переменной окружения
    BOT_TOKEN: str = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN')
    
    # Настройки игры
    GAME_DURATION: int = 60  # секунды
    EASY_MODE_INTERVAL: float = 2.0  # секунды
    HARD_MODE_INTERVAL: float = 0.5
    
    # Очки
    GOOD_CARD_PENALTY: int = -1
    BAD_CARD_REWARD: int = 2
    TOKEN_MULTIPLIER: int = 2  # токены за каждое правильное нажатие
    
    # Цены улучшений
    QUICK_BRUSH_PRICE: int = 50
    EXTRA_TIME_PRICE: int = 75
    CARD_SCANNER_PRICE: int = 100

config = Config() 