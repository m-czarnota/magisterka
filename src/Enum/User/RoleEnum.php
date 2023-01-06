<?php

namespace App\Enum\User;

use App\Interface\Enum\ConvertableEnumInterface;

enum RoleEnum implements ConvertableEnumInterface
{
    case ROLE_PRIMARY_ADMIN;
    case ROLE_ADMIN;
    case ROLE_USER;

    public static function getNames(): array
    {
        return array_map(fn(self $role) => $role->name, self::cases());
    }
}
