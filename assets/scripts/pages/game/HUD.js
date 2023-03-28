import {FadeManager} from "../../utils/animations/FadeManager";
import {Timer} from "../../utils/game/Timer";

export class HUD {
    #startMessageTimerText = null;

    constructor(parent) {
        this.parent = parent
        this.timeElement = null;
        this.hpElement = null;
        this.scoreElement = null;
        this.startButton = null;

        this.timeText = null;
        this.scoreText = null;
        this.startMessageText = null;

        this.timerToStart = null;
        this.timeToPrepare = 2;
    }

    destructor() {
        this.parent = null;
    }

    createHudContainer() {
        this.hudContainer = document.createElement('div');
        this.hudContainer.classList.add('hud-container');

        this.hudContainer.appendChild(this.createTimeElement());
        this.hudContainer.appendChild(this.createHpElement());
        this.hudContainer.appendChild(this.createScoreElement());

        return this.hudContainer;
    }

    createTimeElement() {
        this.timeElement = document.createElement('div');
        // this.timeElement.classList.add('invisible');

        const icon = document.createElement('i');
        icon.className = 'fa-regular fa-clock me-1';
        this.timeElement.appendChild(icon);

        this.timeText = document.createElement('span');
        this.timeText.innerText = '0:00';
        this.timeElement.appendChild(this.timeText);

        return this.timeElement;
    }

    createHpElement() {
        this.hpElement = document.createElement('div');

        return this.hpElement;
    }

    createScoreElement() {
        this.scoreElement = document.createElement('div');
        this.scoreElement.classList.add('text-end');

        const icon = document.createElement('i');
        icon.className = 'fa-regular fa-star me-1';
        this.scoreElement.appendChild(icon);

        this.scoreText = document.createElement('span');
        this.scoreText.innerText = '0';
        this.scoreElement.appendChild(this.scoreText);

        return this.scoreElement;
    }

    createStartButton() {
        this.startButton = document.createElement('button');
        this.startButton.type = 'button';
        this.startButton.className = 'btn btn-primary start-button';
        this.startButton.innerHTML = `
            <i class="fa-solid fa-play fa-bounce"></i>
            Play
        `;

        this.startButton.addEventListener('click', async () => {
            this.showStartMessage();
            await this.hideStartButton();

            let currentTimeToPrepare = this.timeToPrepare;
            this.updateStartMessageTimerText(currentTimeToPrepare);

            new Timer(() => {
                this.parent.newGame();
            }, this.timeToPrepare * 1000).start();
            const countingDownTimer = new Timer(() => {
                this.updateStartMessageTimerText(--currentTimeToPrepare);

                if (currentTimeToPrepare <= 0) {
                    countingDownTimer.stop();
                    this.hideStartMessage();
                }
            }, 1000, false).start();
        });

        return this.startButton;
    }

    createStartMessageText() {
        this.startMessageText = document.createElement('p');
        this.startMessageText.classList = 'start-message-text d-none';
        this.startMessageText.innerText = 'Get ready!'
        this.startMessageText.appendChild(this.#createStartMessageTimerText());

        return this.startMessageText;
    }

    #createStartMessageTimerText() {
        this.#startMessageTimerText = document.createElement('p');
        this.#startMessageTimerText.classList.add('mt-4');
        this.#startMessageTimerText.innerText = '0';

        return this.#startMessageTimerText;
    }

    updateScore(score) {
        this.scoreText.innerText = score.toFixed(2);
    }

    updateTime(gameSeconds) {
        const minutes = Math.floor(gameSeconds / 60);
        const seconds = gameSeconds % 60;

        this.timeText.innerText = `${minutes}:${seconds < 10 ? '0' + seconds : seconds}`;
    }

    updateHp(hp) {

    }

    updateStartMessageTimerText(text) {
        this.#startMessageTimerText.innerText = text;
    }

    async hideStartButton() {
        const fadeManager = new FadeManager(this.startButton);
        await fadeManager.fadeOut(300);
    }

    async showStartMessage() {
        const fadeManager = new FadeManager(this.startMessageText);
        await fadeManager.fadeIn(300);
    }

    async hideStartMessage() {
        const fadeManager = new FadeManager(this.startMessageText);
        await fadeManager.fadeOut(300);
    }
}