<?php

namespace App\Controller\News;

use App\Service\Controller\News\NewsService;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Annotation\Route;

#[Route('/news')]
class NewsController extends AbstractController
{
    public function __construct(
        private readonly NewsService $service,
    ) {
    }

    #[Route('/list/{page}', name: 'app_news_list', requirements: ['page' => '\d+'], options: ['expose' => true])]
    public function list(int $page, Request $request): JsonResponse
    {
        $data = json_decode($request->getContent(), true);

        return $this->json($this->service->list(
            $page,
            $data['pageSize'] ?? 2,
        ));
    }
}