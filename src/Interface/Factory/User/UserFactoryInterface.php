<?php

namespace App\Interface\Factory\User;

use App\Entity\User;
use App\Interface\Factory\BaseFactoryInterface;

interface UserFactoryInterface extends BaseFactoryInterface
{
    public function createPrimaryAdmin(): User;
}