export class HUD {
    constructor() {
        this.timeElement = null;
        this.hpElement = null;
        this.scoreElement = null;
    }

    createHudContainer() {
        this.hudContainer = document.createElement('div');
        this.hudContainer.classList.add('d-flex', 'justify-content-between');

        this.hudContainer.appendChild(this.createTimeElement());
        this.hudContainer.appendChild(this.createHpElement());
        this.hudContainer.appendChild(this.createScoreElement());

        return this.hudContainer;
    }

    createTimeElement() {
        this.timeElement = document.createElement('div');
        // this.timeElement.classList.add('invisible');
        this.timeElement.innerText = '0:00';

        return this.timeElement;
    }

    createHpElement() {
        this.hpElement = document.createElement('div');

        return this.hpElement;
    }

    createScoreElement() {
        this.scoreElement = document.createElement('div');
        this.scoreElement.classList.add('text-end');
        this.scoreElement.innerText = '0';

        return this.scoreElement;
    }

    updateScore(score) {
        this.scoreElement.innerText = score.toFixed(2);
    }

    updateTime(gameSeconds) {
        const minutes = Math.floor(gameSeconds / 60);
        const seconds = gameSeconds % 60;

        this.timeElement.innerText = `${minutes}:${seconds < 10 ? '0' + seconds : seconds}`;
    }

    updateHp(hp) {

    }
}