<?php

namespace App\Controller\Security;

use App\Factory\Form\LoginFormFactory;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class SecurityController extends AbstractController
{
    #[Route(path: '/login', name: 'app_login')]
    public function login(LoginFormFactory $loginFormFactory): Response
    {
        if ($this->getUser()) {
            return $this->redirectToRoute('app_user_dashboard');
        }

        $form = $loginFormFactory->create();

        return $this->render('security/login.html.twig', [
            'form' => $form->createView(),
        ]);
    }

    #[Route(path: '/logout', name: 'app_logout')]
    public function logout()
    {
        throw new \LogicException('This method can be blank - it will be intercepted by the logout key on your firewall.');
    }
}