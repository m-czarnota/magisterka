import {Square} from "./Square";
import {HUD} from "./HUD";
import {Timer} from "../../utils/game/Timer";
import {Statistic} from "./Statistic";

export class GameEngine {
    width = undefined;
    height = undefined;
    appContainer = undefined;
    hud = null;

    squares = [];
    statistics = null;
    
    isOver = false;
    maxSquares = 4;
    squaresHistoryCount = 0;
    hp = 3;
    score = 0;
    gameSeconds = 0;
    gameTimer = 0;

    fillSquaresInterval = null;
    velocityModifierInterval = null;
    squaresCountModifierInterval = null;

    currentVelocityModifier = 0;

    velocityModifierInTime = 0.1;
    velocityModifierTimeInterval = 10000;

    squaresCountModifierInTime = 1;
    squaresCountModifierTimeInterval = 20000;

    debug = true;
    isImmortal = false;
    disableFalling = false;
    displayMissShotArea = false;

    gameWindowContainer = null;
    gameWindow = null;

    constructor(width, height, container) {
        this.width = width;
        this.height = height;
        this.appContainer = container;
        this.hud = new HUD(this);

        this.statistics = new Statistic(this);
    }

    drawGameWindow() {
        this.gameWindowContainer = document.createElement('div');
        this.gameWindowContainer.classList.add('game-window-container');
        this.gameWindowContainer.appendChild(this.hud.createHudContainer());
        this.appContainer.appendChild(this.gameWindowContainer);

        this.gameWindow = document.createElement('div');
        this.gameWindow.style.width = `${this.width}px`;
        this.gameWindow.style.height = `${this.height}px`;
        this.gameWindow.classList.add('game-window');
        this.gameWindowContainer.appendChild(this.gameWindow);

        this.gameWindow.appendChild(this.hud.createStartButton());
        this.gameWindow.appendChild(this.hud.createMessage());
    }

    prepareForNewGame() {
        this.clearSquares();

        this.isOver = false;
        this.maxSquares = 4;
        this.squaresHistoryCount = 0;

        this.hp = 3;
        this.hud.updateHp(this.hp);

        this.score = 0;
        this.hud.updateScore(this.score);

        this.gameSeconds = 0;
        this.gameTimer = null;
        this.hud.updateTime(this.gameSeconds);

        this.currentVelocityModifier = 0;

        this.fillSquaresInterval = null;
        this.velocityModifierInterval = null;
        this.squaresCountModifierInterval = null;

        this.statistics.reset();
    }

    async newGame() {
        // this.prepareForNewGame();

        this.startGameTimer();
        this.startVelocityModifierTimer();
        this.startSquaresCountModifierTimer();

        await this.startFillingSquares();
    }

    isGameOver() {
        if (this.isImmortal) {
            return false;
        }

        if (this.hp <= 0) {
            return true;
        }

        return false;
    }

    async gameOver() {
        if (this.isOver) {
            return;
        }

        this.stopFillingSquares();
        this.stopGameTimer();
        this.stopVelocityModifierTimer();
        this.stopSquaresCountModifierTimer();

        this.isOver = true;

        this.hud.updateMessageHeader('Game over');
        this.hud.updateMessageDescription('Your data has been successfully saved.')
        await this.hud.showMessage();

        await this.saveGameData();

        new Timer(async () => {
            this.hud.updateStartButtonText('Maybe again?');
            await this.hud.showStartButton();
        }, 2000).start();
    }

    async saveGameData() {
        const formData = new FormData();
        formData.append('gameData', this.statistics.actions);

        const response = await fetch(Routing.generate('app_game_save_game_data'), {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(this.statistics.actions),
        });
        const data = await response.json();
    }

    async startFillingSquares() {
        this.fillSquaresInterval = setInterval(() => {
            if (this.squares.length >= this.maxSquares) {
                return;
            }

            const square = new Square(this.squaresHistoryCount, this);
            this.squares.push(square);
            this.gameWindow.appendChild(square.getSquareElement());

            this.setEventListenersForSquare(square);

            square.startFalling();
            this.squaresHistoryCount++;
        }, 300);
    }

    stopFillingSquares() {
        clearInterval(this.fillSquaresInterval);
    }

    setEventListenersForSquare(square) {
        square.element.addEventListener('square-out-of-board', async () => {
            if (this.isImmortal) {
                this.statistics.saveAction();
                await this.destroySquare(square);

                return;
            }

            if (!this.isOver) {
                this.loseHp();
                this.statistics.saveAction();
            }

            await this.destroySquare(square);

            if (this.isGameOver()) {
                await this.gameOver();
            }
        });

        square.element.addEventListener('square-clicked', async () => {
            this.score += square.calcScore();

            this.statistics.increaseAccurateShot();
            this.statistics.saveAction();

            this.hud.updateScore(this.score);

            await this.destroySquare(square);
        });

        square.missShotArea.addEventListener('miss-shot', () => {
            this.statistics.increaseShotCount();
            this.statistics.saveAction();
            this.printDebugInfo('Miss shot! Actual accurate:', this.statistics.calcAccurate());
        });
    }

    loseHp() {
        this.hp -= 1;
        this.hud.updateHp(this.hp);
        this.printDebugInfo('Fail! -1HP, actual HP:', this.hp);
    }

    async destroySquare(square) {
        const index = this.squares.indexOf(square);

        await square.destructor();
        delete this.squares[index];
        this.squares.splice(index, 1);
    }

    startVelocityModifierTimer() {
        this.velocityModifierInterval = setInterval(() => {
            this.currentVelocityModifier += this.velocityModifierInTime;
            this.printDebugInfo('velocity modifier increased, actual velocity modifier', this.currentVelocityModifier)
        }, this.velocityModifierTimeInterval);
    }

    stopVelocityModifierTimer() {
        clearInterval(this.velocityModifierInterval);
    }

    startSquaresCountModifierTimer() {
        this.squaresCountModifierInterval = setInterval(() => {
            this.maxSquares += this.squaresCountModifierInTime;
            this.printDebugInfo('max squares count increased, actual max squares count', this.maxSquares)
        }, this.squaresCountModifierTimeInterval);
    }

    stopSquaresCountModifierTimer() {
        clearInterval(this.squaresCountModifierInterval);
    }

    startGameTimer() {
        this.gameStartedDate = new Date();

        this.gameTimer = setInterval(() => {
            this.gameSeconds += 1;
            this.hud.updateTime(this.gameSeconds);
            this.statistics.saveAction();
        }, 1000);
    }

    stopGameTimer() {
        clearInterval(this.gameTimer);
    }

    printDebugInfo(...message) {
        if (!this.debug) {
            return;
        }

        console.log(...message);
    }

    clearSquares() {
        for (let i = 0; i < this.squares.length; i++) {
            this.squares[i].destructor();
            delete this.squares[i];
        }

        this.squares = [];
    }
}