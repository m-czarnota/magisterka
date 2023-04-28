<?php

namespace App\Enum\InitialSurvey;

use App\Interface\Enum\TranslatableEnumInterface;

enum GameTypeEnum: string implements TranslatableEnumInterface
{
    case SANDBOX = 'SANDBOX';
    case RTS = 'RTS';
    case FPS = 'FPS';
    case MMO = 'MMO';
    case MOBA = 'MOBA';
    case RPG = 'RPG';
    case SIMULATION = 'SIMULATION';
    case ACTION = 'ACTION';
    case SURVIVAL = 'SURVIVAL';
    case HORROR = 'HORROR';
    case ADVENTURE = 'ADVENTURE';
    case PLATFORM = 'PLATFORM';
    case LOGIC = 'LOGIC';
    case HACK_AND_SLASH = 'HACK_AND_SLASH';
    case STEALTH = 'STEALTH';
    case STORY_RICH = 'STORY_RICH';
    case SPORT = 'SPORT';
    case COOP = 'COOP';

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
            self::HACK_AND_SLASH => 'enum.initialSurvey.gameType.hackAndSlash',
            self::STEALTH => 'enum.initialSurvey.gameType.stealth',
            self::STORY_RICH => 'enum.initialSurvey.gameType.storyRich',
            self::SPORT => 'enum.initialSurvey.gameType.sport',
            self::COOP => 'enum.initialSurvey.gameType.coop',
        };
    }

    public function getExamplesGames(): array
    {
        return match ($this) {
            self::SANDBOX => ['Satisfactory', 'Minecraft', 'Arma 3', "No Man's Sky"],
            self::RTS => ['Planetary Annihilation', 'Supreme Commander', 'Stronghold', 'Anno', 'Total War'],
            self::FPS => ['Call of Duty', 'Battlefield'],
            self::MMO => ['Black Desert Online', 'Final Fantasy XIV'],
            self::MOBA => ['Dota 2', 'League of Legends'],
            self::RPG => ['Divinity: Original Sin 2', "Baldur's Gate", 'Skyrim'],
            self::SIMULATION => ['Euro Truck Simulator', 'Goat Simulator', 'Microsoft Flight Simulator'],
            self::ACTION => ['GTA', 'Red Dead Redemption, Cyberpunk', 'Elden Ring', 'God of War: Ragnarok'],
            self::SURVIVAL => ['The Forest', 'The Long Dark', "Don't Starve Together", 'Subnautica', 'Raft'],
            self::HORROR => ['Resident Evil', 'The Evil Within', 'Outlast'],
            self::ADVENTURE => ['Stray', 'It Takes Two', 'LEGO'],
            self::PLATFORM => ['Hollow Knight', 'Dead Cells'],
            self::LOGIC => ['Portal', 'SHENZHEN I/O'],
            self::HACK_AND_SLASH => ['Diablo', 'Torchlight'],
            self::STEALTH => ['Dishonored', 'Hitman'],
            self::STORY_RICH => ['Detroit: Become Human', 'This War of Mine'],
            self::SPORT => ['FIFA', 'NBA', 'WWE', 'Football Manager', 'Madden'],
            self::COOP => ['Overcooked!', 'A Way Out', 'It Takes Two', "Don't Starve Together"],
        };
    }
}
