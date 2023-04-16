import {defaultAnimationDuration} from "./Square";

export class SquareStatistic {
    square = undefined;
    missShots = 0;

    constructor(square) {
        this.square = square;
    }

    increaseMissShots() {
        this.missShots += 1;
    }

    destructor() {
        this.square = null;
    }

    getStatistics() {
        if (!this.square) {
            return {};
        }

        return {
            id: this.square.id,
            size: this.square.getSize(),
            position: this.square.getCurrentPosition(true),
            timeToFall: defaultAnimationDuration -  this.square.reducingFallingTime,
            score: this.square.calcScore(),
            color: this.square.getColor(),
            status: this.square.status,
            missShots: this.missShots,
            timeToClick: this.square.timeToClick,
        };
    }
}