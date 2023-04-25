<?php

namespace App\Repository;

use App\Entity\Square;
use App\Enum\User\RoleEnum;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\ORM\NonUniqueResultException;
use Doctrine\ORM\NoResultException;
use Doctrine\Persistence\ManagerRegistry;

/**
 * @extends ServiceEntityRepository<Square>
 *
 * @method Square|null find($id, $lockMode = null, $lockVersion = null)
 * @method Square|null findOneBy(array $criteria, array $orderBy = null)
 * @method Square[]    findAll()
 * @method Square[]    findBy(array $criteria, array $orderBy = null, $limit = null, $offset = null)
 */
class SquareRepository extends ServiceEntityRepository
{
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, Square::class);
    }

    public function add(Square $square): void
    {
        $this->getEntityManager()->persist($square);
    }

    public function remove(Square $square): void
    {
        $this->getEntityManager()->remove($square);
    }

    /**
     * @throws NonUniqueResultException
     * @throws NoResultException
     */
    public function getAvgTimeToClick(): ?float
    {
        $qb = $this->createQueryBuilder('s');

        return $qb
            ->select($qb->expr()->avg('s.timeToClick'))
            ->join('s.game', 'g')
            ->join('g.user', 'u')
            ->where($qb->expr()->isNotNull('s.timeToClick'))
            ->andWhere($qb->expr()->notLike('u.roles', ':adminRole'))
            ->setParameter('adminRole', '%' . RoleEnum::ROLE_ADMIN->name . '%')
            ->getQuery()
            ->getSingleScalarResult();
    }
}
