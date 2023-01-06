<?php

namespace App\Interface\Transformer;

interface StringTransformerInterface
{
    public function transform(string $string): string;
}