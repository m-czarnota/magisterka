<?php

namespace App\Factory\Game;

use App\Entity\Game;
use App\Entity\User;
use Exception;

class GameFactory
{
    /**
     * @throws Exception
     */
    public function create(array $data, User $user): Game
    {
        $game = new Game();
        $lastActionKey = array_key_last($data);
        $lastAction = $data[$lastActionKey];

        return $game
            ->setData($data)
            ->setUser($user)
            ->setScore($lastAction['score'])
            ->setTimeToNewScoreRecord($lastAction['timeToNewScoreRecord'])
            ->setTimeToNewTimeRecord($lastAction['timeToNewTimeRecord'])
            ->setTime($lastActionKey);
    }
}