<?php

namespace App\Enum\InitialSurvey;

use App\Interface\Enum\TranslatableEnumInterface;

enum GenderEnum implements TranslatableEnumInterface
{
    case MALE;
    case FEMALE;
    case OTHER;

    public function getTransKey(): string
    {
        return match ($this) {
            self::MALE => 'enum.initialSurvey.gender.male',
            self::FEMALE => 'enum.initialSurvey.gender.female',
            self::OTHER => 'enum.initialSurvey.gender.other',
        };
    }
}
