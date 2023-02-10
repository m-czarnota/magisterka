<?php

namespace App\Enum\InitialSurvey;

use App\Interface\Enum\TranslatableEnumInterface;

enum GenderEnum: string implements TranslatableEnumInterface
{
    case MALE = 'MALE';
    case FEMALE = 'FEMALE';
    case OTHER = 'OTHER';

    public function getTransKey(): string
    {
        return match ($this) {
            self::MALE => 'enum.initialSurvey.gender.male',
            self::FEMALE => 'enum.initialSurvey.gender.female',
            self::OTHER => 'enum.initialSurvey.gender.other',
        };
    }
}
