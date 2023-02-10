<?php

namespace App\Service\Controller\Security;

use App\Entity\User;
use App\Interface\Security\User\UserAuthenticatorProgrammaticallyInterface;
use App\Security\Authenticator\PasswordlessAuthenticator;
use Symfony\Component\HttpFoundation\RequestStack;
use Symfony\Component\Security\Http\Authentication\UserAuthenticatorInterface;
use Symfony\Component\Security\Http\Authenticator\Passport\Badge\RememberMeBadge;

class UserAuthenticatorProgrammatically implements UserAuthenticatorProgrammaticallyInterface
{
    public function __construct(
        protected UserAuthenticatorInterface $authenticatorManager,
        protected PasswordlessAuthenticator $authenticator,
        protected RequestStack $requestStack,
    ) {}

    public function authenticateUser(User $user): void
    {
        $this->authenticatorManager->authenticateUser($user, $this->authenticator, $this->requestStack->getCurrentRequest(), [new RememberMeBadge()]);
    }
}