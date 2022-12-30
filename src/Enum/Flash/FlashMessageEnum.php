<?php

namespace App\Enum\Flash;

enum FlashMessageEnum: string
{
    case SUCCESS = 'success';
    case DANGER = 'danger';
    case WARNING = 'warning';
    case INFO = 'info';
}
