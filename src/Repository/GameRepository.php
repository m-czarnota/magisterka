<?php

namespace App\Repository;

use App\Entity\Game;
use App\Enum\User\RoleEnum;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\DBAL\Exception;
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
    public function getMaxTimeByUserId(int $userId): ?string
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
    public function getMaxScoreByUserId(int $userId): ?float
    {
        $qb = $this->createQueryBuilder('g');

        return $qb
            ->select($qb->expr()->max('g.score'))
            ->where('g.user = :id')
            ->setParameter('id', $userId)
            ->getQuery()
            ->getSingleScalarResult();
    }

    /**
     * @throws NonUniqueResultException
     * @throws NoResultException
     */
    public function getMaxTime(): ?string
    {
        $qb = $this->createQueryBuilder('g');

        return $qb
            ->select($qb->expr()->max('g.time'))
            ->join('g.user', 'u')
            ->where($qb->expr()->notLike('u.roles', ':adminRole'))
            ->setParameter('adminRole', '%' . RoleEnum::ROLE_ADMIN->name . '%')
            ->getQuery()
            ->getSingleScalarResult();
    }

    /**
     * @throws NonUniqueResultException
     * @throws NoResultException
     */
    public function getMaxScore(): ?float
    {
        $qb = $this->createQueryBuilder('g');

        return $qb
            ->select($qb->expr()->max('g.score'))
            ->join('g.user', 'u')
            ->where($qb->expr()->notLike('u.roles', ':adminRole'))
            ->setParameter('adminRole', '%' . RoleEnum::ROLE_ADMIN->name . '%')
            ->getQuery()
            ->getSingleScalarResult();
    }

    /**
     * @throws Exception
     */
    public function getMaxGamesByOneUser(): ?int
    {
        $adminRole = RoleEnum::ROLE_ADMIN->name;
        $results = $this->getEntityManager()->getConnection()->executeQuery("
            SELECT COUNT(g.id) 
            FROM game g 
            JOIN user u ON g.user_id = u.id
            WHERE u.roles NOT LIKE '%$adminRole%'
            GROUP BY g.`user_id` 
            WITH ROLLUP
        ")->fetchFirstColumn();

        return empty($results) ? null: $results[array_key_last($results)];
    }

    /**
     * @throws NonUniqueResultException
     * @throws NoResultException
     */
    public function getNumberOfGames(): ?int
    {
        $qb = $this->createQueryBuilder('g');

        return $qb
            ->select($qb->expr()->count('g.id'))
            ->join('g.user', 'u')
            ->where($qb->expr()->notLike('u.roles', ':adminRole'))
            ->setParameter('adminRole', '%' . RoleEnum::ROLE_ADMIN->name . '%')
            ->getQuery()
            ->getSingleScalarResult();
    }
}
