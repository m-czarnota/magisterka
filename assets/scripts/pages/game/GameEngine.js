import {Square} from "./Square";
import {HUD} from "./HUD";

export class GameEngine {
    constructor(width, height, container) {
        this.width = width;
        this.height = height;
        this.appContainer = container;
        this.hud = new HUD();

        this.squares = [];

        this.velocityModifierInTime = 0.1;
        this.velocityModifierTimeInterval = 10000;

        this.squaresCountModifierInTime = 1;
        this.squaresCountModifierTimeInterval = 20000;

        this.debug = true;
        this.isImmortal = false;
    }

    drawGameWindow() {
        this.gameWindowContainer = document.createElement('div');
        this.gameWindowContainer.appendChild(this.hud.createHudContainer());
        // this.gameWindowContainer.style.paddingTop = this.gameWindowContainer.style.paddingBottom = '100px';
        // this.gameWindowContainer.style.width = `${this.width}px`;
        // this.gameWindowContainer.style.height = `${this.height + 200}px`;
        // this.gameWindowContainer.style.zIndex = '1000';
        // this.gameWindowContainer.style.backgroundColor = '#ffffff';
        this.appContainer.appendChild(this.gameWindowContainer);

        this.gameWindow = document.createElement('div');
        this.gameWindow.style.width = `${this.width}px`;
        this.gameWindow.style.height = `${this.height}px`;
        this.gameWindow.classList.add('game-window');

        this.gameWindowContainer.appendChild(this.gameWindow);
    }

    prepareForNewGame() {
        this.clearSquares();

        this.isOver = false;
        this.maxSquares = 4;
        this.squaresHistoryCount = 0;

        this.hp = 3;
        this.score = 0;

        this.gameSeconds = 0;
        this.gameTimer = null;

        this.currentVelocityModifier = 0;

        this.fillSquaresInterval = null;
        this.velocityModifierInterval = null;
        this.squaresCountModifierInterval = null;

        this.shotCount = 0;
        this.accurateShotCount = 0;
    }

    async newGame() {
        this.prepareForNewGame();

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

    gameOver() {
        if (this.isOver) {
            return;
        }

        this.stopFillingSquares();
        this.stopGameTimer();
        this.stopVelocityModifierTimer();
        this.stopSquaresCountModifierTimer();

        console.log('game over!');
        this.isOver = true;
    }

    async startFillingSquares() {
        this.fillSquaresInterval = setInterval(() => {
            if (this.squares.length >= this.maxSquares) {
                return;
            }

            const square = new Square(this.squaresHistoryCount, this);
            this.squares.push(square);
            this.gameWindow.appendChild(square.element);

            this.setEventListenersForSquare(square);

            square.startFalling();
            this.squaresHistoryCount++;
        }, 300);
    }

    stopFillingSquares() {
        clearInterval(this.fillSquaresInterval);
    }

    setEventListenersForSquare(square) {
        square.element.addEventListener('square-out-of-board', (event) => {
            if (this.isImmortal) {
                this.destroySquare(square);

                return;
            }

            if (!this.isOver) {
                this.loseHp();
            }

            this.destroySquare(square);

            if (this.isGameOver()) {
                this.gameOver();
            }
        });

        square.element.addEventListener('square-clicked', (event) => {
            this.score += square.calcScore();
            this.increaseAccurateShot();

            this.hud.updateScore(this.score);

            this.destroySquare(square);

            console.log('actual score', this.score);
        });
    }

    loseHp() {
        this.hp -= 1;
        this.printDebugInfo('Fail! -1HP, actual HP:', this.hp);
    }

    destroySquare(square) {
        const index = this.squares.indexOf(square);

        square.destructor();
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
        this.gameTimer = setInterval(() => {
            this.gameSeconds += 1;
            this.hud.updateTime(this.gameSeconds);
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

    increaseAccurateShot() {
        this.shotCount += 1;
        this.accurateShotCount += 1;
    }
}