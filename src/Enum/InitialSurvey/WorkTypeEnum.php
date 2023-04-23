<?php

namespace App\Enum\InitialSurvey;

use App\Interface\Enum\TranslatableEnumInterface;

enum WorkTypeEnum: string implements TranslatableEnumInterface
{
    case PHYSICAL = 'PHYSICAL';
    case MENTAL = 'MENTAL';
    case MIXED = 'MIXED';
    case STUDENT = 'STUDENT';
    case WORKING_STUDENT_PHYSICAL = 'WORKING_STUDENT_PHYSICAL';
    case WORKING_STUDENT_MENTAL = 'WORKING_STUDENT_MENTAL';
    case BURNT_OUT = 'BURNT_OUT';
    case NO_WORK = 'NO_WORK';

    public function getTransKey(): string
    {
        return match ($this) {
            self::PHYSICAL => 'enum.initialSurvey.workType.physical',
            self::MENTAL => 'enum.initialSurvey.workType.mental',
            self::MIXED => 'enum.initialSurvey.workType.mixed',
            self::NO_WORK => 'enum.initialSurvey.workType.noWork',
            self::STUDENT => 'enum.initialSurvey.workType.student',
            self::WORKING_STUDENT_PHYSICAL => 'enum.initialSurvey.workType.workingStudentPhysical',
            self::WORKING_STUDENT_MENTAL => 'enum.initialSurvey.workType.workingStudentMental',
            self::BURNT_OUT => 'enum.initialSurvey.workType.burntOut',
        };
    }
}
