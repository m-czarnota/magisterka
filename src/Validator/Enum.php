<?php

declare(strict_types=1);

namespace App\Validator;

use Symfony\Component\Validator\Constraint;
use Symfony\Component\Validator\Exception\MissingOptionsException;

#[\Attribute]
final class Enum extends Constraint
{
    public string $message = 'Value is not allowed.';
    public ?string $path;

    public function __construct($options = [], ?string $path = null, ?string $message = null)
    {
        $this->message = $message ?? $this->message;
        $this->path = $path ?? $options['path'] ?? null;
        if (null === $this->path) {
            throw new MissingOptionsException('The path is required option.', ['path']);
        }

        parent::__construct($options, $this->groups, $this->payload);
    }
}
