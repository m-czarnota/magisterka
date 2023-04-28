<?php

namespace App\Util\Game;

class TimeTransformer
{
    public function adjustTimeToBeDisplayed(float $time): string
    {
        $minutes = floor($time / 60);
        $seconds = $time % 60;
        $seconds = $seconds < 10 ? "0$seconds" : $seconds;

        return "$minutes:$seconds";
    }
}