<?php

namespace App\Service\Controller\Admin;

use App\Entity\News;
use App\Factory\Admin\NewsFactory;
use App\Repository\NewsRepository;

class NewsService
{
    public function __construct(
        private readonly NewsRepository $newsRepository,
        private readonly NewsFactory $newsFactory,
    ) {
    }

    public function list(): array
    {
        return $this->newsRepository->findAll();
    }

    public function add(
        string $title,
        string $description,
    ): News {
        $news = $this->newsFactory->create($title, $description);
        $this->newsRepository->add($news);

        return $news;
    }
}