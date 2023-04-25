import {Square} from "./Square";
import {HUD} from "./HUD";
import {Timer} from "../../utils/game/Timer";
import {GameStatistic} from "./GameStatistic";

export class GameEngine {
    width = undefined;
    height = undefined;
    appContainer = undefined;
    hud = null;

    maxTime = null;
    maxScore = null;

    showedRecordTime = false;
    showedRecordScore = false;

    squares = [];
    gameStatistics = null;
    
    isOver = false;
    maxSquares = 4;
    squaresHistoryCount = 0;
    hp = 3;
    score = 0;
    gameTimer = 0;

    fillSquaresInterval = null;
    velocityModifierInterval = null;
    squaresCountModifierInterval = null;

    currentReducingFallingTimeModifier = 0;

    reducingFallingTimeInTime = 0.2;
    reducingFallingTimeModifierInterval = 10000;

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

        this.maxScore = parseFloat(container.getAttribute('data-max-score'));
        this.maxTime = parseFloat(container.getAttribute('data-max-time'));

        this.gameStatistics = new GameStatistic(this);
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
        this.gameWindow.appendChild(this.hud.createEndGameStatistics());
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
        this.hud.hideScoreTrophyIcon();

        this.gameTimer = null;
        this.hud.updateTime(0);
        this.hud.hideTimeTrophyIcon();

        this.gameStatistics.timeToNewTimeRecord = null;
        this.gameStatistics.timeToNewScoreRecord = null;

        this.showedRecordTime = false;
        this.showedRecordScore = false;

        this.currentReducingFallingTimeModifier = 0;

        this.fillSquaresInterval = null;
        this.velocityModifierInterval = null;
        this.squaresCountModifierInterval = null;

        this.gameStatistics.reset();
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

        const lastKey = Object.keys(this.gameStatistics.actions).at(-1);
        const time = Object.keys(this.gameStatistics.actions).at(-1);

        this.hud.updateEndGameStatistics({
            ...this.gameStatistics.actions[lastKey],
            time: time,
            isScoreRecord: this.isNewScoreRecord(),
            isNewTimeRecord: this.isNewTimeRecord(time),
        });
        await this.hud.showMessage();
        await this.hud.showEndGameStatistics();

        await this.saveGameData();

        new Timer(async () => {
            this.hud.updateStartButtonText('Maybe again?');
            await this.hud.showStartButton();
        }, 2000).start();
    }

    async saveGameData() {
        const form = {
            'gameData': this.gameStatistics.actions,
            'squares': this.gameStatistics.historicalSquares,
        }

        const response = await fetch(Routing.generate('app_game_save_game_data'), {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(form),
        });
        const data = await response.json();

        this.maxTime = data.maxTime;
        this.maxScore = data.maxScore;
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
                this.gameStatistics.saveAction();
                await this.destroySquare(square);

                return;
            }

            if (!this.isOver) {
                this.loseHp();
                this.gameStatistics.saveAction();
            }

            await this.destroySquare(square);

            if (this.isGameOver()) {
                await this.gameOver();
            }
        });

        square.element.addEventListener('square-clicked', async () => {
            const squareScore = square.calcScore();
            this.score += squareScore;

            this.gameStatistics.increaseAccurateShot();
            this.gameStatistics.saveAction();

            this.hud.updateScore(this.score);
            this.hud.updateAddedScore(squareScore);

            await this.destroySquare(square);

            if (!this.showedRecordScore && this.isNewScoreRecord()) {
                this.showedRecordScore = true;
                this.gameStatistics.timeToNewScoreRecord = this.getElapsedSeconds();

                this.hud.showScoreTrophyIcon();
                this.showInfo('🏆 New Score record ⭐');
            }
        });

        square.missShotArea.addEventListener('miss-shot', () => {
            this.gameStatistics.increaseShotCount();
            this.gameStatistics.saveAction();
            this.printDebugInfo('Miss shot! Actual accurate:', this.gameStatistics.calcAccurate());
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
            this.currentReducingFallingTimeModifier += this.reducingFallingTimeInTime;
            this.printDebugInfo('velocity modifier increased, actual velocity modifier', this.currentReducingFallingTimeModifier)
        }, this.reducingFallingTimeModifierInterval);
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
            const elapsedTime = Date.now() - this.gameStartedDate;

            this.hud.updateTime(elapsedTime);
            this.gameStatistics.saveAction();

            const elapsedTimeKey = Object.keys(this.gameStatistics.actions).at(-1);
            if (!this.showedRecordTime && this.isNewTimeRecord(elapsedTimeKey)) {
                this.showedRecordTime = true;
                this.gameStatistics.timeToNewTimeRecord = this.getElapsedSeconds();

                this.showInfo('🏆 New Time record ⏲');
                this.hud.showTimeTrophyIcon();
            }
        }, 100);
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

    async showInfo(text) {
        this.hud.updateMessageHeader(text);
        this.hud.updateMessageDescription(null)
        await this.hud.showMessage();

        new Timer(() => this.hud.hideMessage(), 2000, true).start();
    }

    isNewScoreRecord() {
        if (!this.maxScore) {
            return false;
        }

        return this.score > this.maxScore;
    }

    isNewTimeRecord(time) {
        if (!this.maxTime) {
            return false;
        }

        return time > this.maxTime;
    }

    getElapsedSeconds() {
        const elapsedTime = Date.now() - this.gameStartedDate;

        return elapsedTime / 1000;
    }
}