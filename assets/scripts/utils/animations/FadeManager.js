import {delay} from "../general/functions";

export class FadeManager {
    constructor(element) {
        this.element = element;
    }

    /**
     * Hides element
     * @param milliseconds
     * @returns {Promise<unknown>}
     */
    async fadeOut(milliseconds) {
        const time = milliseconds / 1000;

        this.element.style.transition = `opacity ${time}s`;
        this.element.style.opacity = 0;

        return new Promise(resolve => setTimeout(() => {
            this.element.classList.add('d-none');

            // if (typeof (callback) === 'function') {
            //     callback();
            // }

            resolve();
        }, milliseconds));
    }

    /**
     * Shows element
     * @param milliseconds
     * @returns {Promise<unknown>}
     */
    async fadeIn(milliseconds) {
        const time = milliseconds / 1000;

        this.element.style.opacity = 0;
        this.element.classList.remove('d-none');
        this.element.style.transition = `opacity ${time}s`;

        await delay(1);
        this.element.style.opacity = 1;

        return new Promise(resolve => setTimeout(() => {
            // if (typeof (callback) === 'function') {
            //     callback();
            // }
            resolve();
        }, milliseconds));
    }
}