import {delay} from "../general/functions";

export class FadeManager {
    #element = undefined;

    constructor(element) {
        this.#element = element;
    }

    /**
     * Hides element
     * @param milliseconds
     * @returns {Promise<unknown>}
     */
    async fadeOut(milliseconds) {
        const animation = this.#element.animate([
            { opacity: 1 },
            { opacity: 0 }
        ], {
            duration: milliseconds,
            fill: 'forwards',
        });
        animation.onfinish = () => this.#element.classList.add('d-none');

        return animation.finished;
    }

    /**
     * Shows element
     * @param milliseconds
     * @returns {Promise<unknown>}
     */
    async fadeIn(milliseconds) {
        this.#element.classList.remove('d-none');

        await delay(1);

        const animation = this.#element.animate([
            { opacity: 0 },
            { opacity: 1 }
        ], {
            duration: milliseconds,
            fill: 'forwards',
        });
        animation.onfinish = null;

        return animation.finished;
    }
}