<?php

declare(strict_types=1);

namespace App\Controller\User;

use App\Entity\User;
use App\Factory\User\InitialSurveyFactory;
use App\Form\Type\NewInitialSurveyType;
use App\Interface\Service\Controller\User\InitialSurveyServiceInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\RedirectResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

#[Route(path: '/initial_survey')]
class InitialSurveyController extends AbstractController
{
    #[Route(path: '/new', name: 'app_initial_survey_survey')]
    public function new(Request $request, InitialSurveyServiceInterface $initialSurveyService, InitialSurveyFactory $initialSurveyFactory): RedirectResponse|Response
    {
        /** @var User $user */
        $user = $this->getUser();
        if ($user->getInitialSurvey() !== null) {
            return $this->redirectToRoute('app_user_dashboard');
        }

        $initialSurvey = $initialSurveyFactory->create();
        $form = $this->createForm(NewInitialSurveyType::class, $initialSurvey)->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid()) {
            $initialSurveyService->create($form->getViewData());

            return $this->redirectToRoute('app_user_dashboard');
        }

        return $this->render('page/initial_survey/new.html.twig', [
            'form' => $form->createView(),
        ]);
    }
}