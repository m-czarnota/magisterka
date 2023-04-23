<?php

namespace App\Controller\User;

use App\Entity\User;
use App\Repository\GameRepository;
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
    public function index(GameRepository $gameRepository): Response
    {
        /** @var User $user */
        $user = $this->getUser();
        $userId = $user->getId();

        return $this->render('user/dashboard.html.twig', [
            'maxScore' => $gameRepository->getMaxScoreByUserId($userId),
            'maxTime' => $gameRepository->getMaxTimeByUserId($userId),
        ]);
    }
}