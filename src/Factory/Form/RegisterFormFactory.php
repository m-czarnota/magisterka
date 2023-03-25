<?php

namespace App\Factory\Form;

use App\Form\Type\RegisterType;
use App\Entity\User;
use App\Interface\Factory\Form\User\UserFormFactoryInterface;
use App\Interface\Factory\User\UserFactoryInterface;
use Symfony\Component\Form\FormInterface;
use Symfony\Component\HttpFoundation\RequestStack;
use Symfony\Component\Form\FormFactoryInterface as SymfonyFormFactoryInterface;

class RegisterFormFactory implements UserFormFactoryInterface
{
    public function __construct(
        protected SymfonyFormFactoryInterface $formFactory,
        protected UserFactoryInterface $userFactory,
        protected RequestStack $requestStack,
    ) {

    }

    public function create(User $user, array $params = []): FormInterface
    {
        $user = $this->userFactory->create();
        $form = $this->formFactory->create(RegisterType::class, $user);
        $form->handleRequest($this->requestStack->getCurrentRequest());

        return $form;
    }
}