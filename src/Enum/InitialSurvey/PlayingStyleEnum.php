<?php

namespace App\Enum\InitialSurvey;

use App\Interface\Enum\TranslatableEnumInterface;

enum PlayingStyleEnum implements TranslatableEnumInterface
{
    case MOUSE_AND_KEYBOARD;
    case GAMEPAD;

    public function getTransKey(): string
    {
        return match ($this) {
            self::MOUSE_AND_KEYBOARD => 'enum.initialSurvey.playingStyle.mouseAndKeyboard',
            self::GAMEPAD => 'enum.initialSurvey.playingStyle.gamepad',
        };
    }
}