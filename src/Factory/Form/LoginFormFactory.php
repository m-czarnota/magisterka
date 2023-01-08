<?php

namespace App\Factory\Form;

use App\Form\Type\LoginType;
use App\Interface\Factory\Form\FormFactoryInterface;
use Symfony\Component\Form\FormError;
use Symfony\Component\Form\FormFactoryInterface as SymfonyFormFactoryInterface;
use Symfony\Component\Form\FormInterface;
use Symfony\Component\HttpFoundation\RequestStack;
use Symfony\Component\Security\Http\Authentication\AuthenticationUtils;

class LoginFormFactory implements FormFactoryInterface
{
    protected SymfonyFormFactoryInterface $formFactory;
    protected AuthenticationUtils $authenticationUtils;
    protected RequestStack $requestStack;

    public function __construct(SymfonyFormFactoryInterface $formFactory, AuthenticationUtils $authenticationUtils, RequestStack $requestStack)
    {
        $this->formFactory = $formFactory;
        $this->authenticationUtils = $authenticationUtils;
        $this->requestStack = $requestStack;
    }

    public function create(): FormInterface
    {
        $error = $this->authenticationUtils->getLastAuthenticationError();
        $lastUsername = $this->authenticationUtils->getLastUsername();
        $form = $this->formFactory->create(LoginType::class);

        if ($this->requestStack->getCurrentRequest()->headers->get('referer')) {
            $form->get('username')->setData($lastUsername);
        }

        if ($error) {
            $form->addError(new FormError($error->getMessageKey()));
        }

        return $form;
    }
}