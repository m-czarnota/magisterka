export class Timer {
    #timer = null;

    constructor(callback, time = 1000, oneShot = true) {
        this.callback = callback;
        this.time = time;
        this.oneShot = oneShot;
    }

    start() {
        const timerKind = this.oneShot ? setTimeout : setInterval;
        this.#timer = timerKind(this.callback, this.time);

        return this;
    }

    stop() {
        const timerKind = this.oneShot ? clearTimeout : clearInterval;
        timerKind(this.#timer);

        return this;
    }
}