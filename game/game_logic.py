import random
from typing import List, Tuple
import asyncio
from config import config

class GameSession:
    def __init__(self, user_id: int, difficulty: str = "easy"):
        self.user_id = user_id
        self.difficulty = difficulty
        self.score = 0
        self.tokens_earned = 0
        self.cards_hit = 0
        self.is_running = False
        
        # Списки карточек
        self.bad_cards = [
            "Спам", "Мошенничество", "Фейк", "Обман",
            "Вирус", "Взлом", "Скам", "Фишинг"
        ]
        
        self.good_cards = [
            "Правда", "Безопасность", "Защита", "Доверие",
            "Честность", "Надёжность", "Проверено", "Подлинность"
        ]
    
    async def generate_card(self) -> Tuple[str, bool]:
        """Генерирует карточку: (текст, is_bad)"""
        is_bad = random.choice([True, False])
        text = random.choice(self.bad_cards if is_bad else self.good_cards)
        return text, is_bad
    
    def process_tap(self, was_bad_card: bool) -> int:
        """Обрабатывает нажатие на карточку"""
        if was_bad_card:
            self.score += config.BAD_CARD_REWARD
            self.cards_hit += 1
            self.tokens_earned += config.TOKEN_MULTIPLIER
            return config.BAD_CARD_REWARD
        else:
            self.score += config.GOOD_CARD_PENALTY
            return config.GOOD_CARD_PENALTY 