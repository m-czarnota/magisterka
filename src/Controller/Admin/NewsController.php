<?php

namespace App\Controller\Admin;

use App\Form\Type\NewsType;
use App\Interface\Flash\FlashBugManagerInterface;
use App\Service\Controller\Admin\NewsService;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\Security\Http\Attribute\IsGranted;
use Symfony\Contracts\Translation\TranslatorInterface;

#[Route('/admin/news')]
#[IsGranted('ROLE_ADMIN')]
class NewsController extends AbstractController
{
    public function __construct(
        private readonly NewsService $service,
        private readonly EntityManagerInterface $entityManager,
    ) {
    }

    #[Route('/list', name: 'app_admin_news_list')]
    public function list(): Response
    {
        $form = $this->createForm(NewsType::class);

        return $this->render('page/admin/news/list.html.twig', [
            'news' => $this->service->list(),
            'form' => $form->createView(),
        ]);
    }

    #[Route('/add', name: 'app_admin_news_add', methods: Request::METHOD_POST)]
    public function add(Request $request, TranslatorInterface $translator, FlashBugManagerInterface $flashBugManager): Response
    {
        $form = $this->createForm(NewsType::class)->handleRequest($request);
        $data = $form->getData();
        $news = $this->service->add(
            $data?->getTitle() ?? '',
            $data?->getDescription() ?? '',
        );

        $this->entityManager->flush();

        $flashBugManager->addSuccess($translator->trans('page.newsManaging.add.flash.success'));

        return $this->redirectToRoute('app_admin_news_list');
    }
}