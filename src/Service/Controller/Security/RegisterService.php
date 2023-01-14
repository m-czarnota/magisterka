<?php

namespace App\Service\Controller\Security;

use App\Entity\User;
use App\Enum\User\RoleEnum;
use App\Interface\Flash\FlashBugManagerInterface;
use App\Interface\Repository\RepositoryModifierInterface;
use App\Interface\Security\User\UserAuthenticatorProgrammaticallyInterface;
use App\Interface\Service\Controller\Security\RegisterServiceInterface;
use Symfony\Contracts\Translation\TranslatorInterface;

class RegisterService implements RegisterServiceInterface
{
    protected RepositoryModifierInterface $repositoryModifier;
    protected FlashBugManagerInterface $flashBugManager;
    protected TranslatorInterface $translator;
    protected UserAuthenticatorProgrammaticallyInterface $userAuthenticatorProgrammatically;

    public function __construct(RepositoryModifierInterface $repositoryModifier, FlashBugManagerInterface $flashBugManager, TranslatorInterface $translator, UserAuthenticatorProgrammaticallyInterface $userAuthenticatorProgrammatically)
    {
        $this->repositoryModifier = $repositoryModifier;
        $this->flashBugManager = $flashBugManager;
        $this->translator = $translator;
        $this->userAuthenticatorProgrammatically = $userAuthenticatorProgrammatically;
    }

    public function register(User $user): void
    {
        $this->createUser($user);
        $this->addSuccessFlash();
        $this->loginUser($user);
    }

    protected function createUser(User $user): void
    {
        $user->setRoles([RoleEnum::ROLE_USER->name]);
        $this->repositoryModifier->save($user, true);
    }

    protected function addSuccessFlash(): void
    {
        $message = $this->translator->trans('page.register.flash.success');
        $this->flashBugManager->addSuccess($message);
    }

    protected function loginUser(User $user): void
    {
        $this->userAuthenticatorProgrammatically->authenticateUser($user);

        $rememberUsernameMessage = $this->translator->trans('page.register.flash.rememberName', ['%username%' => $user->getUsername()]);
        $this->flashBugManager->addWarning($rememberUsernameMessage);
    }
}