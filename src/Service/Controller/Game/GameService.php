<?php

namespace App\Service\Controller\Game;

use App\Entity\Game;
use App\Entity\Square;
use App\Entity\User;
use App\Enum\Game\SquareStatusEnum;
use App\Factory\Game\GameFactory;
use App\Factory\Game\SquareFactory;
use App\Repository\GameRepository;
use App\Repository\SquareRepository;
use App\Security\Exception\ValidationException;
use Exception;

class GameService
{
    public function __construct(
        private readonly GameRepository $gameRepository,
        private readonly GameFactory $gameFactory,
        private readonly SquareFactory $squareFactory,
        private readonly SquareRepository $squareRepository,
    ) {
    }

    /**
     * @throws Exception
     */
    public function saveGameData(array $gameData, array $squares, User $user): Game
    {
        $game = $this->gameFactory->create($gameData, $user);
        $this->gameRepository->add($game);

        foreach ($squares as $square) {
            $this->createSquare($square, $game);
        }

        return $game;
    }

    /**
     * @throws ValidationException
     */
    private function createSquare(array $data, Game $game): Square
    {
        $square = $this->squareFactory->create(
            $data['size'],
            $data['timeToFall'],
            $data['timeToClick'],
            $data['score'],
            SquareStatusEnum::from($data['status']),
            $data['missShots'],
            $data['position'],
            $data['color'],
            $game,
            $data['id'],
        );
        $this->squareRepository->add($square);

        return $square;
    }
}