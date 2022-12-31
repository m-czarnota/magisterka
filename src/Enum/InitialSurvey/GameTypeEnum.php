<?php

namespace App\Enum\InitialSurvey;

use App\Interface\Enum\TranslatableEnumInterface;

enum GameTypeEnum implements TranslatableEnumInterface
{
    case SANDBOX;
    case RTS;
    case FPS;
    case MOBA;
    case RPG;
    case SIMULATION;
    case ACTION;
    case SURVIVAL;
    case HORROR;
    case ADVENTURE;
    case PLATFORM;

    public function getTransKey(): string
    {
        return match ($this) {
            self::SANDBOX => 'enum.initialSurvey.gameType.sandbox',
            self::RTS => 'enum.initialSurvey.gameType.rts',
            self::FPS => 'enum.initialSurvey.gameType.fps',
            self::MOBA => 'enum.initialSurvey.gameType.moba',
            self::RPG => 'enum.initialSurvey.gameType.rpg',
            self::SIMULATION => 'enum.initialSurvey.gameType.simulation',
            self::ACTION => 'enum.initialSurvey.gameType.action',
            self::SURVIVAL => 'enum.initialSurvey.gameType.survival',
            self::HORROR => 'enum.initialSurvey.gameType.horror',
            self::ADVENTURE => 'enum.initialSurvey.gameType.adventure',
            self::PLATFORM => 'enum.initialSurvey.gameType.platform',
        };
    }
}
