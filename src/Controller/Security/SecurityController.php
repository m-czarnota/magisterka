<?php

namespace App\Controller\Security;

use App\Entity\User;
use App\Factory\Form\UserFormFactory;
use App\Factory\Form\RegisterFormFactory;
use App\Interface\Generator\RandomUsernameGeneratorInterface;
use App\Repository\UserRepository;
use App\Service\Controller\Security\RegisterService;
use Doctrine\ORM\NonUniqueResultException;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class SecurityController extends AbstractController
{
    #[Route(path: '/login', name: 'app_login', methods: [Request::METHOD_GET, Request::METHOD_POST])]
    public function login(UserFormFactory $loginFormFactory): Response
    {
        $user = $this->getUser();
        if ($user instanceof User) {
            return $this->redirectToRoute('app_user_dashboard');
        }

        $form = $loginFormFactory->create();

        return $this->render('security/login.html.twig', [
            'form' => $form->createView(),
        ]);
    }

    /**
     * @throws NonUniqueResultException
     */
    #[Route(path: '/check-if-login-with-password', name: 'user_check_if_login_with_password', options: ['expose' => true], methods: Request::METHOD_POST)]
    public function loginWithPassword(Request $request, UserRepository $userRepository): JsonResponse
    {
        $username = $request->request->get('username');
        $user = $userRepository->findOneByUsername($username ?? '');

        return new JsonResponse(['hasPassword' => $user?->getPassword() !== null]);
    }

    #[Route(path: '/logout', name: 'app_logout')]
    public function logout()
    {
        throw new \LogicException('This method can be blank - it will be intercepted by the logout key on your firewall.');
    }

    #[Route(path: '/register', name: 'app_register', methods: [Request::METHOD_GET, Request::METHOD_POST])]
    public function register(RegisterFormFactory $registerFormFactory, RegisterService $registerService): Response
    {
        if ($this->getUser()) {
            return $this->redirectToRoute('app_user_dashboard');
        }

        $user = new User();
        $form = $registerFormFactory->create($user);

        if ($form->isSubmitted() && $form->isValid()) {
            $registerService->register($form->getViewData());

            return $this->redirectToRoute('app_user_dashboard');
        }

        return $this->render('security/register.html.twig', [
            'form' => $form->createView(),
        ]);
    }

    #[Route(path: '/generate_name', name: 'app_generate_name', options: ['expose' => true], methods: [Request::METHOD_GET])]
    public function generateName(RandomUsernameGeneratorInterface $nameGenerator): Response
    {
        return new JsonResponse(['name' => $nameGenerator->generateRandomName()]);
    }
}