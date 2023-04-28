<?php

namespace App\Factory\Admin;

use App\Entity\News;

class NewsFactory
{
    public function create(
        string $title,
        string $description,
    ): News {
        $news = new News();

        return $news
            ->setTitle($title)
            ->setDescription($description);
    }
}