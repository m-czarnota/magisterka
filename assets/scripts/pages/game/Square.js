import {GameEvents} from "./GameEvents";
import {FadeManager} from "../../utils/animations/FadeManager";
const _ = require('lodash');

const minSize = 45;
const maxSize = 95;

const defaultAnimationDuration = 9;
const minVelocity = 1.1;
const maxVelocity = 2.0;

const colors = [
    '#f3da3a',
    '#a9f33a',
    '#3a8af3',
    '#9a3af3',
    '#f33a65',
    '#f3873a',
];

export class Square {
    id = null;
    parent = null;

    velocity = undefined;

    isFullSizeOnMap = false;
    isExitsFromMap = false;
    destroying = false;

    element = undefined;
    missShotArea = undefined;
    missShotAreaOverSize = 30;

    clicked = false;
    outOfBoard = false;

    fallingInterval = null;

    constructor(id, parent) {
        this.id = id;
        this.parent = parent;

        this.createElement();
        this.drawSize();

        this.createMissShotArea();
        this.missShotArea.appendChild(this.element);

        this.drawPosition();
        this.drawVelocity();
        this.drawColor();

        this.calcScore();
    }

    async destructor() {
        this.destroying = true;

        const fadeManager = new FadeManager(this.element);

        this.stopFalling();

        if (this.outOfBoard) {
            this.element.remove();
        } else {
            await fadeManager.fadeOut(100);
        }

        this.missShotArea.remove();
        this.element = null;
        this.parent = null;
    }

    createElement() {
        this.element = document.createElement('div');
        this.element.classList.add('square');
        this.element.style.zIndex = String(this.id + 10);

        this.element.addEventListener('mousedown', (event) => {
            if (this.parent.isOver) {
                return;
            }

            event.preventDefault();
            event.stopPropagation();

            this.clicked = true;
            this.element.dispatchEvent(GameEvents["square-clicked"]);
        });
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

    drawVelocity() {
        this.velocity = _.random(
            minVelocity + this.parent.currentVelocityModifier,
            maxVelocity + this.parent.currentVelocityModifier,
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
        return 100 / this.getSize() * this.velocity;
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
                this.isFullSizeOnMap = true;
            }

            if (realCurrentPosition > this.parent.height) {
                this.isExitsFromMap = true;
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
        this.outOfBoard = true;
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
        return {
            id: this.id,
            size: this.getSize(),
            position: this.getCurrentPosition(true),
            velocity: this.velocity,
            score: this.calcScore(),
            color: this.getColor(),
            clicked: this.clicked,
            outOfBoard: this.outOfBoard,
            isFullSizeOnMap: this.isFullSizeOnMap,
            existsFromMap: this.isExitsFromMap,
        };
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
        ], (defaultAnimationDuration - this.velocity) * 1000);
    }

    stopAnimation() {
        this.getAnimation()?.pause();
    }

    getAnimation() {
        return this.getSquareElement().getAnimations()[0] ?? null;
    }
}