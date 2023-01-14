<?php

namespace App\Validator\User;

use Attribute;
use Symfony\Component\Validator\Constraint;

#[Attribute]
class UsernameIsUnique extends Constraint
{
    public string $message = '';
}