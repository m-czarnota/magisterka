export class Statistic {
    parent = null;

    actions = {};
    shotCount = 0;
    accurateShotCount = 0;

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
        const elapsedSeconds = (actionDate - this.parent.gameStartedDate) / 1000;

        const minutes = Math.floor(elapsedSeconds / 60);
        const seconds = (elapsedSeconds % 60).toFixed(4);

        const key = `${minutes}:${seconds}`;
        const data = {
            score: this.parent.score,
            hp: this.parent.hp,
            totalShots: this.shotCount,
            accurateShots: this.accurateShotCount,
            squares: this.parent.squares.filter(square => square.destroying === false).map(square => square.serialize()),
            currentVelocityModifier: this.parent.currentVelocityModifier,
            maxSquares: this.parent.maxSquares,
        };

        this.actions[key] = data;
        this.parent.printDebugInfo(elapsedSeconds, key, data);
    }
}