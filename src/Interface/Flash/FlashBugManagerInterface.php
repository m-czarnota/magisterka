<?php

namespace App\Interface\Flash;

interface FlashBugManagerInterface
{
    public function addSuccess(string $message): void;
    public function addDanger(string $message): void;
    public function addWarning(string $message): void;
    public function addInfo(string $message): void;
}