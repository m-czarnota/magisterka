<?php

declare(strict_types=1);

namespace App\Factory\User;

use App\Entity\User;
use App\Interface\Factory\BaseFactoryInterface;

class UserFactory implements BaseFactoryInterface
{
    public static function create(): User
    {
        return new User();
    }
}