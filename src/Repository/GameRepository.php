<?php

namespace App\Repository;

use App\Entity\Game;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\ORM\NonUniqueResultException;
use Doctrine\ORM\NoResultException;
use Doctrine\Persistence\ManagerRegistry;

/**
 * @extends ServiceEntityRepository<Game>
 *
 * @method Game|null find($id, $lockMode = null, $lockVersion = null)
 * @method Game|null findOneBy(array $criteria, array $orderBy = null)
 * @method Game[]    findAll()
 * @method Game[]    findBy(array $criteria, array $orderBy = null, $limit = null, $offset = null)
 */
class GameRepository extends ServiceEntityRepository
{
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, Game::class);
    }

    public function add(Game $game): void
    {
        $this->getEntityManager()->persist($game);
    }

    public function remove(Game $game): void
    {
        $this->getEntityManager()->remove($game);
    }

    /**
     * @throws NonUniqueResultException
     * @throws NoResultException
     */
    public function getMaxTimeByUserId(int $userId): string
    {
        $qb = $this->createQueryBuilder('g');

        return $qb
            ->select($qb->expr()->max('g.time'))
            ->where('g.user = :id')
            ->setParameter('id', $userId)
            ->getQuery()
            ->getSingleScalarResult();
    }

    /**
     * @throws NonUniqueResultException
     * @throws NoResultException
     */
    public function getMaxScoreByUserId(int $userId): float
    {
        $qb = $this->createQueryBuilder('g');

        return $qb
            ->select($qb->expr()->max('g.score'))
            ->where('g.user = :id')
            ->setParameter('id', $userId)
            ->getQuery()
            ->getSingleScalarResult();
    }
}
