<?php

declare(strict_types=1);

namespace App\Controller\Home;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class HomeController extends AbstractController
{
    #[Route(path: '/choice', name: 'app_choice')]
    public function choice(): Response
    {
        return $this->render('page/home/choice.html.twig');
    }
}