<?php

namespace App\EventListener\User;

use App\Entity\User;
use Symfony\Component\HttpFoundation\RedirectResponse;
use Symfony\Component\HttpKernel\Event\RequestEvent;
use Symfony\Component\Routing\Generator\UrlGeneratorInterface;
use Symfony\Component\Security\Core\Authentication\Token\Storage\TokenStorageInterface;

class InitialSurveyListener
{
    public function __construct(
        protected TokenStorageInterface $tokenStorage,
        protected UrlGeneratorInterface $urlGenerator,
        protected readonly string $initialSurveyRoute = 'app_initial_survey_survey'
    ) {}

    public function __invoke(RequestEvent $event): void
    {
        $isRouteToInitialSurvey = $event->getRequest()->get('_route') === $this->initialSurveyRoute;
        if (!$event->isMainRequest() || $isRouteToInitialSurvey) {
            return;
        }

        /** @var User|null $user */
        $user = $this->tokenStorage->getToken()?->getUser();
        if (!($user instanceof User) || $user->getInitialSurvey()) {
            return;
        }

        $this->redirectToInitialSurvey($user, $event);
    }

    protected function redirectToInitialSurvey(User $user, RequestEvent $event): void
    {
        $response = new RedirectResponse($this->urlGenerator->generate($this->initialSurveyRoute));
        $event->setResponse($response);
    }
}