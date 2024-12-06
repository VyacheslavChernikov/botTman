from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String)
    tokens = Column(Integer, default=0)
    games_played = Column(Integer, default=0)
    best_score = Column(Integer, default=0)
    
    # Улучшения
    quick_brush = Column(Integer, default=0)  # уровень улучшения
    extra_time = Column(Integer, default=0)
    card_scanner = Column(Integer, default=0)

class Game(Base):
    __tablename__ = 'games'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    score = Column(Integer)
    tokens_earned = Column(Integer)
    played_at = Column(DateTime, default=datetime.datetime.utcnow)
    difficulty = Column(String)

# Создание базы данных
engine = create_engine('sqlite:///tman_game.db')
Base.metadata.create_all(engine)

# С��здание сессии
Session = sessionmaker(bind=engine) 