<?php

namespace App\Service\Controller\Game;

use App\Entity\Game;
use App\Entity\User;
use App\Factory\Game\GameFactory;
use App\Repository\GameRepository;

class GameService
{
    public function __construct(
        private readonly GameRepository $gameRepository,
        private readonly GameFactory $gameFactory,
    ) {
    }

    public function saveGameData(array $data, User $user): Game
    {
        $game = $this->gameFactory->create($data, $user);
        $this->gameRepository->add($game);

        return $game;
    }
}