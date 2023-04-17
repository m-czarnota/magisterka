import {GameEvents} from "./GameEvents";
import {FadeManager} from "../../utils/animations/FadeManager";
import {SquareStatistic} from "./SquareStatistic";
const _ = require('lodash');

const minSize = 45;
const maxSize = 95;

export const defaultAnimationDuration = 9;
const minReducingFallingTime = 1.1;
const maxReducingFallingTime = 2.0;

const colors = [
    '#f3da3a',
    '#a9f33a',
    '#3a8af3',
    '#9a3af3',
    '#f33a65',
    '#f3873a',
];

const squareStatuses = {
    notFullySpawn: 'NOT_FULLY_SPAWN',
    fullySpawned: 'FULLY_SPAWNED',
    exitsFromMap: 'EXITS_FROM_MAP',
    overBoard: 'OUT_OF_BOARD',
}

export class Square {
    id = null;
    parent = null;
    squareStatistic = null;

    reducingFallingTime = undefined;
    status = squareStatuses.notFullySpawn;

    timeToClick = null;
    created_at = undefined;

    destroying = false;

    element = undefined;
    missShotArea = undefined;
    missShotAreaOverSize = 30;

    fallingInterval = null;

    constructor(id, parent) {
        this.id = id;
        this.parent = parent;
        this.squareStatistic = new SquareStatistic(this);

        this.created_at = new Date();

        this.createElement();
        this.drawSize();

        this.createMissShotArea();
        this.missShotArea.appendChild(this.element);

        this.drawPosition();
        this.drawReducingFallingTime();
        this.drawColor();

        this.element.innerText = this.calcScore().toFixed(2);
    }

    async destructor() {
        this.destroying = true;
        this.stopFalling();

        this.status === squareStatuses.overBoard
            ? this.element.remove()
            : await new FadeManager(this.element).fadeOut(100);

        this.missShotArea.remove();
        this.element = null;
        this.parent = null;

        this.squareStatistic.destructor();
        delete this.squareStatistic;
        this.squareStatistic = null;
    }

    createElement() {
        this.element = document.createElement('div');
        this.element.classList.add('square');
        this.element.style.zIndex = String(this.id + 10);

        this.element.addEventListener('mousedown', (event) => {
            if (this.parent.isOver || this.timeToClick) {
                return;
            }

            event.preventDefault();
            event.stopPropagation();

            this.updateTimeClicked();
            this.element.dispatchEvent(GameEvents["square-clicked"]);
        });
    }

    updateTimeClicked() {
        const actionDate = new Date();
        const elapsedSeconds = (actionDate - this.parent.gameStartedDate) / 1000;

        this.timeToClick = (elapsedSeconds % 60).toFixed(4);
    }

    createMissShotArea() {
        this.missShotArea = document.createElement('div');
        this.missShotArea.classList.add('miss-shot-area');
        this.missShotArea.style.width = this.missShotArea.style.height = `${this.getSize() + this.missShotAreaOverSize}px`;

        if (this.parent.displayMissShotArea) {
            this.missShotArea.style.backgroundColor = '#ff000078';
        }

        this.missShotArea.addEventListener('mousedown', (event) => {
            if (this.parent.isOver) {
                return;
            }

            event.preventDefault();
            event.stopPropagation();

            this.squareStatistic.increaseMissShots();
            this.missShotArea.dispatchEvent(GameEvents["miss-shot"]);
        });
    }

    drawSize() {
        const size = _.random(minSize, maxSize, false);
        this.element.style.width = this.element.style.height = `${size}px`;
    }

    drawPosition() {
        this.missShotArea.style.top = `${-this.getSize() - this.missShotAreaOverSize / 2}px`;

        const maxStartPositionW = this.parent.width - parseInt(this.element.style.width.replace('px', '')) - this.missShotAreaOverSize / 2;
        this.missShotArea.style.left = `${_.random(20, maxStartPositionW, false)}px`;
    }

    drawReducingFallingTime() {
        this.reducingFallingTime = _.random(
            minReducingFallingTime + this.parent.currentReducingFallingTimeModifier,
            maxReducingFallingTime + this.parent.currentReducingFallingTimeModifier,
            true,
        );
    }

    drawColor() {
        const index = _.random(colors.length - 1);
        this.element.style.backgroundColor = colors[index];
    }

    getColor() {
        return this.element.style.backgroundColor;
    }

    calcScore() {
        return 100 / this.getSize() * this.reducingFallingTime;
    }

    startFalling() {
        this.playAnimation();

        this.fallingInterval = setInterval(() => {
            if (this.parent.disableFalling) {
                return;
            }

            const height = this.getSize();
            const realCurrentPosition = this.getCurrentPosition(true);

            if (realCurrentPosition - height > 0) {
                this.status = squareStatuses.fullySpawned;
            }

            if (realCurrentPosition > this.parent.height) {
                this.status = squareStatuses.exitsFromMap;
            }

            if (realCurrentPosition > this.parent.height) {
                this.overBoard();
            }
        }, 1000 / 60);
    }

    stopFalling() {
        this.stopAnimation();
        clearInterval(this.fallingInterval);
    }

    overBoard() {
        this.status = squareStatuses.overBoard;
        this.stopFalling();
        this.element.dispatchEvent(GameEvents["square-out-of-board"]);
    }

    getSize() {
        return parseInt(this.element.style.width.replace('px', ''));
    }

    /**
     * Returns pixels where height of square ends.
     * @param real
     * @returns {*}
     */
    getCurrentPosition(real = false) {
        return this.missShotArea.offsetTop + (real ? this.missShotAreaOverSize / 2: 0);
    }

    setCurrentPosition(position) {
        this.missShotArea.style.top = `${position}px`;
    }

    getSquareElement(real = false) {
        return real ? this.element : this.missShotArea;
    }

    serialize() {
        return this.squareStatistic.getStatistics();
    }

    playAnimation() {
        const animation = this.getAnimation();

        if (animation) {
            animation.play();

            return;
        }

        this.getSquareElement().animate([
            { top: `${parseInt(this.getSquareElement().style.top.replace('px', '')) - this.getSize() / 2}px` },
            { top: `${this.parent.height + this.getSize() + this.missShotAreaOverSize / 2}px` }
        ], (defaultAnimationDuration - this.reducingFallingTime) * 1000);
    }

    stopAnimation() {
        this.getAnimation()?.pause();
    }

    getAnimation() {
        return this.getSquareElement().getAnimations()[0] ?? null;
    }
}