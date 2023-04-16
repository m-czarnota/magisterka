<?php

namespace App\Factory\Game;

use App\Entity\Game;
use App\Entity\Square;
use App\Enum\Game\SquareStatusEnum;
use App\Security\Exception\ValidationException;
use Symfony\Component\Validator\Validator\ValidatorInterface;

class SquareFactory
{
    public function __construct(
        private readonly ValidatorInterface $validator,
    ) {
    }

    /**
     * @throws ValidationException
     */
    public function create(
        int $size,
        float $timeToFall,
        ?float $timeToClick,
        float $score,
        SquareStatusEnum $status,
        int $missShots,
        float $position,
        string $color,
        Game $game,
        int $orderIdInGame,
    ): Square {
        $square = new Square();
        $square
            ->setSize($size)
            ->setTimeToFall($timeToFall)
            ->setTimeToClick($timeToClick)
            ->setScore($score)
            ->setStatus($status)
            ->setMissShots($missShots)
            ->setPosition($position)
            ->setColor($color)
            ->setGame($game)
            ->setOrderIdInGame($orderIdInGame);

        $errors = $this->validator->validate($square);
        if ($errors->count() > 0) {
            $error = $errors->get(0);
            throw new ValidationException($error->getMessage());
        }

        return $square;
    }
}