<?php

declare(strict_types=1);

namespace App\Factory\User;

use App\Entity\User;
use App\Enum\User\RoleEnum;
use App\Interface\Factory\User\UserFactoryInterface;
use Symfony\Component\DependencyInjection\ParameterBag\ParameterBagInterface;
use Symfony\Component\PasswordHasher\Hasher\UserPasswordHasherInterface;

class UserFactory implements UserFactoryInterface
{
    public function __construct(
        protected ParameterBagInterface $parameterBag,
        protected UserPasswordHasherInterface $passwordEncoder,
    ) {}

    public function create(): User
    {
        return new User();
    }

    public function createPrimaryAdmin(): User
    {
        $plainPassword = $this->parameterBag->get('creating.user.admin_default_password');
        $user = $this->create();

        return $user
            ->setUsername($this->parameterBag->get('creating.user.admin_default_username'))
            ->setPassword($this->hashPassword($user, $plainPassword))
            ->setRoles(RoleEnum::getNames());
    }

    protected function hashPassword(User $user, string $plainPassword): string
    {
        return $this->passwordEncoder->hashPassword($user, $plainPassword);
    }
}