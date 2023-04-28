import {GameEngine} from "./GameEngine";
import {isMobile} from "../../utils/general/functions";

(async function() {
    const gameElem = document.querySelector('#game_app');
    if (!Boolean(gameElem)) {
        return;
    }

    const gameEngine = new GameEngine(800, 600, gameElem);
    gameEngine.drawGameWindow();

    if (isMobile()) {
        gameEngine.hud.updateMessageHeader('Game is unavailable on mobile devices.');
        gameEngine.hud.updateMessageDescription(null)
        gameEngine.hud.showMessage();

        gameEngine.hud.hideStartButton();
    }
})();