<?php

namespace App\Command;

use App\Interface\Factory\User\UserFactoryInterface;
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
    public function __construct(
        protected UserRepository $userRepository,
        protected UserFactoryInterface $userFactory,
    ) {
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
        $this->userRepository->save(true, $primaryAdmin);
        $output->writeln('Primary admin successfully created.');

        return Command::SUCCESS;
    }
}