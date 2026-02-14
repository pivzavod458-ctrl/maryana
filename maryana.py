<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Для Марьяны</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        /* СТИЛЬ "ОТКРЫТКА ОТ БАБУШКИ" */
        body {
            background: linear-gradient(45deg, #ff9a9e 0%, #fecfef 99%, #fecfef 100%);
            font-family: 'Comic Sans MS', 'Chalkboard SE', 'Comic Neue', sans-serif;
            text-align: center;
            color: #590000;
            margin: 0;
            padding: 0;
            overflow: hidden;
            height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        h1, h2, h3 {
            text-shadow: 2px 2px 0px #fff;
            margin: 10px;
        }

        .screen {
            display: none;
            width: 100%;
            height: 100%;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: absolute;
            top: 0;
            left: 0;
        }

        .active {
            display: flex;
        }

        /* КНОПКИ */
        .btn {
            background: linear-gradient(to bottom, #ff00cc, #333399);
            border: 5px solid #fff;
            border-radius: 20px;
            color: yellow;
            padding: 20px 40px;
            font-size: 24px;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 10px 20px rgba(0,0,0,0.5);
            animation: pulse 1s infinite;
            margin-top: 20px;
            text-transform: uppercase;
        }

        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }

        /* ЭКРАН СКАНЕРА */
        #video-container {
            position: relative;
            width: 80%;
            height: 50%;
            border: 10px groove gold;
            overflow: hidden;
            background: black;
            border-radius: 50%; /* Круглый скан */
        }

        video {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .scan-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 10px;
            background: lime;
            box-shadow: 0 0 10px lime;
            animation: scan 2s infinite linear;
        }

        @keyframes scan {
            0% { top: 0; }
            100% { top: 100%; }
        }

        #scan-status {
            font-size: 20px;
            color: blue;
            background: rgba(255,255,255,0.8);
            padding: 5px;
            border-radius: 10px;
            margin-top: 10px;
        }

        /* ЭКРАН ИГРЫ */
        .game-area {
            width: 100%;
            height: 70%;
            position: relative;
            background-color: #7a5c5c;
            /* Имитация ковра на стене */
            background-image: repeating-linear-gradient(45deg, #7a5c5c 25%, transparent 25%, transparent 75%, #7a5c5c 75%, #7a5c5c), repeating-linear-gradient(45deg, #7a5c5c 25%, #5e3b3b 25%, #5e3b3b 75%, #7a5c5c 75%, #7a5c5c);
            background-position: 0 0, 10px 10px;
            background-size: 20px 20px;
            border: 5px dashed red;
            overflow: hidden;
        }

        .fighter {
            position: absolute;
            font-size: 80px;
            bottom: 20px;
            transition: transform 0.1s;
        }

        #player { left: 20px; }
        #bot { right: 20px; transform: scaleX(-1); }

        .hp-bar {
            width: 100px;
            height: 20px;
            background: red;
            border: 2px solid white;
            position: absolute;
            top: 20px;
        }

        #player-hp { left: 20px; }
        #bot-hp { right: 20px; }

        .hit-effect {
            position: absolute;
            font-size: 50px;
            color: red;
            font-weight: bold;
            display: none;
            z-index: 100;
        }

        /* РОЗЫ И ГОЛУБИ (Декор) */
        .decor {
            position: absolute;
            font-size: 40px;
            pointer-events: none;
        }
    </style>
</head>
<body>

    <div id="screen1" class="screen active">
        <div style="font-size: 50px;">🌹🕊️🌹</div>
        <h1>ЗДРАВСТВУЙТЕ!!!</h1>
        <p style="font-size: 18px;">Вам пришла открытка...</p>
        <img src="https://media1.tenor.com/m/KWA2wQk9X7QAAAAC/rose-flower.gif" style="width: 150px; border-radius: 50%; border: 5px dotted gold;">
        <br>
        <h2>ВЫ МАРЬЯНА???</h2>
        <button class="btn" onclick="goToScan()">ДА, ЭТО Я!</button>
        <div style="font-size: 50px; margin-top: 20px;">🍓🍾🥂</div>
    </div>

    <div id="screen2" class="screen">
        <h2>ПРОВЕРКА НА КРАСОТУ</h2>
        <p>Посмотри в камеру и медленно поверни голову (телефон) ВПРАВО!</p>
        <div id="video-container">
            <video id="camera" autoplay playsinline muted></video>
            <div class="scan-overlay"></div>
        </div>
        <div id="scan-status">Ожидание поворота... 0%</div>
        <button id="force-btn" style="display:none; font-size:12px; margin-top:10px;" onclick="finishScan()"> (Если не работает, нажми сюда) </button>
    </div>

    <div id="screen3" class="screen">
        <h2>БИТВА ЗА ЛЮБОВЬ</h2>
        <h3>Кто больше даст люлей?</h3>
        <div class="game-area">
            <div id="player-hp"></div>
            <div id="bot-hp"></div>
            
            <div id="player" class="fighter">💃</div>
            <div id="bot" class="fighter">🕺</div>
            
            <div id="hit-msg" class="hit-effect">БАМ!</div>
        </div>
        <p>ТЫКАЙ БЫСТРО!!!</p>
        <button class="btn" style="padding: 30px; background: red;" onmousedown="attack()" ontouchstart="attack()">УДАРИТЬ САШУ!!!</button>
    </div>

    <div id="screen4" class="screen">
        <h1>ТЫ ПОБЕДИЛА!!!</h1>
        <div style="font-size: 80px;">💍💐😻</div>
        <p>Саша повержен твоей красотой (и ударами)!</p>
        <p>С 14 ФЕВРАЛЯ, ЛЮБИМАЯ!</p>
        <p style="font-size: 12px; color: gray;">(Целую, твой электрик)</p>
    </div>

    <script>
        const tg = window.Telegram.WebApp;
        tg.expand();

        // Переключение экранов
        function showScreen(id) {
            document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
            document.getElementById(id).classList.add('active');
        }

        // --- ЛОГИКА СКАНЕРА ---
        let scanProgress = 0;
        let video = document.getElementById('camera');

        function goToScan() {
            showScreen('screen2');
            
            // Запуск камеры
            navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" } })
                .then(stream => { video.srcObject = stream; })
                .catch(err => {
                    alert("Разреши камеру, иначе магии не будет! " + err);
                    document.getElementById('force-btn').style.display = 'block';
                });

            // "Рофл" детектор поворота через гироскоп
            // Если она поворачивает голову, она скорее всего немного поворачивает и телефон
            window.addEventListener('deviceorientation', handleOrientation);
            
            // Запасной таймер, если гироскоп не сработает (чтобы не застряла)
            setInterval(() => {
                scanProgress += 2; 
                updateScanUI();
            }, 500);
        }

        function handleOrientation(event) {
            // Если телефон наклоняют или поворачивают
            let alpha = event.alpha; // поворот вокруг оси Z
            let gamma = event.gamma; // наклон влево/вправо
            
            // Простая логика: любое движение добавляет прогресс
            if (Math.abs(gamma) > 10 || Math.abs(alpha - 180) > 10) {
                scanProgress += 5;
                updateScanUI();
            }
        }

        function updateScanUI() {
            if (scanProgress >= 100) {
                scanProgress = 100;
                finishScan();
            }
            document.getElementById('scan-status').innerText = `Анализ красоты... ${scanProgress}%`;
        }

        let scanFinished = false;
        function finishScan() {
            if(scanFinished) return;
            scanFinished = true;
            window.removeEventListener('deviceorientation', handleOrientation);
            // Остановить камеру
            let stream = video.srcObject;
            if(stream) stream.getTracks().forEach(track => track.stop());
            
            alert("ЛИЧНОСТЬ ПОДТВЕРЖДЕНА: ЭТО САМАЯ КРАСИВАЯ ДЕВУШКА!");
            setTimeout(() => showScreen('screen3'), 1000);
            startGame();
        }

        // --- ЛОГИКА ИГРЫ ---
        let playerHp = 10;
        let botHp = 10;
        let gameActive = false;

        function startGame() {
            gameActive = true;
            botAttackLoop();
        }

        function attack() {
            if (!gameActive) return;
            
            // Анимация удара игрока
            document.getElementById('player').style.transform = "translateX(50px) rotate(20deg)";
            setTimeout(() => document.getElementById('player').style.transform = "translateX(0)", 100);

            // Урон боту
            botHp--;
            showHitEffect("НА!", "bot");
            updateHp();

            if (botHp <= 0) {
                endGame(true);
            }
        }

        function botAttack() {
            if (!gameActive) return;

            // Анимация удара бота
            document.getElementById('bot').style.transform = "translateX(-50px) scaleX(-1) rotate(-20deg)";
            setTimeout(() => document.getElementById('bot').style.transform = "scaleX(-1)", 100);

            // Урон игроку (медленнее, чтобы она выиграла)
            playerHp--;
            showHitEffect("ХДЫЩ!", "player");
            updateHp();

            if (playerHp <= 0) {
                alert("Саша победил... Но он поддавался! Попробуй еще раз.");
                playerHp = 10;
                botHp = 10;
                updateHp();
            }
        }

        function botAttackLoop() {
            if (!gameActive) return;
            // Бот бьет каждые 800мс (достаточно медленно)
            setTimeout(() => {
                botAttack();
                botAttackLoop();
            }, 800);
        }

        function showHitEffect(text, target) {
            let el = document.getElementById('hit-msg');
            el.innerText = text;
            el.style.display = 'block';
            
            // Позиция текста
            let rect = document.getElementById(target).getBoundingClientRect();
            el.style.top = (rect.top - 50) + 'px';
            el.style.left = (rect.left + 20) + 'px';

            setTimeout(() => el.style.display = 'none', 300);
        }

        function updateHp() {
            let pPct = (playerHp / 10) * 100;
            let bPct = (botHp / 10) * 100;
            document.getElementById('player-hp').style.width = pPct + 'px';
            document.getElementById('bot-hp').style.width = bPct + 'px';
        }

        function endGame(win) {
            gameActive = false;
            if (win) {
                showScreen('screen4');
                // Конфетти эффект (простой css)
                document.body.style.backgroundImage = "url('https://media.giphy.com/media/26tOZ42Mg6pbTUPv2/giphy.gif')";
            }
        }
    </script>
</body>
</html>
