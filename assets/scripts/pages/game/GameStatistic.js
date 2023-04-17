import {formatTimeToGameTime} from "../../utils/general/functions";

export class GameStatistic {
    parent = null;

    actions = {};
    shotCount = 0;
    accurateShotCount = 0;

    historicalSquares = {};

    constructor(parent) {
        this.parent = parent;
    }

    reset() {
        this.actions = {};
        this.shotCount = 0;
        this.accurateShotCount = 0;
    }

    increaseShotCount() {
        this.shotCount += 1;
    }

    increaseAccurateShot() {
        this.shotCount += 1;
        this.accurateShotCount += 1;
    }

    calcAccurate() {
        return this.accurateShotCount / this.shotCount;
    }

    saveAction() {
        const actionDate = new Date();
        const elapsedSeconds = actionDate - this.parent.gameStartedDate;

        const livingSquares = this.parent.squares.filter(square => square.destroying === false);

        const key = formatTimeToGameTime(elapsedSeconds);
        const data = {
            score: this.parent.score,
            hp: this.parent.hp,
            totalShots: this.shotCount,
            accurateShots: this.accurateShotCount,
            squares: livingSquares.map(square => square.serialize()),
            currentReducingFallingTimeModifier: this.parent.currentReducingFallingTimeModifier,
            maxSquares: this.parent.maxSquares,
        };

        this.actions[key] = data;
        this.parent.printDebugInfo(elapsedSeconds, key, data);

        for (const square of livingSquares) {
            this.historicalSquares[square.id] = square.serialize();
        }
    }
}