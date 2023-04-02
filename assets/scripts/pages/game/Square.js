import {GameEvents} from "./GameEvents";
import {FadeManager} from "../../utils/animations/FadeManager";
const _ = require('lodash');

const minSize = 45;
const maxSize = 95;

// todo: more true random - maybe animation
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
    constructor(id, parent) {
        this.id = id;
        this.parent = parent;
        this.velocity = undefined;

        this.startedHeightAchieve = false;
        this.exitsFromMap = false;
        this.destroying = false;

        this.element = undefined;
        this.missShotArea = undefined;
        this.missShotAreaOverSize = 30;

        this.clicked = false;
        this.outOfBoard = false;

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
        this.missShotArea.style.width = `${this.getWidth() + this.missShotAreaOverSize}px`;
        this.missShotArea.style.height = 0;

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
        this.element.style.width = `${size}px`;
        this.element.style.height = 0;
    }

    drawPosition() {
        this.missShotArea.style.top = `${-this.missShotAreaOverSize / 2}px`;

        const maxStartPositionW = this.parent.width - parseInt(this.element.style.width.replace('px', '')) - this.missShotAreaOverSize / 2;
        this.missShotArea.style.left = `${_.random(20, maxStartPositionW, false)}px`;
    }

    drawVelocity() {
        this.velocity = _.random(
            minVelocity + this.parent.currentVelocityModifier,
            maxVelocity + this.parent.currentVelocityModifier,
            true,
        );
        // console.log(this.velocity)
    }

    drawColor() {
        const index = _.random(colors.length - 1);
        this.element.style.backgroundColor = colors[index];
    }

    getColor() {
        return this.element.style.backgroundColor;
    }

    calcScore() {
        return 100 / this.getWidth() * this.velocity;
    }

    startFalling() {
        this.fallingInterval = setInterval(() => {
            const width = parseInt(this.element.style.width.replace('px', ''));
            const height = this.getHeight(!this.startedHeightAchieve);

            if (!this.startedHeightAchieve && height < width) {
                this.setHeight(height + this.velocity);

                return;
            }
            this.startedHeightAchieve = true;

            if (this.parent.disableFalling) {
                return;
            }

            const currentPosition = this.getCurrentPosition();
            this.setCurrentPosition(currentPosition + this.velocity);

            if (this.getCurrentPosition(true) + height > this.parent.height) {
                this.exitsFromMap = true;

                const newHeight = height - this.velocity;
                this.setHeight(newHeight);

                if (newHeight < 0) {
                    this.overBoard();
                }
            }
        }, 1000 / 60);
    }

    stopFalling() {
        clearInterval(this.fallingInterval);
    }

    overBoard() {
        this.outOfBoard = true;
        this.stopFalling();
        this.element.dispatchEvent(GameEvents["square-out-of-board"]);
    }

    getWidth() {
        return parseInt(this.element.style.width.replace('px', ''));
    }

    getHeight(asFloat = false) {
        const height = this.element.style.height.replace('px', '');

        return asFloat ? parseFloat(height) : parseInt(height);
    }

    setHeight(height) {
        this.element.style.height = `${height}px`;
        this.missShotArea.style.height = `${height + this.missShotAreaOverSize}px`;
    }

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
            size: this.getWidth(),
            position: this.getCurrentPosition(),
            actualHeight: this.getHeight(),
            velocity: this.velocity,
            score: this.calcScore(),
            color: this.getColor(),
            clicked: this.clicked,
            outOfBoard: this.outOfBoard,
            startsFromBegin: !this.startedHeightAchieve,
            existsFromMap: this.exitsFromMap,
        };
    }
}