<?php

namespace App\Validator;

use Symfony\Component\Validator\Constraint;
use Symfony\Component\Validator\ConstraintValidator;
use Symfony\Component\Validator\Exception\UnexpectedTypeException;
use UnitEnum;

class EnumValidator extends ConstraintValidator
{
    public function validate(mixed $value, Constraint $constraint): void
    {
        if (!$constraint instanceof Enum) {
            throw new UnexpectedTypeException($constraint, Enum::class);
        }

        if ($value instanceof UnitEnum) {
            return;
        }

        if (null === $constraint->path::tryFrom($value)) {
            $this->context
                ->buildViolation($constraint->message)
                ->addViolation();
        }
    }
}
