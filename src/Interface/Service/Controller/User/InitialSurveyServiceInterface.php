<?php

namespace App\Interface\Service\Controller\User;

use App\Entity\InitialSurvey;

interface InitialSurveyServiceInterface
{
    public function create(InitialSurvey $initialSurvey): void;
}