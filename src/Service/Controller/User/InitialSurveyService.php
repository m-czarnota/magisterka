<?php

namespace App\Service\Controller\User;

use App\Entity\InitialSurvey;
use App\Entity\User;
use App\Interface\Flash\FlashBugManagerInterface;
use App\Interface\Service\Controller\User\InitialSurveyServiceInterface;
use App\Repository\InitialSurveyRepository;
use Symfony\Component\Security\Core\Authentication\Token\Storage\TokenStorageInterface;
use Symfony\Component\Security\Core\Exception\UserNotFoundException;
use Symfony\Contracts\Translation\TranslatorInterface;

class InitialSurveyService implements InitialSurveyServiceInterface
{
    public function __construct(
        protected InitialSurveyRepository $initialSurveyRepository,
        protected TokenStorageInterface $tokenStorage,
        protected FlashBugManagerInterface $flashBugManager,
        protected TranslatorInterface $translator,
    ) {}

    public function create(InitialSurvey $initialSurvey): void
    {
        $this->createInitialSurvey($initialSurvey);
        $this->addCreateSuccessFlash();
    }

    protected function createInitialSurvey(InitialSurvey $initialSurvey): void
    {
        $user = $this->tokenStorage->getToken()?->getUser();
        if (!($user instanceof User)) {
            throw new UserNotFoundException("To create initial survey for user the user must be logged.");
        }

        $initialSurvey->setUser($user);
        $user->setInitialSurvey($initialSurvey);

        $this->initialSurveyRepository->save(true, $initialSurvey);
    }

    protected function addCreateSuccessFlash(): void
    {
        $message = $this->translator->trans('page.initialSurvey.flash.success');
        $this->flashBugManager->addSuccess($message);
    }
}