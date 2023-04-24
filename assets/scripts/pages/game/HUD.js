import {FadeManager} from "../../utils/animations/FadeManager";
import {Timer} from "../../utils/game/Timer";
import {HP} from "./HP";
import {formatTimeToGameTime} from "../../utils/general/functions";

export class HUD {
    parent = undefined;

    hudContainer = undefined;

    timeElement = null;
    scoreElement = null;
    startButton = null;

    addedScoreElement = null;
    addedScoreElementTimer = null;

    hp = null;

    timeText = null;
    scoreText = null;

    message = null;
    messageHeader = null;
    messageDescription = null;

    timeToPrepare = 2;

    constructor(parent) {
        this.parent = parent
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
        this.timeElement.classList.add('time-container');

        const subContainer = document.createElement('span');
        subContainer.title = 'Time';
        this.timeElement.appendChild(subContainer);

        const timeIcon = document.createElement('i');
        timeIcon.className = 'fa-regular fa-clock me-1';
        subContainer.appendChild(timeIcon);

        this.timeText = document.createElement('span');
        this.timeText.innerText = '0:00:000';
        subContainer.appendChild(this.timeText);

        this.timeTrophyIcon = document.createElement('i');
        this.timeTrophyIcon.className = 'fa-solid fa-trophy ms-2 d-none text-success';
        subContainer.appendChild(this.timeTrophyIcon);

        return this.timeElement;
    }

    createHpElement() {
        this.hp = new HP();

        return this.hp.createHpContainer();
    }

    createScoreElement() {
        this.scoreElement = document.createElement('div');
        this.scoreElement.classList.add('text-end', 'score-container');

        const subContainer = document.createElement('span');
        subContainer.title = 'Score';
        this.scoreElement.appendChild(subContainer);

        this.addedScoreElement = document.createElement('span');
        this.addedScoreElement.innerText = '+ 1.3';
        this.addedScoreElement.classList.add('d-none', 'me-2', 'text-success', 'fw-semibold');
        subContainer.appendChild(this.addedScoreElement);

        const starIcon = document.createElement('i');
        starIcon.className = 'fa-regular fa-star me-1';
        subContainer.appendChild(starIcon);

        this.scoreText = document.createElement('span');
        this.updateScore(0);
        subContainer.appendChild(this.scoreText);

        this.scoreTrophyIcon = document.createElement('i');
        this.scoreTrophyIcon.className = 'fa-solid fa-trophy ms-2 d-none text-success';
        subContainer.appendChild(this.scoreTrophyIcon);

        return this.scoreElement;
    }

    createStartButton() {
        this.startButton = document.createElement('button');
        this.startButton.type = 'button';
        this.startButton.className = 'btn btn-primary start-button';
        this.startButton.innerHTML = `
            <i class="fa-solid fa-play fa-bounce"></i>
            <span>Play</span>
        `;

        this.startButton.addEventListener('click', async () => {
            // disabling button prevents from double click
            this.startButton.setAttribute('disabled', 'disabled');
            new Timer(() => this.startButton.removeAttribute('disabled'), 1000).start();

            // prepare game and update hud
            this.parent.prepareForNewGame();
            this.updateMessageHeader('Get ready');

            this.showMessage();
            this.hideEndGameStatistics();
            await this.hideStartButton();

            let currentTimeToPrepare = this.timeToPrepare;
            this.updateMessageDescription(currentTimeToPrepare);

            new Timer(() => {
                this.parent.newGame();
            }, this.timeToPrepare * 1000).start();
            const countingDownTimer = new Timer(() => {
                this.updateMessageDescription(--currentTimeToPrepare);

                if (currentTimeToPrepare <= 0) {
                    countingDownTimer.stop();
                    this.hideMessage();
                }
            }, 1000, false).start();
        });

        return this.startButton;
    }

    createMessage() {
        this.message = document.createElement('p');
        this.message.className = 'start-message-text d-none';

        this.message.appendChild(this.createMessageHeader());
        this.message.appendChild(this.createMessageDescription());

        return this.message;
    }

