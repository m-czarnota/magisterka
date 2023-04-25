<?php

namespace App\Enum\Game;

enum SquareStatusEnum: string
{
    case NOT_FULLY_SPAWN = 'NOT_FULLY_SPAWN';
    case FULLY_SPAWNED = 'FULLY_SPAWNED' ;
    case EXITING_FROM_MAP = 'EXITING_FROM_MAP' ;
    case OUT_OF_BOARD = 'OUT_OF_BOARD' ;
}
