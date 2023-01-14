<?php

namespace App\Interface\Security\User;

use App\Entity\User;

interface UserAuthenticatorProgrammaticallyInterface
{
    public function authenticateUser(User $user): void;
}