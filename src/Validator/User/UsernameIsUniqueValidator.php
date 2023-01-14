<?php

namespace App\Validator\User;

use App\Repository\UserRepository;
use Doctrine\ORM\NonUniqueResultException;
use Symfony\Component\Validator\Constraint;
use Symfony\Component\Validator\ConstraintValidator;
use Symfony\Component\Validator\Exception\UnexpectedTypeException;
use Symfony\Component\Validator\Exception\UnexpectedValueException;

class UsernameIsUniqueValidator extends ConstraintValidator
{
    protected UserRepository $userRepository;

    public function __construct(UserRepository $userRepository)
    {
        $this->userRepository = $userRepository;
    }

    /**
     * @throws NonUniqueResultException
     */
    public function validate(mixed $value, Constraint $constraint): void
    {
        if (!$constraint instanceof UsernameIsUnique) {
            throw new UnexpectedTypeException($constraint, UsernameIsUnique::class);
        }

        if (!is_string($value)) {
            throw new UnexpectedValueException($value, 'string');
        }

        if (!$this->usernameIsUnique($value)) {
            $this->context->buildViolation($constraint->message)
                ->atPath('username')
                ->addViolation();
        }
    }

    /**
     * @throws NonUniqueResultException
     */
    protected function usernameIsUnique(string $username): bool
    {
        $user = $this->userRepository->findOneByUsername($username);

        return !$user;
    }
}