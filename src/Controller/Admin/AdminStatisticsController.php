<?php

namespace App\Controller\Admin;

use App\Service\Controller\Admin\AdminStatisticsService;
use Doctrine\DBAL\Exception;
use Doctrine\ORM\NonUniqueResultException;
use Doctrine\ORM\NoResultException;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\Security\Http\Attribute\IsGranted;

#[Route('/admin/statistics')]
#[IsGranted('ROLE_ADMIN')]
class AdminStatisticsController extends AbstractController
{
    public function __construct(
        private readonly AdminStatisticsService $service,
    ) {
    }

    /**
     * @throws NonUniqueResultException
     * @throws NoResultException
     * @throws Exception
     */
    #[Route('/', name: 'app_statistics_adminstatistics_dashboard')]
    public function dashboard(): Response
    {
        return $this->render('page/admin/admin_dashboard_statistics.html.twig', $this->service->dashboard());
    }
}