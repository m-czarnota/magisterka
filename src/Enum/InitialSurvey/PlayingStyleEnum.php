<?php

namespace App\Enum\InitialSurvey;

use App\Interface\Enum\TranslatableEnumInterface;

enum PlayingStyleEnum: string implements TranslatableEnumInterface
{
    case MOUSE_AND_KEYBOARD = 'MOUSE_AND_KEYBOARD';
    case GAMEPAD = 'GAMEPAD';
    case PHONE = 'PHONE';

    public function getTransKey(): string
    {
        return match ($this) {
            self::MOUSE_AND_KEYBOARD => 'enum.initialSurvey.playingStyle.mouseAndKeyboard',
            self::GAMEPAD => 'enum.initialSurvey.playingStyle.gamepad',
            self::PHONE => 'enum.initialSurvey.playingStyle.phone',
        };
    }
}
