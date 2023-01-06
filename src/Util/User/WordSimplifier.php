<?php

namespace App\Util\User;

use App\Interface\Transformer\StringTransformerInterface;

class WordSimplifier implements StringTransformerInterface
{
    public function transform(string $string): string
    {
        $string = str_replace("\r", '', $string);
        $string = str_replace("\n", '', $string);
        $string = str_replace("-", '', $string);

        return $string;
    }
}