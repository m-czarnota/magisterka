<?php

namespace App\Factory\Game;

use App\Entity\Game;
use App\Entity\User;
use Exception;
use Symfony\Component\DependencyInjection\ParameterBag\ParameterBagInterface;

class GameFactory
{
    public function __construct(
        private readonly ParameterBagInterface $parameterBag,
    ) {
    }

    /**
     * @throws Exception
     */
    public function create(array $data, User $user): Game
    {
        $game = new Game();

        $lastActionKey = array_key_last($data);
        $lastAction = $data[$lastActionKey];

        $collectingAllData = $this->parameterBag->get('game.collecting_all_data');

        return $game
            ->setData($collectingAllData ? $data : null)
            ->setUser($user)
            ->setScore($lastAction['score'])
            ->setTimeToNewScoreRecord($lastAction['timeToNewScoreRecord'])
            ->setTimeToNewTimeRecord($lastAction['timeToNewTimeRecord'])
            ->setTime($lastActionKey);
    }
}