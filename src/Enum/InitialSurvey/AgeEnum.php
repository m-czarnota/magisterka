<?php

namespace App\Enum\InitialSurvey;

enum AgeEnum: string
{
    case VERY_YOUNG = '<15';
    case YOUNG = '15-25';
    case MIDDLE = '25-45';
    case MIDDLE_AGE = '45-60';
    case OLD = '>60';

    public static function values(): array
    {
        return array_map(fn(self $case) => $case->value, self::cases());
    }
}
