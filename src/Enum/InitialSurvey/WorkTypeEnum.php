<?php

namespace App\Enum\InitialSurvey;

use App\Interface\Enum\TranslatableEnumInterface;

enum WorkTypeEnum: string implements TranslatableEnumInterface
{
    case PHYSICAL = 'PHYSICAL';
    case MENTAL = 'MENTAL';
    case MIXED = 'MIXED';
    case NO_WORK = 'NO_WORK';

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
