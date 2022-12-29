<?php

namespace App\Repository;

use App\Entity\InitialSurvey;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Persistence\ManagerRegistry;

/**
 * @extends ServiceEntityRepository<InitialSurvey>
 *
 * @method InitialSurvey|null find($id, $lockMode = null, $lockVersion = null)
 * @method InitialSurvey|null findOneBy(array $criteria, array $orderBy = null)
 * @method InitialSurvey[]    findAll()
 * @method InitialSurvey[]    findBy(array $criteria, array $orderBy = null, $limit = null, $offset = null)
 */
class InitialSurveyRepository extends ServiceEntityRepository
{
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, InitialSurvey::class);
    }

    public function save(InitialSurvey $entity, bool $flush = false): void
    {
        $this->getEntityManager()->persist($entity);

        if ($flush) {
            $this->getEntityManager()->flush();
        }
    }

    public function remove(InitialSurvey $entity, bool $flush = false): void
    {
        $this->getEntityManager()->remove($entity);

        if ($flush) {
            $this->getEntityManager()->flush();
        }
    }
}
