<?php

namespace App\Service\Controller\Statistics;

use App\Repository\GameRepository;
use App\Repository\SquareRepository;
use App\Repository\UserRepository;
use Doctrine\DBAL\Exception;
use Doctrine\ORM\NonUniqueResultException;
use Doctrine\ORM\NoResultException;

class AdminStatisticsService
{
    public function __construct(
        private readonly GameRepository $gameRepository,
        private readonly UserRepository $userRepository,
        private readonly SquareRepository $squareRepository,
    ) {
    }

    /**
     * @throws NonUniqueResultException
     * @throws NoResultException
     * @throws Exception
     */
    public function dashboard(): array
    {
        return [
            'maxTime' => $this->gameRepository->getMaxTime(),
            'maxScore' => $this->gameRepository->getMaxScore(),
            'numbersOfRegisteredUsers' => $this->userRepository->getNumberOfRegisteredUsers(),
            'getMaxGamesByOneUser' => $this->gameRepository->getMaxGamesByOneUser(),
            'numberOfUsersWithSurveyAndGame' => $this->userRepository->getNumberOfUsersWithSurveyAndGame(),
            'numberOfGames' => $this->gameRepository->getNumberOfGames(),
            'avgTimeToClick' => $this->squareRepository->getAvgTimeToClick(),
        ];
    }
}