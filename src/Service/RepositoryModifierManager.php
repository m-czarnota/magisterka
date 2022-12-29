<?php

namespace App\Service;

use App\Entity\User;
use App\Interface\RepositoryModifierInterface;
use Doctrine\Persistence\ManagerRegistry;
use Doctrine\Persistence\ObjectManager;
use Symfony\Component\Security\Core\Exception\UnsupportedUserException;
use Symfony\Component\Security\Core\User\PasswordAuthenticatedUserInterface;
use Symfony\Component\Security\Core\User\PasswordUpgraderInterface;

class RepositoryModifierManager implements RepositoryModifierInterface, PasswordUpgraderInterface
{
    private ObjectManager $objectManager;

    public function __construct(ManagerRegistry $managerRegistry)
    {
        $this->objectManager = $managerRegistry->getManager();
    }

    public function save(object $entity, bool $flash = false): self
    {
        $this->objectManager->persist($entity);

        if ($flash) {
            $this->objectManager->flush();
        }

        return $this;
    }

    public function remove(object $entity, bool $flash = false): self
    {
        $this->objectManager->remove($entity);

        if ($flash) {
            $this->objectManager->flush();
        }

        return $this;
    }

    public function saveMultiple(array $entities, bool $flash = false): self
    {
        foreach ($entities as $entity) {
            $this->save($entity);
        }

        if ($flash) {
            $this->objectManager->flush();
        }

        return $this;
    }

    public function removeMultiple(array $entities, bool $flash = false): self
    {
        foreach ($entities as $entity) {
            $this->remove($entity);
        }

        if ($flash) {
            $this->objectManager->flush();
        }

        return $this;
    }

    /**
     * Used to upgrade (rehash) the user's password automatically over time.
     */
    public function upgradePassword(PasswordAuthenticatedUserInterface $user, string $newHashedPassword): void
    {
        if (!$user instanceof User) {
            throw new UnsupportedUserException(sprintf('Instances of "%s" are not supported.', \get_class($user)));
        }

        $user->setPassword($newHashedPassword);

        $this->save($user, true);
    }

    public function setObjectManager(ObjectManager $objectManager): self
    {
        $this->objectManager = $objectManager;

        return $this;
    }
}