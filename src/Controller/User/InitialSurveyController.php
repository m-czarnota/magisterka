<?php

declare(strict_types=1);

namespace App\Controller\User;

use App\Factory\User\InitialSurveyFactory;
use App\Form\Type\NewInitialSurveyType;
use App\Interface\Flash\FlashBugManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\RedirectResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Contracts\Translation\TranslatorInterface;

#[Route(path: '/initial_survey')]
class InitialSurveyController extends AbstractController
{
    #[Route(path: '/new', name: 'app_initial_survey_survey')]
    public function new(Request $request, FlashBugManagerInterface $flashBugManager, TranslatorInterface $translator, InitialSurveyFactory $initialSurveyFactory): RedirectResponse|Response
    {
        $initialSurvey = $initialSurveyFactory->create();
        $form = $this->createForm(NewInitialSurveyType::class, $initialSurvey)->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid()) {
            $flashBugManager->addSuccess($translator->trans('page.initialSurvey.flash.success'));
            return $this->redirectToRoute('app_user_dashboard');
        }

        return $this->render('page/initial_survey/new.html.twig', [
            'form' => $form->createView(),
        ]);
    }
}