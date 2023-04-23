<?php

namespace App\Enum\InitialSurvey;

use App\Interface\Enum\TranslatableEnumInterface;

enum GenderEnum: string implements TranslatableEnumInterface
{
    case MALE = 'MALE';
    case FEMALE = 'FEMALE';
    case BOTH = 'BOTH';
    case NOT_KNOW = 'NOT_KNOW';
    case NOT_ANSWER = 'NOT_ANSWER';
    case OTHER = 'OTHER';

    public function getTransKey(): string
    {
        return match ($this) {
            self::MALE => 'enum.initialSurvey.gender.male',
            self::FEMALE => 'enum.initialSurvey.gender.female',
            self::OTHER => 'enum.initialSurvey.gender.other',
            self::BOTH => 'enum.initialSurvey.gender.both',
            self::NOT_KNOW => 'enum.initialSurvey.gender.notKnow',
            self::NOT_ANSWER => 'enum.initialSurvey.gender.notAnswer',
        };
    }
}
