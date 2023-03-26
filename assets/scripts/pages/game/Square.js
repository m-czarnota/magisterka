import {GameEvents} from "./GameEvents";
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
        this.element = undefined;
        this.velocity = undefined;
        this.startedHeightAchieve = false;

        this.createElement();
        this.drawSize();
        this.drawPosition();
        this.drawVelocity();
        this.drawColor();

        this.calcScore();
    }

    destructor() {
        this.stopFalling();
        this.element.remove();
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

            this.element.dispatchEvent(GameEvents["square-clicked"]);
        })
    }

    drawSize() {
        const size = _.random(minSize, maxSize, false);
        this.element.style.width = `${size}px`;
        this.element.style.height = 0;
    }

    drawPosition() {
        this.element.style.top = 0;

        const maxStartPositionW = this.parent.width - parseInt(this.element.style.width.replace('px', ''));
        this.element.style.left = `${_.random(20, maxStartPositionW, false)}px`;
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

    calcScore() {
        const width = parseInt(this.element.style.width.replace('px', ''));

        return 100 / width * this.velocity;
    }

    startFalling() {
        this.fallingInterval = setInterval(() => {
            const width = parseInt(this.element.style.width.replace('px', ''));
            let height = this.element.style.height.replace('px', '');
            height = this.startedHeightAchieve ? parseInt(height) : parseFloat(height);

            if (!this.startedHeightAchieve && height < width) {
                const newHeight = height + this.velocity;
                this.element.style.height = `${newHeight}px`;

                return;
            }
            this.startedHeightAchieve = true;

            const currentTop = this.element.offsetTop;
            this.element.style.top = `${currentTop + this.velocity}px`;

            if (this.element.offsetTop + height > this.parent.height) {
                const newHeight = height - this.velocity;
                this.element.style.height = `${newHeight}px`;

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
        this.element.dispatchEvent(GameEvents["square-out-of-board"]);
        this.stopFalling();
    }
}