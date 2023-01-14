<?php

namespace App\Interface\Service\Controller\Security;

use App\Entity\User;

interface RegisterServiceInterface
{
    public function register(User $user): void;
}