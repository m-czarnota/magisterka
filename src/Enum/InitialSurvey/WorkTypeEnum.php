<?php

namespace App\Enum\InitialSurvey;

use App\Interface\Enum\TranslatableEnumInterface;

enum WorkTypeEnum implements TranslatableEnumInterface
{
    case PHYSICAL;
    case MENTAL;
    case MIXED;
    case NO_WORK;

    public function getTransKey(): string
    {
        return match ($this) {
            self::PHYSICAL => 'enum.initialSurvey.workType.physical',
            self::MENTAL => 'enum.initialSurvey.workType.mental',
            self::MIXED => 'enum.initialSurvey.workType.mixed',
            self::NO_WORK => 'enum.initialSurvey.workType.noWork',
        };
    }
}