    createMessageHeader() {
        this.messageHeader = document.createElement('span');
        this.messageHeader.innerText = 'Get ready!'

        return this.messageHeader;
    }

    createMessageDescription() {
        this.messageDescription = document.createElement('p');
        this.messageDescription.classList.add('mt-4');
        this.messageDescription.innerText = '0';

        return this.messageDescription;
    }

    createEndGameStatistics() {
        this.endGameStatisticsElement = document.createElement('div');
        this.endGameStatisticsElement.className = 'end-game-statistics d-none';
        this.endGameStatisticsElement.innerText = 'dupa';

        return this.endGameStatisticsElement;
    }

    updateEndGameStatistics(data) {
        const template = document.createElement('template');
        template.innerHTML = `
            <div class="d-flex flex-column">
                <span class="mb-1">
                    <i class="fa-regular fa-star me-1"></i>
                    Score: ${data.score.toFixed(2)}
                    ${data.isScoreRecord ? '🏆' : ''}
                </span>
                <span>
                    <i class="fa-regular fa-clock me-1"></i>
                    Time: ${data.time}s
                    ${data.isNewTimeRecord ? '🏆' : ''}
                </span>
            </div>
        `.trim();

        this.endGameStatisticsElement.innerHTML = '';
        this.endGameStatisticsElement.appendChild(template.content.firstChild);
    }

    updateScore(score) {
        this.scoreText.innerText = score.toFixed(2);
    }

    async updateAddedScore(score) {
        this.addedScoreElement.innerText = `+ ${score.toFixed(2)}`;
        const fadeManager = new FadeManager(this.addedScoreElement);

        await fadeManager.fadeIn(100);

        if (this.addedScoreElementTimer) {
            this.addedScoreElementTimer.start();

            return;
        }

        this.addedScoreElementTimer = new Timer(async () => {
            await fadeManager.fadeOut(100);
            this.addedScoreElementTimer = null;
        }, 1000, true).start();
    }

    updateTime(elapsedTime) {
        this.timeText.innerText = formatTimeToGameTime(elapsedTime);
    }

    updateHp(hp) {
        this.hp.setActualHp(hp);
    }

    updateMessageHeader(text) {
        this.messageHeader.innerText = text;
    }

    updateMessageDescription(text) {
        this.messageDescription.innerText = text;
    }

    updateStartButtonText(text) {
        this.startButton.querySelector('span').innerText = text;
    }

    async showStartButton() {
        const fadeManager = new FadeManager(this.startButton);
        await fadeManager.fadeIn(300);
    }

    async hideStartButton() {
        const fadeManager = new FadeManager(this.startButton);
        await fadeManager.fadeOut(300);
    }

    async showMessage() {
        const fadeManager = new FadeManager(this.message);
        await fadeManager.fadeIn(300);
    }

    async hideMessage() {
        const fadeManager = new FadeManager(this.message);
        await fadeManager.fadeOut(300);
    }

    async showEndGameStatistics() {
        await new FadeManager(this.endGameStatisticsElement).fadeIn(300);
    }

    async hideEndGameStatistics() {
        await new FadeManager(this.endGameStatisticsElement).fadeOut(300);
    }

    showTimeTrophyIcon() {
        if (!this.timeTrophyIcon.classList.contains('d-none')) {
            return;
        }

        new FadeManager(this.timeTrophyIcon).fadeIn(100);
    }

    hideTimeTrophyIcon() {
        new FadeManager(this.timeTrophyIcon).fadeOut(100);
    }

    showScoreTrophyIcon() {
        if (!this.scoreTrophyIcon.classList.contains('d-none')) {
            return;
        }

        new FadeManager(this.scoreTrophyIcon).fadeIn(100);
    }

    hideScoreTrophyIcon() {
        new FadeManager(this.scoreTrophyIcon).fadeOut(100);
    }
}