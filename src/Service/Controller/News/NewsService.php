<?php

namespace App\Service\Controller\News;

use App\Repository\NewsRepository;

class NewsService
{
    public function __construct(
        private readonly NewsRepository $newsRepository,
    ) {
    }

    public function list(int $pageNumber, int $pageSize): array
    {
        $news = $this->newsRepository->findPage($pageNumber, $pageSize);
        $records = [];

        foreach ($news as $info) {
            $records[] = [
                'id' => $info->getId(),
                'title' => $info->getTitle(),
                'description' => $info->getDescription(),
            ];
        }

        return $records;
    }
}