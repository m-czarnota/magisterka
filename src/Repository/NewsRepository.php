<?php

namespace App\Repository;

use App\Entity\News;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Persistence\ManagerRegistry;

/**
 * @extends ServiceEntityRepository<News>
 *
 * @method News|null find($id, $lockMode = null, $lockVersion = null)
 * @method News|null findOneBy(array $criteria, array $orderBy = null)
 * @method News[]    findAll()
 * @method News[]    findBy(array $criteria, array $orderBy = null, $limit = null, $offset = null)
 */
class NewsRepository extends ServiceEntityRepository
{
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, News::class);
    }

    public function add(News $news): void
    {
        $this->getEntityManager()->persist($news);
    }

    public function remove(News $news): void
    {
        $this->getEntityManager()->remove($news);
    }

    /**
     * @param int $pageNumber
     * @param int $pageSize
     * @return array<int, News>
     */
    public function findPage(int $pageNumber, int $pageSize): array
    {
        return $this->createQueryBuilder('n')
            ->setMaxResults($pageSize)
            ->setFirstResult(($pageNumber - 1) * $pageSize)
            ->orderBy('n.id', 'DESC')
            ->getQuery()
            ->getResult();
    }
}
