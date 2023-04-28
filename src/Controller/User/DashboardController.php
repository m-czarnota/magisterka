<?php

namespace App\Controller\User;

use App\Entity\User;
use App\Mapper\Game\GameMapper;
use App\Repository\GameRepository;
use App\Util\Game\TimeTransformer;
use Doctrine\ORM\NonUniqueResultException;
use Doctrine\ORM\NoResultException;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\Security\Http\Attribute\IsGranted;

#[Route(path: '/user')]
#[IsGranted('ROLE_DASHBOARD_AG')]
class DashboardController extends AbstractController
{
    /**
     * @throws NonUniqueResultException
     * @throws NoResultException
     */
    #[Route(path: '/dashboard', name: 'app_user_dashboard')]
    public function index(GameRepository $gameRepository, TimeTransformer $timeTransformer, GameMapper $gameMapper): Response
    {
        /** @var User $user */
        $user = $this->getUser();
        $userId = $user->getId();

        $maxTime = $gameRepository->getMaxTimeByUserId($userId);
        $lastGame = $gameRepository->findOneLastGameForUserId($userId);
        $lastGame = $lastGame ? $gameMapper->toArray($lastGame) : [];

        if (!empty($lastGame)) {
            $lastGame['time'] = $timeTransformer->adjustTimeToBeDisplayed($lastGame['time']);

            if ($lastGame['timeToNewScoreRecord']) {
                $lastGame['timeToNewScoreRecord'] = $timeTransformer->adjustTimeToBeDisplayed($lastGame['timeToNewScoreRecord']);
            }

            if ($lastGame['timeToNewTimeRecord']) {
                $lastGame['timeToNewTimeRecord'] = $timeTransformer->adjustTimeToBeDisplayed($lastGame['timeToNewTimeRecord']);
            }
        }

        return $this->render('user/dashboard.html.twig', [
            'maxScore' => $gameRepository->getMaxScoreByUserId($userId),
            'maxTime' => $maxTime ? $timeTransformer->adjustTimeToBeDisplayed($maxTime) : null,
            'numberOfGames' => $gameRepository->getNumberOfGamesByUserId($userId),
            'lastGame' => $lastGame,
        ]);
    }
}