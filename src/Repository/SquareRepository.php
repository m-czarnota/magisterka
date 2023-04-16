<?php

namespace App\Repository;

use App\Entity\Square;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
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
}
