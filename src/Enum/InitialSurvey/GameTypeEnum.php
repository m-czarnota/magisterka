<?php

namespace App\Enum\InitialSurvey;

use App\Interface\Enum\TranslatableEnumInterface;

enum GameTypeEnum implements TranslatableEnumInterface
{
    case SANDBOX;
    case RTS;
    case FPS;
    case MMO;
    case MOBA;
    case RPG;
    case SIMULATION;
    case ACTION;
    case SURVIVAL;
    case HORROR;
    case ADVENTURE;
    case PLATFORM;
    case LOGIC;

    public function getTransKey(): string
    {
        return match ($this) {
            self::SANDBOX => 'enum.initialSurvey.gameType.sandbox',
            self::RTS => 'enum.initialSurvey.gameType.rts',
            self::FPS => 'enum.initialSurvey.gameType.fps',
            self::MMO => 'enum.initialSurvey.gameType.mmo',
            self::MOBA => 'enum.initialSurvey.gameType.moba',
            self::RPG => 'enum.initialSurvey.gameType.rpg',
            self::SIMULATION => 'enum.initialSurvey.gameType.simulation',
            self::ACTION => 'enum.initialSurvey.gameType.action',
            self::SURVIVAL => 'enum.initialSurvey.gameType.survival',
            self::HORROR => 'enum.initialSurvey.gameType.horror',
            self::ADVENTURE => 'enum.initialSurvey.gameType.adventure',
            self::PLATFORM => 'enum.initialSurvey.gameType.platform',
            self::LOGIC => 'enum.initialSurvey.gameType.logic',
        };
    }

    public function getExamplesGames(): array
    {
        return match ($this) {
            self::SANDBOX => ['Satisfactory', 'Minecraft', 'GTA', 'Skyrim', "No Man's Sky"],
            self::RTS => ['Planetary Annihilation', 'Supreme Commander', 'Stronghold', 'Anno', 'Total War'],
            self::FPS => ['Call of Duty', 'Battlefield'],
            self::MMO => ['Black Desert Online', 'Final Fantasy XIV'],
            self::MOBA => ['Dota 2', 'League of Legends'],
            self::RPG => ['Divinity: Original Sin 2', "Baldur's Gate", 'Skyrim'],
            self::SIMULATION => ['Euro Truck Simulator', 'Goat Simulator', 'Microsoft Flight Simulator'],
            self::ACTION => ['GTA', 'Red Dead Redemption, Cyberpunk', 'Elden Ring', 'God of War'],
            self::SURVIVAL => ['The Forest', 'The Long Dark', "Don't Starve Together", 'Subnautica'],
            self::HORROR => ['Resident Evil', 'The Evil Within', 'Outlast'],
            self::ADVENTURE => ['Stray', 'It Takes Two', 'LEGO'],
            self::PLATFORM => ['Hollow Knight', 'Dead Cells'],
            self::LOGIC => ['Portal', 'SHENZHEN I/O'],
        };
    }
}
