<?php

namespace App\Controller\User;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

#[Route(path: '/user')]
class DashboardController extends AbstractController
{
    #[Route(path: '/dashboard', name: 'app_user_dashboard')]
    public function index(): Response
    {
        return $this->render('user/dashboard.html.twig');
    }
}