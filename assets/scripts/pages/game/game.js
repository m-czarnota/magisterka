import {GameEngine} from "./GameEngine";

(async function() {
    const gameElem = document.querySelector('#game_app');
    if (!Boolean(gameElem)) {
        return;
    }

    const gameEngine = new GameEngine(800, 600, gameElem);
    gameEngine.drawGameWindow();
})();