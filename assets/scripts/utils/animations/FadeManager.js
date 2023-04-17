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
        this.#element.onfinish = () => this.#element.classList.add('d-none');
        const animation = this.#element.animate([
            { opacity: 1 },
            { opacity: 0 }
        ], {
            duration: milliseconds,
            fill: 'forwards',
        });

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

        this.#element.onfinish = null;
        const animation = this.#element.animate([
            { opacity: 0 },
            { opacity: 1 }
        ], {
            duration: milliseconds,
            fill: 'forwards',
        });

        return animation.finished;
    }
}