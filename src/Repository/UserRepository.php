<?php

namespace App\Repository;

use App\Entity\User;
use App\Enum\User\RoleEnum;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\ORM\NonUniqueResultException;
use Doctrine\ORM\NoResultException;
use Doctrine\Persistence\ManagerRegistry;

/**
 * @extends ServiceEntityRepository<User>
 *
 * @method User|null find($id, $lockMode = null, $lockVersion = null)
 * @method User|null findOneBy(array $criteria, array $orderBy = null)
 * @method User[]    findAll()
 * @method User[]    findBy(array $criteria, array $orderBy = null, $limit = null, $offset = null)
 */
class UserRepository extends ServiceEntityRepository
{
    public function __construct(
        protected GameRepository $gameRepository,
        ManagerRegistry $registry,
    ) {
        parent::__construct($registry, User::class);
    }

    public function save(bool $flash = false, User ...$users): self
    {
        foreach ($users as $user) {
            $this->getEntityManager()->persist($user);
        }

        if ($flash) {
            $this->getEntityManager()->flush();
        }

        return $this;
    }

    public function remove(bool $flash = false, User ...$users): self
    {
        foreach ($users as $user) {
            $this->removeAllAssociations($user);
            $this->getEntityManager()->remove($user);
        }

        if ($flash) {
            $this->getEntityManager()->flush();
        }

        return $this;
    }

    /**
     * @throws NonUniqueResultException
     */
    public function findOnePrimaryAdmin(): ?User
    {
        $qb = $this->createQueryBuilder('u');

        return $qb
            ->where($qb->expr()->like('u.roles', ':role'))
            ->setParameter('role', '%' . RoleEnum::ROLE_PRIMARY_ADMIN->name . '%')
            ->getQuery()
            ->getOneOrNullResult();
    }

    /**
     * @throws NonUniqueResultException
     */
    public function findOneByUsername(string $username): ?User
    {
        return $this->createQueryBuilder('u')
            ->where('u.username = :username')
            ->setParameter('username', $username)
            ->getQuery()
            ->getOneOrNullResult();
    }

    /**
     * @throws NonUniqueResultException
     * @throws NoResultException
     */
    public function getNumberOfRegisteredUsers(): ?int
    {
        $qb = $this->createQueryBuilder('u');

        return $qb
            ->select($qb->expr()->count('u.id'))
            ->where($qb->expr()->notLike('u.roles', ':adminRole'))
            ->setParameter('adminRole', '%' . RoleEnum::ROLE_ADMIN->name . '%')
            ->getQuery()
            ->getSingleScalarResult();
    }

    /**
     * @throws NonUniqueResultException
     * @throws NoResultException
     */
    public function getNumberOfUsersWithSurveyAndGame(): ?int
    {
        $qb = $this->createQueryBuilder('u');

        return $qb
            ->select($qb->expr()->count('u.id'))
            ->join('u.games', 'g')
            ->join('u.initialSurvey', 'is')
            ->where($qb->expr()->notLike('u.roles', ':adminRole'))
            ->setParameter('adminRole', '%' . RoleEnum::ROLE_ADMIN->name . '%')
            ->getQuery()
            ->getSingleScalarResult();
    }

    protected function removeAllAssociations(User $user): self
    {
        $this->gameRepository->remove(false, ...$user->getGames());

        return $this;
    }
}
