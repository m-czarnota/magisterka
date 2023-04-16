export class Timer {
    #timer = null;

    constructor(callback, milliseconds = 1000, oneShot = true) {
        this.callback = callback;
        this.time = milliseconds;
        this.oneShot = oneShot;
    }

    start() {
        const timerKind = this.oneShot ? setTimeout : setInterval;
        const cleanKind = this.oneShot ? clearTimeout : clearInterval;

        cleanKind(this.#timer);
        this.#timer = timerKind(this.callback, this.time);

        return this;
    }

    stop() {
        const timerKind = this.oneShot ? clearTimeout : clearInterval;
        timerKind(this.#timer);

        return this;
    }
}