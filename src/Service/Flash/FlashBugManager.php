<?php

namespace App\Service\Flash;

use App\Enum\Flash\FlashMessageEnum;
use Symfony\Component\HttpFoundation\RequestStack;

class FlashBugManager
{
    protected RequestStack $requestStack;

    public function __construct(RequestStack $requestStack)
    {
        $this->requestStack = $requestStack;
    }

    public function push(string $type, string $message): void
    {
        $this->requestStack->getSession()->getFlashBag()->add($type, $message);
    }

    public function addSuccess(string $message): void
    {
        $this->push(FlashMessageEnum::SUCCESS->value, $message);
    }

    public function addDanger(string $message): void
    {
        $this->push(FlashMessageEnum::DANGER->value, $message);
    }

    public function addWarning(string $message): void
    {
        $this->push(FlashMessageEnum::WARNING->value, $message);
    }

    public function addInfo(string $message): void
    {
        $this->push(FlashMessageEnum::INFO->value, $message);
    }
}