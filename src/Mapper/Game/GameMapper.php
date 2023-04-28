<?php

namespace App\Mapper\Game;

use App\Entity\Game;
use App\Entity\Square;

class GameMapper
{
    public function __construct(
        private readonly SquareMapper $squareMapper,
    ) {
    }

    public function toArray(Game $game): array
    {
        return [
            'id' => $game->getId(),
            'userId' => $game->getUser()->getId(),
            'time' => $game->getTime(),
            'data' => $game->getData(),
            'score' => $game->getScore(),
            'createdAt' => $game->getCreatedAt(),
            'squares' => array_map(fn(Square $square) => $this->squareMapper->toArray($square), $game->getSquares()->getValues()),
            'timeToNewScoreRecord' => $game->getTimeToNewScoreRecord(),
            'timeToNewTimeRecord' => $game->getTimeToNewTimeRecord(),
        ];
    }
}