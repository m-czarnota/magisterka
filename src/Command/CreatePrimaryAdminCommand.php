<?php

namespace App\Command;

use App\Interface\Factory\User\UserFactoryInterface;
use App\Interface\Repository\RepositoryModifierInterface;
use App\Repository\UserRepository;
use Doctrine\ORM\NonUniqueResultException;
use Symfony\Component\Console\Attribute\AsCommand;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;

#[AsCommand(
    name: 'app:user:create_primary_admin',
    description: 'Create an primary admin user in system'
)]
class CreatePrimaryAdminCommand extends Command
{
    protected RepositoryModifierInterface $repositoryModifier;
    protected UserRepository $userRepository;
    protected UserFactoryInterface $userFactory;

    public function __construct(RepositoryModifierInterface $repositoryModifier, UserRepository $userRepository, UserFactoryInterface $userFactory)
    {
        $this->repositoryModifier = $repositoryModifier;
        $this->userRepository = $userRepository;
        $this->userFactory = $userFactory;

        parent::__construct();
    }

    /**
     * @throws NonUniqueResultException
     */
    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $primaryAdmin = $this->userRepository->findOnePrimaryAdmin();
        if ($primaryAdmin) {
            $output->writeln('Cannot create primary admin, because he exists.');

            return Command::FAILURE;
        }

        $primaryAdmin = $this->userFactory->createPrimaryAdmin();
        $this->repositoryModifier->save($primaryAdmin, true);
        $output->writeln('Primary admin successfully created.');

        return Command::SUCCESS;
    }
}