<?php

declare(strict_types=1);

namespace App\Factory\User;

use App\Entity\InitialSurvey;
use App\Interface\Factory\BaseFactoryInterface;

class InitialSurveyFactory implements BaseFactoryInterface
{
    public function create(): InitialSurvey
    {
        return new InitialSurvey();
    }
}