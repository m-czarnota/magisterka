<?php

namespace App\Mapper\Game;

use App\Entity\Square;

class SquareMapper
{
    public function toArray(Square $square): array
    {
        return [
            'id' => $square->getId(),
            'size' => $square->getSize(),
            'timeToFall' => $square->getTimeToFall(),
            'timeToClick' => $square->getTimeToClick(),
            'score' => $square->getScore(),
            'status' => $square->getStatus(),
            'missShots' => $square->getMissShots(),
            'position' => $square->getPosition(),
            'color' => $square->getColor(),
            'game' => $square->getGame()->getId(),
            'orderIdInGame' => $square->getOrderIdInGame(),
        ];
    }
}