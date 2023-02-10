<?php

namespace App\Factory\Form;

use App\Form\Type\RegisterType;
use App\Interface\Factory\Form\FormFactoryInterface;
use App\Interface\Factory\User\UserFactoryInterface;
use Symfony\Component\Form\FormInterface;
use Symfony\Component\HttpFoundation\RequestStack;
use Symfony\Component\Form\FormFactoryInterface as SymfonyFormFactoryInterface;

class RegisterFormFactory implements FormFactoryInterface
{
    public function __construct(
        protected SymfonyFormFactoryInterface $formFactory,
        protected UserFactoryInterface $userFactory,
        protected RequestStack $requestStack,
    ) {}

    public function create(): FormInterface
    {
        $user = $this->userFactory->create();
        $form = $this->formFactory->create(RegisterType::class, $user);
        $form->handleRequest($this->requestStack->getCurrentRequest());

        return $form;
    }
}