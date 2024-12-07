let tg = window.Telegram.WebApp;
let game = {
    score: 0,
    timeLeft: 60,
    isRunning: false
};

// Инициализация Telegram Mini App
tg.expand();
tg.ready();

function startGame() {
    game.score = 0;
    game.timeLeft = 60;
    game.isRunning = true;
    
    document.getElementById('main-menu').classList.add('hidden');
    document.getElementById('game-area').classList.remove('hidden');
    
    updateScore();
    startTimer();
    generateCards();
}

function generateCards() {
    if (!game.isRunning) return;
    
    const cardContainer = document.getElementById('card-container');
    cardContainer.innerHTML = '';
    
    const isBadCard = Math.random() > 0.5;
    const card = document.createElement('div');
    card.className = 'card';
    card.textContent = isBadCard ? getRandomBadCard() : getRandomGoodCard();
    card.dataset.isBad = isBadCard;
    
    card.onclick = () => handleCardClick(card);
    
    cardContainer.appendChild(card);
    
    setTimeout(generateCards, 2000);
}

function handleCardClick(card) {
    const isBad = card.dataset.isBad === 'true';
    
    if (isBad) {
        game.score += 2;
        tg.HapticFeedback.impactOccurred('heavy');
    } else {
        game.score -= 1;
        tg.HapticFeedback.notificationOccurred('error');
    }
    
    updateScore();
    card.remove();
}

function updateScore() {
    document.getElementById('score').textContent = `Счёт: ${game.score}`;
}

function startTimer() {
    const timerElement = document.getElementById('timer');
    
    const timer = setInterval(() => {
        game.timeLeft--;
        timerElement.textContent = `Время: ${game.timeLeft}`;
        
        if (game.timeLeft <= 0) {
            clearInterval(timer);
            endGame();
        }
    }, 1000);
}

function endGame() {
    game.isRunning = false;
    
    // Отправляем результаты в бот
    tg.sendData(JSON.stringify({
        action: 'gameEnd',
        score: game.score
    }));
    
    document.getElementById('game-area').classList.add('hidden');
    document.getElementById('main-menu').classList.remove('hidden');
}

function getRandomBadCard() {
    const badCards = ["Спам", "Мошенничество", "Фейк", "Обман", "Вирус", "Взлом", "Скам", "Фишинг"];
    return badCards[Math.floor(Math.random() * badCards.length)];
}

function getRandomGoodCard() {
    const goodCards = ["Правда", "Безопасность", "Защита", "Доверие", "Честность", "Надёжность", "Проверено", "Подлинность"];
    return goodCards[Math.floor(Math.random() * goodCards.length)];
}

function openShop() {
    tg.sendData(JSON.stringify({
        action: 'openShop'
    }));
}

function showBalance() {
    tg.sendData(JSON.stringify({
        action: 'showBalance'
    }));
} 