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
        const elapsedSeconds = (actionDate - this.parent.gameStartedDate) / 1000;

        const minutes = Math.floor(elapsedSeconds / 60);
        const seconds = (elapsedSeconds % 60);
        const secondsFixed = seconds.toFixed(4);

        const livingSquares = this.parent.squares.filter(square => square.destroying === false);

        const key = `${minutes}:${seconds < 10 ? '0' + secondsFixed : secondsFixed}`;
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