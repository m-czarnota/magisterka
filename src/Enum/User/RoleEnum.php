<?php

namespace App\Enum\User;

enum RoleEnum: string
{
    case ROLE_PRIMARY_ADMIN = 'ROLE_PRIMARY_ADMIN';
    case ROLE_ADMIN = 'ROLE_ADMIN';
    case ROLE_USER = 'ROLE_USER';
}
