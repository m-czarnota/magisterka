<?php

namespace App\Interface\Factory\Form\User;

use App\Entity\User;
use Symfony\Component\Form\FormInterface;

interface UserFormFactoryInterface
{
    public function create(User $user, array $params = []): FormInterface;
}